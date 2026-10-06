// The five neighbours (lock 8) in 3D, from the user's Stud.io export of the solved figures (assets/lego-minifigs.ldr,
// packed by tools/pack-lego.mjs). Each bag option is the set of parts one figure has in the export; picking it on a
// stand moves those parts there. Held items follow the hand of whatever torso is on the stand. Design record: DG-H27.
import * as THREE from 'three';
import { createStage, toMatrix4 } from './lego3d.js';
import { loadPack } from './lego-model.js';
import { BAG, SOLVED, NAME_FILES } from './lego-minifigs-data.js';

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
  const add = (ref, matrix, ghost) => {
    const o = pack.build(ref); o.matrix.copy(matrix);
    if (ghost) ghostly(o);
    g.add(o);
  };
  const place = (src, ref) => new THREE.Matrix4().copy(src.base).invert().multiply(toMatrix4(ref.m));   // relative to its own base
  // Name base (a plain one with its print hidden when no name is chosen).
  const nameSrc = figures[fig.names || 'DICK'];
  const base = pack.build(nameSrc.baseRef); base.matrix.copy(place(nameSrc, nameSrc.baseRef));
  if (!fig.names) base.traverse(o => { if (o.material?.map) o.visible = false; });
  g.add(base);
  // Body, head and hair, with a faint stand-in where the outfit or head is missing.
  const body = fig.jobs ? figures[owner('jobs', fig.jobs)] : null;
  for (const [bag, standIn] of [['jobs', 'DICK'], ['faces', 'DICK'], ['hair', null], ['pets', null]]) {
    const src = fig[bag] ? figures[owner(bag, fig[bag])] : standIn && figures[standIn];
    if (src) for (const ref of src.parts[bag]) add(ref, place(src, ref), !fig[bag]);
  }
  // Held items go in the same hand of this stand's torso; items not held (the flippers) lie by the base.
  if (fig.hobbies) {
    const src = figures[owner('hobbies', fig.hobbies)];
    for (const ref of src.parts.hobbies) {
      const m = toMatrix4(ref.m), at = new THREE.Vector3().setFromMatrixPosition(m);
      const hand = src.hands.findIndex(h => new THREE.Vector3().setFromMatrixPosition(h).distanceTo(at) < 24);
      if (hand >= 0 && body) {
        const rel = src.hands[hand].clone().invert().multiply(m);
        add(ref, new THREE.Matrix4().copy(body.base).invert().multiply(body.hands[hand]).multiply(rel));
      } else add(ref, place(src, ref));
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

// Workbench view: five stands in one picture above the stands' part lists. Drag a figure to turn it.
export async function mount(container, { figures: state }) {
  const data = await load();
  const stage = createStage(container);
  Object.assign(stage.controls, { enabled: false, minDistance: 0, maxDistance: 1e5, maxPolarAngle: Math.PI });   // still run each frame; keep them out of the way
  const cam = stage.camera; cam.fov = 14; cam.updateProjectionMatrix();
  stage.scene.traverse(o => { if (o.isDirectionalLight) { Object.assign(o.shadow.camera, { left: -450, right: 450, top: 250, bottom: -250 }); o.shadow.camera.updateProjectionMatrix(); } });
  stage.centreOn(2 * SPACING, 0);
  const stands = state.map((fig, i) => {
    const holder = new THREE.Group(); holder.position.set(i * SPACING, -8, -10);
    holder.add(buildStand(data, fig)); stage.root.add(holder); return holder;
  });
  // Fit the row to the canvas width (and the figures' height) whenever its shape changes.
  let fitted = 0;
  stage.onTick(() => {
    if (cam.aspect === fitted) return; fitted = cam.aspect;
    const half = Math.tan(THREE.MathUtils.degToRad(cam.fov / 2)), width = 5 * SPACING + 20, height = 150;
    const d = Math.max(width / 2 / (half * cam.aspect), height / 2 / half);
    const tilt = THREE.MathUtils.degToRad(14);
    stage.controls.target.set(0, 52, 0); cam.position.set(0, 52 + d * Math.sin(tilt), d * Math.cos(tilt)); cam.lookAt(0, 52, 0);
  });
  // Turning: drag over a figure turns that one; the arrow keys turn them all.
  const canvas = stage.renderer.domElement;
  canvas.tabIndex = 0;
  canvas.setAttribute('aria-label', 'The five stands in 3D. Drag a figure to turn it; left and right arrow keys turn them all.');
  canvas.addEventListener('pointerdown', e => {
    const r = canvas.getBoundingClientRect(), i = Math.min(4, Math.max(0, Math.floor((e.clientX - r.left) / r.width * 5)));
    canvas.setPointerCapture(e.pointerId);
    let x = e.clientX;
    const move = ev => { stands[i].rotation.y += (ev.clientX - x) * 0.012; x = ev.clientX; };
    const up = () => { canvas.removeEventListener('pointermove', move); canvas.removeEventListener('pointerup', up); canvas.removeEventListener('pointercancel', up); };
    canvas.addEventListener('pointermove', move); canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
  });
  canvas.addEventListener('keydown', e => {
    const d = { ArrowLeft: -0.25, ArrowRight: 0.25 }[e.key]; if (!d) return;
    e.preventDefault(); stands.forEach(s => { s.rotation.y += d; });
  });
  // Rebuild one stand after its parts change (keeps how it is turned).
  function update(i) {
    stands[i].clear(); stands[i].add(buildStand(data, state[i]));
  }
  return { update, dispose: stage.dispose };
}
