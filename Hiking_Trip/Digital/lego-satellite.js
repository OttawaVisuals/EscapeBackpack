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
  function add(page) {
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
  return { add, dispose: stage.dispose };
}
