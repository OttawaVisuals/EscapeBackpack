// The five neighbours (lock 8) in 3D, from the user's Stud.io export of the solved figures (assets/lego-minifigs.ldr,
// packed by tools/pack-lego.mjs). Loose parts lie on the table in one row per bag; players drag them onto five
// stands. Each bag option is the set of parts one figure has in the export. Held items follow the hand of whatever
// torso is on the stand. Design record: DG-H27, DG-H28.
import * as THREE from 'three';
import { createStage, createScene, renderStill, toMatrix4 } from './lego3d.js';
import { loadPack } from './lego-model.js';
import { BAG, SOLVED, NAME_FILES, ROWS, ORDER } from './lego-minifigs-data.js';

const SPACING = 150;                       // LDU between stands
const isTorso = file => file.includes('973');

let loading;
const load = () => loading ??= loadPack(new URL('assets/lego-minifigs.pack.json', import.meta.url).href).then(index);

// Sort the export into figures: each name base, and the parts nearest to it along the row.
function index(pack) {
  const bases = pack.main.filter(r => NAME_FILES[r.file]).map(r => ({ ref: r, name: NAME_FILES[r.file] }));
  const figures = {};
  for (const b of bases) figures[b.name] = { base: toMatrix4(b.ref.m), baseRef: b.ref, parts: {} };
  const roleOf = file => Object.keys(BAG).find(k => BAG[k].includes(file));
  for (const ref of pack.main) {
    if (NAME_FILES[ref.file]) continue;
    const role = roleOf(ref.file);
    if (!role) { console.warn('Minifig part with no bag:', ref.file); continue; }
    const near = bases.reduce((a, b) => Math.abs(b.ref.m[0] - ref.m[0]) < Math.abs(a.ref.m[0] - ref.m[0]) ? b : a);
    (figures[near.name].parts[role] ??= []).push(ref);
  }
  // Hands of each figure's torso, in model space: from the posed torso's own file, or from the packed library part.
  for (const f of Object.values(figures)) {
    const torso = f.parts.jobs.find(r => isTorso(r.file)), M = toMatrix4(torso.m);
    const local = pack.files[torso.file] ? pack.files[torso.file].filter(k => k.file === '3820.dat').map(k => toMatrix4(k.m)) : (pack.json.parts[torso.file].hands || []).map(toMatrix4);
    f.hands = local.map(h => M.clone().multiply(h)).sort((a, b) => a.elements[12] - b.elements[12]);
  }
  return { pack, figures };
}
const owner = (bag, value) => bag === 'names' ? value : Object.keys(SOLVED).find(n => SOLVED[n][bag] === value);

// One stand: the figure's parts moved from their source figure onto this stand's base.
function buildStand(data, fig) {
  const { pack, figures } = data, g = new THREE.Group();
  const add = (ref, matrix, ghost, bag) => {
    const o = pack.build(ref); o.matrix.copy(matrix);
    if (ghost) ghostly(o); else o.userData.pick = { bag, value: fig[bag] };    // can be picked up off the stand
    g.add(o);
  };
  const place = (src, ref) => new THREE.Matrix4().copy(src.base).invert().multiply(toMatrix4(ref.m));   // relative to its own base
  // Name base (a plain one with its print hidden when no name is chosen).
  const nameSrc = figures[fig.names || 'DICK'];
  const base = pack.build(nameSrc.baseRef); base.matrix.copy(place(nameSrc, nameSrc.baseRef));
  if (!fig.names) base.traverse(o => { if (o.material?.map) o.visible = false; });
  else base.userData.pick = { bag: 'names', value: fig.names };
  g.add(base);
  // Body, head and hair, with a faint stand-in where the outfit or head is missing.
  const body = fig.jobs ? figures[owner('jobs', fig.jobs)] : null;
  for (const [bag, standIn] of [['jobs', 'DICK'], ['faces', 'DICK'], ['hair', null], ['pets', null]]) {
    const src = fig[bag] ? figures[owner(bag, fig[bag])] : standIn && figures[standIn];
    if (src) for (const ref of src.parts[bag]) add(ref, place(src, ref), !fig[bag], bag);
  }
  // Held items go in the same hand of this stand's torso; items not held (the flippers) lie by the base.
  if (fig.hobbies) {
    const src = figures[owner('hobbies', fig.hobbies)];
    for (const ref of src.parts.hobbies) {
      const m = toMatrix4(ref.m), at = new THREE.Vector3().setFromMatrixPosition(m);
      const hand = src.hands.findIndex(h => new THREE.Vector3().setFromMatrixPosition(h).distanceTo(at) < 24);
      if (hand >= 0 && body) {
        const rel = src.hands[hand].clone().invert().multiply(m);
        add(ref, new THREE.Matrix4().copy(body.base).invert().multiply(body.hands[hand]).multiply(rel), false, 'hobbies');
      } else add(ref, place(src, ref), false, 'hobbies');
    }
  }
  return g;
}
const ghostMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.16, depthWrite: false });
function ghostly(o) {
  const drop = [];
  o.traverse(c => { if (c.isLineSegments || c.material?.map) drop.push(c); else if (c.isMesh) { c.material = ghostMaterial; c.castShadow = false; } });
  drop.forEach(c => c.removeFromParent());
}

// ---- Workbench: five stands at the back, loose parts in front in one row per bag (DG-H28) ----
// Rows run from the stands towards the player (ROWS, ORDER in lego-minifigs-data.js).
const ROW_DEPTH = { jobs: 50, pets: 50, hobbies: 60, hair: 46, faces: 42, names: 74 };
const FIRST_ROW = -150, LIFT = -14;                  // LDraw z of the row nearest the stands; drag height (y is down)

// Box of an object's meshes in its own frame (the object must not be in a scene yet, or be its own root).
function ownBox(o) {
  o.updateMatrixWorld(true);
  const inv = o.matrixWorld.clone().invert(), box = new THREE.Box3(), m = new THREE.Matrix4();
  o.traverse(c => { if (c.isMesh) { c.geometry.boundingBox ?? c.geometry.computeBoundingBox(); box.union(c.geometry.boundingBox.clone().applyMatrix4(m.multiplyMatrices(inv, c.matrixWorld))); } });
  return box;
}
// One loose option: its parts as exported around their own base, set down centred on the table at `home`.
function buildLoose(data, bag, value) {
  const { pack, figures } = data, src = figures[owner(bag, value)];
  const inner = new THREE.Group(), refs = bag === 'names' ? [src.baseRef] : src.parts[bag];
  for (const ref of refs) { const o = pack.build(ref); o.matrix.copy(new THREE.Matrix4().copy(src.base).invert().multiply(toMatrix4(ref.m))); inner.add(o); }
  const b = ownBox(inner), c = b.getCenter(new THREE.Vector3());
  inner.position.set(-c.x, -b.max.y, -c.z);
  const outer = new THREE.Group(); outer.add(inner);
  const size = b.getSize(new THREE.Vector3());
  const proxy = new THREE.Mesh(new THREE.BoxGeometry(size.x + 8, size.y + 6, size.z + 8), new THREE.MeshBasicMaterial({ visible: false }));
  proxy.position.set(0, -size.y / 2, 0); outer.add(proxy);
  outer.userData.pick = { bag, value }; proxy.userData.pick = outer.userData.pick;
  return { bag, value, group: outer, proxy };
}
// A flat label on the table at the start of a row.
function rowLabel(text) {
  const canvas = document.createElement('canvas'); canvas.width = 256; canvas.height = 64;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#f4ebd5'; ctx.font = '700 40px "Inter Tight", "Segoe UI", sans-serif'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
  ctx.fillText(text.toUpperCase(), 250, 34);
  const tex = new THREE.CanvasTexture(canvas); tex.colorSpace = THREE.SRGBColorSpace;
  const label = new THREE.Mesh(new THREE.PlaneGeometry(120, 30), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, depthTest: false }));
  label.renderOrder = -1;                             // on the felt, left of every row: nothing to hide it behind
  label.rotation.x = Math.PI / 2;                    // lie flat on the table, readable from the front (LDraw y is down)
  return label;
}

// ---- The picture inside each bag on the table: its five real parts in a loose pile (DG-H29) ----
// Fixed spots and turns so the picture stays the same; outfits and name bases lie flat, as they would in a bag.
const PILE = [[-34, -30, 0.5], [30, -36, 2.4], [-2, 4, 4.1], [-36, 40, 1.3], [32, 38, 5.6]];
const LIE_DOWN = new Set(['jobs', 'hair', 'faces']);                     // on their backs: prints face up
const SPREAD = { jobs: [1.55, 1.3], names: [1.6, 1.25] };                // bigger parts need more room
const pictures = new Map();
export async function bagPicture(bag, size = 360) {
  if (pictures.has(bag)) return pictures.get(bag);
  const job = (async () => {
    const data = await load(), { scene, root } = createScene('shadow');
    const pile = new THREE.Group();
    ORDER[bag].forEach((value, k) => {
      const { group } = buildLoose(data, bag, value), [x, z, turn] = PILE[k];
      const holder = new THREE.Group(); holder.add(group);
      if (LIE_DOWN.has(bag)) group.rotation.x = -Math.PI / 2;                  // on its back
      const b = ownBox(holder), c = b.getCenter(new THREE.Vector3());
      group.position.sub(new THREE.Vector3(c.x, b.max.y, c.z));               // rest on the table, centred
      const [sx, sz] = SPREAD[bag] || [1, 1];
      holder.position.set(x * sx, 0, z * sz); holder.rotation.y = turn;
      pile.add(holder);
    });
    root.add(pile);
    // Orthographic, from above at an angle, framed on the pile.
    const tilt = THREE.MathUtils.degToRad(62), cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 4000);
    cam.position.set(0, 1000 * Math.sin(tilt), 1000 * Math.cos(tilt)); cam.lookAt(0, 0, 0); cam.updateMatrixWorld();
    root.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(pile), v = new THREE.Vector3(), lo = new THREE.Vector2(1e9, 1e9), hi = new THREE.Vector2(-1e9, -1e9);
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
      v.set(x, y, z).applyMatrix4(cam.matrixWorldInverse); lo.min(v); hi.max(v);
    }
    const half = Math.max(hi.x - lo.x, hi.y - lo.y) / 2 * 1.06, mx = (lo.x + hi.x) / 2, my = (lo.y + hi.y) / 2;
    Object.assign(cam, { left: mx - half, right: mx + half, top: my + half, bottom: my - half }); cam.updateProjectionMatrix();
    await data.pack.ready();
    return renderStill(scene, cam, size);
  })();
  pictures.set(bag, job);
  return job;
}

// mount(container, { figures, bags, labels, names, onChange })
//   figures: the save's five stands (changed in place); bags: bags found, in ROWS order or any order;
//   labels: { bag: 'Jobs', … } for the row labels; names: { bag: { value: 'Doctor’s coat', … } } for hover text;
//   onChange(): called after a part is put on or taken off a stand.
export async function mount(container, { figures: state, bags, labels = {}, names = {}, onChange = () => {} }) {
  const data = await load();
  const stage = createStage(container);
  Object.assign(stage.controls, { enabled: false, minDistance: 0, maxDistance: 1e5, maxPolarAngle: Math.PI });
  const cam = stage.camera; cam.fov = 30; cam.updateProjectionMatrix();
  stage.scene.traverse(o => { if (o.isDirectionalLight) { Object.assign(o.shadow.camera, { left: -520, right: 520, top: 420, bottom: -420 }); o.shadow.camera.updateProjectionMatrix(); } });
  const root = stage.root, rows = ROWS.filter(b => bags.includes(b));
  let held = null;                                   // the part being dragged: { item, x, y, moved }

  // Stands, each with a ring that lights up while a part is held over it.
  const stands = state.map((fig, i) => {
    const holder = new THREE.Group(); holder.position.set(i * SPACING, -8, 0);
    holder.add(buildStand(data, fig)); root.add(holder);
    const ring = new THREE.Mesh(new THREE.RingGeometry(52, 60, 48), new THREE.MeshBasicMaterial({ color: 0xe39a45, transparent: true, opacity: 0.9, side: THREE.DoubleSide }));
    ring.rotation.x = Math.PI / 2; ring.position.set(i * SPACING, -1.2, 0); ring.visible = false; root.add(ring);
    holder.userData = { ring, turn: 0 };
    return holder;
  });
  // Loose parts: one row per bag found.
  const loose = [];
  let z = FIRST_ROW;
  rows.forEach((bag, r) => {
    z -= r ? (ROW_DEPTH[rows[r - 1]] + ROW_DEPTH[bag]) / 2 + 14 : 0;
    const shift = ROWS.indexOf(bag) % 2 ? 35 : -35;     // by the bag's own row, so the scramble holds with fewer bags
    ORDER[bag].forEach((value, k) => {
      const item = buildLoose(data, bag, value);
      item.home = new THREE.Vector3(k * SPACING + shift, 0, z);
      item.group.position.copy(item.home); root.add(item.group); loose.push(item);
    });
    const label = rowLabel(labels[bag] || bag); label.position.set(-130, -1.2, z); root.add(label);
  });
  const front = z - ROW_DEPTH[rows.at(-1) || 'names'] / 2;
  const sync = () => { for (const l of loose) if (l !== held?.item) l.group.visible = !state.some(f => f[l.bag] === l.value); };
  sync();

  // Camera: from the front and above. Refitted when the canvas changes shape, by projecting the corners of the scene
  // (the front rows look wider than the stands, so a flat estimate would cut them off).
  const box = { x0: -195, x1: 4 * SPACING + 80, z0: front - 6, z1: 40 }, cx = (box.x0 + box.x1) / 2, cz = (box.z0 + box.z1) / 2;
  stage.centreOn(cx, cz);
  const corners = [];
  for (const x of [box.x0, box.x1]) {
    for (const zz of [box.z0, box.z1]) corners.push(new THREE.Vector3(x, 0, zz));    // the table
    corners.push(new THREE.Vector3(x, -125, box.z1), new THREE.Vector3(x, -125, -30));   // the figures' heads (only the stands are tall)
  }
  let fitted = 0;
  stage.onTick(() => {
    if (cam.aspect === fitted) return; fitted = cam.aspect;
    const tilt = THREE.MathUtils.degToRad(52), target = new THREE.Vector3(0, 30, 0), v = new THREE.Vector3();
    let d = 1200;
    for (let k = 0; k < 6; k++) {
      cam.position.set(0, target.y + d * Math.sin(tilt), d * Math.cos(tilt)); cam.lookAt(target); cam.updateMatrixWorld();
      let x0 = 1, x1 = -1, y0 = 1, y1 = -1;
      root.updateMatrixWorld();
      for (const c of corners) { v.copy(c); root.localToWorld(v).project(cam); x0 = Math.min(x0, v.x); x1 = Math.max(x1, v.x); y0 = Math.min(y0, v.y); y1 = Math.max(y1, v.y); }
      // Centre the picture vertically, then scale the distance so the widest side fills 96% of the canvas.
      target.y += (y0 + y1) / 2 * d * Math.tan(THREE.MathUtils.degToRad(cam.fov / 2)) * 0.9;
      d *= Math.max((x1 - x0) / 2, (y1 - y0) / 2) / 0.96;
    }
    cam.position.set(0, target.y + d * Math.sin(tilt), d * Math.cos(tilt)); cam.lookAt(target);
    stage.controls.target.copy(target);
  });

  // ---- Picking and dragging ----
  const canvas = stage.renderer.domElement, ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  const tip = document.createElement('div'); tip.className = 'lego-tip'; tip.hidden = true; container.append(tip);
  const table = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  canvas.setAttribute('aria-label', 'Lego parts on a table and five stands, in 3D. Drag a part onto a stand. Use the lists button for keyboard controls.');
  const aim = e => { const r = canvas.getBoundingClientRect(); ndc.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1); ray.setFromCamera(ndc, cam); };
  const tagOf = o => { while (o && !o.userData.pick) o = o.parent; return o; };
  function pick(e) {
    aim(e);
    const looseHit = ray.intersectObjects(loose.filter(l => l.group.visible).map(l => l.proxy), false)[0];
    const meshes = []; stands.forEach((s, i) => s.traverse(o => { if (o.isMesh && tagOf(o)) { o.userData.stand = i; meshes.push(o); } }));
    const standHit = ray.intersectObjects(meshes, false)[0];
    if (standHit && (!looseHit || standHit.distance < looseHit.distance)) return { ...tagOf(standHit.object).userData.pick, stand: standHit.object.userData.stand };
    return looseHit ? { ...looseHit.object.userData.pick } : null;
  }
  const onTable = e => { aim(e); const p = ray.ray.intersectPlane(table, new THREE.Vector3()); return p && root.worldToLocal(p); };
  const standAt = p => { const i = Math.round(p.x / SPACING); return p.z > -62 && i >= 0 && i < 5 && Math.abs(p.x - i * SPACING) < 72 ? i : -1; };
  const rebuild = i => { stands[i].clear(); stands[i].add(buildStand(data, state[i])); };
  const showTip = (e, text) => {
    if (!text) { tip.hidden = true; return; }
    const r = container.getBoundingClientRect(); tip.textContent = text; tip.hidden = false;
    tip.style.left = `${e.clientX - r.left + 14}px`; tip.style.top = `${e.clientY - r.top + 12}px`;
  };
  canvas.addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    const hit = pick(e); if (!hit) return;
    const item = loose.find(l => l.bag === hit.bag && l.value === hit.value);
    if (!item) return;
    if (hit.stand !== undefined) { delete state[hit.stand][hit.bag]; rebuild(hit.stand); onChange(); }   // taken off its stand
    held = { item, x: e.clientX, y: e.clientY, moved: hit.stand !== undefined };
    item.group.visible = true;
    const p = onTable(e); if (p) item.group.position.set(p.x, LIFT, p.z);
    canvas.setPointerCapture(e.pointerId); canvas.style.cursor = 'grabbing'; tip.hidden = true;
  });
  canvas.addEventListener('pointermove', e => {
    if (!held) { const hit = pick(e); canvas.style.cursor = hit ? 'grab' : ''; showTip(e, hit && names[hit.bag]?.[hit.value]); return; }
    if (Math.hypot(e.clientX - held.x, e.clientY - held.y) > 4) held.moved = true;
    const p = onTable(e); if (!p) return;
    held.item.group.position.set(p.x, LIFT, p.z);
    const i = standAt(p); stands.forEach((s, j) => { s.userData.ring.visible = j === i; });
  });
  const drop = e => {
    if (!held) return;
    const { item } = held, p = onTable(e), i = held.moved && p ? standAt(p) : -1;
    stands.forEach(s => { s.userData.ring.visible = false; });
    held = null; canvas.style.cursor = '';
    item.group.position.copy(item.home);
    if (i >= 0) {
      state.forEach((f, j) => { if (j !== i && f[item.bag] === item.value) { delete f[item.bag]; rebuild(j); } });
      state[i][item.bag] = item.value; rebuild(i); onChange();      // a part already there goes back to its row (sync)
    }
    sync();
  };
  canvas.addEventListener('pointerup', drop); canvas.addEventListener('pointercancel', drop);
  canvas.addEventListener('pointerleave', () => { if (!held) tip.hidden = true; });

  // ---- Turn arrows under each stand, kept under the stand as the canvas resizes ----
  const turns = document.createElement('div'); turns.className = 'lego-turns'; container.append(turns);
  const arrows = stands.map(s => {
    const box = document.createElement('div');
    for (const [text, d, name] of [['⟲', -1, 'left'], ['⟳', 1, 'right']]) {
      const b = document.createElement('button'); b.type = 'button'; b.textContent = text; b.setAttribute('aria-label', `Turn this figure ${name}`);
      b.addEventListener('click', () => { s.userData.turn += d * Math.PI / 4; });
      box.append(b);
    }
    turns.append(box); return box;
  });
  const at = new THREE.Vector3();
  stage.onTick(() => {
    stands.forEach((s, i) => {
      s.rotation.y += (s.userData.turn - s.rotation.y) * 0.2;
      at.set(i * SPACING, 0, -42); root.localToWorld(at).project(cam);
      arrows[i].style.left = `${(at.x + 1) / 2 * 100}%`; arrows[i].style.top = `${(1 - at.y) / 2 * 100}%`;
    });
  });

  // After a change from the lists: rebuild that stand (or all) and put the loose parts right.
  function update(i) { if (i === undefined) state.forEach((_, j) => rebuild(j)); else rebuild(i); sync(); }
  return { update, dispose: stage.dispose };
}
