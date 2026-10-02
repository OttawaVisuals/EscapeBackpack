/* Player assets reuse the physical edition. Sequence: PC-18, 29 September 2026.
   This friends-only prototype checks answers locally; source is not spoiler-proof. */
(function (root) {
  /* Every prop is drawn at its real printed size. Sizes and start positions come from
     table-layout.js (inches), which plans the whole game's table; here they become
     table units. Postcards and maps take their slots in the order they arrive. */
  const L = root.TableLayout || require('./table-layout.js');
  const PPI = L.PPI;
  const table = { w: L.table.w * PPI, h: L.table.h * PPI };
  const units = ({ w, h, x, y }) => ({ w: Math.round(w * PPI), h: Math.round(h * PPI), at: [Math.round(x * PPI), Math.round(y * PPI)] });
  const cardSlot = n => units(L.cardSlot(n)), mapSlot = n => units(L.mapSlot(n)), slot = key => units(L.props[key]);
  const postcard = (slug) => ['Front', 'Back'].map(side => `../Web/Postcards/Postcard_${slug}_${side}.webp`);
  const items = {
    L1: { name: "L’Anse aux Meadows", kind: 'Postcard', faces: postcard('L1_LAnse'), ...cardSlot(1) },
    tagA: { name: 'Luggage tag · Vinland', kind: 'Luggage tag', crop: [460, 260, 610, 356], ...slot('tagA') },
    tagB: { name: 'Luggage tag · Rouen', kind: 'Luggage tag', crop: [460, 735, 610, 356], ...slot('tagB') },
    ticket: { name: 'Brattahlíð museum ticket', kind: 'Ticket', faces: ['../Props/_Renders/Museum_Ticket_Front.png', '../Props/_Renders/Museum_Ticket_Back.png'], ...slot('museumTicket') },
    L2: { name: 'Battle Harbour', kind: 'Postcard', faces: postcard('L2_Battle_Harbour'), ...cardSlot(2) },
    L3: { name: 'Baffin Island', kind: 'Postcard', faces: postcard('L3_Baffin_Island'), ...cardSlot(3) },
    LD: { name: 'Brattahlíð', kind: 'Postcard', faces: postcard('LD_Brattahlid'), ...cardSlot(4) },
    map: { name: 'Leif’s sea chart', kind: 'Map', faces: ['../Props/_Renders/Trail_Map_1_Leif_Print.png'], ...mapSlot(1) },
    R2: { name: 'Rouen', kind: 'Postcard', faces: postcard('R2_Rouen'), ...cardSlot(5) },
    rolloMap: { name: 'Rollo’s trail map', kind: 'Map', faces: ['../Props/_Renders/Trail_Map_2_Rollo_Print.png'], ...mapSlot(2) },
    R1: { name: 'Châlus', kind: 'Postcard', faces: postcard('R1_Chalus'), ...cardSlot(6) },
    R6: { name: 'Roumare Forest', kind: 'Postcard', faces: postcard('R6_Roumare_Forest'), ...cardSlot(7) },
    RD: { name: 'Walcheren', kind: 'Postcard', faces: postcard('RD_Walcheren'), ...cardSlot(8) },
    R3: { name: 'Bayeux', kind: 'Postcard', faces: postcard('R3_Bayeux'), ...cardSlot(9) },
    R4: { name: 'Winchester', kind: 'Postcard', faces: postcard('R4_Winchester'), ...cardSlot(10) },
    R5: { name: 'Battle', kind: 'Postcard', faces: postcard('R5_Battle'), ...cardSlot(11) },
    // Triangular 30 cm architect's scale ruler: three faces, Flip turns to the next one.
    ruler: { name: 'Architect’s scale ruler', kind: 'Ruler', faces: [1, 2, 3].map(n => `./assets/Ruler_Face_${n}.svg`), ...slot('ruler') },
    rouenTicket: { name: 'Rouen museum ticket', kind: 'Ticket', faces: ['../Props/RouenTicket/Rouen_Ticket_Front_300dpi.png', '../Props/RouenTicket/Rouen_Ticket_Back_300dpi.png'], ...slot('rouenTicket') }
  };
  const locks = [
    { leg: 1, name: 'Main compartment', answer: '1021', releases: ['L2', 'L3'], message: 'Inside are two more postcards from Liv.', hints: [
      'Look at both luggage tags and both sides of the first postcard.',
      'Each tag has a street number. The postcard is from the first stop of Liv’s journey. Which tag matches that place?',
      'Use the Vinland tag’s street number first, followed by the Rouen tag’s street number.',
      'The combination is 1021.'
    ] },
    { leg: 1, name: 'Lower front pocket', answer: '1576', releases: ['LD', 'map'], message: 'A postcard from Greenland and Leif’s sea chart were tucked inside.', hints: [
      'Read the two new postcards. What do they both say about the sky?',
      'Try bringing the two illustrated skies together on the table. You can rotate and move the cards.',
      'Put Battle Harbour above Baffin Island, both picture-side up. Rotate Battle Harbour twice so it is upside down, then move it until its top edge meets Baffin Island’s top edge. Use the magnifier on the join.',
      'The joined cloud fragments read 1576.'
    ] },
    { leg: 1, name: 'Rollo’s pouch', answer: '3212', releases: ['R2', 'rolloMap', 'rouenTicket'], message: 'Leif’s leg is complete. Liv’s journey continues with Rollo.', hints: [
      'Inspect every detail on the Brattahlíð postcard, including the small print. Keep the sea chart and museum ticket nearby.',
      '“Series F, No. 1” points to a square on the chart. What animal is there?',
      'The animal is a bear. Spell its name using the visitor index on the back of the museum ticket, taking one digit per letter.',
      'B → 3, E → 2, A → 1, R → 2. The combination is 3212.'
    ] },
    { leg: 2, name: 'Lower left pocket', answer: '1486', releases: ['R1', 'R6', 'RD'], message: 'Three more postcards from Rollo’s trail.', hints: [
      'Read the Rouen postcard next to the back of the Rouen museum ticket. Some of Liv’s words have a partner on the ticket.',
      'The ticket pairs everyday Saxon words (numbered) with their Norman partners (lettered). A matched pair gives a letter and a number: a square on Rollo’s map.',
      'Liv mentions fighting, people, poultry and an inn, in that order. For each, match the pair, find its square on the map, and count the squares to the drawing for that word.',
      'Fight 1, people 4, poultry 8, inn 6. The combination is 1486.'
    ] },
    { leg: 2, name: 'Lower right pocket', answer: '562', releases: ['R3', 'R4', 'R5', 'ruler'], message: 'Three more postcards, and Liv’s architect’s ruler.', hints: [
      'Look closely at the pictures on the three new postcards. Each message mentions something small in passing.',
      'Count the Viking boats at Walcheren, the wild boars in Roumare Forest and the crossbow bolts at Châlus. Use the magnifier: some hide well. Read Roumare’s message again before you settle on its number.',
      'The Fun Facts on the backs date each place. Put the counts in date order: Walcheren, then Roumare, then Châlus. Liv thinks there were twice as many boars as she saw.',
      '5 boats, 3 boars doubled to 6, 2 bolts. The combination is 562.'
    ] }
  ];
  const legs = { 1: 'Leif’s trail', 2: 'Rollo’s trail' };
  const initial = ['L1', 'tagA', 'tagB', 'ticket'];
  const available = stage => [...initial, ...locks.slice(0, stage).flatMap(lock => lock.releases)];
  const fresh = () => ({ version: 1, stage: 0, table: 0, pieces: {}, hints: locks.map(() => 0), notes: '' });
  const clamp = (v, min, max, fallback) => Number.isFinite(v) ? Math.min(max, Math.max(min, v)) : fallback;
  function restore(raw) {
    const state = fresh();
    if (!raw || raw.version !== 1) return state;
    state.stage = Number.isInteger(raw.stage) ? clamp(raw.stage, 0, locks.length, 0) : 0;
    state.notes = typeof raw.notes === 'string' ? raw.notes.slice(0, 6000) : '';
    state.hints = state.hints.map((_, i) => Math.floor(clamp(raw.hints?.[i], 0, 4, 0)));
    for (const id of available(state.stage)) {
      const p = raw.pieces?.[id];
      if (!p || typeof p !== 'object') continue;
      state.pieces[id] = { x: clamp(p.x, 10, table.w - items[id].w - 10, items[id].at[0]), y: clamp(p.y, 10, table.h - items[id].h - 10, items[id].at[1]), rot: [0, 90, 180, 270].includes(p.rot) ? p.rot : 0, face: faceOf(id, p), stowed: !!p.stowed };
    }
    state.table = Math.max(Number.isInteger(raw.table) ? clamp(raw.table, 0, sizes.length - 1, 0) : 0, sizeFor(state));
    return state;
  }

  /* The table starts small and grows as props arrive; it never shrinks during play.
     A new prop goes in the first free spot, scanning rows from the top left; if none is
     free, the table grows a size. Only arrival order decides where things land. */
  const sizes = L.sizes.map(([w, h]) => ({ w: Math.round(w * PPI), h: Math.round(h * PPI) }));
  const EDGE = Math.round(0.4 * PPI), GAP = Math.round(0.5 * PPI), STEP = Math.round(0.25 * PPI);
  function footprint(id, p) {
    const it = items[id], sideways = p.rot % 180 !== 0, w = sideways ? it.h : it.w, h = sideways ? it.w : it.h;
    return { x: p.x + (it.w - w) / 2, y: p.y + (it.h - h) / 2, w, h };
  }
  function sizeFor(state) {
    const boxes = Object.entries(state.pieces).map(([id, p]) => footprint(id, p));
    const i = sizes.findIndex(s => boxes.every(b => b.x + b.w <= s.w && b.y + b.h <= s.h));
    return i < 0 ? sizes.length - 1 : i;
  }
  function findSpot(pieces, id, size) {
    const it = items[id], taken = Object.entries(pieces).filter(([k, p]) => k !== id && !p.stowed).map(([k, p]) => footprint(k, p));
    for (let y = EDGE; y + it.h + EDGE <= size.h; y += STEP)
      for (let x = EDGE; x + it.w + EDGE <= size.w; x += STEP)
        if (taken.every(b => x + it.w + GAP <= b.x || b.x + b.w + GAP <= x || y + it.h + GAP <= b.y || b.y + b.h + GAP <= y)) return [x, y];
    return null;
  }
  /* Snap: when a prop's edge comes within `reach` table units of another prop's edge,
     pull it flush (cards meeting edge to edge, or pulled out of a slight overlap).
     Then, beside the prop it now touches, line up the side edges if they are close. */
  function snap(state, id, reach) {
    const p = state.pieces[id], others = Object.entries(state.pieces).filter(([k, q]) => k !== id && !q.stowed).map(([k, q]) => footprint(k, q));
    let a = footprint(id, p), dx = 0, dy = 0, bestX = reach, bestY = reach;
    const consider = (d, axis) => {
      if (axis === 'x' && Math.abs(d) < bestX) { bestX = Math.abs(d); dx = d; }
      if (axis === 'y' && Math.abs(d) < bestY) { bestY = Math.abs(d); dy = d; }
    };
    for (const b of others) {
      if (a.x < b.x + b.w && b.x < a.x + a.w) { consider(b.y + b.h - a.y, 'y'); consider(b.y - (a.y + a.h), 'y'); }
      if (a.y < b.y + b.h && b.y < a.y + a.h) { consider(b.x + b.w - a.x, 'x'); consider(b.x - (a.x + a.w), 'x'); }
    }
    a = { ...a, x: a.x + dx, y: a.y + dy };
    const meets = (u, v) => Math.abs(u - v) < 0.5;
    for (const b of others) {
      if (dy && !dx && (meets(a.y, b.y + b.h) || meets(a.y + a.h, b.y))) { consider(b.x - a.x, 'x'); consider(b.x + b.w - (a.x + a.w), 'x'); }
      if (dx && !dy && (meets(a.x, b.x + b.w) || meets(a.x + a.w, b.x))) { consider(b.y - a.y, 'y'); consider(b.y + b.h - (a.y + a.h), 'y'); }
    }
    p.x += dx; p.y += dy;
    return dx !== 0 || dy !== 0;
  }
  const lying = ([x, y]) => ({ x, y, rot: 0, face: 0, stowed: false });
  // Which face is up. Saves before 1 Oct 2026 stored back: true/false instead.
  function faceOf(id, p) {
    const n = items[id].faces?.length || 1;
    return Number.isInteger(p.face) ? clamp(p.face, 0, n - 1, 0) : (p.back && n > 1 ? 1 : 0);
  }
  // Deal every collected prop that is not on the table yet, growing the table if needed.
  function deal(state) {
    for (const id of available(state.stage)) {
      if (state.pieces[id]) continue;
      let spot = null;
      while (!(spot = findSpot(state.pieces, id, sizes[state.table])) && state.table < sizes.length - 1) state.table++;
      state.pieces[id] = lying(spot || items[id].at);
    }
  }
  // Tidy: every prop face up, packed in arrival order on the smallest table that holds them all.
  function arrange(state) {
    for (let i = 0; i < sizes.length; i++) {
      const pieces = {};
      for (const id of available(state.stage)) {
        const spot = findSpot(pieces, id, sizes[i]);
        if (!spot) break;
        pieces[id] = lying(spot);
      }
      if (Object.keys(pieces).length === available(state.stage).length) { state.table = i; state.pieces = pieces; return; }
    }
    state.table = sizes.length - 1;
    state.pieces = Object.fromEntries(available(state.stage).map(id => [id, lying(items[id].at)]));
  }
  function attempt(state, answer) {
    if (state.stage >= locks.length || String(answer).trim() !== locks[state.stage].answer) return false;
    state.stage++;
    return true;
  }
  const api = { PPI, table, sizes, items, locks, legs, initial, available, fresh, restore, attempt, clamp, deal, arrange, footprint, snap };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LeifGame = api;
})(typeof window === 'undefined' ? globalThis : window);
