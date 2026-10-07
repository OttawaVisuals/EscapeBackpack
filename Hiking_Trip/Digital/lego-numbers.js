// The four Lego numbers (blue 0, orange 4, brown 1, red 3; locks 1, 4, 7, 9, used for lock 10) in 3D, from the
// user's Stud.io exports (assets/lego-number0…4.ldr, packed together by tools/pack-lego.mjs as lego-numbers).
// Look-only: a picture for the table and a model to turn in the close-up. Design record: DG-H30.
import * as THREE from 'three';
import { createScene, createStage, renderStill } from './lego3d.js';
import { loadPack } from './lego-model.js';

const MODELS = { blue0: 'lego-number0', orange4: 'lego-number4', brown1: 'lego-number1', red3: 'lego-number3' };
// The 4 is built facing the back (seen from the front it reads mirrored and its slopes face inwards), so it is turned round.
const TURN = { orange4: Math.PI };

let loading;
const load = () => loading ??= loadPack(new URL('assets/lego-numbers.pack.json', import.meta.url).href);

// The number standing on the table, centred, facing the front (-z in LDraw). Some are built facing sideways
// (the 0 runs along z), so a number deeper than it is wide is turned a quarter.
function build(pack, id) {
  const inner = new THREE.Group();
  for (const ref of pack.files[MODELS[id]]) inner.add(pack.build(ref));
  const box = b => { const r = new THREE.Box3(); b.updateMatrixWorld(true); b.traverse(c => { if (c.isMesh) { c.geometry.boundingBox ?? c.geometry.computeBoundingBox(); r.union(c.geometry.boundingBox.clone().applyMatrix4(c.matrixWorld)); } }); return r; };
  const turn = new THREE.Group(); turn.add(inner);
  let b = box(turn);
  turn.rotation.y = (b.max.z - b.min.z > b.max.x - b.min.x ? -Math.PI / 2 : 0) + (TURN[id] || 0);
  b = box(turn);
  const c = b.getCenter(new THREE.Vector3());
  turn.position.set(-c.x, -b.max.y, -c.z);                                  // bottom on the table (LDraw y is down)
  const g = new THREE.Group(); g.add(turn);
  const size = b.getSize(new THREE.Vector3());
  return { group: g, height: size.y, width: Math.max(size.x, size.z) };
}

// ---- Table picture: from the front, a little above and to the side ----
const pictures = new Map();
export function picture(id, size = 360) {
  if (!pictures.has(id)) pictures.set(id, (async () => {
    const pack = await load(), { scene, root } = createScene('shadow'), { group, height } = build(pack, id);
    root.add(group);
    const cam = new THREE.PerspectiveCamera(24, 1, 1, 4000), d = height * 2.55;
    cam.position.set(d * 0.32, height * 0.62 + d * 0.3, d * 0.92); cam.lookAt(0, height * 0.5, 0);
    await pack.ready();
    return renderStill(scene, cam, size);
  })());
  return pictures.get(id);
}

// ---- Close-up: the number on the felt, turned with the mouse ----
export async function mount(container, id) {
  const pack = await load(), stage = createStage(container), { group, height } = build(pack, id);
  stage.root.add(group);
  stage.controls.target.set(0, height * 0.5, 0);
  stage.controls.minDistance = height * 1.2; stage.controls.maxDistance = height * 5;
  stage.camera.position.set(height * 0.7, height * 1.1, height * 2.3); stage.controls.update();
  stage.renderer.domElement.setAttribute('aria-label', 'The Lego number in 3D. Drag to turn it, scroll to zoom.');
  return { dispose: stage.dispose };
}
