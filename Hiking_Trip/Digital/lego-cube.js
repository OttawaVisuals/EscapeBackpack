// The Lego cube (lock 7, DG-H31): six flat pieces from the designer's Stud.io exports (assets/lego-cube.ldr assembled,
// assets/lego-cube-flat.ldr laid out; packed by tools/pack-lego.mjs as lego-cube). Players drag pieces onto the faces of
// a cube outline, turn or flip them, and turn the cube to reach the far faces. The rules (cells, faces, clashes, solved)
// live in game-data.js (cubeTurn, pieceCells, placeCube, cubeStatus) and are passed in as `G`.
import * as THREE from 'three';
import { createScene, createStage, renderStill } from './lego3d.js';
import { loadPack } from './lego-model.js';

export const FILES = { red: 'red_piece', blue: 'bue_piece', green: 'green_piece', pink: 'pink_piece', orange: 'orange_piece', purple: 'purple_piece' };
const IDS = Object.keys(FILES);
const NAMES = { red: 'Red', blue: 'Blue', green: 'Green', pink: 'Pink', orange: 'Orange', purple: 'Purple' };
// Loose pieces on the table (LDraw x, z; -z is the front), three each side of the cube, turned a little for a natural look.
const HOME = { red: [-300, 190, 0.2], blue: [-310, 0, 1.75], green: [-295, -190, 3.3], pink: [300, 190, 4.5], orange: [310, 0, 0.9], purple: [295, -190, 2.4] };
const LIFT = 150;            // the cube's centre above the table
const CLASH = 18;            // a piece that overlaps another stands this far off its face

let loading;
const load = () => loading ??= loadPack(new URL('assets/lego-cube.pack.json', import.meta.url).href);

// One piece in LDraw space, centred on its 4 × 4 plate and half way through its thickness (it is 40 LDU, tiles on -y),
// with its share of the marker marks.
function buildPiece(pack, id, G) {
  const refs = pack.files[FILES[id]], plate = refs.find(r => r.file === '3031.dat').m;
  const inner = new THREE.Group(); for (const r of refs) inner.add(pack.build(r));
  inner.position.set(-plate[0], 20, -plate[2]);
  const g = new THREE.Group(); g.add(inner, marks(G, id)); g.userData.id = id;
  return g;
}

// Black marker “5 + 3” round the sides of the solved cube (game-data.js cubeMarks, DG-H33), drawn as one band over the
// four side faces (front, right, back, left). Each 40 × 40 square of a side face is drawn on the piece that owns that cell
// in the solved cube (its tiles, or the end of an edge cell), so the marks travel with the pieces: loose pieces show
// fragments, and each symbol, sitting on a corner, reads whole only on the finished cube.
const NORMALS = [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0]];
let band;
function bandInk(G) {
  if (band) return band;
  const canvas = document.createElement('canvas'); canvas.width = 2048; canvas.height = 512;
  const ctx = canvas.getContext('2d'), face = 512;
  Object.assign(ctx, { strokeStyle: '#161616', lineWidth: G.cubePen * face, lineCap: 'round', lineJoin: 'round' });
  for (const mark of G.cubeMarks) for (const shift of [0, -4]) {         // a symbol on the left|front corner also wraps to x = 0
    const left = (mark.corner + 1 - mark.width / 2 + shift) * face;
    for (const line of mark.strokes) {
      ctx.beginPath(); line.forEach(([x, y], i) => ctx[i ? 'lineTo' : 'moveTo'](left + x * mark.width * face, y * face)); ctx.stroke();
    }
  }
  const map = new THREE.CanvasTexture(canvas); map.colorSpace = THREE.SRGBColorSpace; map.anisotropy = 4;
  return band = new THREE.MeshStandardMaterial({ map, transparent: true, roughness: 0.55, side: THREE.DoubleSide, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
}
function marks(G, id) {
  const owner = new Map();
  for (const [other, at] of Object.entries(G.cubeSolved)) for (const c of G.pieceCells(other, ...at)) owner.set(c, other);
  const back = placement(G, G.cubeSolved[id]).invert(), v = new THREE.Vector3(), up = new THREE.Vector3(0, -1, 0), pos = [], uv = [];   // LDraw up is -y
  NORMALS.forEach((normal, face) => {
    const n = new THREE.Vector3(...normal), right = n.clone().negate().cross(up);
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
      const centre = right.clone().multiplyScalar(40 * (j - 1.5)).addScaledVector(up, 40 * (1.5 - i)).addScaledVector(n, 60);
      if (owner.get(centre.toArray().map(x => Math.round(x / 40 + 1.5)).join(',')) !== id) continue;
      for (const [a, b] of [[-1, -1], [1, -1], [1, 1], [-1, -1], [1, 1], [-1, 1]]) {
        v.copy(centre).addScaledVector(n, 20.3).addScaledVector(right, 20 * a).addScaledVector(up, 20 * b);
        uv.push((face + v.dot(right) / 160 + 0.5) / 4, v.dot(up) / 160 + 0.5); v.applyMatrix4(back); pos.push(v.x, v.y, v.z);
      }
    }
  });
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  const mesh = new THREE.Mesh(geo, bandInk(G)); mesh.renderOrder = 1;
  return mesh;
}

// Where a placed piece sits in the cube (LDraw space, cube centred on the origin).
function placement(G, [face, turn, flip], out = 0) {
  const r = G.cubeTurn(face, turn, flip), n = [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 1, 0]][face], d = 60 + out;
  return new THREE.Matrix4().set(r[0][0], r[0][1], r[0][2], n[0] * d, r[1][0], r[1][1], r[1][2], n[1] * d, r[2][0], r[2][1], r[2][2], n[2] * d, 0, 0, 0, 1);
}

// ---- Table picture: the pieces in a heap, or the finished cube ----
const pictures = new Map();
export function picture(G, cube, size = 360) {
  const solved = G.cubeStatus({ cube }).solved, key = solved ? 'cube' : 'heap';
  if (!pictures.has(key)) pictures.set(key, (async () => {
    const pack = await load(), { scene, root } = createScene('shadow');
    let cam;
    if (solved) {
      for (const id of IDS) { const p = buildPiece(pack, id, G); p.matrixAutoUpdate = false; p.matrix.copy(placement(G, cube[id])); root.add(p); }
      root.position.y = 80;
      const turn = new THREE.Group(); turn.rotation.y = -Math.PI / 2; turn.add(root); scene.add(turn);   // the “5” corner (right|back) faces the camera
      cam = new THREE.PerspectiveCamera(24, 1, 1, 5000); cam.position.set(330, 420, 560); cam.lookAt(0, 70, 0);
    } else {
      const heap = { red: [-95, -80, 0.3, 0], blue: [90, -95, 1.4, 0], green: [-10, 25, 2.6, 46], pink: [-110, 105, 0.9, 0], orange: [110, 85, 2.1, 0], purple: [15, -150, 3.6, 0] };
      for (const [id, [x, z, yaw, y]] of Object.entries(heap)) { const p = buildPiece(pack, id, G); p.position.set(x, -20 - y, z); p.rotation.y = yaw; if (y) p.rotation.z = 0.08; root.add(p); }
      cam = new THREE.PerspectiveCamera(24, 1, 1, 5000); cam.position.set(0, 820, 560); cam.lookAt(0, 0, -10);
    }
    await pack.ready();
    return renderStill(scene, cam, size);
  })());
  return pictures.get(key);
}

// mount(container, { cube, G, bar, onChange }): cube is the save's { id: [face, turn, flip] } (changed in place);
// the status line and buttons go in `bar` (later.js puts it under the canvas).
export async function mount(container, { cube, G, bar = container, onChange = () => {} }) {
  const pack = await load(), stage = createStage(container), state = { cube };
  Object.assign(stage.controls, { enabled: false, minDistance: 0, maxDistance: 1e5, maxPolarAngle: Math.PI });   // the camera is set by the fit below
  const cam = stage.camera; cam.fov = 30; cam.updateProjectionMatrix();
  stage.scene.traverse(o => { if (o.isDirectionalLight) { Object.assign(o.shadow.camera, { left: -480, right: 480, top: 420, bottom: -420, far: 1400 }); o.shadow.camera.updateProjectionMatrix(); } });
  const root = stage.root;

  // The cube: spun as a whole, LDraw space inside. An outline shows where the pieces go.
  const holder = new THREE.Group(); holder.position.y = LIFT; stage.scene.add(holder);
  const spin = new THREE.Group(); holder.add(spin);
  const inside = new THREE.Group(); inside.rotation.x = Math.PI; spin.add(inside);
  const shell = new THREE.Mesh(new THREE.BoxGeometry(160, 160, 160), new THREE.MeshBasicMaterial({ color: 0xf4ebd5, transparent: true, opacity: 0.07, depthWrite: false }));
  const outline = new THREE.LineSegments(new THREE.EdgesGeometry(shell.geometry), new THREE.LineBasicMaterial({ color: 0xf4ebd5, transparent: true, opacity: 0.55 }));
  inside.add(shell, outline);
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(156, 156), new THREE.MeshBasicMaterial({ color: 0xe39a45, transparent: true, opacity: 0.45, side: THREE.DoubleSide, depthWrite: false }));
  glow.visible = false; inside.add(glow);
  const aim = new THREE.Quaternion().setFromEuler(new THREE.Euler(-0.18, -0.62, 0));   // the cube's turn: front and right face the camera, top in view
  spin.quaternion.copy(aim);

  const pieces = Object.fromEntries(IDS.map(id => [id, buildPiece(pack, id, G)]));
  const ring = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(166, 46, 166)), new THREE.LineBasicMaterial({ color: 0xe39a45 }));
  let selected = null, held = null, turning = null;

  function layout() {
    const status = G.cubeStatus(state);
    for (const id of IDS) {
      const p = pieces[id], at = state.cube[id];
      if (held?.id === id && held.dragging) continue;
      if (at) { inside.add(p); placement(G, at, status.clashes.includes(id) ? CLASH : 0).decompose(p.position, p.quaternion, p.scale); }
      else { root.add(p); const [x, z, yaw] = HOME[id]; p.position.set(x, -20, z); p.quaternion.setFromEuler(new THREE.Euler(0, yaw, 0)); }
    }
    shell.visible = outline.visible = !status.solved;
    if (selected) pieces[selected].add(ring); else ring.removeFromParent();
    tools.sync(status);
  }
  const showFace = face => {
    glow.visible = face >= 0; if (face < 0) return;
    const n = [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 1, 0]][face];
    glow.position.set(n[0] * 82, n[1] * 82, n[2] * 82); glow.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), new THREE.Vector3(...n));
  };

  // ---- Camera: from the front and above, fitted to the table and the turning cube (to the cube alone once every piece is on) ----
  const table = [], ball = [];
  for (const x of [-400, 400]) for (const z of [-290, 290]) table.push(new THREE.Vector3(x, 0, -z));   // world z = -LDraw z
  for (const x of [-150, 150]) for (const y of [LIFT - 150, LIFT + 150]) for (const z of [-150, 150]) ball.push(new THREE.Vector3(x, y, z));
  let fitted = '';
  stage.onTick(() => {
    spin.quaternion.slerp(aim, 0.2);
    const all = Object.keys(state.cube).length === 6 && !held?.dragging, key = `${cam.aspect}|${all}`;
    if (key === fitted) return; fitted = key;
    const corners = all ? ball : [...table, ...ball.map(c => new THREE.Vector3(c.x, c.y, 0))];
    const tilt = THREE.MathUtils.degToRad(40), target = new THREE.Vector3(0, 60, 0), v = new THREE.Vector3();
    let d = 1500;
    for (let k = 0; k < 6; k++) {
      cam.position.set(0, target.y + d * Math.sin(tilt), d * Math.cos(tilt)); cam.lookAt(target); cam.updateMatrixWorld();
      let x0 = 1, x1 = -1, y0 = 1, y1 = -1;
      for (const c of corners) { v.copy(c).project(cam); x0 = Math.min(x0, v.x); x1 = Math.max(x1, v.x); y0 = Math.min(y0, v.y); y1 = Math.max(y1, v.y); }
      target.y += (y0 + y1) / 2 * d * Math.tan(THREE.MathUtils.degToRad(cam.fov / 2)) * 0.9;
      d *= Math.max((x1 - x0) / 2, (y1 - y0) / 2) / 0.95;
    }
    cam.position.set(0, target.y + d * Math.sin(tilt), d * Math.cos(tilt)); cam.lookAt(target);
    stage.controls.target.copy(target);
  });

  // ---- Picking, dragging and turning the cube ----
  const canvas = stage.renderer.domElement, ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  canvas.setAttribute('aria-label', 'Six flat Lego pieces on a table and the outline of a cube, in 3D. Drag a piece onto a face; drag elsewhere to turn the cube. The buttons above do the same with the keyboard.');
  const point = e => { const r = canvas.getBoundingClientRect(); ndc.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1); ray.setFromCamera(ndc, cam); };
  const idOf = o => { while (o && !o.userData.id) o = o.parent; return o?.userData.id; };
  const pickPiece = e => { point(e); const meshes = []; for (const id of IDS) if (held?.id !== id) pieces[id].traverse(o => { if (o.isMesh) meshes.push(o); }); return idOf(ray.intersectObjects(meshes, false)[0]?.object); };
  const faceAt = e => {
    point(e); const hit = ray.intersectObject(shell, false)[0]; if (!hit) return -1;
    const n = hit.face.normal; return [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 1, 0]].findIndex(f => f[0] === Math.round(n.x) && f[1] === Math.round(n.y) && f[2] === Math.round(n.z));
  };
  const carry = new THREE.Plane(new THREE.Vector3(0, 1, 0), -70), spot = new THREE.Vector3();
  const follow = e => { point(e); if (!ray.ray.intersectPlane(carry, spot)) return; root.worldToLocal(spot); pieces[held.id].position.set(spot.x, -70, spot.z); };

  canvas.addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    const id = pickPiece(e);
    canvas.setPointerCapture(e.pointerId);
    if (id) { held = { id, x: e.clientX, y: e.clientY, dragging: false }; selected = id; layout(); canvas.style.cursor = 'grabbing'; }
    else turning = { x: e.clientX, y: e.clientY };
  });
  canvas.addEventListener('pointermove', e => {
    if (turning) {
      const dx = e.clientX - turning.x, dy = e.clientY - turning.y; turning.x = e.clientX; turning.y = e.clientY;
      aim.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), dx * 0.01)).premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), dy * 0.01));
      spin.quaternion.copy(aim); return;
    }
    if (!held) { canvas.style.cursor = pickPiece(e) ? 'grab' : 'move'; return; }
    if (!held.dragging && Math.hypot(e.clientX - held.x, e.clientY - held.y) < 5) return;
    if (!held.dragging) {
      held.dragging = true; held.was = state.cube[held.id];
      if (held.was) { G.placeCube(state, held.id, null); layout(); }
      root.add(pieces[held.id]); pieces[held.id].quaternion.identity();
    }
    follow(e); showFace(faceAt(e));
  });
  const drop = e => {
    if (turning) { turning = null; return; }
    if (!held) return;
    const { id, dragging, was } = held; held = null; canvas.style.cursor = '';
    showFace(-1);
    if (dragging) {
      const face = e.type === 'pointerup' ? faceAt(e) : -1;
      if (face >= 0) G.placeCube(state, id, face, was?.[1] ?? 0, was?.[2] ?? 0);
      if (face >= 0 || was) onChange();
    }
    layout();
  };
  canvas.addEventListener('pointerup', drop); canvas.addEventListener('pointercancel', drop);

  // ---- Buttons: the same moves for the keyboard, plus turning and flipping a placed piece ----
  const tools = (() => {
    const tools = document.createElement('div'); tools.className = 'cube-tools';
    const make = (tag, text, label, fn) => { const b = document.createElement(tag); if (tag === 'button') { b.type = 'button'; b.textContent = text; b.addEventListener('click', fn); } if (label) b.setAttribute('aria-label', label); return b; };
    const pieceList = make('select', '', 'Piece'), faceList = make('select', '', 'Where the piece goes');
    pieceList.append(...IDS.map(id => new Option(`${NAMES[id]} piece`, id)));
    faceList.append(new Option('On the table', ''), ...G.cubeFaces.map((f, i) => new Option(`${f[0].toUpperCase()}${f.slice(1)} face`, i)));
    pieceList.addEventListener('change', () => { selected = pieceList.value; layout(); });
    faceList.addEventListener('change', () => {
      const id = pieceList.value, was = state.cube[id];
      G.placeCube(state, id, faceList.value === '' ? null : +faceList.value, was?.[1] ?? 0, was?.[2] ?? 0); selected = id; onChange(); layout();
    });
    const change = fn => () => { const id = pieceList.value, at = state.cube[id]; if (!at) return; G.placeCube(state, id, ...fn(at)); selected = id; onChange(); layout(); };
    const turnLeft = make('button', '⟲', 'Turn the piece anticlockwise', change(([f, t, k]) => [f, (t + 1) % 4, k]));
    const turnRight = make('button', '⟳', 'Turn the piece clockwise', change(([f, t, k]) => [f, (t + 3) % 4, k]));
    const flip = make('button', 'Flip', 'Flip the piece over', change(([f, t, k]) => [f, t, 1 - k]));
    const spinBy = (axis, angle) => () => aim.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(...axis), angle));
    const cubeTurns = [['←', 'Turn the cube left', [0, 1, 0], -Math.PI / 2], ['→', 'Turn the cube right', [0, 1, 0], Math.PI / 2], ['↑', 'Tip the cube away', [1, 0, 0], -Math.PI / 2], ['↓', 'Tip the cube towards you', [1, 0, 0], Math.PI / 2]]
      .map(([t, l, axis, a]) => make('button', t, l, spinBy(axis, a)));
    const group = (label, ...kids) => { const g = document.createElement('span'); g.className = 'cube-group'; const s = document.createElement('span'); s.textContent = label; g.append(s, ...kids); return g; };
    const status = document.createElement('p'); status.className = 'lego3d-status'; status.setAttribute('role', 'status');
    tools.append(group('Piece', pieceList, faceList, turnLeft, turnRight, flip), group('Cube', ...cubeTurns));
    bar.replaceChildren(status, tools);
    const list = ids => { const n = ids.map(id => NAMES[id].toLowerCase()); return n.length > 1 ? `${n.slice(0, -1).join(', ')} and ${n.at(-1)}` : n[0]; };
    return {
      sync(s) {
        if (selected) pieceList.value = selected;
        const at = state.cube[pieceList.value]; faceList.value = at ? String(at[0]) : '';
        turnLeft.disabled = turnRight.disabled = flip.disabled = !at;
        status.textContent = s.solved ? 'The cube is complete: all six pieces fit.'
          : s.clashes.length ? `The ${list(s.clashes)} pieces overlap. Turn, flip or swap one of them.`
          : s.inside.length ? `${s.placed} of 6 pieces on. The ${list(s.inside)} ${s.inside.length > 1 ? 'pieces have their' : 'piece has its'} smooth side facing in.`
          : s.placed ? `${s.placed} of 6 pieces on.` : 'Drag a piece onto a face of the cube. Drag anywhere else to turn the cube.';
        status.classList.toggle('solved', s.solved);
      }
    };
  })();
  layout();
  return { dispose: stage.dispose };
}
