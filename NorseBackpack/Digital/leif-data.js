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
    map: { name: 'Leif’s sea chart', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_1_Leif_Print.png'], ...mapSlot(1) },
    R2: { name: 'Rouen', kind: 'Postcard', faces: postcard('R2_Rouen'), ...cardSlot(5) },
    rolloMap: { name: 'Rollo’s trail map', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_2_Rollo_Print.png'], ...mapSlot(2) },
    R1: { name: 'Châlus', kind: 'Postcard', faces: postcard('R1_Chalus'), ...cardSlot(6) },
    R6: { name: 'Roumare Forest', kind: 'Postcard', faces: postcard('R6_Roumare_Forest'), ...cardSlot(7) },
    RD: { name: 'Walcheren', kind: 'Postcard', faces: postcard('RD_Walcheren'), ...cardSlot(8) },
    R3: { name: 'Bayeux', kind: 'Postcard', faces: postcard('R3_Bayeux'), ...cardSlot(9) },
    R4: { name: 'Winchester', kind: 'Postcard', faces: postcard('R4_Winchester'), ...cardSlot(10) },
    R5: { name: 'Battle', kind: 'Postcard', faces: postcard('R5_Battle'), ...cardSlot(11) },
    // Triangular 30 cm architect's scale ruler: three faces, Flip turns to the next one.
    ruler: { name: 'Architect’s scale ruler', kind: 'Ruler', faces: [1, 2, 3].map(n => `./assets/Ruler_Face_${n}.svg`), freeRotate: true, pivot: [6 / 300, 0.5], handle: [0.985, 0.5], ...slot('ruler') },
    A1: { name: 'Dögurðarnes', kind: 'Postcard', faces: postcard('A1_Dogurdarnes'), ...cardSlot(12) },
    A2: { name: 'Hvammur', kind: 'Postcard', faces: postcard('A2_Hvammur'), ...cardSlot(13) },
    A3: { name: 'Esjuberg', kind: 'Postcard', faces: postcard('A3_Esjuberg'), ...cardSlot(14) },
    AD: { name: 'Bjarnarhöfn', kind: 'Postcard', faces: postcard('AD_Bjarnarhofn'), ...cardSlot(15) },
    audMap: { name: 'Aud’s trail map', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_3_Aud_Print.png'], ...mapSlot(3) },
    audTicket: { name: 'Aud’s Treasure Museum ticket', kind: 'Ticket', faces: ['../Props/_Renders/Aud_Ticket_Front.png', '../Props/_Renders/Aud_Ticket_Back.png'], ...slot('audTicket') },
    // The four-wheel treasure tally (PR-24): digits drawn like the printed seven-segment ring.
    tally: { name: 'Tally', kind: 'Tally', widget: 'tally', noSnap: true, ...slot('tally') },
    // Aud's comb (PR-19): seats on AD's message side over the two printed ring-and-dots.
    comb: { name: 'Aud’s comb', kind: 'Comb', faces: ['./assets/Comb_Front.svg', './assets/Comb_Back.svg'], noSnap: true, ...slot('comb') },
    H4: { name: 'Hedeby', kind: 'Postcard', faces: postcard('H4_Hedeby'), ...cardSlot(16) },
    H5: { name: 'Sicily', kind: 'Postcard', faces: postcard('H5_Sicily'), ...cardSlot(17) },
    haraldMap: { name: 'Harald’s trail map', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_4_Harald_Front.png', '../Props/_Renders/Trail_Map_4_Harald_Back.png'], ...mapSlot(4) },
    ravenCard: { name: 'Raven’s flights card', kind: 'Card', faces: ['../Props/RavenFlights/Raven_Flights_Card_preview.png'], ...slot('ravenFlights') },
    H1: { name: 'Oslo', kind: 'Postcard', faces: postcard('H1_Oslo'), ...cardSlot(18) },
    H2: { name: 'Staraya Ladoga', kind: 'Postcard', faces: postcard('H2_Staraya_Ladoga'), ...cardSlot(19) },
    H3: { name: 'Kyiv', kind: 'Postcard', faces: postcard('H3_Kyiv'), ...cardSlot(20) },
    HD: { name: 'Constantinople', kind: 'Postcard', faces: postcard('HD_Constantinople'), ...cardSlot(21) },
    H6: { name: 'Patara', kind: 'Postcard', faces: postcard('H6_Patara'), ...cardSlot(22) },
    // Its back holds columns I–K in mirror image; online it can also be held up to the light (PZ-01).
    osloTicket: { name: 'Hnefatafl Museum ticket', kind: 'Ticket', faces: ['../Props/_Renders/Hnefatafl_Ticket_Front.png', '../Props/_Renders/Hnefatafl_Ticket_Back.png', './assets/Hnefatafl_Ticket_Light.webp'], faceNames: ['front', 'back', 'held to the light'], ...slot('hnefataflTicket') },
    // The 11 × 11 board (PR-08) with its 16 dark pieces, 6 light pieces and the king in a tray below.
    board: { name: 'Hnefatafl board', kind: 'Board', widget: 'tafl', ...slot('board') },
    transition1: { name: 'Booking confirmation', kind: 'Ticket', faces: ['../Props/_Renders/Transition_Tickets_Ticket1.png'], ...slot('transition1') },
    transition2: { name: 'Booking confirmation', kind: 'Ticket', faces: ['../Props/_Renders/Transition_Tickets_Ticket2.png'], ...slot('transition2') },
    transition3: { name: 'Booking confirmation', kind: 'Ticket', faces: ['../Props/_Renders/Transition_Tickets_Ticket3.png'], ...slot('transition3') },
    journal: { name: 'Journal page', kind: 'Journal page', faces: ['../Props/_Renders/Journal_Family_Iconography_Page.png'], ...slot('journalIconography') },
    // The end-of-game keepsake: 50 mm, raven crest on the front, "Adventure complete" on the back.
    medallion: { name: 'Medallion', kind: 'Medallion', faces: ['./assets/Medallion_Front.webp', './assets/Medallion_Back.webp'], round: true, noSnap: true, ...slot('medallion') },
    rouenTicket: { name: 'Rouen museum ticket', kind: 'Ticket', faces: ['../Props/RouenTicket/Rouen_Ticket_Front_300dpi.png', '../Props/RouenTicket/Rouen_Ticket_Back_300dpi.png'], ...slot('rouenTicket') }
  };
  // The hoard (PZ-03): 12 loose coins, mixed so the three piles are not handed over sorted.
  const COINS = ['01_dirham_common', '03_denier_common', '05_hedeby_ship', '01_dirham_common', '07_raven', '03_denier_common',
    '02_dirham_rare', '06_york_cross', '01_dirham_common', '04_denier_rare', '03_denier_common', '01_dirham_common'];
  const coinIds = COINS.map((_, i) => 'coin' + (i + 1));
  COINS.forEach((art, i) => { items[coinIds[i]] = { name: 'Coin', kind: 'Coin', faces: [`./assets/Coin_${art}.svg`], round: true, noSnap: true, ...slot(coinIds[i]) }; });
  const locks = [
    { leg: 1, nudge: 'Liv sent her bag with a postcard, two luggage tags and a museum ticket. Start with her postcard.', name: 'Main compartment', answer: '1021', releases: ['L2', 'L3'], message: 'Inside are two more postcards from Liv.', hints: [
      'Look at both luggage tags and both sides of the first postcard.',
      'Each tag has a street number. The postcard is from the first stop of Liv’s journey. Which tag matches that place?',
      'Use the Vinland tag’s street number first, followed by the Rouen tag’s street number.',
      'The combination is 1021.'
    ] },
    { leg: 1, nudge: 'Two more postcards from Liv. Read them side by side.', name: 'Lower front pocket', answer: '1576', releases: ['LD', 'map'], message: 'A postcard from Greenland and Leif’s sea chart were tucked inside.', hints: [
      'Read the two new postcards. What do they both say about the sky?',
      'Try bringing the two illustrated skies together on the table. You can rotate and move the cards.',
      'Put Battle Harbour above Baffin Island, both picture-side up. Rotate Battle Harbour twice so it is upside down, then move it until its top edge meets Baffin Island’s top edge. Use the magnifier on the join.',
      'The joined cloud fragments read 1576.'
    ] },
    { leg: 1, nudge: 'A postcard from Greenland and Leif’s sea chart. Every little detail counts.', name: 'Rollo’s pouch', answer: '3212', releases: ['R2', 'rolloMap', 'rouenTicket'], message: 'Leif’s leg is complete. Liv’s journey continues with Rollo.', hints: [
      'Inspect every detail on the Brattahlíð postcard, including the small print. Keep the sea chart and museum ticket nearby.',
      '“Series F, No. 1” points to a square on the chart. What animal is there?',
      'The animal is a bear. Spell its name using the visitor index on the back of the museum ticket, taking one digit per letter.',
      'B → 3, E → 2, A → 1, R → 2. The combination is 3212.'
    ] },
    { leg: 2, nudge: 'Rollo’s map, a postcard from Rouen and a museum ticket. See what they have in common.', name: 'Lower left pocket', answer: '1486', releases: ['R1', 'R6', 'RD'], message: 'Three more postcards from Rollo’s trail.', hints: [
      'Read the Rouen postcard next to the back of the Rouen museum ticket. Some of Liv’s words have a partner on the ticket.',
      'The ticket pairs everyday Saxon words (numbered) with their Norman partners (lettered). A matched pair gives a letter and a number: a square on Rollo’s map.',
      'Liv mentions fighting, people, poultry and an inn, in that order. For each, match the pair, find its square on the map, and count the squares to the drawing for that word.',
      'Fight 1, people 4, poultry 8, inn 6. The combination is 1486.'
    ] },
    { leg: 2, nudge: 'Three more places on Rollo’s trail. Look closely at their pictures.', name: 'Lower right pocket', answer: '562', releases: ['R3', 'R4', 'R5', 'ruler'], message: 'Three more postcards, and Liv’s architect’s ruler.', hints: [
      'Look closely at the pictures on the three new postcards. Each message mentions something small in passing.',
      'Count the Viking boats at Walcheren, the wild boars in Roumare Forest and the crossbow bolts at Châlus. Use the magnifier: some hide well. Read Roumare’s message again before you settle on its number.',
      'The Fun Facts on the backs date each place. Put the counts in date order: Walcheren, then Roumare, then Châlus. Liv thinks there were twice as many boars as she saw.',
      '5 boats, 3 boars doubled to 6, 2 bolts. The combination is 562.'
    ] },
    // Lock 6's code waits for a measurement on a 100% print (PZ-14, DG-06): the lock is shown but cannot open yet.
    { leg: 2, nudge: 'Three more postcards and Liv’s ruler. Her drawings only make sense at the right scale.', name: 'Large pouch', answer: null, pending: true, releases: ['A2', 'audMap', 'audTicket'], message: 'A postcard from Iceland, Aud’s trail map and a museum ticket.', hints: [
      'The Bayeux, Winchester and Battle postcards each end with a little picture puzzle. Read them as rebuses.',
      'Two of the rebuses point to places on Rollo’s map; the third tells you which scale of the ruler to use.',
      'Measure between those two places on Rollo’s map with the architect’s ruler, on its 1:125 scale.',
      'The combination for this lock is still being set.'
    ] },
    { leg: 3, nudge: 'Aud’s map and a ticket from her treasure museum. Liv went on a treasure hunt.', name: 'Lower front pocket, again', answer: '521', releases: ['A1', 'A3', ...coinIds, 'tally'], message: 'Two more postcards, a pouch of coins and a little tally.', hints: [
      'Aud’s map and her museum ticket go together: the ticket gives directions, and the Hvammur card says what to count on the way.',
      'Start at the northernmost chapel on Aud’s map and follow the ticket’s six steps along the roads.',
      'As you go, count the bridges, the fords and the gates you cross. Keep three separate tallies, in that order.',
      '5 bridges, 2 fords, 1 gate. The combination is 521.'
    ] },
    { leg: 3, nudge: 'A pouch of coins and a little tally. Not every coin was Aud’s.', name: 'Inside top pocket', answer: 'SOLE', releases: ['AD', 'comb'], message: 'A postcard from Bjarnarhöfn and Aud’s carved comb.', hints: [
      'Not every coin belongs to the same hoard. The front of Aud’s ticket sorts them into three groups and gives their values.',
      'Aud’s map marks where her treasure was hidden with a rune. Find that rune on the ticket: it picks one group of coins.',
      'Add up the values of the coins in that group, set the total on the tally’s wheels, then turn the tally upside down.',
      '5 + 100 + 3,600 = 3705, which reads SOLE upside down.'
    ] },
    { leg: 3, nudge: 'A postcard from Bjarnarhöfn and a carved comb. Aud’s things are rarely just what they seem.', name: 'Large pouch, once more', answer: 'BOOK', releases: ['H4', 'H5', 'haraldMap', 'ravenCard'], message: 'Two postcards from Harald’s trail, his map and a card of raven flights.', hints: [
      'Aud’s comb is more than a comb. Try it on one of the postcards.',
      'Its two holes fit over the two little ring-and-dot marks on the Bjarnarhöfn card’s message side. Line them up and the comb settles in.',
      'With the comb in place, most lines are hidden, but four of its teeth are broken short. Read the first letter that shows after each short tooth, from the top down.',
      'The short teeth uncover “brother’s”, “ould”, “ongside” and “Keep”: B, O, O, K. The combination is BOOK.'
    ] },
    { leg: 4, nudge: 'Harald’s map and a card of raven flights. Look for marks that don’t belong on a map.', name: 'Lower left pocket, again', answer: '2648', releases: ['H2', 'H3', 'HD'], message: 'Three more postcards from Harald’s trail.', hints: [
      'Harald’s map has a few odd little marks among the places. The Hedeby postcard explains what they are.',
      'They are branch runes: the Hedeby card shows how the branches on each side pick a rune. The word the Sicily card writes in capitals tells you which columns of the map to read, and in what order.',
      'Reading the runes in columns R, A, V, E and N gives H, R, A, F, N. Follow H → R → A → F → N on the raven’s flights card and note the number on each flight.',
      '2, 6, 4 and 8. The combination is 2648.'
    ] },
    { leg: 4, nudge: 'Three more postcards. What was in Harald’s horn?', name: 'Board bag', answer: 'MEAD', releases: ['H1', 'board', 'osloTicket'], message: 'The Oslo postcard, a Hnefatafl board with its pieces, and a museum ticket.', hints: [
      'Each of the three new postcards hides one word. Together they say what was in Harald’s horn.',
      'On the Staraya Ladoga card, only a few letters sit right on the left margin: read them downwards. The Kyiv card is a riddle, and the Constantinople card ends with a picture puzzle.',
      'Staraya Ladoga spells DRINK, Kyiv’s riddle answers HONEY, and Constantinople’s pictures (sugar and yeast becoming a fizzing flask) mean FERMENTED. A fermented honey drink is…',
      'MEAD. The combination is MEAD.'
    ] },
    { leg: 4, nudge: 'A Hnefatafl board and its pieces. Liv kept a note of how to set them out.', name: 'Large pouch, last time', answer: '253', releases: ['H6', 'transition1', 'transition2', 'transition3', 'journal'], message: 'The last postcard, three booking confirmations and a page from Liv’s journal.', hints: [
      'The back of Harald’s map is Liv’s note of a Hnefatafl starting position. Set the pieces out on the board to match it.',
      'A wet ticket ruined columns I to K of her note. The museum ticket carries them: turn it over until you can see it held up to the light, the right way round.',
      'The Oslo postcard says the king escapes in exactly three moves. The king starts on the centre square and slides like a rook, never jumping, until it reaches a corner. Count the squares of each move.',
      'F6 → H6 → H11 → K11: moves of 2, 5 and 3 squares. The combination is 253.'
    ] },
    // The final riddle (PZ-18, PZ-06): filter the decoys, order each trail, draw it on its map.
    { leg: 5, nudge: 'All 22 postcards, four maps, three bookings and Liv’s journal page. Her whole year is on the table.', name: 'Inside middle pocket', answer: '1972', releases: ['medallion'], message: 'A plane ticket, a medallion and a note from Liv.', hints: [
      'Not every postcard belongs. Liv’s journal page shows the family’s marks; each real card carries one of them in its corner.',
      'Four cards carry a mark that is not in the drawings: a horned helmet or a double-sided axe. Set those four decoys aside.',
      'Sort each trail’s real cards into the order Liv visited them. The booking confirmations show where each trail ended and the next began, and the journal lists journeys she made. Then use the marker to join the stops on each map in that order.',
      'Leif’s route draws a 1, Rollo’s a 9, Aud’s a 7 and Harald’s a 2. The combination is 1972.'
    ] }
  ];
  const legs = { 1: 'Leif’s trail', 2: 'Rollo’s trail', 3: 'Aud’s trail', 4: 'Harald’s trail', 5: 'The final route' };
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
      const extra = {};
      if (items[id].widget === 'tally') extra.wheels = [0, 1, 2, 3].map(i => Math.floor(clamp(p.wheels?.[i], 0, 9, 0)));
      if (id === 'comb' && p.seated === true) extra.seated = true;
      if (items[id].widget === 'tafl') extra.tafl = taflSquares(p.tafl);
      if (items[id].marker) extra.marks = markLines(p.marks);
      state.pieces[id] = { x: clamp(p.x, 10, table.w - items[id].w - 10, items[id].at[0]), y: clamp(p.y, 10, table.h - items[id].h - 10, items[id].at[1]), rot: items[id].freeRotate && Number.isFinite(p.rot) ? ((p.rot % 360) + 360) % 360 : [0, 90, 180, 270].includes(p.rot) ? p.rot : 0, face: faceOf(id, p), stowed: !!p.stowed, ...extra };
    }
    state.table = Math.max(Number.isInteger(raw.table) ? clamp(raw.table, 0, sizes.length - 1, 0) : 0, sizeFor(state));
    return state;
  }

  /* The table starts small and grows as props arrive; it never shrinks during play.
     A new prop goes in the first free spot, scanning rows from the top left; if none is
     free, the table grows a size. Only arrival order decides where things land. */
  const sizes = L.sizes.map(([w, h]) => ({ w: Math.round(w * PPI), h: Math.round(h * PPI) }));
  const EDGE = Math.round(0.4 * PPI), GAP = Math.round(0.5 * PPI), STEP = Math.round(0.25 * PPI), TIGHTER = [0.25, 0.1].map(g => Math.round(g * PPI));
  // The upright box a prop covers on the table, at any rotation.
  const square = p => p.rot % 90 === 0;
  function footprint(id, p) {
    const it = items[id];
    let w = it.w, h = it.h;
    if (square(p)) { if (p.rot % 180) [w, h] = [it.h, it.w]; }
    else {
      const a = p.rot * Math.PI / 180, c = Math.abs(Math.cos(a)), s = Math.abs(Math.sin(a));
      [w, h] = [it.w * c + it.h * s, it.w * s + it.h * c];
    }
    return { x: p.x + (it.w - w) / 2, y: p.y + (it.h - h) / 2, w, h };
  }
  // A point given in a prop's own unrotated units (from its top left), as it lies on the table.
  function onTable(id, p, [lx, ly]) {
    const it = items[id], a = p.rot * Math.PI / 180, vx = lx - it.w / 2, vy = ly - it.h / 2;
    return [p.x + it.w / 2 + vx * Math.cos(a) - vy * Math.sin(a), p.y + it.h / 2 + vx * Math.sin(a) + vy * Math.cos(a)];
  }
  // Turn a prop to `rot` degrees about one of its own points, keeping that point where it is.
  function turnAbout(id, p, rot, local) {
    const it = items[id], [ax, ay] = onTable(id, p, local);
    p.rot = ((rot % 360) + 360) % 360;
    const [bx, by] = onTable(id, p, local);
    p.x += ax - bx; p.y += ay - by;
  }
  function sizeFor(state) {
    const boxes = Object.entries(state.pieces).map(([id, p]) => footprint(id, p));
    const i = sizes.findIndex(s => boxes.every(b => b.x + b.w <= s.w && b.y + b.h <= s.h));
    return i < 0 ? sizes.length - 1 : i;
  }
  function findSpot(pieces, id, size, gap = GAP) {
    const it = items[id], taken = Object.entries(pieces).filter(([k, p]) => k !== id && !p.stowed).map(([k, p]) => footprint(k, p));
    for (let y = EDGE; y + it.h + EDGE <= size.h; y += STEP)
      for (let x = EDGE; x + it.w + EDGE <= size.w; x += STEP)
        if (taken.every(b => x + it.w + gap <= b.x || b.x + b.w + gap <= x || y + it.h + gap <= b.y || b.y + b.h + gap <= y)) return [x, y];
    return null;
  }
  /* Snap: when a prop's edge comes within `reach` table units of another prop's edge,
     pull it flush (cards meeting edge to edge, or pulled out of a slight overlap).
     Then, beside the prop it now touches, line up the side edges if they are close. */
  function snap(state, id, reach) {
    const p = state.pieces[id];
    if (!square(p) || items[id].noSnap) return false;
    const others = Object.entries(state.pieces).filter(([k, q]) => k !== id && !q.stowed && square(q) && !items[k].noSnap).map(([k, q]) => footprint(k, q));
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
  const lying = ([x, y], id) => ({ x, y, rot: 0, face: 0, stowed: false, ...(items[id]?.widget === 'tally' ? { wheels: [0, 0, 0, 0] } : {}), ...(items[id]?.widget === 'tafl' ? { tafl: taflSquares() } : {}) });
  /* Hnefatafl pieces: 16 dark, 6 light, then the king. Each is on a square ('A1'–'K11') or in
     the tray (null). Bad entries and second pieces on a square go back to the tray. */
  // Wet-erase marker lines on a map: [x1, y1, x2, y2] as fractions of the map's width and height.
  const markLines = raw => (Array.isArray(raw) ? raw : []).filter(l => Array.isArray(l) && l.length === 4 && l.every(v => Number.isFinite(v) && v >= 0 && v <= 1)).slice(0, 300).map(l => l.map(v => Math.round(v * 1e5) / 1e5));
  const TAFL = [...Array(16).fill('dark'), ...Array(6).fill('light'), 'king'];
  function taflSquares(raw) {
    const seen = new Set();
    return TAFL.map((_, i) => { const sq = raw?.[i]; if (typeof sq !== 'string' || !/^[A-K](?:[1-9]|1[01])$/.test(sq) || seen.has(sq)) return null; seen.add(sq); return sq; });
  }
  // Which face is up. Saves before 1 Oct 2026 stored back: true/false instead.
  function faceOf(id, p) {
    const n = items[id].faces?.length || 1;
    return Number.isInteger(p.face) ? clamp(p.face, 0, n - 1, 0) : (p.back && n > 1 ? 1 : 0);
  }
  // Deal every collected prop that is not on the table yet, growing the table if needed.
  // Returns true if the table had to be laid out again because the free space ran out.
  function deal(state) {
    for (const id of available(state.stage)) {
      if (state.pieces[id]) continue;
      let spot = null;
      while (!(spot = findSpot(state.pieces, id, sizes[state.table])) && state.table < sizes.length - 1) state.table++;
      // On the biggest table, squeeze the gaps before giving up on a free spot.
      for (const gap of TIGHTER) spot = spot || findSpot(state.pieces, id, sizes[state.table], gap);
      if (!spot) { arrange(state); return true; }
      state.pieces[id] = lying(spot, id);
    }
    return false;
  }
  // Tidy keeps the work done on props: tally digits, board pieces, marker lines.
  const keepWork = (state, id, piece) => { const k = state.pieces[id] || {}; for (const key of ['wheels', 'tafl', 'marks']) if (k[key]) piece[key] = k[key]; return piece; };
  // Tidy: every prop face up, packed in arrival order on the smallest table that holds them all.
  function arrange(state) {
    const tries = [...sizes.map((_, i) => [i, GAP]), ...TIGHTER.map(gap => [sizes.length - 1, gap])];
    for (const [i, gap] of tries) {
      const pieces = {};
      for (const id of available(state.stage)) {
        const spot = findSpot(pieces, id, sizes[i], gap);
        if (!spot) break;
        pieces[id] = keepWork(state, id, lying(spot, id));
      }
      if (Object.keys(pieces).length === available(state.stage).length) { state.table = i; state.pieces = pieces; return; }
    }
    state.table = sizes.length - 1;
    state.pieces = Object.fromEntries(available(state.stage).map(id => [id, keepWork(state, id, lying(items[id].at, id))]));
  }
  function attempt(state, answer) {
    const lock = locks[state.stage];
    if (!lock || lock.pending || String(answer).trim().toUpperCase() !== lock.answer) return false;
    state.stage++;
    return true;
  }
    /* Aud's comb seats the way the real one does: comb face up, AD message side up, both
     square to each other, and both holes over both printed ring-and-dots (card points from
     Props/Comb). Seated, it travels and turns with the card. */
  const PT = PPI / 72;
  const COMB = { origin: [-16.5, 7], holes: [[22, 16], [22, 186]], dots: [[22, 16], [22, 186]] };
  function combPoints(state) {
    const c = state.pieces.comb, ad = state.pieces.AD;
    return { holes: COMB.holes.map(([x, y]) => onTable('comb', c, [(x - COMB.origin[0]) * PT, (y - COMB.origin[1]) * PT])), dots: COMB.dots.map(([x, y]) => onTable('AD', ad, [x * PT, y * PT])) };
  }
  const canSeat = (c, ad) => c && ad && !c.stowed && !ad.stowed && ad.face === 1 && c.face === 0 && ((c.rot - ad.rot) % 360 + 360) % 360 === 0;
  function seatComb(state, reach) {
    const c = state.pieces.comb, ad = state.pieces.AD;
    if (!canSeat(c, ad)) return false;
    const { holes: h, dots: d } = combPoints(state);
    if (Math.max(Math.hypot(h[0][0] - d[0][0], h[0][1] - d[0][1]), Math.hypot(h[1][0] - d[1][0], h[1][1] - d[1][1])) > reach) return false;
    c.seated = true; followSeat(state); return true;
  }
  function followSeat(state) {
    const c = state.pieces.comb, ad = state.pieces.AD;
    if (!c?.seated) return;
    c.rot = ad?.rot ?? c.rot;
    if (!canSeat(c, ad)) { c.seated = false; return; }
    const { holes: h, dots: d } = combPoints(state);
    c.x += (d[0][0] + d[1][0] - h[0][0] - h[1][0]) / 2; c.y += (d[0][1] + d[1][1] - h[0][1] - h[1][1]) / 2;
  }
  const api = { PPI, table, sizes, items, locks, legs, initial, available, fresh, restore, attempt, clamp, deal, arrange, footprint, snap, onTable, turnAbout, seatComb, followSeat, combPoints, TAFL, taflSquares, markLines };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LeifGame = api;
})(typeof window === 'undefined' ? globalThis : window);
