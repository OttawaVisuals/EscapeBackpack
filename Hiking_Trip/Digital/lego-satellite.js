// Lego satellite (locks 4–5) in 3D, from the user's Stud.io export (assets/lego-satellite.ldr, packed by
// tools/pack-lego.mjs). The build follows the instruction booklet one page at a time; the telescope is built beside
// the satellite (pages 6–7) and then fixed on (page 8). Design record: DG-H25.
import * as THREE from 'three';
import { createScene, createStage, renderStill, toMatrix4 } from './lego3d.js';
import { loadPack } from './lego-model.js';

// What each booklet page (2–11) adds: steps of the main model and of the telescope (0 STEP order in the export).
export const PAGES = [
  { main: [0, 1] }, { main: [2, 3] }, { main: [4] }, { main: [5] },
  { telescope: [0, 1, 2] }, { telescope: [3, 4] }, { main: [6] }, { main: [7] }, { main: [8] }, { main: [9] }
];
const TELESCOPE = 'telescope', LENS = '10830p01.dat';

let loading;
const load = () => loading ??= loadPack(new URL('assets/lego-satellite.pack.json', import.meta.url).href);

// Steps shown after `built` pages.
function shownSteps(built) {
  const main = new Set(), tele = new Set();
  for (const p of PAGES.slice(0, built)) { p.main?.forEach(s => main.add(s)); p.telescope?.forEach(s => tele.add(s)); }
  return { main, tele, fixed: main.has(6) };
}

// The model as objects: one per main part, the telescope as a group of its parts.
function buildModel(pack, root) {
  const objects = [];
  let telescope = null;
  for (const ref of pack.main) {
    if (ref.file === TELESCOPE) {
      const group = new THREE.Group(); group.matrixAutoUpdate = false;
      for (const k of pack.files[TELESCOPE]) { const o = pack.build(k); o.userData.teleStep = k.step; group.add(o); }
      telescope = { group, fixed: toMatrix4(ref.m), beside: null };     // fixed: its place on the satellite
      root.add(group);
      continue;
    }
    const o = pack.build(ref); o.userData.step = ref.step; objects.push(o); root.add(o);
  }
  // Beside the satellite on the table while it is being built: same turn, moved to the +x side, standing on the table.
  telescope.group.matrix.copy(telescope.fixed);
  const base = new THREE.Box3(); objects.forEach(o => base.union(ldrawBox(o, root)));
  const tb = ldrawBox(telescope.group, root);
  const shift = new THREE.Vector3(base.max.x + 40 - tb.min.x, -tb.max.y, -40);
  telescope.beside = telescope.fixed.clone().premultiply(new THREE.Matrix4().makeTranslation(shift.x, shift.y, shift.z));
  const box = base.clone().union(tb);
  return { objects, telescope, box, buildBox: box.clone().union(tb.clone().translate(shift)) };   // buildBox: with the telescope beside it
}
// Bounding box of an object in LDraw space (the frame of `root`).
function ldrawBox(o, root) {
  root.updateWorldMatrix(true, true);
  const inv = root.matrixWorld.clone().invert(), box = new THREE.Box3(), m = new THREE.Matrix4();
  o.traverse(c => {
    if (!c.isMesh) return;
    c.geometry.boundingBox ?? c.geometry.computeBoundingBox();
    box.union(c.geometry.boundingBox.clone().applyMatrix4(m.multiplyMatrices(inv, c.matrixWorld)));
  });
  return box;
}
function showState(model, built) {
  const { main, tele, fixed } = shownSteps(built);
  for (const o of model.objects) o.visible = main.has(o.userData.step);
  const t = model.telescope;
  for (const c of t.group.children) c.visible = tele.has(c.userData.teleStep);
  t.group.visible = tele.size > 0;
  t.group.matrix.copy(fixed ? t.fixed : t.beside);
}

// ---- Table picture: the finished satellite at an angle, cached ----
let still;
export async function picture(built = PAGES.length) {
  const pack = await load();
  if (!still) {
    const { scene, root } = createScene('shadow');
    const model = buildModel(pack, root);
    const c = model.box.getCenter(new THREE.Vector3());
    root.position.set(-c.x, 0, c.z);
    const camera = new THREE.PerspectiveCamera(30, 1, 1, 5000);
    camera.position.set(80, 560, 420); camera.lookAt(0, 0, 0);
    still = { scene, camera, model, urls: new Map() };
    await pack.ready();
  }
  if (!still.urls.has(built)) { showState(still.model, built); still.urls.set(built, renderStill(still.scene, still.camera, 520)); }
  return still.urls.get(built);
}

// ---- Top view for the back of the ISS note: picture plus where the four magnifier lenses are in it ----
export async function topView(size = 1024) {
  const pack = await load();
  const { scene, root } = createScene('shadow');
  scene.traverse(o => { if (o.material?.isShadowMaterial) o.visible = false; });   // no shadow on the card (the page adds a soft one)
  const model = buildModel(pack, root);
  showState(model, PAGES.length);
  const b = model.box, cx = (b.min.x + b.max.x) / 2, cz = (b.min.z + b.max.z) / 2;
  const span = Math.max(b.max.x - b.min.x, b.max.z - b.min.z) + 30;
  root.position.set(-cx, 0, cz);
  // Looking straight down; image right = LDraw +x, image top = LDraw +z.
  const camera = new THREE.OrthographicCamera(-span / 2, span / 2, span / 2, -span / 2, 1, 2000);
  camera.position.set(0, 800, 0); camera.up.set(0, 0, -1); camera.lookAt(0, 0, 0);
  await pack.ready();
  const url = renderStill(scene, camera, size);
  const local = pack.centroid(LENS, '47');
  const lenses = pack.main.filter(r => r.file === LENS).map(r => {
    const m = r.m, x = m[0] + m[3] * local[0] + m[4] * local[1] + m[5] * local[2], z = m[2] + m[9] * local[0] + m[10] * local[1] + m[11] * local[2];
    return [(x - cx) / span * size + size / 2, size / 2 - (z - cz) / span * size];
  });
  return { url, size, lenses, pxPerLdu: size / span };
}

// ---- The bag of pieces on the table before the build: every part of the export lying loose (DG-H29) ----
// Each part keeps its built orientation (so plates lie flat), turned about the vertical by a fixed amount, resting on
// the table; parts go down in loose rows in a fixed jumbled order, with a little fixed jitter. Cached once rendered.
let bagShot;
export function bagPicture(size = 360) {
  return bagShot ??= (async () => {
    const pack = await load(), { scene, root } = createScene('shadow');
    const refs = [...pack.main.filter(r => r.file !== TELESCOPE), ...pack.files[TELESCOPE]];
    const items = refs.map((ref, k) => {
      const part = pack.build(ref); part.matrix.setPosition(0, 0, 0);
      const holder = new THREE.Group(); holder.add(part); holder.rotation.y = (k * 2.39996) % (2 * Math.PI);
      holder.updateMatrixWorld(true);
      const b = new THREE.Box3();
      holder.traverse(c => { if (c.isMesh) { c.geometry.boundingBox ?? c.geometry.computeBoundingBox(); b.union(c.geometry.boundingBox.clone().applyMatrix4(c.matrixWorld)); } });
      const c = b.getCenter(new THREE.Vector3()), s = b.getSize(new THREE.Vector3());
      return { holder, offset: new THREE.Vector3(-c.x, -b.max.y, -c.z), w: s.x, d: s.z, k };
    });
    const width = Math.sqrt(items.reduce((a, i) => a + (i.w + 4) * (i.d + 4), 0)) * 1.2;
    let x = 0, z = 0, row = 0;
    for (const i of [...items].sort((a, b) => (a.k * 7919) % 97 - (b.k * 7919) % 97)) {    // a fixed jumble, not sorted by size
      if (x + i.w > width && x > 0) { x = 0; z += row + 4; row = 0; }
      const jx = ((i.k * 37) % 7) - 3, jz = ((i.k * 53) % 7) - 3;
      i.holder.position.set(x + i.w / 2 + jx, 0, z + i.d / 2 + jz).add(i.offset);
      root.add(i.holder);
      x += i.w + 4; row = Math.max(row, i.d);
    }
    root.position.set(-width / 2, 0, (z + row) / 2);                     // centred, so the shadows stay in the light's range
    root.updateMatrixWorld(true);
    // Orthographic, from above at an angle, framed on the pile.
    const tilt = THREE.MathUtils.degToRad(62), cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 4000);
    const box = new THREE.Box3(); root.traverse(o => { if (o.isMesh && o.parent !== scene) box.expandByObject(o); });
    const mid = box.getCenter(new THREE.Vector3());
    cam.position.set(mid.x, mid.y + 1000 * Math.sin(tilt), mid.z + 1000 * Math.cos(tilt)); cam.lookAt(mid); cam.updateMatrixWorld();
    const v = new THREE.Vector3(), lo = new THREE.Vector2(1e9, 1e9), hi = new THREE.Vector2(-1e9, -1e9);
    for (const px of [box.min.x, box.max.x]) for (const py of [box.min.y, box.max.y]) for (const pz of [box.min.z, box.max.z]) { v.set(px, py, pz).applyMatrix4(cam.matrixWorldInverse); lo.min(v); hi.max(v); }
    const half = Math.max(hi.x - lo.x, hi.y - lo.y) / 2 * 1.05, mx = (lo.x + hi.x) / 2, my = (lo.y + hi.y) / 2;
    Object.assign(cam, { left: mx - half, right: mx + half, top: my + half, bottom: my - half }); cam.updateProjectionMatrix();
    await pack.ready();
    return renderStill(scene, cam, size);
  })();
}

// ---- Build view: the model so far; add(page) animates the parts of the next page into place ----
export async function mount(container, { built = 0 } = {}) {
  const pack = await load();
  const stage = createStage(container);
  const model = buildModel(pack, stage.root);
  const frame = built >= PAGES.length ? model.box : model.buildBox;            // room for the telescope beside it while building
  const c = frame.getCenter(new THREE.Vector3()), size = frame.getSize(new THREE.Vector3());
  stage.centreOn(c.x, c.z);
  const reach = Math.max(size.x, size.z);
  stage.controls.minDistance = reach * 0.5; stage.controls.maxDistance = reach * 3;
  stage.camera.position.set(reach * 0.4, reach * 1.05, reach * 1.15); stage.controls.target.set(0, 10, 0); stage.controls.update();
  showState(model, built);

  // Drops: each new object starts above its place and falls in, a little after the one before.
  let tweens = [];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  stage.onTick(now => {
    tweens = tweens.filter(t => {
      const k = Math.min(1, Math.max(0, (now - t.start) / t.ms)), e = 1 - Math.pow(1 - k, 3);
      t.obj.matrix.copy(t.to); t.obj.matrix.elements[12] += t.dx * (1 - e); t.obj.matrix.elements[13] += t.dy * (1 - e); t.obj.matrix.elements[14] += t.dz * (1 - e);
      return k < 1;
    });
  });
  // ---- Drag and drop: the page's parts wait on the table in front; the player drops each on its outline ----
  // A piece has a `slot` (where it belongs: matrices and an outline) and a `center` (where it is now, LDraw space).
  // Pieces of the same part and colour are interchangeable, so a piece snaps to any free outline of its kind.
  const el = stage.renderer.domElement, raycaster = new THREE.Raycaster(), T = new THREE.Matrix4();
  let session = null;
  const pageParts = page => {
    const before = shownSteps(page), after = shownSteps(page + 1), t = model.telescope, list = [];
    for (const o of model.objects) if (after.main.has(o.userData.step) && !before.main.has(o.userData.step)) list.push({ obj: o });
    for (const k of t.group.children) if (after.tele.has(k.userData.teleStep) && !before.tele.has(k.userData.teleStep)) list.push({ obj: k, inTelescope: true });
    if (after.fixed && !before.fixed) list.push({ obj: t.group, fix: true });
    return list;
  };
  function place(p, slot = p.slot, center = p.center) {         // put the piece's object at `center`, turned as `slot` says
    T.makeTranslation(center.x - slot.c0.x, center.y - slot.c0.y, center.z - slot.c0.z);
    p.obj.matrix.copy(slot.Pinv).multiply(T).multiply(slot.P).multiply(slot.toL);
  }
  const rayLd = e => {                                           // the pointer's ray in LDraw space
    const r = el.getBoundingClientRect();
    raycaster.setFromCamera(new THREE.Vector2((e.clientX - r.left) / r.width * 2 - 1, -((e.clientY - r.top) / r.height * 2 - 1)), stage.camera);
    stage.root.updateWorldMatrix(true, false);
    return raycaster.ray.clone().applyMatrix4(stage.root.matrixWorld.clone().invert());
  };
  const onPlane = (ray, y) => {                                  // where the ray meets the horizontal plane at LDraw height y
    const t = ray.direction.y > 1e-4 ? (y - ray.origin.y) / ray.direction.y : -1;
    return t > 0 ? ray.at(t, new THREE.Vector3()) : null;
  };
  const glow = (kind = null) => { for (const p of session.pieces) { const g = p.slot.ghost; g.visible = !p.placed; g.material.opacity = kind && p.key === kind ? 1 : kind ? 0.2 : 0.6; } };
  function startManual(page, { onProgress, onDone }) {
    cancelManual(); showState(model, page);
    const t = model.telescope, pieces = pageParts(page), frame = model.buildBox;
    const ghostMat = new THREE.LineBasicMaterial({ color: 0xffc24a, transparent: true, depthTest: false });
    let x = frame.min.x, z = frame.min.z - 30, rowDepth = 0;
    const rowMax = frame.min.x + Math.max(frame.max.x - frame.min.x, 240);
    for (const p of pieces) {
      p.key = (p.obj.userData.ref?.file || '') + ':' + (p.obj.userData.ref?.color ?? '');
      p.home = p.obj.matrix.clone(); p.obj.visible = true;
      const toL = p.fix ? t.fixed.clone() : p.obj.matrix.clone(), P = p.inTelescope ? t.group.matrix.clone() : new THREE.Matrix4();
      p.slot = { toL, P, Pinv: P.clone().invert() };
      p.obj.matrix.copy(toL); const box = ldrawBox(p.obj, stage.root), size = box.getSize(new THREE.Vector3());
      Object.assign(p.slot, { c0: box.getCenter(new THREE.Vector3()), size });
      const ghost = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(size.x + 2, size.y + 2, size.z + 2)), ghostMat.clone());
      ghost.position.copy(p.slot.c0); ghost.renderOrder = 10; stage.root.add(ghost); p.slot.ghost = ghost;
      if (p.fix) {                                               // the telescope waits where it was built, beside the satellite
        p.center = p.slot.c0.clone().add(new THREE.Vector3().setFromMatrixPosition(t.beside).sub(new THREE.Vector3().setFromMatrixPosition(t.fixed)));
      } else {                                                   // a tray of parts in front of the model, resting on the table
        if (x > frame.min.x && x + size.x > rowMax) { x = frame.min.x; z -= rowDepth + 18; rowDepth = 0; }
        p.center = new THREE.Vector3(x + size.x / 2, -size.y / 2, z - size.z / 2);
        x += size.x + 18; rowDepth = Math.max(rowDepth, size.z);
      }
      p.restY = p.center.y; p.obj.userData.piece = p; place(p);
    }
    const tray = new THREE.Box3(); pieces.forEach(p => tray.union(ldrawBox(p.obj, stage.root)));
    session = { pieces, onProgress, onDone, drag: null };
    glow();
    // Pull the camera back so the tray and the model are both in view.
    const all = frame.clone().union(tray), c = stage.root.localToWorld(all.getCenter(new THREE.Vector3())), s = all.getSize(new THREE.Vector3());
    const dir = stage.camera.position.clone().sub(stage.controls.target).normalize(), dist = Math.max(stage.camera.position.distanceTo(stage.controls.target), Math.max(s.x, s.z) * 1.45);
    stage.controls.target.set(c.x, 10, c.z); stage.camera.position.copy(stage.controls.target).addScaledVector(dir, dist); stage.controls.update();
    el.addEventListener('pointerdown', down, { capture: true }); el.addEventListener('pointermove', hover);
    el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
    onProgress?.(0, pieces.length);
  }
  function endSession(reset) {
    if (!session) return;
    el.removeEventListener('pointerdown', down, { capture: true }); el.removeEventListener('pointermove', hover);
    el.removeEventListener('pointerup', up); el.removeEventListener('pointercancel', up); el.style.cursor = '';
    for (const p of session.pieces) { p.slot.ghost.removeFromParent(); p.slot.ghost.geometry.dispose(); p.slot.ghost.material.dispose(); delete p.obj.userData.piece; if (reset) p.obj.matrix.copy(p.home); }
    session = null;
  }
  const cancelManual = () => endSession(true);
  const pick = e => {
    const r = el.getBoundingClientRect();
    raycaster.setFromCamera(new THREE.Vector2((e.clientX - r.left) / r.width * 2 - 1, -((e.clientY - r.top) / r.height * 2 - 1)), stage.camera);
    for (const h of raycaster.intersectObjects(session.pieces.filter(p => !p.placed).map(p => p.obj), true)) {
      for (let o = h.object; o; o = o.parent) if (o.userData.piece) return o.userData.piece;
    }
    return null;
  };
  function hover(e) {
    if (!session) return;
    const d = session.drag;
    if (!d) { el.style.cursor = pick(e) ? 'grab' : ''; return; }
    const ray = rayLd(e), p = d.piece;
    let best = null, bd = Infinity;                              // a free outline of the same kind that the pointer is over
    for (const q of session.pieces) if (!q.placed && q.key === p.key) {
      const r = Math.max(24, Math.max(q.slot.size.x, q.slot.size.y, q.slot.size.z) * 0.55), dist = ray.distanceToPoint(q.slot.c0);
      if (dist < r && dist < bd) { best = q.slot; bd = dist; }
    }
    d.over = best;
    if (best) { place(p, best, best.c0); return; }
    const at = onPlane(ray, p.restY);
    if (at) { p.center.set(at.x + d.off.x, p.restY - 12, at.z + d.off.z); place(p); }
  }
  function down(e) {
    if (!session || session.drag || (e.pointerType === 'mouse' && e.button !== 0)) return;
    const p = pick(e); if (!p) return;
    e.stopImmediatePropagation(); el.setPointerCapture(e.pointerId);
    const at = onPlane(rayLd(e), p.center.y) ?? p.center;
    session.drag = { piece: p, over: null, off: new THREE.Vector3(p.center.x - at.x, 0, p.center.z - at.z) };
    el.style.cursor = 'grabbing'; glow(p.key); hover(e);
  }
  function up(e) {
    const d = session?.drag; if (!d) return;
    session.drag = null; el.style.cursor = ''; if (el.hasPointerCapture(e.pointerId)) el.releasePointerCapture(e.pointerId);
    const p = d.piece;
    if (d.over) {
      const owner = session.pieces.find(q => q.slot === d.over);
      if (owner !== p) { owner.slot = p.slot; place(owner); }    // the piece that owned this outline takes over the one just left
      p.slot = d.over; p.placed = true; p.center.copy(d.over.c0); place(p);
    } else { p.center.y = p.restY; place(p); }
    glow();
    const placed = session.pieces.filter(q => q.placed).length, { onProgress, onDone, pieces } = session;
    onProgress?.(placed, pieces.length);
    if (placed === pieces.length) { endSession(false); setTimeout(() => onDone?.(), 350); }
  }
  // Drops every piece still on the table into place (the button for people who would rather not drag).
  function solveManual() {
    if (!session) return;
    const now = performance.now(); let delay = 0;
    for (const p of session.pieces) if (!p.placed) {
      p.placed = true; p.center.copy(p.slot.c0); place(p);
      tweens.push({ obj: p.obj, to: p.obj.matrix.clone(), start: now + delay, ms: 420, dx: 0, dy: -70, dz: 0 }); delay += 110;
    }
    const { onDone } = session; endSession(false); onDone?.();
  }

  function add(page) {
    cancelManual(); showState(model, page);
    const before = shownSteps(page), after = shownSteps(page + 1), now = performance.now();
    let delay = 0;
    const drop = obj => { const to = obj.matrix.clone(); obj.visible = true; if (!reduce) tweens.push({ obj, to, start: now + delay, ms: 420, dx: 0, dy: -70, dz: 0 }); delay += 110; };
    for (const o of model.objects) if (after.main.has(o.userData.step) && !before.main.has(o.userData.step)) drop(o);
    const t = model.telescope;
    for (const k of t.group.children) if (after.tele.has(k.userData.teleStep) && !before.tele.has(k.userData.teleStep)) { t.group.visible = true; drop(k); }
    if (after.fixed && !before.fixed) {
      const from = new THREE.Vector3().setFromMatrixPosition(t.beside), to = new THREE.Vector3().setFromMatrixPosition(t.fixed);
      t.group.matrix.copy(t.fixed);
      if (!reduce) tweens.push({ obj: t.group, to: t.fixed.clone(), start: now, ms: 700, dx: from.x - to.x, dy: from.y - to.y, dz: from.z - to.z });
    }
  }
  return { add, dispose: stage.dispose, manual: { start: startManual, cancel: page => { if (session) { cancelManual(); showState(model, page); } }, solve: solveManual } };
}
