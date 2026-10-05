// node --test Hiking_Trip/Digital/lego.test.mjs
// Rules of the 3D Lego push puzzles (lego-sim.js), checked against the user's Stud.io step exports.
// The puzzle modules set the same rules; keep RULES in step with lego-flat.js and lego-square.js.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseLdr, cellsOf, createPuzzle, shape } from './lego-sim.js';

const load = (name, n) => Array.from({ length: n }, (_, i) => parseLdr(readFileSync(new URL(`assets/lego-${name}-step${i}.ldr`, import.meta.url), 'utf8')));
const RULES = {
  flat: { limitByColor: { 25: 1 } },
  square: { limitAll: 1, stayInside: false, lateral: true, handPush: (ref, files) => !!files[ref.file],
    winPart: movers => movers.at(-1).find(i => movers.slice(0, -1).every(s => !s.includes(i))) }
};
const puzzles = { flat: load('flat', 4), square: load('square', 5) };
const flat = createPuzzle(puzzles.flat, RULES.flat), square = createPuzzle(puzzles.square, RULES.square);
const SOLUTION = {
  flat: ['in:right:0:-3', 'out', 'in:front:-11:-3', 'out', 'in:left:-2:-3'],
  square: ['in:back:0:-3', 'shift:-1', 'deeper', 'shift:+1']       // the user's four exported steps
};
const run = (p, actions) => actions.reduce((st, a) => { const r = p.act(st, a); assert.ok(r.ok, a); return p.settle(r.state); }, p.initialState());

// Every reachable state, breadth first; returns the shortest action lists that solve the puzzle.
function shortest(p, maxMoves = 10) {
  const options = st => [
    ...(st.tool ? ['deeper', 'out', ...(p.lateral ? ['shift:+1', 'shift:-1'] : [])] : p.openings.map(o => 'in:' + o.id)),
    ...p.pushable.flatMap((ok, j) => ok ? ['1,0', '-1,0', '0,1', '0,-1'].map(d => `hand:${j}:${d}`) : [])
  ];
  const k = st => JSON.stringify([st.offsets, st.tool]);
  const seen = new Set([k(p.initialState())]); let layer = [{ st: p.initialState(), path: [] }];
  for (let n = 0; n < maxMoves && layer.length; n++) {
    const next = [], wins = [];
    for (const { st, path } of layer) for (const a of options(st)) {
      const r = p.act(st, a); if (!r.ok) continue;
      const ns = p.settle(r.state);
      if (p.solved(ns)) { wins.push([...path, a]); continue; }
      if (!seen.has(k(ns))) { seen.add(k(ns)); next.push({ st: ns, path: [...path, a] }); }
    }
    if (wins.length) return wins;
    layer = next;
  }
  return [];
}

test('every part is known and no two parts overlap in any step', () => {
  for (const [name, steps] of Object.entries(puzzles)) steps.forEach((s, k) => {
    const seen = new Map(), toolAtStart = k === 0 ? (name === 'flat' ? flat : square).tool : -1;
    s.parts.forEach((p, i) => {
      if (i === toolAtStart) return;                                  // resting at an angle on top
      for (const c of cellsOf(p, s.files)) {
        assert.ok(!seen.has(c.join()), `${name} step ${k}: parts ${seen.get(c.join())} and ${i} overlap at ${c}`);
        seen.set(c.join(), i);
      }
    });
    for (const p of Object.values(s.files).flat()) if (!s.files[p.file]) assert.ok(shape(p.file).known, p.file);
  });
});

test('roles come from the step files', () => {
  assert.equal(flat.refs[flat.tool].color, 10, 'flat: green tool');
  assert.deepEqual(flat.loose.map(i => flat.refs[i].color).sort(), [16, 25, 25, 25]);
  assert.equal(flat.refs[flat.loose[flat.goal]].file, 'submodel group 2', 'flat: the red piece falls out');
  assert.equal(square.refs[square.tool].color, 4, 'square: red tool');
  assert.deepEqual(square.loose.map(i => square.refs[i].color).sort(), [16, 25, 25], 'square: bridge and two orange tiles');
  assert.equal(square.goal, -1);
  assert.deepEqual(square.pushable, square.loose.map(i => i === 22), 'square: only the bridge is pushed by hand');
  assert.equal(square.refs[square.loose[square.win]].color, 25, 'square: the orange tile with the 5');
});

test('the solutions reproduce each exported step', () => {
  for (const [name, p, perStep] of [['flat', flat, [1, 2, 2]], ['square', square, [1, 1, 1, 1]]]) {
    let st = p.initialState(), a = 0;
    perStep.forEach((count, k) => {
      for (let n = 0; n < count; n++) { const r = p.act(st, SOLUTION[name][a++]); assert.ok(r.ok, `${name} ${SOLUTION[name][a - 1]}`); st = p.settle(r.state); }
      const s = puzzles[name][k + 1];
      p.loose.forEach((i, j) => {
        if (j === p.goal && st.free) return;                          // the export shows it already on the table
        assert.deepEqual(p.cellsOfLoose(j, st.offsets[j]).sort(), cellsOf(s.parts[i], s.files).sort(), `${name} step ${k + 1}, part ${i}`);
      });
      // In the flat export the tile is drawn one stud further in, after the red piece has dropped out.
      if (st.tool && !st.free) assert.deepEqual(p.toolCells(st.tool).sort(), cellsOf(s.parts[p.tool], s.files).sort(), `${name} step ${k + 1}, tool`);
    });
    assert.ok(p.solved(st), `${name} solved`);
  }
});

test('flat: orange tiles move one stud and stay inside, so left-first is blocked', () => {
  const r = flat.act(flat.initialState(), 'in:left:-2:-3');
  assert.equal(r.state.tool.depth, 1);
  assert.equal(flat.settle(r.state).free, false);
  assert.equal(flat.act(flat.initialState(), 'in:right:0:-3').state.tool.depth, 1);
  assert.equal(flat.act(run(flat, ['in:right:0:-3']), 'shift:+1').ok, false, 'no sideways moves in the flat puzzle');
});

test('flat: the only way out is right, front, left', () => {
  const wins = shortest(flat);
  assert.deepEqual(wins, [SOLUTION.flat]);
});

test('square: pushing deeper before dragging the bridge is blocked; every solution pushes both orange tiles', () => {
  assert.equal(square.act(run(square, ['in:back:0:-3']), 'deeper').ok, false);
  assert.equal(square.act(square.initialState(), 'in:front:-1:-3').ok, false);
  const wins = shortest(square);
  assert.ok(wins.length > 0);
  for (const w of wins) {
    const st = run(square, w);
    assert.deepEqual(st.offsets, square.finalOffsets, w.join(' → '));
  }
  assert.equal(Math.min(...wins.map(w => w.length)), 3, 'pushing the bridge by hand saves a move');
});

test('square: the red tile drags the bridge and the bridge drags the tile', () => {
  const inSlot = run(square, ['in:back:0:-3']);
  const left = square.act(inSlot, 'shift:-1').state;
  assert.deepEqual(left.offsets[square.loose.indexOf(22)], [-1, 0]);
  const byHand = square.act(inSlot, 'hand:0:-1,0').state;
  assert.deepEqual(byHand.tool, { op: 'back:0:-3', depth: 2, shift: -1 });
  assert.equal(square.act(left, 'shift:-1').ok, false, 'the bridge moves one stud only');
});

test('saved actions replay to the same state; junk and blocked actions are skipped', () => {
  assert.equal(flat.replay([]).free, false);
  assert.equal(flat.replay(SOLUTION.flat).free, true);
  assert.equal(flat.replay(['in:left:-2:-3', 'out', 'nonsense', ...SOLUTION.flat]).free, true);
  assert.equal(flat.replay(['in:front:-11:-3', 'out']).offsets.every(o => !o[0] && !o[1]), true, 'blocked before push 1');
  assert.ok(square.solved(square.replay(SOLUTION.square)));
  assert.ok(!square.solved(square.replay(['in:back:0:-3', 'deeper', 'shift:+1'])));
  assert.ok(square.solved(square.replay(['hand:0:-1,0', 'in:back:-1:-3', 'shift:+1'])));
});
