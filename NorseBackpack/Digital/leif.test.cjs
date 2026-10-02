const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const G = require('./leif-data.js');
test('a new game exposes only the starting props', () => {
  assert.deepEqual(G.available(0), ['L1', 'tagA', 'tagB', 'ticket']);
  assert.ok(!G.available(0).includes('map'));
});
test('locks reject wrong and later answers; each correct answer releases the next set once', () => {
  const s = G.fresh();
  assert.equal(G.attempt(s, '3212'), false); assert.equal(s.stage, 0);
  assert.equal(G.attempt(s, '1021'), true); assert.equal(s.stage, 1);
  assert.equal(G.attempt(s, '1021'), false);
  assert.deepEqual(G.available(s.stage).slice(4), ['L2', 'L3']);
  assert.equal(G.attempt(s, '1576'), true); assert.ok(G.available(s.stage).includes('map'));
  assert.equal(G.attempt(s, '3212'), true); assert.ok(G.available(s.stage).includes('R2'));
  assert.equal(G.attempt(s, '3212'), false); assert.equal(s.stage, 3);
});
test('save round-trip preserves progress, notes and arrangement', () => {
  const s = G.fresh(); G.attempt(s, '1021'); s.notes = 'Try the skies'; s.hints[1] = 2;
  s.pieces.L2 = { x: 120, y: 180, rot: 180, face: 1, stowed: true };
  assert.deepEqual(G.restore(JSON.parse(JSON.stringify(s))), s);
});
test('corrupt save data cannot inject unavailable props or invalid positions', () => {
  const s = G.restore({ version: 1, stage: -10, hints: [-8, 999, 'bad'], pieces: { L1: { x: Infinity, y: -1000, rot: 42 }, map: { x: 3 } }, light: { top: 'map', dx: 99999 }, notes: {} });
  assert.equal(s.stage, 0); assert.equal(s.pieces.map, undefined); assert.equal(s.pieces.L1.rot, 0); assert.equal(s.pieces.L1.y, 10);
  assert.deepEqual(s.hints, [0, 4, 0, 0, 0]); assert.equal(s.light, undefined);
  assert.deepEqual(G.restore(null), G.fresh());
});
test('all referenced physical artwork exists', () => {
  for (const item of Object.values(G.items)) for (const face of item.faces || []) assert.ok(fs.existsSync(path.join(__dirname, face)), face);
  assert.ok(fs.existsSync(path.join(__dirname, '../Props/_Renders/Luggage_Tag_Inserts_Sheet.png')));
});
test('props on the table never overlap or leave it', () => {
  const ids = G.available(G.locks.length), inside = id => { const { w, h, at: [x, y] } = G.items[id]; return x >= 0 && y >= 0 && x + w <= G.table.w && y + h <= G.table.h; };
  for (const id of ids) assert.ok(inside(id), id);
  for (const a of ids) for (const b of ids) if (a < b) {
    const A = G.items[a], B = G.items[b];
    assert.ok(A.at[0] + A.w <= B.at[0] || B.at[0] + B.w <= A.at[0] || A.at[1] + A.h <= B.at[1] || B.at[1] + B.h <= A.at[1], `${a} overlaps ${b}`);
  }
});
test('the planned whole-game layout fits: 22 postcards, 4 maps and every other prop, no overlaps', () => {
  const L = require('./table-layout.js'), all = L.all();
  assert.equal(all.filter(([k]) => k.startsWith('card')).length, 22);
  assert.equal(all.filter(([k]) => k.startsWith('map')).length, 4);
  for (const [k, p] of all) assert.ok(p.x >= 0 && p.y >= 0 && p.x + p.w <= L.table.w && p.y + p.h <= L.table.h, `${k} leaves the table`);
  for (let i = 0; i < all.length; i++) for (let j = i + 1; j < all.length; j++) {
    const [a, A] = all[i], [b, B] = all[j];
    assert.ok(A.x + A.w <= B.x || B.x + B.w <= A.x || A.y + A.h <= B.y || B.y + B.h <= A.y, `${a} overlaps ${b}`);
  }
});
test('every prop is drawn at the same scale', () => {
  const real = { Postcard: [5, 3.5], Map: [8.5, 11] };
  for (const item of Object.values(G.items)) if (real[item.kind]) assert.deepEqual([item.w, item.h], real[item.kind].map(v => Math.round(v * G.PPI)), item.name);
});
const overlapFree = s => {
  const ids = Object.keys(s.pieces), size = G.sizes[s.table];
  for (const id of ids) { const b = G.footprint(id, s.pieces[id]); assert.ok(b.x >= 0 && b.y >= 0 && b.x + b.w <= size.w && b.y + b.h <= size.h, `${id} is off the table`); }
  for (const a of ids) for (const b of ids) if (a < b) {
    const A = G.footprint(a, s.pieces[a]), B = G.footprint(b, s.pieces[b]);
    assert.ok(A.x + A.w <= B.x || B.x + B.w <= A.x || A.y + A.h <= B.y || B.y + B.h <= A.y, `${a} overlaps ${b}`);
  }
};
test('a new game starts on the smallest table, with the four starting props apart', () => {
  const s = G.fresh(); G.deal(s);
  assert.equal(s.table, 0); assert.deepEqual(Object.keys(s.pieces), G.initial); overlapFree(s);
});
test('the table grows as props arrive, never shrinks, and moved props stay put', () => {
  const s = G.fresh(); G.deal(s);
  s.pieces.L1.x = 600; s.pieces.L1.y = 500;
  let last = s.table;
  for (const code of ['1021', '1576', '3212']) {
    G.attempt(s, code); G.deal(s);
    assert.ok(s.table >= last); last = s.table; overlapFree(s);
  }
  assert.deepEqual([s.pieces.L1.x, s.pieces.L1.y], [600, 500]);
  assert.ok(s.table > 0 && s.table < G.sizes.length);
});
test('tidy packs everything face up on the smallest table that holds it', () => {
  const s = G.fresh(); G.attempt(s, '1021'); G.attempt(s, '1576'); G.deal(s);
  s.table = 3; s.pieces.L2.rot = 90; s.pieces.L2.face = 1;
  G.arrange(s);
  assert.ok(s.table < 3); assert.equal(s.pieces.L2.rot, 0); assert.equal(s.pieces.L2.face, 0); overlapFree(s);
});
test('old saves without a table size open on a table big enough for their pieces', () => {
  const s = G.restore({ version: 1, stage: 2, pieces: { map: { x: 3500, y: 1500, rot: 0 } } });
  const right = x => x + G.items.map.w;
  assert.ok(right(3500) <= G.sizes[s.table].w && right(3500) > G.sizes[s.table - 1].w);
});
test('the largest table is the whole-game table', () => {
  assert.deepEqual(G.sizes.at(-1), G.table);
});
test('snap pulls nearby edges flush and lines up the sides, but leaves distant props alone', () => {
  const s = G.fresh(); G.attempt(s, '1021'); G.deal(s);
  s.pieces.L3 = { x: 1000, y: 600, rot: 0, face: 0, stowed: false };
  s.pieces.L2 = { x: 1010, y: 600 - G.items.L2.h - 15, rot: 180, face: 0, stowed: false };
  assert.equal(G.snap(s, 'L2', 25), true);
  assert.deepEqual([s.pieces.L2.x, s.pieces.L2.y], [1000, 600 - G.items.L2.h]);
  s.pieces.L2.y -= 200;
  const before = { ...s.pieces.L2 };
  assert.equal(G.snap(s, 'L2', 25), false); assert.deepEqual(s.pieces.L2, before);
});
test('snap pulls a slightly overlapping card out to meet the edge', () => {
  const s = G.fresh(); G.attempt(s, '1021'); G.deal(s);
  s.pieces.L3 = { x: 1000, y: 600, rot: 0, face: 0, stowed: false };
  s.pieces.L2 = { x: 1000, y: 600 - G.items.L2.h + 10, rot: 180, face: 0, stowed: false };
  G.snap(s, 'L2', 25);
  assert.equal(s.pieces.L2.y, 600 - G.items.L2.h);
});
test('Rollo’s leg: 1486 releases Châlus, Roumare and Walcheren; the three-digit 562 releases Bayeux–Battle and the ruler', () => {
  const s = G.fresh();
  for (const code of ['1021', '1576', '3212']) assert.equal(G.attempt(s, code), true);
  assert.equal(G.attempt(s, '562'), false);
  assert.equal(G.attempt(s, '1486'), true); assert.deepEqual(G.available(s.stage).slice(-3), ['R1', 'R6', 'RD']);
  assert.equal(G.attempt(s, '562'), true); assert.deepEqual(G.available(s.stage).slice(-4), ['R3', 'R4', 'R5', 'ruler']);
  assert.equal(s.stage, G.locks.length);
  G.deal(s); overlapFree(s);
  assert.deepEqual(G.locks.map(l => l.leg), [1, 1, 1, 2, 2]);
});
test('old saves with back: true keep their card turned over; the ruler has three faces', () => {
  const s = G.restore({ version: 1, stage: 1, pieces: { L2: { x: 100, y: 100, rot: 0, back: true } } });
  assert.equal(s.pieces.L2.face, 1); assert.equal(G.items.ruler.faces.length, 3);
});
