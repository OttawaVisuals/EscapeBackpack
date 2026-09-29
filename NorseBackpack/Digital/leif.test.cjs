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
  s.pieces.L2 = { x: 120, y: 180, rot: 180, back: true, stowed: true };
  s.light = { ...s.light, top: 'L2', bottom: 'L3', dx: 0, dy: 0, rotation: 180, on: true };
  assert.deepEqual(G.restore(JSON.parse(JSON.stringify(s))), s);
});
test('corrupt save data cannot inject unavailable props or invalid positions', () => {
  const s = G.restore({ version: 1, stage: -10, hints: [-8, 999, 'bad'], pieces: { L1: { x: Infinity, y: -1000, rot: 42 }, map: { x: 3 } }, light: { top: 'map', dx: 99999 }, notes: {} });
  assert.equal(s.stage, 0); assert.equal(s.pieces.map, undefined); assert.equal(s.pieces.L1.rot, 0); assert.equal(s.pieces.L1.y, 10);
  assert.deepEqual(s.hints, [0, 4, 0]); assert.equal(s.light.top, 'L1'); assert.equal(s.light.dx, 600);
  assert.deepEqual(G.restore(null), G.fresh());
});
test('all referenced physical artwork exists', () => {
  for (const item of Object.values(G.items)) for (const face of item.faces || []) assert.ok(fs.existsSync(path.join(__dirname, face)), face);
  assert.ok(fs.existsSync(path.join(__dirname, '../Props/_Renders/Luggage_Tag_Inserts_Sheet.png')));
});
