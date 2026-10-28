const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const G = require('./raven2-data.js');
const L = require('./table-layout2.js');
const CODES = ['1021', 'BOOK', '1576', 'MEAD', '532', '562', '4865', 'SOLE', '1486', '120', '2134', '2648', '1972'];
// The printed labels (PR-007's envelope table, Cypher_Wheel_Print.pdf).
const RUNES = ['ᚷᛉᚦᛉ', 'ᛉᛖᚠᛁ', 'ᛒᛚᛟᛉ', 'ᚱᛒᛚᚷ', 'ᛈᚹᛟᛇ', 'ᛈᛏᛟᛇ', 'ᚺᛏᛏᚦ', 'ᛏᚾᚠᛖ', 'ᛒᚠᛞᛉ', 'ᛁᛉᚲᛇ', 'ᛚᚹᚲᛏ', 'ᚲᛟᛉᛏ', 'ᛈᛚᚹᛉ'];
test('the thirteen codes and the runes the wheel shows for them match the printed envelopes', () => {
  assert.deepEqual(G.locks.map(l => l.answer), CODES);
  assert.deepEqual(G.labels, RUNES);
  assert.equal(new Set(G.labels).size, 13);
  // A 3-digit code starts with the blank; a leading 0 shows other runes and opens nothing.
  assert.notEqual(G.runesFor('0532'), G.runesFor('532'));
  assert.equal(G.runesFor(' 532'), RUNES[4]);
});
test('a new game starts with L1 and Liv’s notes only', () => {
  assert.deepEqual(G.available(0), ['L1', 'notes']);
});
test('each envelope opens only with its own runes and only in turn', () => {
  const s = G.fresh();
  assert.equal(G.tryEnvelope(s, '1021', 1), 'nomatch'); assert.equal(s.stage, 0);
  assert.equal(G.tryEnvelope(s, '4865', 6), 'later'); assert.equal(s.stage, 0);
  assert.equal(G.tryEnvelope(s, '1021', 0), 'open'); assert.equal(s.stage, 1);
  assert.equal(G.tryEnvelope(s, '1021', 0), 'open-done');
  assert.deepEqual(G.available(1).slice(2), ['AD', 'comb']);
  // A wrong code is remembered once; the right code at the wrong envelope is not a wrong try.
  assert.equal(G.tryEnvelope(s, 'MEAD', 1), 'nomatch'); assert.equal(G.tryEnvelope(s, 'MEAD', 1), 'nomatch');
  assert.deepEqual(s.attempts[1], ['MEAD']);
  assert.equal(G.tryEnvelope(s, 'BOOK', 5), 'nomatch'); assert.deepEqual(s.attempts[1], ['MEAD']);
  CODES.slice(1).forEach((code, i) => assert.equal(G.tryEnvelope(s, code, i + 1), 'open', code));
  assert.equal(s.stage, 13);
});
test('every prop is released exactly once and the whole game hands over every item', () => {
  const released = G.locks.flatMap(l => l.releases);
  assert.equal(new Set(released).size, released.length);
  assert.deepEqual([...new Set([...G.initial, ...released])].sort(), Object.keys(G.items).sort());
  assert.equal(G.locks.length, 13);
});
test('the box holds the contents Full_Adventure.html lists', () => {
  const by = n => G.locks[n - 1].releases;
  assert.deepEqual(by(1), ['AD', 'comb']);
  assert.deepEqual(by(2), ['L2', 'L3']);
  assert.deepEqual(by(3), ['H2', 'H3', 'HD']);
  assert.deepEqual(by(4), ['A2', 'audMap', 'audTicket']);
  assert.deepEqual(by(5), ['R1', 'R6', 'RD']);
  assert.deepEqual(by(6), ['LD', 'ticket', 'map']);
  assert.deepEqual(by(9), ['R3', 'R4', 'R5', 'ruler']);
  assert.deepEqual(by(10), ['H1', 'haraldMap', 'board', 'osloTicket']);
  assert.deepEqual(by(11), ['H4', 'H5', 'ravenCard']);
  assert.deepEqual(by(13), ['planeTicket', 'finalLetter', 'medallion']);
  assert.equal(by(7).filter(id => id.startsWith('coin')).length, 12);
  assert.ok(by(7).includes('tally') && by(12).includes('H6'));
  assert.equal(Object.keys(G.items).filter(k => /^(L|R|A|H)[1-6D]$/.test(k)).length, 22);
});
test('every hint list has text and a solution', () => {
  for (const l of G.locks) { assert.ok(l.hints.length >= 3 && l.hints.every(h => h.length > 10), l.name); assert.ok(l.solution.length > 20, l.name); }
});
test('save round-trip preserves progress, notes and arrangement', () => {
  const s = G.fresh(); G.tryEnvelope(s, '1021', 0); s.notes = 'Try the skies'; s.hints[1] = 3;
  s.pieces.AD = { x: 120, y: 180, rot: 180, face: 1, stowed: true };
  assert.deepEqual(G.restore(JSON.parse(JSON.stringify(s))), s);
});
test('corrupt save data cannot inject unavailable props or invalid positions', () => {
  const s = G.restore({ version: 1, stage: -10, hints: [-8, 999, 'bad'], pieces: { L1: { x: Infinity, y: -1000, rot: 42 }, map: { x: 3 } }, notes: {} });
  assert.equal(s.stage, 0); assert.equal(s.pieces.map, undefined); assert.equal(s.pieces.L1.rot, 0); assert.equal(s.pieces.L1.y, 10);
  assert.deepEqual(s.hints, [0, 7, ...Array(G.locks.length - 2).fill(0)]);
  assert.deepEqual(G.restore(null), G.fresh());
});
test('all referenced physical artwork exists', () => {
  for (const item of Object.values(G.items)) for (const face of item.faces || []) assert.ok(fs.existsSync(path.join(__dirname, face)), face);
});
test('the planned whole-game layout fits: 22 postcards, 4 maps and every other prop, no overlaps', () => {
  const all = L.all();
  assert.equal(all.filter(([k]) => k.startsWith('card')).length, 22);
  assert.equal(all.filter(([k]) => k.startsWith('map')).length, 4);
  for (const [k, p] of all) assert.ok(p.x >= 0 && p.y >= 0 && p.x + p.w <= L.table.w && p.y + p.h <= L.table.h, `${k} leaves the table`);
  for (let i = 0; i < all.length; i++) for (let j = i + 1; j < all.length; j++) {
    const [a, A] = all[i], [b, B] = all[j];
    assert.ok(A.x + A.w <= B.x || B.x + B.w <= A.x || A.y + A.h <= B.y || B.y + B.h <= A.y, `${a} overlaps ${b}`);
  }
});
test('postcards and maps are drawn at print size; the ruler is Liv’s printed card', () => {
  const real = { Postcard: [6, 4], Map: [8.5, 11] };
  for (const item of Object.values(G.items)) if (real[item.kind]) assert.deepEqual([item.w, item.h], real[item.kind].map(v => Math.round(v * G.PPI)), item.name);
  const r = G.items.ruler; assert.ok(r.w / G.PPI > 6 && r.w / G.PPI < 6.6 && r.h / G.PPI < 2, 'ruler card about 160 mm');
  assert.equal(r.faces.length, 2); assert.equal(r.pivots.length, 2);
});
test('the Hnefatafl set has 19 dark pieces, 6 light and the king', () => {
  assert.equal(G.TAFL.filter(k => k === 'dark').length, 19);
  assert.equal(G.TAFL.filter(k => k === 'light').length, 6);
  assert.equal(G.TAFL.filter(k => k === 'king').length, 1);
});
test('the whole game can be dealt onto the table without anything leaving it', () => {
  const s = G.fresh();
  G.deal(s);
  for (let i = 0; i < 13; i++) { G.tryEnvelope(s, CODES[i], i); if (i === 11) G.bringBack(s); G.deal(s); }
  assert.equal(s.stage, 13);
  const size = G.sizes[s.table];
  for (const [id, p] of Object.entries(s.pieces)) { if (p.stowed) continue; const b = G.footprint(id, p); assert.ok(b.x >= -1 && b.y >= -1 && b.x + b.w <= size.w + 1 && b.y + b.h <= size.h + 1, id); }
});
