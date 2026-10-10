const { test } = require('node:test');
const assert = require('node:assert/strict');
const G = require('./game-data.js');
const codes = ['749', '734', 'MOON', '326', '414', '102', '518', 'DICK', '632', '4130'];
const playTo = (stage, { card = true } = {}) => { const s = G.fresh(); for (const code of codes.slice(0, stage)) { if (card && s.stage === 2) G.discover(s, 'newspaper'); assert.equal(G.unlock(s, code), true, code); } return s; };

test('all ten real locks gate progression in order', () => {
  const state = G.fresh();
  assert.deepEqual(G.available(state.stage), ['bottle']);
  for (const [i, code] of codes.entries()) {
    for (const later of codes.slice(i + 1)) if (later !== code) assert.equal(G.unlock(state, later), false, `${later} at lock ${i + 1}`);
    assert.equal(G.unlock(state, code.toLowerCase()), true, code);
    assert.equal(state.stage, i + 1);
  }
  assert.equal(G.unlock(state, '4130'), false);
  assert.equal(G.locks.length, 10);
});

test('the clipping stays inside the card until the card is opened', () => {
  const state = playTo(2, { card: false });
  assert.equal(G.available(2, state.found).includes('newspaper'), false);
  assert.equal(G.discover(state, 'newspaper'), true);
  assert.equal(G.discover(state, 'newspaper'), false);
  assert.ok(G.available(2, state.found).includes('newspaper'));
  assert.ok(state.pieces.newspaper);
  assert.equal(G.discover(G.fresh(), 'newspaper'), false);
});

test('PDF transcription preserves all letters and all six clue word paths', () => {
  assert.equal(G.grid.length, 15);
  G.grid.forEach(row => assert.equal(row.length, 16));
  const paths = { FORGET: [1,9,1,4], FAMILY: [1,9,6,4], LOCK: [4,10,4,13], BACKPACK: [11,13,4,13], HELP: [7,10,7,13], BEST: [11,13,11,10] };
  for (const [word, [r,c,er,ec]] of Object.entries(paths)) {
    const dr = Math.sign(er-r), dc = Math.sign(ec-c);
    assert.equal([...word].map((_,i) => G.grid[r+i*dr][c+i*dc]).join(''), word);
  }
});

test('marking permits incorrect straight choices and can toggle reversed lines', () => {
  const state = G.fresh();
  assert.equal(G.markLine(state, [0,0,0,2]), false);
  G.unlock(state, '749');
  assert.equal(G.markLine(state, [0,0,0,2]), true);
  assert.equal(state.lines.length, 1);
  assert.equal(G.markLine(state, [0,2,0,0]), true);
  assert.equal(state.lines.length, 0);
  for (const line of [[0,0,0,0], [0,0,2,3], [-1,0,0,0], [0,16,1,16], [0,0,NaN,1]]) assert.equal(!!G.validLine(line), false);
});

test('the original Sudoku has one solution and its blue cell is four', () => {
  const board=[...G.givens], solutions=[];
  function solve() {
    const i=board.indexOf(0); if(i<0){solutions.push([...board]);return;}
    const r=Math.floor(i/4),c=i%4;
    for(let n=1;n<=4;n++){
      if(board.some((v,j)=>v===n&&(Math.floor(j/4)===r||j%4===c||(Math.floor(j/8)===Math.floor(r/2)&&Math.floor(j%4/2)===Math.floor(c/2)))))continue;
      board[i]=n;solve();board[i]=0;
    }
  }
  solve(); assert.equal(solutions.length,1); assert.equal(solutions[0][2],4);
});

test('calculator evaluates arithmetic without executing code or hiding input errors', () => {
  assert.equal(G.calculate('19+102+74+7+15+1+39+14+55'),326);
  assert.equal(G.calculate('2+3×4'),14); assert.equal(G.calculate('(2+3)×4'),20);
  assert.equal(G.calculate('−2 + .5'),-1.5);assert.equal(G.calculate('10÷4'),2.5);
  for(const bad of ['','2+','1/0','(2+3','2(3)','alert(1)','2;3','1e9','2**3']) assert.throws(()=>G.calculate(bad));
});

test('lock 5: the printed values give 408, and the satellite correction makes 414', () => {
  const num = s => s.split(' ')[0];
  assert.equal(G.calculate(`${num(G.values.GM)} ÷ (${num(G.values.v)} × ${num(G.values.v)}) − ${num(G.values.Re)}`), 408);
  assert.equal(408 + 6, Number(codes[4]));
});

test('lock 6: exactly four Canadian-born players, whose card numbers add to 102', () => {
  const canadians = G.hockey.filter(card => card.born.endsWith('Canada'));
  assert.deepEqual(canadians.map(card => card.number).sort((a, b) => a - b), [13, 18, 22, 49]);
  assert.equal(canadians.reduce((sum, card) => sum + card.number, 0), 102);
  assert.equal(new Set(G.hockey.map(card => card.number)).size, G.hockey.length);
});

test('lock 7: both Lego push puzzles are 3D; their rules are tested in lego.test.mjs', () => {
  assert.equal(G.pushPuzzles, undefined);
  assert.equal(G.push, undefined);
  assert.deepEqual(G.fresh().push, { square: { actions: [] }, flat: { actions: [] } });
});

test('lock 7: the six cube pieces close one way only, tiles out; clashes and inside-out pieces are reported', () => {
  const ids = Object.keys(G.cubePieces), cells = ids.map(id => G.cubePieces[id].join('').split('#').length - 1);
  assert.equal(cells.reduce((a, b) => a + b), 56, 'the shell of a 4 × 4 × 4 cube');
  // Every way to put the six pieces on the six faces: 24 (each turn of the whole cube) with tiles out, and the same 24
  // turned inside out. Turning a piece in place is a proper turn, so nothing else fits.
  let out = 0, inside = 0;
  const memo = new Map(), cellsAt = (...k) => memo.get(k.join()) || memo.set(k.join(), G.pieceCells(...k)).get(k.join());
  const used = new Set(), place = (face, left, flips) => {
    if (face === 6) { if (flips === 0) out++; else if (flips === 6) inside++; else assert.fail('mixed flips'); return; }
    for (const id of left) for (let t = 0; t < 4; t++) for (let f = 0; f < 2; f++) {
      const c = cellsAt(id, face, t, f); if (c.some(x => used.has(x))) continue;
      c.forEach(x => used.add(x)); place(face + 1, left.filter(x => x !== id), flips + f); c.forEach(x => used.delete(x));
    }
  };
  place(0, ids, 0);
  assert.equal(out, 24); assert.equal(inside, 24);
  const state = playTo(3);
  assert.equal(G.placeCube(state, 'red', 0, 0, 0), true); assert.equal(G.placeCube(state, 'red', 6, 0, 0), false); assert.equal(G.placeCube(state, 'nope', 0, 0, 0), false);
  assert.equal(G.placeCube(state, 'blue', 0, 1, 1), true); assert.deepEqual(Object.keys(state.cube), ['blue'], 'a piece already on that face goes back');
  assert.deepEqual(G.cubeStatus(state), { placed: 1, clashes: [], inside: ['blue'], solved: false });
  G.placeCube(state, 'red', 1, 0, 0); G.placeCube(state, 'green', 4, 0, 0);
  assert.ok(G.cubeStatus(state).clashes.length > 0, 'three pieces at random leave some corner claimed twice');
  assert.equal(G.placeCube(state, 'red', null), true); assert.equal(state.cube.red, undefined);
});
test('lock 7: each marker symbol on the cube is split over pieces, so it reads only once the cube is built', () => {
  const owner = new Map(); for (const [id, at] of Object.entries(G.cubeSolved)) for (const c of G.pieceCells(id, ...at)) owner.set(c, id);
  const normal = [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0]];
  const cellAt = (face, row, col) => {   // seen from outside, up is LDraw -y
    const n = normal[face], right = [n[2], 0, -n[0]].map(v => -v), p = [0, 1, 2].map(k => right[k] * 40 * (col - 1.5) + (k === 1 ? -40 * (1.5 - row) : 0) + n[k] * 60);
    return owner.get(p.map(x => Math.round(x / 40 + 1.5)).join(','));
  };
  for (const mark of G.cubeMarks) {
    const ink = {}; let total = 0;
    for (const line of mark.strokes) for (let k = 0; k < line.length - 1; k++) for (let t = 0; t < 1; t += 0.05) {
      const gx = line[k][0] + (line[k + 1][0] - line[k][0]) * t, gy = line[k][1] + (line[k + 1][1] - line[k][1]) * t;
      for (let dx = -0.06; dx <= 0.06; dx += 0.02) for (let dy = -0.06; dy <= 0.06; dy += 0.02) {
        const x = mark.corner + 1 - mark.width / 2 + (gx + dx) * mark.width, y = gy + dy;   // x in faces round the band
        if (dx * dx + dy * dy > G.cubePen ** 2 / 4 || y < 0 || y >= 1) continue;
        const face = (Math.floor(x) + 4) % 4, id = cellAt(face, Math.floor(y * 4), Math.floor((x - Math.floor(x)) * 4));
        ink[id] = (ink[id] || 0) + 1; total++;
      }
    }
    const shares = Object.values(ink).map(v => v / total).sort((a, b) => b - a);
    assert.ok(shares[0] < 0.56, `${mark.text}: no piece holds most of it (${shares.map(v => v.toFixed(2))})`);
    assert.ok(shares[1] > 0.3, `${mark.text}: a second piece holds a good part`);
  }
  assert.deepEqual(G.cubeMarks.map(m => m.text), ['5', '+', '3']); assert.deepEqual(G.cubeMarks.map(m => m.corner), [1, 2, 3], 'read in order turning the cube left');
});

test('lock 8: the neighbours riddle has one solution, and the doctor is DICK', () => {
  const perms = list => list.length < 2 ? [list] : list.flatMap((x, i) => perms([...list.slice(0, i), ...list.slice(i + 1)]).map(p => [x, ...p]));
  const opts = bag => G.parts[bag].options.map(([v]) => v), names = opts('names');
  const n = name => names.indexOf(name), w = (list, v) => list.indexOf(v), solutions = [];
  for (const job of perms(['doctor', 'engineer', 'ranger', 'astronaut', 'chef'])) for (const face of perms(opts('faces'))) {
    // The headband is printed on the big-smile head (DG-H27), so the headband clues are about that face.
    if (face[n('RICH')] !== 'mark' || face[n('BART')] !== 'scar' || face[w(job, 'engineer')] !== 'scar' || face[w(job, 'chef')] !== 'stars' || face[n('MADY')] !== 'stars' || face[n('JUNE')] !== 'plain') continue;
    for (const hair of perms(opts('hair'))) {
      if (['grey', 'black', 'blonde'].includes(hair[n('MADY')]) || ['grey', 'black', 'blonde'].includes(hair[n('BART')]) || hair[n('DICK')] !== 'grey' || hair[w(job, 'astronaut')] !== 'blonde' || hair[w(face, 'plain')] !== 'black') continue;
      for (const pet of perms(opts('pets'))) {
        if (pet[w(hair, 'orange')] !== 'rat' || pet[w(job, 'astronaut')] !== 'dog' || pet[w(job, 'doctor')] !== 'frog' || pet[w(job, 'ranger')] !== 'bird') continue;
        for (const hobby of perms(opts('hobbies'))) {
          if (hobby[w(job, 'ranger')] !== 'brush' || hair[w(hobby, 'camera')] !== 'blonde' || hobby[w(face, 'mark')] !== 'camera' || face[w(hobby, 'guitar')] !== 'beard' || hobby[w(hair, 'grey')] !== 'guitar' || hobby[w(job, 'engineer')] !== 'stick' || hobby[w(face, 'plain')] !== 'brush' || pet[w(hobby, 'stick')] !== 'cat') continue;
          solutions.push(names[job.indexOf('doctor')]);
        }
      }
    }
  }
  assert.deepEqual(solutions, ['DICK']);
  assert.equal(G.riddle.length, 24);
});

test('every prop fits on the table without overlapping, at every lock and after Tidy', () => {
  const check = (state, label) => {
    const table = G.tableSize(state.stage, state), ids = G.available(state.stage, state.found), boxes = ids.map(id => [id, G.box(id, state.pieces[id])]);
    for (const [id, b] of boxes) assert.ok(b.x >= 0 && b.y >= 0 && b.x + b.w <= table.w && b.y + b.h <= table.h, `${label}: ${id} is off the table`);
    boxes.forEach(([a, A], i) => boxes.slice(i + 1).forEach(([b, B]) => assert.ok(!G.overlaps(A, B, 0), `${label}: ${a} overlaps ${b}`)));
  };
  const state = G.fresh(); state.pieces.bottle = { x: 490, y: 120, rot: 0, face: 0, stowed: false };
  for (const [i, code] of codes.entries()) { if (state.stage === 2) G.discover(state, 'newspaper'); G.unlock(state, code); check(state, `lock ${i + 1}`); }
  G.layout(state); check(state, 'tidy');
  assert.equal(G.available(10, state.found).length, Object.keys(G.items).length);
});

test('save round trip keeps work, faces, rotation, put-away items and notebook', () => {
  const state = playTo(9);
  state.lines = [[1,9,1,4], [1,9,6,4]]; state.sudoku[2] = 4; state.notes = '<script>notes are just text</script>';
  state.hints = [2,1,0,0,0,0,0,0,4,0]; state.pieces.note = {x:302, y:90, rot:90, face:1, stowed:true};
  state.satellite = { built: 10, on: true, x: -12, y: 4, rot: 355 }; state.otter.reverse(); state.map.reverse(); state.mapLines = [[1, 2, 300, 400]];
  state.push.square = { actions: ['in:back:0:-3', 'shift:-1', 'deeper'] }; state.push.flat = { actions: ['in:right:0:-3', 'out', 'in:front:-11:-3'] }; G.placeCube(state, 'a', 0, 0, 0); state.figures[2] = { names: 'DICK', hair: 'grey', pets: 'frog' };
  const restored = G.restore(JSON.parse(JSON.stringify(state)));
  for (const key of ['lines', 'sudoku', 'hints', 'notes', 'satellite', 'otter', 'map', 'mapLines', 'push', 'cube', 'figures', 'found']) assert.deepEqual(restored[key], state[key], key);
  assert.deepEqual(restored.pieces.note, state.pieces.note);
});

test('bad saves cannot overwrite givens, leak future props or inject unbounded work', () => {
  assert.throws(() => G.restore({version:1,game:'norse'}));
  const raw = {...G.fresh(), stage:1, sudoku:Array(16).fill(9), hints:[-1,99], lines:[[1,9,1,4],[1,4,1,9],[100,1,0,1]], pieces:{unknown:{},note:{x:Infinity,y:-900,rot:123,face:44}}};
  const restored = G.restore(raw);
  assert.deepEqual(restored.sudoku, G.givens); assert.deepEqual(restored.hints, Array(10).fill(0)); assert.equal(restored.lines.length,1);
  assert.equal(restored.pieces.unknown,undefined); assert.equal(restored.pieces.note.x,302); assert.equal(restored.pieces.note.y,0); assert.equal(restored.pieces.note.rot,0); assert.equal(restored.pieces.note.face,0);
  raw.stage=0; assert.deepEqual(G.restore(raw).lines,[]); assert.equal(G.restore(raw).pieces.note,undefined);
  const late = { ...G.fresh(), stage: 4, otter: [0, 0, 1], map: 'x', mapLines: [[0, 0, 5000, 1]], satellite: { built: 99, x: 1e9, y: 'a', rot: 7 }, push: { square: { actions: ['in:back:0:-3'] } }, cube: { red: [9, 0, 0], blue: [2, 3, 1], green: [2, 0, 0], a: [0, 0, 0] }, figures: [{ names: 'DICK', hobbies: 'guitar', pets: 'frog' }], found: ['newspaper', 'note'] };
  const r = G.restore(late);
  assert.deepEqual(r.otter, G.boards.otter.start); assert.deepEqual(r.mapLines, []); assert.deepEqual(r.satellite, { built: 0, on: false, x: 600, y: 60, rot: 35 });
  assert.deepEqual(r.push.square, { actions: [] }, 'the square puzzle arrives at lock 6'); assert.deepEqual(r.cube, { blue: [2, 3, 1] }, 'bad, doubled and old four-piece cube saves are dropped');
  assert.deepEqual(r.figures[0], { hobbies: 'guitar', pets: 'frog' }, 'name tiles arrive at lock 7'); assert.deepEqual(r.found, ['newspaper']);
  const lego = (which, actions, stage = 6) => G.restore({ ...G.fresh(), stage, push: { [which]: { actions } } }).push[which];
  assert.deepEqual(lego('flat', ['in:right:0:-3', '<img onerror=x>', 7, 'in:up:1:1', 'out', 'shift:+2', 'hand:0:1,0', 'deeper']), { actions: ['in:right:0:-3', 'out', 'hand:0:1,0', 'deeper'] });
  assert.equal(lego('square', Array(500).fill('out')).actions.length, 200);
  assert.deepEqual(G.restore({ ...G.fresh(), stage: 6, push: { flat: { pushes: ['right:0:-3'] }, square: { moves: 3, side: 1 } } }).push, { square: { actions: [] }, flat: { actions: [] } }, 'saves from earlier versions start both afresh');
  assert.deepEqual(lego('flat', ['out'], 1), { actions: [] }, 'the flat puzzle arrives at lock 2');
  assert.deepEqual(lego('square', ['out'], 5), { actions: [] }, 'the square puzzle arrives at lock 6');
});

test('a save from the four-lock opening continues with work preserved', () => {
  const old = {game:'hiking-opening',version:1,stage:4,pieces:{bottle:{x:60,y:120,face:2,rot:0,stowed:false},newspaper:{x:1140,y:70,rot:0,face:0,stowed:false}},hints:[1,2,0,3],lines:[[1,9,1,4]],sudoku:[3,1,4,2,4,2,3,1,1,3,2,4,2,4,1,3],notes:'Keep this note.',calculator:{expression:'19+102',result:'121'}};
  const state = G.restore(old);
  assert.equal(state.stage, 4); assert.equal(G.locks[state.stage].name, 'Inside pocket');
  assert.deepEqual(state.hints, [1,2,0,3,0,0,0,0,0,0]); assert.deepEqual(state.found, ['newspaper'], 'the clipping was already on the table');
  assert.ok(G.available(state.stage, state.found).includes('satellite'));
  assert.equal(state.pieces.satellite, undefined, 'new props are placed when the table is drawn');
  G.place(state, 'satellite'); assert.ok(state.pieces.satellite);
});

test('answer input adapts to letters, three digits and four digits', () => {
  assert.equal(G.normalizeAnswer(2,'m0oo-n'), 'MOON');
  assert.equal(G.normalizeAnswer(3,'326'), '326');
  assert.equal(G.normalizeAnswer(7,'di ck!'), 'DICK');
  assert.equal(G.normalizeAnswer(9,'4-1-3-0-9'), '4130');
  const state=G.fresh();state.stage=2;assert.equal(G.unlock(state,'MOONLIGHT'),false);assert.equal(G.unlock(state,'MOON'),true);
});

test('Tidy table keeps put-away items put away', () => {
  const state = playTo(3); state.pieces.note.stowed = true; state.pieces.note.face = 1;
  G.layout(state);
  assert.equal(state.pieces.note.stowed, true); assert.equal(state.pieces.note.face, 1);
  assert.equal(state.pieces.sheet.stowed, false);
});

test('Star ratings are saved and restored, and bad values are dropped', () => {
  const state = G.fresh(); state.ratings[0] = 4;
  const back = G.restore(JSON.parse(JSON.stringify(state)));
  assert.deepEqual(back.ratings, [4, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
  assert.deepEqual(G.restore({ ...JSON.parse(JSON.stringify(state)), ratings: [9, 'x', 3] }).ratings, [0, 0, 3, 0, 0, 0, 0, 0, 0, 0]);
  assert.deepEqual(G.restore({ ...JSON.parse(JSON.stringify(G.fresh())), ratings: undefined }).ratings, Array(10).fill(0));
});

test('Tidy packs the props onto a table smaller than the full one, and unlocking gives the full table back', () => {
  const state = playTo(8, { card: true }); G.layout(state);
  const full = G.tableSize(state.stage), tight = G.tableSize(state.stage, state);
  assert.ok(tight.w * tight.h < full.w * full.h * 0.7, `tight ${tight.w}x${tight.h} vs full ${full.w}x${full.h}`);
  const ids = G.available(state.stage, state.found).filter(id => !state.pieces[id].stowed);
  const boxes = ids.map(id => G.box(id, state.pieces[id]));
  for (const b of boxes) assert.ok(b.x >= 24 - 1 && b.y >= 24 - 1 && b.x + b.w <= tight.w - 24 + 1 && b.y + b.h <= tight.h - 24 + 1, 'padding');
  assert.ok(Math.max(...boxes.map(b => b.x + b.w)) >= tight.w - 24 - 1, 'no spare width');
  const next = G.unlock(state, codes[8]); assert.equal(next, true); assert.equal(state.table, null);
  assert.deepEqual(G.restore(JSON.parse(JSON.stringify(Object.assign(G.fresh(), { table: { w: 700, h: 400 } })))).table, { w: 700, h: 400 });
  assert.equal(G.restore({ ...JSON.parse(JSON.stringify(G.fresh())), table: { w: 9, h: 'x' } }).table, null);
});

test('The four-letter padlock wheels hold ten letters each, and both letter codes can be set', () => {
  assert.deepEqual(G.wheelLetters.map(w => w.length), [10, 10, 10, 10]);
  for (const lock of G.locks.filter(l => l.letters)) [...lock.answer].forEach((ch, i) => assert.ok(G.wheelLetters[i].includes(ch), `${lock.answer}: ${ch} on wheel ${i + 1}`));
});
