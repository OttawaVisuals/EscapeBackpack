// Three.js drawing for the Lego puzzles: simplified parts, scenes, a still renderer and a small tween queue.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { shape, partId } from './lego-sim.js';

export const COLORS = { 0: 0x1b2a34, 1: 0x1e5aa8, 2: 0x00852b, 4: 0xb40000, 10: 0x58ab41, 14: 0xfac80a, 15: 0xf4f4f4, 19: 0xe4cd9e, 25: 0xd67923, 36: 0xc91a09, 70: 0x5f3109, 71: 0xa0a5a9, 72: 0x6c6e68 };
const TRANSPARENT = new Set([33, 34, 36, 40, 41, 42, 43, 46, 47]);

export const toMatrix4 = m => new THREE.Matrix4().set(m[3], m[4], m[5], m[0], m[6], m[7], m[8], m[1], m[9], m[10], m[11], m[2], 0, 0, 0, 1);

// One part in LDraw space: a box (or cylinder) per footprint, studs on top unless it is a tile.
export function partMesh(file, colorCode) {
  const g = new THREE.Group();
  const color = new THREE.Color(COLORS[colorCode] ?? 0x999999);
  const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.42, metalness: 0 });
  if (TRANSPARENT.has(colorCode)) { mat.transparent = true; mat.opacity = 0.6; }
  const edgeMat = new THREE.LineBasicMaterial({ color: color.clone().multiplyScalar(0.55) });
  const { cells, h, kind, known } = shape(file);
  if (!known) console.warn('Unknown part, drawn as 1x1:', file);
  const add = geo => {
    const m = new THREE.Mesh(geo, mat); m.castShadow = m.receiveShadow = true; g.add(m);
    if (!kind.startsWith('round')) g.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo), edgeMat));
  };
  const gap = 0.5;
  if (kind.startsWith('round')) add(new THREE.CylinderGeometry(10 - gap, 10 - gap, h - 0.3, 28).translate(0, h / 2, 0));
  else if (partId(file) === '2420') for (const [x, z] of cells) add(new THREE.BoxGeometry(20 - gap, h - 0.3, 20 - gap).translate(x, h / 2, z));
  else {
    const xs = cells.map(c => c[0]), zs = cells.map(c => c[1]);
    const [x0, x1, z0, z1] = [Math.min(...xs), Math.max(...xs), Math.min(...zs), Math.max(...zs)];
    add(new THREE.BoxGeometry(x1 - x0 + 20 - gap, h - 0.3, z1 - z0 + 20 - gap).translate((x0 + x1) / 2, h / 2, (z0 + z1) / 2));
  }
  if (!kind.includes('tile')) {
    const stud = new THREE.CylinderGeometry(6, 6, 4, 20);
    for (const [x, z] of kind === 'jumper' ? [[0, 0]] : cells) { const s = new THREE.Mesh(stud, mat); s.position.set(x, -2, z); s.castShadow = true; g.add(s); }
  }
  g.userData.materials = [mat, edgeMat];
  return g;
}

export function buildPart(ref, files) {
  if (!files[ref.file]) return partMesh(ref.file, ref.color);
  const g = new THREE.Group(); g.userData.materials = [];          // submodel: its children in place
  for (const ch of files[ref.file]) {
    const c = buildPart(ch, files); c.matrixAutoUpdate = false; c.matrix.copy(toMatrix4(ch.m)); g.add(c);
    g.userData.materials.push(...c.userData.materials);
  }
  return g;
}

// A handwritten-looking mark on the top face of a part at local (x, y, z) (LDraw y points down).
// `turn` matches the part's own turn about y so the mark reads upright from the front.
export function addLabel(object, text, y, { x = 0, z = 0, turn = Math.PI } = {}) {
  const canvas = document.createElement('canvas'); canvas.width = canvas.height = 128;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#1d1a17'; ctx.font = 'bold 92px "Segoe Print", "Comic Sans MS", cursive';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 64, 70);
  const tex = new THREE.CanvasTexture(canvas); tex.colorSpace = THREE.SRGBColorSpace;
  const decal = new THREE.Mesh(new THREE.CircleGeometry(8.5, 32), new THREE.MeshBasicMaterial({ map: tex, transparent: true }));
  decal.rotation.set(Math.PI / 2, 0, turn); decal.position.set(x, y - 0.15, z);   // face up
  object.add(decal);
  return decal;
}

// Lights and a floor. `root` holds LDraw space (turned 180° about x so y is up, keeping handedness).
// floor: 'table' draws a wooden-coloured floor; 'shadow' draws only the shadow (for transparent stills).
export function createScene(floor = 'table') {
  const scene = new THREE.Scene();
  if (floor === 'table') scene.background = new THREE.Color(0x102b25);           // the game's table edge and felt (styles.css)
  scene.add(new THREE.HemisphereLight(0xfffbef, 0x8a7d62, 1.6));
  const sun = new THREE.DirectionalLight(0xffffff, 2.2);
  sun.position.set(-160, 320, 220); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0005;
  Object.assign(sun.shadow.camera, { left: -200, right: 200, top: 200, bottom: -200, near: 10, far: 900 });
  scene.add(sun);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(1600, 1600),
    floor === 'table' ? new THREE.MeshStandardMaterial({ color: 0x28534a, roughness: 0.95 }) : new THREE.ShadowMaterial({ opacity: 0.22 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const root = new THREE.Group(); root.rotation.x = Math.PI; scene.add(root);
  return { scene, root, centreOn: (x, z) => root.position.set(-x, 0, z) };   // put LDraw point (x, z) at the origin
}

function renderer(alpha = false) {
  const r = new THREE.WebGLRenderer({ antialias: true, alpha });
  r.setPixelRatio(Math.min(devicePixelRatio, 2));
  r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
  return r;
}

// Interactive view in `container`. Stops and frees the GPU context once the container leaves the page.
export function createStage(container) {
  const { scene, root, centreOn } = createScene('table');
  const gl = renderer();
  container.prepend(gl.domElement);
  const camera = new THREE.PerspectiveCamera(35, 1, 1, 5000);
  const controls = new OrbitControls(camera, gl.domElement);
  controls.enableDamping = true; controls.maxPolarAngle = Math.PI * 0.49; controls.minDistance = 120; controls.maxDistance = 900;
  const ticks = [];
  const resize = () => {
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    gl.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  };
  const observer = new ResizeObserver(resize); observer.observe(container); resize();
  camera.position.set(130, 180, 250); controls.target.set(0, 20, 0); controls.update();
  let seen = false;
  const dispose = () => { gl.setAnimationLoop(null); observer.disconnect(); controls.dispose(); gl.dispose(); gl.forceContextLoss(); };
  gl.setAnimationLoop(now => {
    if (container.isConnected) seen = true; else if (seen) return dispose();
    for (const f of ticks) f(now);
    controls.update(); gl.render(scene, camera);
  });
  return { renderer: gl, scene, camera, controls, root, centreOn, dispose, onTick: f => ticks.push(f) };
}

// One shared offscreen renderer for still pictures (table thumbnails) on a transparent background.
let still;
export function renderStill(scene, camera, size = 460) {
  still ??= renderer(true);
  still.setSize(size, size, false);
  camera.aspect = 1; camera.updateProjectionMatrix();
  still.render(scene, camera);
  return still.domElement.toDataURL('image/png');
}

// Tween queue. A phase moves objects to target matrices together:
// { ms, moves: { index: Matrix4 }, arc: index (lifts it on the way), fall: true (accelerates) }
export function createAnimator(objects) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const p1 = new THREE.Vector3(), p2 = new THREE.Vector3(), q1 = new THREE.Quaternion(), q2 = new THREE.Quaternion(), s = new THREE.Vector3(), one = new THREE.Vector3(1, 1, 1);
  let queue = [], phase = null, start = 0, done = null;
  function begin(now) {
    phase = queue.shift(); start = now;
    if (!phase) { const d = done; done = null; d?.(); return; }
    phase.from = Object.fromEntries(Object.keys(phase.moves).map(i => [i, objects[i].matrix.clone()]));
  }
  return {
    get busy() { return !!phase || queue.length > 0; },
    play(phases, onDone) { queue = phases.slice(); done = onDone; phase = null; begin(performance.now()); },
    stop() { queue = []; phase = null; done = null; },
    tick(now) {
      if (!phase) return;
      const raw = Math.min(1, (now - start) / (reduce ? 1 : phase.ms));
      const t = phase.fall ? raw * raw : ease(raw);
      for (const [i, to] of Object.entries(phase.moves)) {
        phase.from[i].decompose(p1, q1, s); to.decompose(p2, q2, s);
        objects[i].matrix.compose(p1.lerp(p2, t), q1.slerp(q2, t), one);
        if (+i === phase.arc) objects[i].matrix.elements[13] -= 50 * Math.sin(Math.PI * t);
      }
      if (raw >= 1) begin(now);
    }
  };
}
