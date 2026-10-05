// Shared 3D view for the Lego push puzzles (lock 7). Each puzzle module passes its Stud.io exports, rules and texts.
// The player picks up the tool tile, slides it into holes, slides it sideways (if the rules allow) and pushes
// some pieces by hand. Progress is a list of action strings (see lego-sim.js `act`), saved by the game.
import * as THREE from 'three';
import { parseLdr, createPuzzle, shape } from './lego-sim.js';
import { toMatrix4, buildPart, addLabel, createScene, createStage, createAnimator, renderStill } from './lego3d.js';

const DEFAULT_MESSAGES = {
  start: 'Click the tile on top to pick it up.',
  held: 'Point at a hole in the side and click to slide the tile in.',
  inserted: 'The tile is in as far as it will go. Click it to pull it out.',
  blocked: 'It won’t go in. Something is in the way.',
  stuck: 'It won’t budge.',
  solved: 'Solved.'
};

// config: { files: URL[], rules (createPuzzle options), label: { text, on: 'goal' | 'win' }, messages }
export function definePuzzle(config) {
  const messages = { ...DEFAULT_MESSAGES, ...config.messages };
  let loading;
  const load = () => loading ??= Promise.all(config.files.map(f => fetch(f).then(r => { if (!r.ok) throw new Error(`${f}: ${r.status}`); return r.text(); })))
    .then(texts => createPuzzle(texts.map(parseLdr), config.rules));

  // Everything that depends only on the puzzle: built parts and the poses they take.
  function model(puzzle) {
    const { refs, files, box, loose, tool } = puzzle;
    const start = refs.map(r => toMatrix4(r.m));
    const cx = (box.minX + box.maxX + 1) * 10, cz = (box.minZ + box.maxZ + 1) * 10;
    const toolLength = shape(refs[tool].file).cells.length * 20;
    const pose = (x, y, z, turn = 0) => new THREE.Matrix4().makeRotationY(turn).setPosition(x, y, z);
    // Tool `depth` studs inside the face of its opening (negative = outside), `shift` studs sideways.
    const toolPose = ({ op: id, depth, shift = 0 }) => {
      const op = puzzle.opening(id), [dx, dz] = op.dir, alongX = dx !== 0;
      const face = alongX ? (dx > 0 ? box.minX : box.maxX + 1) * 20 : (dz > 0 ? box.minZ : box.maxZ + 1) * 20;
      const centre = face + (alongX ? dx : dz) * (depth * 20 - toolLength / 2);
      const side = (op.row + shift) * 20 + 10, y = op.layer * 8;
      return alongX ? pose(centre, y, side) : pose(side, y, centre, Math.PI / 2);
    };
    const loosePose = (j, off) => start[loose[j]].clone().premultiply(new THREE.Matrix4().makeTranslation(off[0] * 20, 0, off[1] * 20));
    const parked = pose(cx, box.minL * 8 - 37, cz - 10);
    const goalRef = loose[puzzle.goal], goalKids = goalRef === undefined ? [] : files[refs[goalRef].file] || [];
    const goalBottom = Math.max(0, ...goalKids.map(c => c.m[1] + shape(c.file).h));
    // Where the goal piece goes when it slides out and drops onto the table.
    const fall = (state, out) => {
      const off = state.offsets[puzzle.goal], s = [off[0] + out.dir[0] * out.studs, off[1] + out.dir[1] * out.studs];
      const land = loosePose(puzzle.goal, [s[0] + out.dir[0] * 0.6, s[1] + out.dir[1] * 0.6]);
      land.elements[13] = -goalBottom;
      return { edge: loosePose(puzzle.goal, s), land };
    };
    // Poses for a state; the tool, when not in a hole, is at `hand` (default: resting where the start file has it).
    const posesFor = (state, hand = start[tool]) => {
      const list = start.map(m => m.clone());
      state.offsets.forEach((off, j) => { list[loose[j]] = loosePose(j, off); });
      if (state.free) { const out = puzzle.escape({ ...state, free: false, tool: null }); if (out) list[goalRef] = fall(state, out).land; }
      list[tool] = state.tool ? toolPose(state.tool) : hand;
      return list;
    };
    const yaw = m => Math.atan2(m[5], m[3]);
    const build = root => {
      const objects = refs.map((ref, i) => { const o = buildPart(ref, files); o.matrixAutoUpdate = false; o.matrix.copy(start[i]); o.userData.part = i; root.add(o); return o; });
      const { text, on } = config.label || {};
      if (on === 'goal' && goalRef !== undefined) addLabel(objects[goalRef], text, Math.min(0, ...goalKids.map(c => c.m[1])), { turn: yaw(refs[goalRef].m) });
      if (on === 'win' && puzzle.win >= 0) {
        // On top of the end of the piece that comes out of the box.
        const ref = refs[loose[puzzle.win]], [fx, fz] = puzzle.finalOffsets[puzzle.win], m = ref.m;
        const [lx, lz] = shape(ref.file).cells.reduce((best, c) => {
          const score = c2 => fx * (m[3] * c2[0] + m[5] * c2[1]) + fz * (m[9] * c2[0] + m[11] * c2[1]);
          return score(c) > score(best) ? c : best;
        });
        addLabel(objects[loose[puzzle.win]], text, 0, { x: lx, z: lz, turn: yaw(m) });
      }
      return objects;
    };
    return { start, cx, cz, pose, toolPose, loosePose, fall, posesFor, build, parked };
  }

  // ---- Table thumbnail: a still picture of the current state, cached ----
  let thumb;
  const pictures = new Map();
  async function picture(actions = []) {
    const key = JSON.stringify(actions);
    if (pictures.has(key)) return pictures.get(key);
    const puzzle = await load();
    if (!thumb) {
      const m = model(puzzle), { scene, root, centreOn } = createScene('shadow');
      centreOn(m.cx, m.cz);
      const camera = new THREE.PerspectiveCamera(30, 1, 1, 5000);
      camera.position.set(48, 262, 136); camera.lookAt(0, 0, 18);
      thumb = { m, scene, camera, objects: m.build(root) };
    }
    thumb.m.posesFor(puzzle.replay(actions)).forEach((p, i) => thumb.objects[i].matrix.copy(p));
    const url = renderStill(thumb.scene, thumb.camera);
    pictures.set(key, url);
    return url;
  }

  // ---- Interactive view. onChange(actions) is called after each move and on Start over. ----
  async function mount(container, { actions = [], onChange = () => {} } = {}) {
    const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; };
    const view = el('div', 'lego3d-view'), canvasBox = el('div', 'lego3d-canvas'), bar = el('div', 'lego3d-bar');
    const help = el('div', 'lego3d-help', 'Drag to turn · scroll to zoom · keyboard: Enter, then arrows');
    const status = el('p', 'lego3d-status', 'Loading…'); status.setAttribute('role', 'status');
    const moves = el('div', 'lego3d-moves'), left = el('button', '', '◀ Slide'), deeper = el('button', '', 'Push in'), right = el('button', '', 'Slide ▶');
    const again = el('button', '', 'Start over');
    moves.append(left, deeper, right); moves.hidden = true;
    canvasBox.append(help); bar.append(status, moves, again); view.append(canvasBox, bar); container.append(view);

    const puzzle = await load();
    const { tool, loose, openings } = puzzle;
    const m = model(puzzle);
    const stage = createStage(canvasBox);
    stage.centreOn(m.cx, m.cz);
    const objects = m.build(stage.root);
    const anim = createAnimator(objects);
    stage.onTick(now => anim.tick(now));
    const canvas = stage.renderer.domElement;
    canvas.tabIndex = 0;
    canvas.setAttribute('aria-label', 'Lego puzzle in 3D. Enter picks up or pulls out the tile. While holding it, arrow keys choose a hole and Enter slides it in.'
      + (puzzle.lateral ? ' While it is in, left and right arrows slide it sideways and up pushes it further in.' : ''));

    // Openings: invisible pads on the outside faces that glow on hover, plus a see-through preview tile.
    const pads = openings.map(op => {
      const alongX = op.dir[0] !== 0;
      const pad = new THREE.Mesh(new THREE.BoxGeometry(alongX ? 3 : 19, 7.5, alongX ? 19 : 3),
        new THREE.MeshBasicMaterial({ color: 0xffb347, transparent: true, opacity: 0, depthWrite: false }));
      const p = new THREE.Vector3().setFromMatrixPosition(m.toolPose({ op: op.id, depth: 0 }));
      p[alongX ? 'x' : 'z'] += (alongX ? op.dir[0] : op.dir[1]) * 38.5; p.y += 4;
      pad.position.copy(p); pad.userData.opening = op; stage.root.add(pad);
      return pad;
    });
    const ghost = buildPart(puzzle.refs[tool], puzzle.files);
    ghost.traverse(c => { if (c.material) { c.material = c.material.clone(); c.material.transparent = true; c.material.opacity = 0.35; c.material.depthWrite = false; c.castShadow = false; } });
    ghost.matrixAutoUpdate = false; ghost.visible = false; stage.root.add(ghost);
    const perSide = side => openings.filter(o => o.side === side);
    const describe = op => `${op.side[0].toUpperCase() + op.side.slice(1)} side, hole ${perSide(op.side).indexOf(op) + 1} of ${perSide(op.side).length}.`;

    let state, history, picked;
    const mode = () => puzzle.solved(state) ? 'solved' : state.tool ? 'inserted' : picked ? 'held' : 'resting';
    const say = (key, cls = '') => { status.textContent = messages[key] || key; status.className = 'lego3d-status ' + cls; };
    function refresh() {
      const now = mode();
      moves.hidden = !(now === 'inserted' && puzzle.lateral);
      if (now === 'solved') say('solved', 'solved');
      else say(now === 'inserted' ? 'inserted' : now === 'held' ? 'held' : 'start');
    }
    function show(saved) {
      anim.stop(); hover(null);
      history = [...saved]; state = puzzle.replay(history); picked = history.length > 0;
      m.posesFor(state, picked ? m.parked : undefined).forEach((p, i) => objects[i].matrix.copy(p));
      refresh();
    }
    // Phases for a run of states: every piece that changed moves to its new pose together, one stud at a time.
    function phasesFor(from, frames, ms = 380) {
      let prev = from;
      return frames.map(f => {
        const moves = {};
        f.offsets.forEach((off, j) => { if (off[0] !== prev.offsets[j][0] || off[1] !== prev.offsets[j][1]) moves[loose[j]] = m.loosePose(j, off); });
        if (f.tool) moves[tool] = m.toolPose(f.tool);
        prev = f;
        return { ms: Object.keys(moves).length > 1 ? ms + 60 : ms, moves };
      });
    }
    function perform(action) {
      const before = state, r = puzzle.act(state, action);
      const verb = action.split(':')[0];
      if (!r.ok) {
        if (verb === 'in') {
          const op = puzzle.opening(action.slice(3)), stage0 = { op: op.id, depth: -1 }, face = { op: op.id, depth: 0 };
          anim.play([{ ms: 650, arc: tool, moves: { [tool]: m.toolPose(stage0) } }, { ms: 300, moves: { [tool]: m.toolPose(face) } },
            { ms: 120, moves: { [tool]: m.toolPose({ ...face, depth: 0.25 }) } }, { ms: 160, moves: { [tool]: m.toolPose(face) } },
            { ms: 600, arc: tool, moves: { [tool]: m.parked } }], () => {});
          say('blocked', 'bump');
        } else say('stuck', 'bump');
        return;
      }
      const phases = [];
      if (verb === 'in') {
        const t = r.state.tool;
        phases.push({ ms: 650, arc: tool, moves: { [tool]: m.toolPose({ ...t, depth: -1, shift: 0 }) } }, { ms: 300, moves: { [tool]: m.toolPose({ ...t, depth: 0, shift: 0 }) } });
      }
      if (verb === 'out') {
        phases.push({ ms: 380, moves: { [tool]: m.toolPose({ ...before.tool, depth: -1 }) } }, { ms: 600, arc: tool, moves: { [tool]: m.parked } });
      } else phases.push(...phasesFor(before, r.frames, verb === 'in' || verb === 'deeper' ? 300 : 380));
      // A tool pushed back out of its hole by a hand push returns to the hand.
      if (before.tool && !r.state.tool && verb !== 'out') phases.push({ ms: 600, arc: tool, moves: { [tool]: m.parked } });
      let next = r.state;
      const settled = puzzle.settle(next);
      if (settled.free && !next.free) {
        const out = puzzle.escape(next), { edge, land } = m.fall(next, out), g = loose[puzzle.goal];
        phases.push({ ms: 160 * out.studs + 300, moves: { [g]: edge } }, { ms: 380, fall: true, moves: { [g]: land } });
        next = settled;
      }
      state = next; picked = true;
      history.push(action); onChange([...history]);
      hover(null); moves.hidden = true;
      anim.play(phases, refresh);
    }
    function pickUp() { picked = true; anim.play([{ ms: 700, arc: tool, moves: { [tool]: m.parked } }], refresh); }
    // ◀ and ▶ follow the screen: work out which sideways direction currently points right.
    function slide(screenDir) {
      const [ax, az] = puzzle.across(puzzle.opening(state.tool.op));
      const right = new THREE.Vector3().setFromMatrixColumn(stage.camera.matrixWorld, 0);
      const s = Math.sign(ax * right.x - az * right.z) || 1;     // LDraw (x, z) is (x, -z) on screen
      perform(`shift:${s * screenDir > 0 ? '+1' : '-1'}`);
    }

    // ---- Pointer ----
    const raycaster = new THREE.Raycaster(), ndc = new THREE.Vector2();
    function pick(e) {
      const r = canvas.getBoundingClientRect();
      ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
      raycaster.setFromCamera(ndc, stage.camera);
      const hit = raycaster.intersectObjects(mode() === 'held' ? [...pads, ...objects] : objects, true).find(h => h.object.isMesh);
      if (!hit) return null;
      if (hit.object.userData.opening) return { opening: hit.object.userData.opening };
      let o = hit.object; while (o && o.userData.part === undefined) o = o.parent;
      if (!o) return null;
      const j = loose.indexOf(o.userData.part);
      if (j >= 0 && puzzle.pushable[j] && hit.face) {
        // Push into the face that was clicked (sides only). LDraw space is the scene turned 180° about x.
        const n = hit.face.normal.clone().transformDirection(hit.object.matrixWorld), nx = n.x, nz = -n.z;
        if (Math.abs(n.y) < Math.max(Math.abs(nx), Math.abs(nz))) return { part: o.userData.part, hand: j, dir: Math.abs(nx) > Math.abs(nz) ? [-Math.sign(nx), 0] : [0, -Math.sign(nz)] };
      }
      return { part: o.userData.part };
    }
    let hovered = null, glowing = null;
    function hover(op) {
      if (hovered) pads[openings.indexOf(hovered)].material.opacity = 0;
      hovered = op || null;
      if (hovered) { pads[openings.indexOf(hovered)].material.opacity = 0.6; ghost.matrix.copy(m.toolPose({ op: hovered.id, depth: 0 })); ghost.visible = true; }
      else ghost.visible = false;
    }
    function glow(part) {
      if (glowing === part) return;
      for (const p of [glowing, part]) if (p !== null) for (const mat of objects[p].userData.materials) if (mat.emissive) mat.emissive.setHex(p === part ? 0x3a2a10 : 0);
      glowing = part;
    }
    const clickable = t => {
      const now = mode();
      if (!t || now === 'solved') return false;
      return (t.part === tool && (now === 'resting' || now === 'inserted')) || (t.opening && now === 'held') || !!t.dir;
    };
    canvas.addEventListener('pointermove', e => {
      if (anim.busy || e.buttons) return;
      const t = pick(e);
      canvas.style.cursor = clickable(t) ? 'pointer' : '';
      if (mode() === 'held') hover(t?.opening);
      glow(t?.dir && mode() !== 'solved' ? t.part : null);
    });
    let down = null;
    canvas.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; });
    canvas.addEventListener('pointerup', e => {
      if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 6 || anim.busy) return;
      const t = pick(e), now = mode();
      if (!clickable(t)) return;
      if (t.part === tool && now === 'resting') pickUp();
      else if (t.part === tool && now === 'inserted') perform('out');
      else if (t.opening) perform('in:' + t.opening.id);
      else if (t.dir) perform(`hand:${t.hand}:${t.dir[0]},${t.dir[1]}`);
    });
    canvas.addEventListener('keydown', e => {
      if (anim.busy) return;
      const now = mode(), arrow = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (now === 'held' && arrow) {
        e.preventDefault();
        const n = openings.length, at = hovered ? openings.indexOf(hovered) : arrow > 0 ? -1 : 0, next = openings[(at + arrow + n) % n];
        hover(next); status.textContent = describe(next);
      } else if (now === 'inserted' && puzzle.lateral && (e.key === 'ArrowLeft' || e.key === 'ArrowRight' || e.key === 'ArrowUp')) {
        e.preventDefault();
        if (e.key === 'ArrowUp') perform('deeper'); else slide(e.key === 'ArrowRight' ? 1 : -1);
      } else if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (now === 'resting') pickUp();
        else if (now === 'inserted') perform('out');
        else if (now === 'held' && hovered) perform('in:' + hovered.id);
      }
    });
    left.addEventListener('click', () => { if (!anim.busy && mode() === 'inserted') slide(-1); });
    right.addEventListener('click', () => { if (!anim.busy && mode() === 'inserted') slide(1); });
    deeper.addEventListener('click', () => { if (!anim.busy && mode() === 'inserted') perform('deeper'); });
    again.addEventListener('click', () => { show([]); onChange([]); });

    show(actions);
    return { stage, puzzle, perform, get state() { return state; }, get mode() { return mode(); }, get busy() { return anim.busy; } };
  }

  return { load, picture, mount };
}
