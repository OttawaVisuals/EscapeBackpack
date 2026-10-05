// Grid model of a sliding Lego puzzle, built from Stud.io LDraw exports (one file per solution step).
// Units are LDraw: 1 stud = 20, 1 plate = 8, y points down. No Three.js here so Node tests can use it.

// Footprint in studs (x × z), height in LDU, kind. Origin is the top centre of the part.
export const PARTS = {
  '3020': [4, 2, 8], '3021': [3, 2, 8], '3023': [2, 1, 8], '3024': [1, 1, 8], '3623': [3, 1, 8],
  '3710': [4, 1, 8], '3031': [4, 4, 8], '3004': [2, 1, 24], '3005': [1, 1, 24], '3010': [4, 1, 24], '3065': [2, 1, 24],
  '3069': [2, 1, 8, 'tile'], '3070': [1, 1, 8, 'tile'], '63864': [3, 1, 8, 'tile'], '87079': [4, 2, 8, 'tile'], '2431': [4, 1, 8, 'tile'],
  '6141': [1, 1, 8, 'round'], '98138': [1, 1, 8, 'roundtile'], '87580': [2, 2, 8, 'jumper'], '41740': [4, 1, 8, 'jumper2']   // 41740: 1 x 4 with two centre studs
};

// A line-type-1 reference keeps its placement as [x, y, z, a, b, c, d, e, f, g, h, i].
export function parseLdr(text) {
  const files = {}; let cur = null, main = null;
  for (const raw of text.split(/\r?\n/)) {
    const p = raw.trim().split(/\s+/);
    if (p[0] === '0' && p[1] === 'FILE') { cur = p.slice(2).join(' ').toLowerCase(); files[cur] = []; main ??= cur; continue; }
    if (p[0] === '1' && cur) files[cur].push({ color: +p[1], m: p.slice(2, 14).map(Number), file: p.slice(14).join(' ').toLowerCase().replace(/\.dat$/, '') });
  }
  return { files, main, parts: files[main] };
}

export const partId = file => file.replace(/^(\d+)[a-z]$/, '$1');

// Stud cells (centres, local LDU), height and kind of a part.
export function shape(file) {
  const id = partId(file);
  if (id === '2420') return { cells: [[0, 0], [20, 0], [0, 20]], h: 8, kind: '', known: true };   // corner plate: origin on the corner stud
  const [w, d, h, kind = ''] = PARTS[id] || [1, 1, 8];
  const cells = [];
  for (let i = 0; i < w; i++) for (let j = 0; j < d; j++) cells.push([-w * 10 + 10 + 20 * i, -d * 10 + 10 + 20 * j]);
  return { cells, h, kind, known: !!PARTS[id] };
}

export function mul(A, B) {
  const [ax, ay, az, a, b, c, d, e, f, g, h, i] = A, [bx, by, bz, p, q, r, s, t, u, v, w, x] = B;
  return [ax + a * bx + b * by + c * bz, ay + d * bx + e * by + f * bz, az + g * bx + h * by + i * bz,
    a * p + b * s + c * v, a * q + b * t + c * w, a * r + b * u + c * x,
    d * p + e * s + f * v, d * q + e * t + f * w, d * r + e * u + f * x,
    g * p + h * s + i * v, g * q + h * t + i * w, g * r + h * u + i * x];
}

// Grid cells [x, layer, z] a part fills. x and z count studs (cell n spans n*20..n*20+20), layer counts plates.
export function cellsOf(ref, files, M = ref.m) {
  if (files[ref.file]) return files[ref.file].flatMap(ch => cellsOf(ch, files, mul(M, ch.m)));
  const { cells, h } = shape(ref.file);
  const out = [];
  for (const [lx, lz] of cells) {
    const X = M[0] + M[3] * lx + M[5] * lz, Z = M[2] + M[9] * lx + M[11] * lz;
    for (let l = 0; l < h / 8; l++) out.push([Math.floor(X / 20), Math.round(M[1] / 8) + l, Math.floor(Z / 20)]);
  }
  return out;
}

const key = c => c.join(',');
const same = (a, b) => a.every((v, i) => Math.abs(v - b[i]) < 0.1);

export const SIDES = [
  { side: 'left', dir: [1, 0] }, { side: 'right', dir: [-1, 0] },
  { side: 'front', dir: [0, 1] }, { side: 'back', dir: [0, -1] }   // front is the -z face
];

// steps: parsed step files, start first. Rules:
//   limitByColor / limitAll  how far (studs, from the start) a loose part may move
//   stayInside               loose parts may not be pushed past the edge of the box
//   lateral                  the inserted tool may be slid sideways
//   handPush(ref, files)     loose parts the player may push directly
//   winPart(movers)          ref index of the part whose final position solves the puzzle (default: the goal falling out)
export function createPuzzle(steps, { limitByColor = {}, limitAll = Infinity, stayInside = true, maxDepth = 3, lateral = false, handPush = () => false, winPart } = {}) {
  const { parts: refs, files } = steps[0];
  const movedIn = k => refs.map((_, i) => i).filter(i => !same(steps[k].parts[i].m, steps[k - 1].parts[i].m));
  const movers = steps.slice(1).map((_, k) => movedIn(k + 1));
  const tool = movers[0].find(i => movers.every(s => s.includes(i)));           // the piece used in every step
  const loose = [...new Set(movers.flat())].filter(i => i !== tool);
  const base = loose.map(i => cellsOf(refs[i], files));
  const toolLength = shape(refs[tool].file).cells.length;

  const fixed = new Set();
  refs.forEach((r, i) => { if (i !== tool && !loose.includes(i)) for (const c of cellsOf(r, files)) fixed.add(key(c)); });
  const all = [...fixed].map(k => k.split(',').map(Number));
  const box = {
    minX: Math.min(...all.map(c => c[0])), maxX: Math.max(...all.map(c => c[0])),
    minL: Math.min(...all.map(c => c[1])), maxL: Math.max(...all.map(c => c[1])),
    minZ: Math.min(...all.map(c => c[2])), maxZ: Math.max(...all.map(c => c[2]))
  };
  const inBox = ([x, , z]) => x >= box.minX && x <= box.maxX && z >= box.minZ && z <= box.maxZ;
  const at = (j, off) => base[j].map(([x, l, z]) => [x + off[0], l, z + off[1]]);

  // Where each loose part sits in the last export, as a stud offset (null if it left the grid, e.g. fell).
  const last = steps[steps.length - 1];
  const sortCells = cs => cs.map(c => [...c]).sort((a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2]);
  const finalOffsets = loose.map((i, j) => {
    const a = sortCells(base[j]), b = sortCells(cellsOf(last.parts[i], last.files));
    const d = [b[0][0] - a[0][0], b[0][1] - a[0][1], b[0][2] - a[0][2]];
    return a.length === b.length && d[1] === 0 && a.every((c, n) => c[0] + d[0] === b[n][0] && c[1] === b[n][1] && c[2] + d[2] === b[n][2]) ? [d[0], d[2]] : null;
  });
  // The goal is the loose piece that ends up outside the box in the last step.
  const goal = loose.findIndex(i => cellsOf(last.parts[i], last.files).every(c => !inBox(c)));
  const win = winPart ? loose.indexOf(winPart(movers)) : -1;
  const limit = loose.map(i => limitByColor[refs[i].color] ?? limitAll);
  const pushable = loose.map(i => !!handPush(refs[i], files));

  // Every empty cell on the outside of the box is a hole the tool can enter.
  const openings = [];
  for (const { side, dir } of SIDES) {
    const alongX = dir[0] !== 0;
    const [lo, hi] = alongX ? [box.minZ, box.maxZ] : [box.minX, box.maxX];
    for (let row = lo; row <= hi; row++) for (let layer = box.minL; layer <= box.maxL; layer++) {
      const face = alongX ? [dir[0] > 0 ? box.minX : box.maxX, layer, row] : [row, layer, dir[1] > 0 ? box.minZ : box.maxZ];
      if (!fixed.has(key(face))) openings.push({ id: `${side}:${row}:${layer}`, side, dir, row, layer, face });
    }
  }
  const opening = id => openings.find(o => o.id === id);
  const across = op => op.dir[0] ? [0, 1] : [1, 0];      // the sideways direction for a tool in this opening

  // Tool state { op, depth, shift }: `depth` studs inside the face, moved `shift` studs sideways. Cells cover its whole length.
  function toolCells(t) {
    if (!t) return [];
    const op = opening(t.op), [ax, az] = across(op);
    return Array.from({ length: toolLength }, (_, k) => {
      const d = t.depth - k;
      return [op.face[0] + op.dir[0] * (d - 1) + ax * t.shift, op.layer, op.face[2] + op.dir[1] * (d - 1) + az * t.shift];
    });
  }
  const initialState = () => ({ offsets: loose.map(() => [0, 0]), tool: null, free: false });
  function occupancy(state) {
    const m = new Map();
    state.offsets.forEach((off, j) => { for (const c of at(j, off)) m.set(key(c), j); });
    for (const c of toolCells(state.tool)) m.set(key(c), 'tool');
    return m;
  }

  // Move `seeds` (loose indices or 'tool') one stud along dir, with everything they push. Null if anything can't move.
  function shove(state, seeds, dir) {
    const occ = occupancy(state), moved = new Set(seeds), queue = [...seeds];
    while (queue.length) {
      const m = queue.shift();
      for (const [x, l, z] of m === 'tool' ? toolCells(state.tool) : at(m, state.offsets[m])) {
        const k = key([x + dir[0], l, z + dir[1]]);
        if (fixed.has(k)) return null;
        const o = occ.get(k);
        if (o !== undefined && !moved.has(o)) { moved.add(o); queue.push(o); }
      }
    }
    const offsets = state.offsets.map((o, j) => moved.has(j) ? [o[0] + dir[0], o[1] + dir[1]] : o);
    for (const j of moved) {
      if (j === 'tool') continue;
      if (Math.abs(offsets[j][0]) + Math.abs(offsets[j][1]) > limit[j]) return null;
      if (stayInside && at(j, offsets[j]).some(c => !inBox(c))) return null;
    }
    let t = state.tool;
    if (moved.has('tool')) {
      const op = opening(t.op), [ax, az] = across(op);
      t = { ...t, depth: t.depth + op.dir[0] * dir[0] + op.dir[1] * dir[1], shift: t.shift + ax * dir[0] + az * dir[1] };
      if (t.depth > maxDepth) return null;
      if (t.depth < 1) t = null;                         // pushed back out into the hand
    }
    return { ...state, offsets, tool: t };
  }

  // Slide the tool in along its opening as far as it goes; frames collect the state after each stud.
  function advance(state, frames) {
    let cur = state;
    while (cur.tool && cur.tool.depth < maxDepth) {
      const next = shove(cur, ['tool'], opening(cur.tool.op).dir);
      if (!next?.tool) break;
      cur = next; frames.push(cur);
    }
    return cur;
  }

  // Actions (saved as strings): in:<opening id>, deeper, shift:+1, shift:-1, out, hand:<loose index>:<dx>,<dz>.
  // Returns { ok, state, frames } where frames are the states after each stud of movement.
  function act(state, action) {
    const fail = { ok: false, state, frames: [] };
    if (state.free || typeof action !== 'string') return fail;
    const [verb, ...rest] = action.split(':'), arg = rest.join(':'), frames = [];
    if (verb === 'in') {
      const op = opening(arg);
      if (!op || state.tool) return fail;
      const end = advance({ ...state, tool: { op: op.id, depth: 0, shift: 0 } }, frames);
      return end.tool?.depth ? { ok: true, state: end, frames } : fail;
    }
    if (verb === 'deeper') {
      if (!state.tool) return fail;
      const end = advance(state, frames);
      return frames.length ? { ok: true, state: end, frames } : fail;
    }
    if (verb === 'shift') {
      const s = arg === '+1' ? 1 : arg === '-1' ? -1 : 0;
      if (!lateral || !state.tool || !s) return fail;
      const [ax, az] = across(opening(state.tool.op)), next = shove(state, ['tool'], [ax * s, az * s]);
      return next ? { ok: true, state: next, frames: [next] } : fail;
    }
    if (verb === 'out') {
      const next = { ...state, tool: null };
      return state.tool ? { ok: true, state: next, frames: [next] } : fail;
    }
    if (verb === 'hand') {
      const j = Number(rest[0]), d = (rest[1] || '').split(',').map(Number);
      if (!pushable[j] || d.length !== 2 || Math.abs(d[0]) + Math.abs(d[1]) !== 1) return fail;
      const next = shove(state, [j], d);
      return next ? { ok: true, state: next, frames: [next] } : fail;
    }
    return fail;
  }

  // Can the goal piece slide straight out of the box (tilting the puzzle)? Returns its direction and distance.
  function escape(state) {
    if (goal < 0) return null;
    const occ = occupancy(state);
    for (const { dir } of SIDES) {
      for (let n = 1; n <= 20; n++) {
        const off = [state.offsets[goal][0] + dir[0] * n, state.offsets[goal][1] + dir[1] * n];
        const cs = at(goal, off);
        if (cs.some(c => fixed.has(key(c)) || (occ.has(key(c)) && occ.get(key(c)) !== goal))) break;
        if (cs.every(c => !inBox(c))) return { dir, studs: n };
      }
    }
    return null;
  }
  const solved = state => win >= 0 ? same(state.offsets[win], finalOffsets[win]) : state.free;
  // After a move, a goal piece that can slide out does (gravity, in person).
  const settle = state => !state.free && escape(state) ? { ...state, free: true } : state;

  // Replay saved actions. Unknown or blocked actions are skipped.
  function replay(actions = []) {
    let state = initialState();
    for (const a of actions) {
      const r = act(state, a);
      if (r.ok) state = settle(r.state);
    }
    return state;
  }

  return { refs, files, tool, loose, goal, win, box, openings, limit, pushable, movers, finalOffsets, lateral,
    initialState, act, escape, settle, solved, replay, toolCells, across, opening, cellsOfLoose: at };
}
