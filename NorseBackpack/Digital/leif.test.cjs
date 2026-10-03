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
  assert.deepEqual(s.hints, [0, 4, ...Array(G.locks.length - 2).fill(0)]); assert.equal(s.light, undefined);
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
// Props on the table stay on it and apart; the cards of a pile overlap by design, so each pile counts as one block.
const overlapFree = s => {
  const size = G.sizes[s.table], blocks = {};
  for (const [id, p] of Object.entries(s.pieces)) {
    if (p.stowed) continue;
    const b = G.footprint(id, p), key = p.pile ? 'pile:' + p.pile : id, u = blocks[key];
    assert.ok(b.x >= 0 && b.y >= 0 && b.x + b.w <= size.w && b.y + b.h <= size.h, `${id} is off the table`);
    blocks[key] = u ? { x: Math.min(u.x, b.x), y: Math.min(u.y, b.y), w: Math.max(u.x + u.w, b.x + b.w) - Math.min(u.x, b.x), h: Math.max(u.y + u.h, b.y + b.h) - Math.min(u.y, b.y) } : b;
  }
  const keys = Object.keys(blocks);
  for (const a of keys) for (const b of keys) if (a < b) {
    const A = blocks[a], B = blocks[b];
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
  assert.equal(s.stage, 5);
  G.deal(s); overlapFree(s);
});
test('old saves with back: true keep their card turned over; the ruler has three faces', () => {
  const s = G.restore({ version: 1, stage: 1, pieces: { L2: { x: 100, y: 100, rot: 0, back: true } } });
  assert.equal(s.pieces.L2.face, 1); assert.equal(G.items.ruler.faces.length, 3);
});
test('the ruler turns about its 0 mark to any angle, keeping that point fixed', () => {
  const p = { x: 500, y: 400, rot: 0, face: 0, stowed: false }, it = G.items.ruler, zero = [it.w * 6 / 300, it.h / 2];
  const before = G.onTable('ruler', p, zero);
  G.turnAbout('ruler', p, 37.5, zero);
  assert.equal(p.rot, 37.5);
  const after = G.onTable('ruler', p, zero);
  assert.ok(Math.abs(after[0] - before[0]) < 1e-9 && Math.abs(after[1] - before[1]) < 1e-9);
  const b = G.footprint('ruler', p), a = 37.5 * Math.PI / 180;
  assert.ok(Math.abs(b.w - (it.w * Math.cos(a) + it.h * Math.sin(a))) < 1e-9);
});
test('an angled ruler survives a save and never snaps; other props keep quarter turns', () => {
  const s = G.restore({ version: 1, stage: 5, pieces: { ruler: { x: 900, y: 300, rot: 397.5 }, L1: { x: 100, y: 100, rot: 37.5 } } });
  assert.equal(s.pieces.ruler.rot, 37.5); assert.equal(s.pieces.L1.rot, 0);
  s.pieces.L2 = { x: 900, y: 300 + G.items.ruler.h + 5, rot: 0, face: 0, stowed: false };
  const r = { ...s.pieces.ruler };
  assert.equal(G.snap(s, 'ruler', 50), false); assert.deepEqual(s.pieces.ruler, r);
});
const toStage = n => { const s = G.fresh(); for (const c of ['1021', '1576', '3212', '1486', '562', '104', '521', 'SOLE', 'BOOK', '2648', 'MEAD', '253', '1972'].slice(0, n)) assert.equal(G.attempt(s, c), true, c); assert.equal(s.stage, n); return s; };
test('lock 6 opens with 104 and brings Aud’s first props', () => {
  const s = toStage(5);
  assert.equal(G.locks[5].pending, undefined);
  for (const guess of ['1039', '1040', '0000', '', 'null']) assert.equal(G.attempt(s, guess), false);
  assert.equal(G.attempt(s, '104'), true); assert.equal(s.stage, 6);
  assert.deepEqual(G.available(6).slice(-3), ['A2', 'audMap', 'audTicket']);
});
test('Aud’s leg: 521 brings the coins and tally, SOLE (any case) the comb, BOOK the first of Harald’s props', () => {
  const s = toStage(6);
  assert.equal(G.attempt(s, '521'), true);
  const coins = G.available(s.stage).filter(id => G.items[id].kind === 'Coin');
  assert.equal(coins.length, 12); assert.ok(G.available(s.stage).includes('tally'));
  assert.equal(G.attempt(s, 'sole'), true); assert.deepEqual(G.available(s.stage).slice(-2), ['AD', 'comb']);
  assert.equal(G.attempt(s, 'BOOK'), true); assert.deepEqual(G.available(s.stage).slice(-4), ['H4', 'H5', 'haraldMap', 'ravenCard']);
  G.deal(s); overlapFree(s);
});
test('the comb settles over AD’s two printed dots, travels with the card, and comes loose if the card turns face up', () => {
  const s = toStage(8); G.attempt(s, 'SOLE'); G.deal(s);
  Object.assign(s.pieces.AD, { x: 600, y: 500, rot: 0, face: 1 });
  Object.assign(s.pieces.comb, { x: 600 - 16.5 * 88 / 72 + 5, y: 500 + 7 * 88 / 72 - 4, rot: 0, face: 0 });
  assert.equal(G.seatComb(s, 3), false);
  assert.equal(G.seatComb(s, 12), true);
  const near = () => { const { holes: h, dots: d } = G.combPoints(s); return Math.max(...[0, 1].map(i => Math.hypot(h[i][0] - d[i][0], h[i][1] - d[i][1]))); };
  assert.ok(near() < 1e-9);
  s.pieces.AD.x += 300; s.pieces.AD.rot = 90; G.followSeat(s);
  assert.ok(near() < 1e-9); assert.equal(s.pieces.comb.rot, 90);
  s.pieces.AD.face = 0; G.followSeat(s); assert.equal(s.pieces.comb.seated, false);
});
test('the comb will not settle face down, or on the picture side of the card', () => {
  const s = toStage(8); G.attempt(s, 'SOLE'); G.deal(s);
  Object.assign(s.pieces.AD, { x: 600, y: 500, rot: 0, face: 0 });
  Object.assign(s.pieces.comb, { x: 600 - 16.5 * 88 / 72, y: 500 + 7 * 88 / 72, rot: 0, face: 0 });
  assert.equal(G.seatComb(s, 12), false);
  s.pieces.AD.face = 1; s.pieces.comb.face = 1; assert.equal(G.seatComb(s, 12), false);
});
test('the tally keeps its digits through a save and through Tidy', () => {
  const s = toStage(7); G.deal(s); s.pieces.tally.wheels = [3, 7, 0, 5];
  const r = G.restore(JSON.parse(JSON.stringify(s))); assert.deepEqual(r.pieces.tally.wheels, [3, 7, 0, 5]);
  G.arrange(r); assert.deepEqual(r.pieces.tally.wheels, [3, 7, 0, 5]);
  assert.deepEqual(G.restore({ version: 1, stage: 7, pieces: { tally: { x: 10, y: 10, wheels: [12, -1, 'x'] } } }).pieces.tally.wheels, [9, 0, 0, 0]);
});
test('Harald’s leg: 2648, MEAD (any case) and 253 bring the board, ticket, last card, bookings and journal', () => {
  const s = toStage(9);
  assert.equal(G.attempt(s, '2648'), true); assert.deepEqual(G.available(s.stage).slice(-3), ['H2', 'H3', 'HD']);
  assert.equal(G.attempt(s, 'mead'), true); assert.deepEqual(G.available(s.stage).slice(-3), ['H1', 'board', 'osloTicket']);
  assert.equal(G.attempt(s, '235'), false); assert.equal(G.attempt(s, '253'), true);
  assert.deepEqual(G.available(s.stage).slice(-5), ['H6', 'transition1', 'transition2', 'transition3', 'journal']);
  assert.equal(G.available(s.stage).filter(id => G.items[id].kind === 'Postcard').length, 22);
  G.deal(s); overlapFree(s);
  assert.deepEqual(G.items.osloTicket.faceNames, ['front', 'back', 'held to the light']);
});
test('Hnefatafl pieces keep their squares through a save; bad or doubled squares go back to the tray', () => {
  const s = toStage(11); G.attempt(s, 'MEAD'); G.deal(s);
  assert.equal(s.pieces.board.tafl.length, 23); assert.ok(s.pieces.board.tafl.every(sq => sq === null));
  s.pieces.board.tafl[22] = 'F6'; s.pieces.board.tafl[0] = 'K8';
  const r = G.restore(JSON.parse(JSON.stringify(s))); assert.equal(r.pieces.board.tafl[22], 'F6'); assert.equal(r.pieces.board.tafl[0], 'K8');
  const bad = G.restore({ version: 1, stage: 11, pieces: { board: { x: 10, y: 10, tafl: ['A1', 'A1', 'Z9', 'K12', 5, 'F6'] } } }).pieces.board.tafl;
  assert.deepEqual(bad.slice(0, 6), ['A1', null, null, null, null, 'F6']); assert.equal(bad.length, 23);
});
test('every lock has a one-line nudge for the lock box and the lock-open pop-up', () => {
  for (const lock of G.locks) { assert.equal(typeof lock.nudge, 'string', lock.name); assert.ok(lock.nudge.length > 10 && lock.nudge.length < 120, lock.name); }
});
test('the final lock: 1972 opens the middle pocket and brings the medallion', () => {
  const s = toStage(12);
  assert.equal(G.attempt(s, '1279'), false);
  assert.equal(G.attempt(s, '1972'), true); assert.equal(s.stage, G.locks.length);
  assert.deepEqual(G.available(s.stage).slice(-1), ['medallion']);
  G.deal(s); overlapFree(s);
});
test('marker lines on the maps survive a save and Tidy; bad lines are dropped', () => {
  const s = toStage(12); G.deal(s);
  s.pieces.map.marks = [[0.1, 0.2, 0.3, 0.4], [0.5, 0.5, 0.6, 0.7]];
  const r = G.restore(JSON.parse(JSON.stringify(s))); assert.deepEqual(r.pieces.map.marks, [[0.1, 0.2, 0.3, 0.4], [0.5, 0.5, 0.6, 0.7]]);
  G.arrange(r); assert.equal(r.pieces.map.marks.length, 2);
  assert.deepEqual(G.markLines([[0, 0, 1, 1], [2, 0, 0, 0], [0, 0, 0], 'x', [0, NaN, 0, 0]]), [[0, 0, 1, 1]]);
  assert.ok(['map', 'rolloMap', 'audMap', 'haraldMap'].every(id => G.items[id].marker));
});
test('Tidy stacks older keepsakes: postcards, maps and papers in piles, solid props put away', () => {
  // Played through without tidying: every lock's props were dealt as they arrived.
  const s = G.fresh(); G.deal(s);
  for (const c of ['1021', '1576', '3212', '1486', '562', '104', '521', 'SOLE']) { G.attempt(s, c); G.deal(s); }
  const before = s.table;
  G.arrange(s); overlapFree(s);
  const pile = name => G.pileMembers(s, name);
  assert.deepEqual(pile('cards'), ['L1', 'L2', 'L3', 'LD', 'R2', 'R1', 'R6', 'RD', 'R3', 'R4', 'R5', 'A2']);
  assert.deepEqual(pile('maps'), ['map', 'rolloMap', 'audMap']);
  assert.deepEqual(new Set(pile('papers')), new Set(['tagA', 'tagB', 'ticket', 'rouenTicket', 'audTicket']));
  assert.equal(s.pieces.ruler.stowed, true);
  for (const id of ['A1', 'A3', 'coin1', 'tally', 'AD', 'comb']) assert.ok(!s.pieces[id].pile && !s.pieces[id].stowed, id);
  assert.ok(s.table < before, 'the table shrinks');
  // Fanned: each card's bottom edge sits one strip below the card on top of it.
  const bottom = id => s.pieces[id].y + G.items[id].h;
  for (const name of ['cards', 'maps', 'papers']) pile(name).slice(1).forEach((id, i) => assert.equal(bottom(id) - bottom(pile(name)[i]), G.STRIP, id));
});
test('Tidy piles what came before the last two locks, and for the last lock leaves every postcard and map out', () => {
  const s = toStage(3); G.attempt(s, '1486'); G.deal(s); G.arrange(s);
  for (const id of ['R2', 'rolloMap', 'rouenTicket', 'R1']) assert.ok(!s.pieces[id].pile, id);
  assert.equal(s.pieces.L1.pile, 'cards');
  const f = toStage(12); G.deal(f); G.arrange(f); overlapFree(f);
  for (const id of G.available(12)) if (['Postcard', 'Map'].includes(G.items[id].kind) || id.startsWith('transition') || id === 'journal') assert.ok(!f.pieces[id].pile && !f.pieces[id].stowed, id);
  assert.equal(f.pieces.tagA.pile, 'papers'); assert.equal(f.pieces.coin1.stowed, true);
  assert.ok(!f.pieces.board.stowed, 'the board came with lock 11, one of the last two');
});
test('a card taken out of its pile goes to a free spot and the pile closes up; piles survive a save', () => {
  const s = toStage(6); G.deal(s); G.arrange(s);
  const top = s.pieces.L1.y;
  assert.equal(G.release(s, 'L1'), true); overlapFree(s);
  assert.ok(!s.pieces.L1.pile); assert.equal(s.pieces.L2.y, top);
  assert.equal(G.release(s, 'ruler'), true); assert.equal(s.pieces.ruler.stowed, false); overlapFree(s);
  G.unpile(s, 'R5'); assert.ok(!s.pieces.R5.pile);
  const r = G.restore(JSON.parse(JSON.stringify(s)));
  assert.deepEqual(G.pileMembers(r, 'cards'), G.pileMembers(s, 'cards')); assert.deepEqual(r.piles, s.piles);
  const bad = G.restore({ version: 1, stage: 6, pieces: { L1: { x: 10, y: 10, pile: 'maps' }, map: { x: 10, y: 10, pile: 'maps' } } });
  assert.ok(!bad.pieces.L1.pile && !bad.pieces.map.pile, 'wrong pile or no pile corner: not piled');
});
test('opening a lock never moves props the player has laid out, even on a full table', () => {
  const s = toStage(9); G.deal(s);
  const before = JSON.parse(JSON.stringify(s.pieces));
  // Deal the next lock's props onto a table that is already well filled.
  G.attempt(s, '2648'); const crowded = G.deal(s);
  for (const [id, p] of Object.entries(before)) assert.deepEqual([s.pieces[id].x, s.pieces[id].y, s.pieces[id].rot], [p.x, p.y, p.rot], id);
  assert.equal(typeof crowded, 'boolean');
  for (const id of ['H2', 'H3', 'HD']) assert.ok(s.pieces[id], id);
});
test('opening a lock never stacks anything; the last lock brings piled postcards and maps back out', () => {
  const s = toStage(9); G.deal(s); G.arrange(s); overlapFree(s);
  const piled = id => s.pieces[id].pile;
  assert.equal(piled('L1'), 'cards'); assert.equal(piled('rolloMap'), 'maps');
  Object.assign(s.pieces.A2, { x: 2000, y: 1500 });
  for (const c of ['2648', 'MEAD', '253']) { G.attempt(s, c); G.deal(s); }
  assert.deepEqual([s.pieces.A2.x, s.pieces.A2.y], [2000, 1500], 'a card the player laid out stays put');
  assert.ok(!s.pieces.H4.pile, 'nothing is stacked when a lock opens, even what Tidy would now pile');
  G.bringBack(s); overlapFree(s);
  for (const id of G.available(s.stage)) if (['Postcard', 'Map'].includes(G.items[id].kind)) assert.ok(!s.pieces[id].pile && !s.pieces[id].stowed, id);
  assert.equal(s.pieces.tagA.pile, 'papers');
});
test('every lock names a pocket of the drawn backpack', () => {
  for (const lock of G.locks) assert.ok(G.POCKETS[lock.pocket], lock.name);
  assert.deepEqual(new Set(G.locks.map(l => l.pocket)), new Set(Object.keys(G.POCKETS)));
});
test('the attempt log keeps each wrong code once, newest last, and survives a save; junk is dropped', () => {
  const s = toStage(1);
  for (const c of ['1234', '0000', '1234', 'abcd']) G.attempt(s, c);
  assert.deepEqual(s.attempts[1], ['0000', '1234', 'ABCD']);
  for (let i = 0; i < 40; i++) G.attempt(s, String(1000 + i));
  assert.equal(s.attempts[1].length, G.MAX_ATTEMPTS);
  assert.deepEqual(G.restore(JSON.parse(JSON.stringify(s))).attempts, s.attempts);
  const bad = G.restore({ version: 1, stage: 1, attempts: [['12', 'X'.repeat(9), 5, '1021'], 'nope'] });
  assert.deepEqual(bad.attempts[0], ['1021']); assert.deepEqual(bad.attempts[1], []);
});
test('an earlier lock’s code is recognised, a later one is not', () => {
  const s = toStage(3);
  assert.equal(G.earlierLock(s, '1576'), 1); assert.equal(G.earlierLock(s, ' 1021 '), 0);
  assert.equal(G.earlierLock(s, '1486'), -1, 'lock 4 is the current lock'); assert.equal(G.earlierLock(s, '521'), -1);
});
test('play time, ratings, pinned notes and team name survive a save and are cleaned', () => {
  const s = toStage(2); Object.assign(s, { played: 123456, team: '  The   Ravens ' }); s.lockTime[0] = 5000; s.ratings[0] = 4; s.itemNotes.L1 = 'Two numbers';
  const r = G.restore(JSON.parse(JSON.stringify(s)));
  assert.equal(r.played, 123456); assert.equal(r.lockTime[0], 5000); assert.equal(r.ratings[0], 4); assert.equal(r.itemNotes.L1, 'Two numbers'); assert.equal(r.team, 'The Ravens');
  const bad = G.restore({ version: 1, stage: 0, played: -5, ratings: [9, 'x'], itemNotes: { nope: 'x', L1: 7, tagA: '   ' }, team: 42 });
  assert.equal(bad.played, 0); assert.deepEqual(bad.ratings.slice(0, 2), [5, 0]); assert.deepEqual(bad.itemNotes, {}); assert.equal(bad.team, '');
});
test('the shared result and durations read well', () => {
  assert.equal(G.duration(59 * 60000), '59 min'); assert.equal(G.duration(161 * 60000), '2 h 41 min'); assert.equal(G.duration(0), 'under a minute'); assert.equal(G.duration(61000), '1 min');
  const s = toStage(13); s.hints[0] = 1; s.hints[4] = 4; s.played = 90 * 60000;
  const text = G.shareText(s);
  assert.match(text, /13\/13 locks · 1 h 30 min · 5 hints/); assert.ok(text.includes('💡') && text.includes('🔓'));
  assert.ok(!/1021|1972|SOLE/.test(text), 'no answers in the shared result');
});
test('Liv has an ending; nothing on screen sorts keepsakes into trails', () => {
  assert.ok(G.STORY.letter.length >= 3 && G.STORY.ending.length >= 2); assert.equal(G.STORY.chapters, undefined);
  assert.equal(G.legs, undefined); assert.ok(G.locks.every(l => l.leg === undefined));
  const viking = /Leif|Rollo|Aud|Harald/;
  // Only names printed on the prop itself may name a Viking.
  for (const [id, it] of Object.entries(G.items)) if (viking.test(it.name)) assert.equal(id, 'audTicket', it.name);
  for (const name of Object.values(G.POCKETS)) assert.ok(!viking.test(name), name);
  for (const lock of G.locks) for (const t of [lock.nudge, lock.message, ...lock.hints]) assert.ok(!/\btrail\b|’s (map|trail|comb|sea chart)/i.test(t), t);
});
