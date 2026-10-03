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
    map: { name: 'The Western Lands', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_1_Leif_Print.png'], ...mapSlot(1) },
    R2: { name: 'Rouen', kind: 'Postcard', faces: postcard('R2_Rouen'), ...cardSlot(5) },
    rolloMap: { name: 'The Granted Lands', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_2_Rollo_Print.png'], ...mapSlot(2) },
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
    audMap: { name: 'The Island Settlement', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_3_Aud_Print.png'], ...mapSlot(3) },
    audTicket: { name: 'Aud’s Treasure Museum ticket', kind: 'Ticket', faces: ['../Props/_Renders/Aud_Ticket_Front.png', '../Props/_Renders/Aud_Ticket_Back.png'], ...slot('audTicket') },
    // The four-wheel treasure tally (PR-24): digits drawn like the printed seven-segment ring.
    tally: { name: 'Tally', kind: 'Tally', widget: 'tally', noSnap: true, ...slot('tally') },
    // Aud's comb (PR-19): seats on AD's message side over the two printed ring-and-dots.
    comb: { name: 'Carved comb', kind: 'Comb', faces: ['./assets/Comb_Front.svg', './assets/Comb_Back.svg'], noSnap: true, ...slot('comb') },
    H4: { name: 'Hedeby', kind: 'Postcard', faces: postcard('H4_Hedeby'), ...cardSlot(16) },
    H5: { name: 'Sicily', kind: 'Postcard', faces: postcard('H5_Sicily'), ...cardSlot(17) },
    haraldMap: { name: 'The Varangian Road', kind: 'Map', marker: true, faces: ['../Props/_Renders/Trail_Map_4_Harald_Front.png', '../Props/_Renders/Trail_Map_4_Harald_Back.png'], ...mapSlot(4) },
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
    { nudge: 'Liv sent her bag with a postcard, two luggage tags and a museum ticket. Start with her postcard.', name: 'Main compartment', pocket: 'main', answer: '1021', releases: ['L2', 'L3'], message: 'Inside are two more postcards from Liv.', hints: [
      'Look at both luggage tags and both sides of the first postcard.',
      'Each tag has a street number. The postcard is from the first stop of Liv’s journey. Which tag matches that place?',
      'Use the Vinland tag’s street number first, followed by the Rouen tag’s street number.',
      'The combination is 1021.'
    ] },
    { nudge: 'Two more postcards from Liv. Read them side by side.', name: 'Lower front pocket', pocket: 'lowerFront', answer: '1576', releases: ['LD', 'map'], message: 'A postcard from Greenland and a map of the Western Lands were tucked inside.', hints: [
      'Read the two new postcards. What do they both say about the sky?',
      'Try bringing the two illustrated skies together on the table. You can rotate and move the cards.',
      'Put Battle Harbour above Baffin Island, both picture-side up. Rotate Battle Harbour twice so it is upside down, then move it until its top edge meets Baffin Island’s top edge. Use the magnifier on the join.',
      'The joined cloud fragments read 1576.'
    ] },
    { nudge: 'A postcard from Greenland and a map of the Western Lands. Every little detail counts.', name: 'Small pouch', pocket: 'rolloPouch', answer: '3212', releases: ['R2', 'rolloMap', 'rouenTicket'], message: 'A postcard from Rouen, a map of the Granted Lands and a museum ticket.', hints: [
      'Inspect every detail on the Brattahlíð postcard, including the small print. Keep the sea chart and museum ticket nearby.',
      '“Series F, No. 1” points to a square on the chart. What animal is there?',
      'The animal is a bear. Spell its name using the visitor index on the back of the museum ticket, taking one digit per letter.',
      'B → 3, E → 2, A → 1, R → 2. The combination is 3212.'
    ] },
    { nudge: 'The Granted Lands map, a postcard from Rouen and a museum ticket. See what they have in common.', name: 'Lower left pocket', pocket: 'lowerLeft', answer: '1486', releases: ['R1', 'R6', 'RD'], message: 'Three more postcards.', hints: [
      'Read the Rouen postcard next to the back of the Rouen museum ticket. Some of Liv’s words have a partner on the ticket.',
      'The ticket pairs everyday Saxon words (numbered) with their Norman partners (lettered). A matched pair gives a letter and a number: a square on the Granted Lands map.',
      'Liv mentions fighting, people, poultry and an inn, in that order. For each, match the pair, find its square on the map, and count the squares to the drawing for that word.',
      'Fight 1, people 4, poultry 8, inn 6. The combination is 1486.'
    ] },
    { nudge: 'Three more postcards. Look closely at their pictures.', name: 'Lower right pocket', pocket: 'lowerRight', answer: '562', releases: ['R3', 'R4', 'R5', 'ruler'], message: 'Three more postcards, and Liv’s architect’s ruler.', hints: [
      'Look closely at the pictures on the three new postcards. Each message mentions something small in passing.',
      'Count the Viking boats at Walcheren, the wild boars in Roumare Forest and the crossbow bolts at Châlus. Use the magnifier: some hide well. Read Roumare’s message again before you settle on its number.',
      'The Fun Facts on the backs date each place. Put the counts in date order: Walcheren, then Roumare, then Châlus. Liv thinks there were twice as many boars as she saw.',
      '5 boats, 3 boars doubled to 6, 2 bolts. The combination is 562.'
    ] },
    // Lock 6 (PZ-14): measured on Rollo's map with the ruler's 1:125 face. Code confirmed 2 Oct 2026.
    { nudge: 'Three more postcards and Liv’s ruler. Her drawings only make sense at the right scale.', name: 'Large pouch', pocket: 'largePouch', answer: '104', releases: ['A2', 'audMap', 'audTicket'], message: 'A postcard from Iceland, a map of the Island Settlement and a museum ticket.', hints: [
      'The Bayeux, Winchester and Battle postcards each end with a little picture puzzle. Read them as rebuses.',
      'Two of the rebuses point to places on the Granted Lands map; the third tells you which scale of the ruler to use.',
      'Measure between those two places on the Granted Lands map with the architect’s ruler, on its 1:125 scale.',
      'The distance measures 104 on the 1:125 scale. The combination is 104.'
    ] },
    { nudge: 'The Island Settlement map and a ticket from a treasure museum. Liv went on a treasure hunt.', name: 'Lower front pocket, again', pocket: 'lowerFront', answer: '521', releases: ['A1', 'A3', ...coinIds, 'tally'], message: 'Two more postcards, a pouch of coins and a little tally.', hints: [
      'The Island Settlement map and the Treasure Museum ticket go together: the ticket gives directions, and the Hvammur card says what to count on the way.',
      'Start at the northernmost chapel on the Island Settlement map and follow the ticket’s six steps along the roads.',
      'As you go, count the bridges, the fords and the gates you cross. Keep three separate tallies, in that order.',
      '5 bridges, 2 fords, 1 gate. The combination is 521.'
    ] },
    { nudge: 'A pouch of coins and a little tally. Not every coin belongs together.', name: 'Inside top pocket', pocket: 'insideTop', answer: 'SOLE', releases: ['AD', 'comb'], message: 'A postcard from Bjarnarhöfn and a carved comb.', hints: [
      'Not every coin belongs to the same hoard. The front of the Treasure Museum ticket sorts them into three groups and gives their values.',
      'The Island Settlement map marks where the treasure was hidden with a rune. Find that rune on the ticket: it picks one group of coins.',
      'Add up the values of the coins in that group, set the total on the tally’s wheels, then turn the tally upside down.',
      '5 + 100 + 3,600 = 3705, which reads SOLE upside down.'
    ] },
    { nudge: 'A postcard from Bjarnarhöfn and a carved comb. Liv’s souvenirs are rarely just what they seem.', name: 'Large pouch, once more', pocket: 'largePouch', answer: 'BOOK', releases: ['H4', 'H5', 'haraldMap', 'ravenCard'], message: 'Two more postcards, a map of the Varangian Road and a card of raven flights.', hints: [
      'The comb is more than a comb. Try it on one of the postcards.',
      'Its two holes fit over the two little ring-and-dot marks on the Bjarnarhöfn card’s message side. Line them up and the comb settles in.',
      'With the comb in place, most lines are hidden, but four of its teeth are broken short. Read the first letter that shows after each short tooth, from the top down.',
      'The short teeth uncover “brother’s”, “ould”, “ongside” and “Keep”: B, O, O, K. The combination is BOOK.'
    ] },
    { nudge: 'The Varangian Road map and a card of raven flights. Look for marks that don’t belong on a map.', name: 'Lower left pocket, again', pocket: 'lowerLeft', answer: '2648', releases: ['H2', 'H3', 'HD'], message: 'Three more postcards.', hints: [
      'The Varangian Road map has a few odd little marks among the places. The Hedeby postcard explains what they are.',
      'They are branch runes: the Hedeby card shows how the branches on each side pick a rune. The word the Sicily card writes in capitals tells you which columns of the map to read, and in what order.',
      'Reading the runes in columns R, A, V, E and N gives H, R, A, F, N. Follow H → R → A → F → N on the raven’s flights card and note the number on each flight.',
      '2, 6, 4 and 8. The combination is 2648.'
    ] },
    { nudge: 'Three more postcards. What was in Harald’s horn?', name: 'Board bag', pocket: 'boardBag', answer: 'MEAD', releases: ['H1', 'board', 'osloTicket'], message: 'The Oslo postcard, a Hnefatafl board with its pieces, and a museum ticket.', hints: [
      'Each of the three new postcards hides one word. Together they say what was in Harald’s horn.',
      'On the Staraya Ladoga card, only a few letters sit right on the left margin: read them downwards. The Kyiv card is a riddle, and the Constantinople card ends with a picture puzzle.',
      'Staraya Ladoga spells DRINK, Kyiv’s riddle answers HONEY, and Constantinople’s pictures (sugar and yeast becoming a fizzing flask) mean FERMENTED. A fermented honey drink is…',
      'MEAD. The combination is MEAD.'
    ] },
    { nudge: 'A Hnefatafl board and its pieces. Liv kept a note of how to set them out.', name: 'Large pouch, last time', pocket: 'largePouch', answer: '253', releases: ['H6', 'transition1', 'transition2', 'transition3', 'journal'], message: 'The last postcard, three booking confirmations and a page from Liv’s journal.', hints: [
      'The back of the Varangian Road map is Liv’s note of a Hnefatafl starting position. Set the pieces out on the board to match it.',
      'A wet ticket ruined columns I to K of her note. The museum ticket carries them: turn it over until you can see it held up to the light, the right way round.',
      'The Oslo postcard says the king escapes in exactly three moves. The king starts on the centre square and slides like a rook, never jumping, until it reaches a corner. Count the squares of each move.',
      'F6 → H6 → H11 → K11: moves of 2, 5 and 3 squares. The combination is 253.'
    ] },
    // The final riddle (PZ-18, PZ-06): filter the decoys, order each trail, draw it on its map.
    { nudge: 'All 22 postcards, four maps, three bookings and Liv’s journal page. Her whole year is on the table.', name: 'Inside middle pocket', pocket: 'insideMiddle', answer: '1972', releases: ['medallion'], message: 'A plane ticket, a medallion and a note from Liv.', hints: [
      'Not every postcard belongs. Liv’s journal page shows the family’s marks; each real card carries one of them in its corner.',
      'Four cards carry a mark that is not in the drawings: a horned helmet or a double-sided axe. Set those four decoys aside.',
      'Sort the real cards for each map into the order Liv visited them. The booking confirmations show where one journey ended and the next began, and the journal lists journeys she made. Then use the marker to join the stops on each map in that order.',
      'The Western Lands route draws a 1, the Granted Lands a 9, the Island Settlement a 7 and the Varangian Road a 2. The combination is 1972.'
    ] }
  ];
  const MAX_ATTEMPTS = 30;
  /* Liv's handwritten notes for the online edition: the opening letter, one note per new trail
     and the closing letter (its last lines are the ones the physical ending uses). DRAFT copy,
     2 Oct 2026: swap in the printed letters once they are written. */
  const STORY = {
    // The opening quotes postcard L1 word for word (Postcards/build_postcard_L1_pdf.py), so it sets the scene without adding to the story.
    letter: ['Hello nephew!',
      'I know you love puzzles, so I created an adventure for you! With a surprise at the end!',
      'With love, Aunt Liv'],
    ending: ['You followed every stop I made and found the story that brought me here.',
      'I could use someone who notices what everyone else walks past, and I have a spare place on the dig.',
      'Pack your bag. I’ll meet you in Norway.'],
    signature: 'Love, Aunt Liv'
  };
  // The backpack's pockets, as drawn in the backpack panel; each lock names the pocket it closes.
  const POCKETS = { main: 'Main compartment', insideTop: 'Inside top pocket', insideMiddle: 'Inside middle pocket', lowerFront: 'Lower front pocket', lowerLeft: 'Lower left pocket', lowerRight: 'Lower right pocket', rolloPouch: 'Small pouch', largePouch: 'Large pouch', boardBag: 'Board bag' };
  const initial = ['L1', 'tagA', 'tagB', 'ticket'];
  const available = stage => [...initial, ...locks.slice(0, stage).flatMap(lock => lock.releases)];
  /* A saved game. attempts: wrong codes tried per lock; played/lockTime: active play in ms
     (whole game and per lock); ratings: the player's 1-5 for each opened puzzle (0 = none);
     itemNotes: notes pinned to keepsakes; team: the name on the certificate. */
  const fresh = () => ({ version: 1, stage: 0, table: 0, pieces: {}, piles: {}, hints: locks.map(() => 0), notes: '',
    attempts: locks.map(() => []), played: 0, lockTime: locks.map(() => 0), ratings: locks.map(() => 0), itemNotes: {}, team: '' });
  const clamp = (v, min, max, fallback) => Number.isFinite(v) ? Math.min(max, Math.max(min, v)) : fallback;
  function restore(raw) {
    const state = fresh();
    if (!raw || raw.version !== 1) return state;
    state.stage = Number.isInteger(raw.stage) ? clamp(raw.stage, 0, locks.length, 0) : 0;
    state.notes = typeof raw.notes === 'string' ? raw.notes.slice(0, 6000) : '';
    state.attempts = state.attempts.map((_, i) => (Array.isArray(raw.attempts?.[i]) ? raw.attempts[i] : []).filter(code => typeof code === 'string' && /^[0-9A-Z]{3,4}$/.test(code)).slice(-MAX_ATTEMPTS));
    state.played = Math.round(clamp(raw.played, 0, 1e10, 0));
    state.lockTime = state.lockTime.map((_, i) => Math.round(clamp(raw.lockTime?.[i], 0, 1e10, 0)));
    state.ratings = state.ratings.map((_, i) => Math.round(clamp(raw.ratings?.[i], 0, 5, 0)));
    for (const [id, text] of Object.entries(raw.itemNotes && typeof raw.itemNotes === 'object' ? raw.itemNotes : {}))
      if (items[id] && typeof text === 'string' && text.trim()) state.itemNotes[id] = text.slice(0, 1000);
    state.team = typeof raw.team === 'string' ? raw.team.replace(/\s+/g, ' ').trim().slice(0, 40) : '';
    state.hints = state.hints.map((_, i) => Math.floor(clamp(raw.hints?.[i], 0, 4, 0)));
    for (const id of available(state.stage)) {
      const p = raw.pieces?.[id];
      if (!p || typeof p !== 'object') continue;
      const extra = {};
      if (items[id].widget === 'tally') extra.wheels = [0, 1, 2, 3].map(i => Math.floor(clamp(p.wheels?.[i], 0, 9, 0)));
      if (id === 'comb' && p.seated === true) extra.seated = true;
      if (items[id].widget === 'tafl') extra.tafl = taflSquares(p.tafl);
      if (items[id].marker) extra.marks = markLines(p.marks);
      if (p.pile && p.pile === pileFor(id) && !p.stowed) extra.pile = p.pile;
      state.pieces[id] = { x: clamp(p.x, 10, table.w - items[id].w - 10, items[id].at[0]), y: clamp(p.y, 10, table.h - items[id].h - 10, items[id].at[1]), rot: items[id].freeRotate && Number.isFinite(p.rot) ? ((p.rot % 360) + 360) % 360 : [0, 90, 180, 270].includes(p.rot) ? p.rot : 0, face: faceOf(id, p), stowed: !!p.stowed, ...extra };
    }
    for (const name of Object.keys(PILES)) {
      const at = raw.piles?.[name];
      if (Array.isArray(at) && at.length === 2) state.piles[name] = [clamp(at[0], 10, table.w - 10, 10), clamp(at[1], 10, table.h - 10, 10)];
    }
    for (const q of Object.values(state.pieces)) if (q.pile && !state.piles[q.pile]) delete q.pile;
    repack(state);
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
  // What a new prop must keep clear of: every prop on the table, with each pile taken as one block.
  function takenBoxes(pieces, except) {
    const out = [], piles = {};
    for (const [k, p] of Object.entries(pieces)) {
      if (k === except || p.stowed) continue;
      const b = footprint(k, p), u = p.pile && piles[p.pile];
      if (!p.pile) out.push(b);
      else piles[p.pile] = u ? { x: Math.min(u.x, b.x), y: Math.min(u.y, b.y), w: Math.max(u.x + u.w, b.x + b.w) - Math.min(u.x, b.x), h: Math.max(u.y + u.h, b.y + b.h) - Math.min(u.y, b.y) } : b;
    }
    return [...out, ...Object.values(piles)];
  }
  function findSpot(pieces, id, size, gap = GAP) { return freeAt(takenBoxes(pieces, id), items[id], size, gap); }
  // The first spot, scanning rows from the top left, where a w x h box clears every taken box by gap.
  function freeAt(taken, { w, h }, size, gap) {
    for (let y = EDGE; y + h + EDGE <= size.h; y += STEP)
      for (let x = EDGE; x + w + EDGE <= size.w; x += STEP)
        if (taken.every(b => x + w + gap <= b.x || b.x + b.w + gap <= x || y + h + gap <= b.y || b.y + b.h + gap <= y)) return [x, y];
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
  /* Where a box can go without moving anything already on the table: the first free
     spot, growing the table a size at a time, then with tighter gaps on the biggest table. If
     the table is truly full, the spot that covers least of what is there: it lies on top. */
  function spotFor(state, box, taken = takenBoxes(state.pieces)) {
    let spot = null;
    while (!(spot = freeAt(taken, box, sizes[state.table], GAP)) && state.table < sizes.length - 1) state.table++;
    for (const gap of TIGHTER) spot = spot || freeAt(taken, box, sizes[state.table], gap);
    return spot ? { at: spot, crowded: false } : { at: leastCovered(taken, box, sizes[state.table]), crowded: true };
  }
  function leastCovered(taken, { w, h }, size) {
    let best = [EDGE, EDGE], least = Infinity;
    for (let y = EDGE; y + h + EDGE <= size.h; y += STEP * 2)
      for (let x = EDGE; x + w + EDGE <= size.w; x += STEP * 2) {
        let cover = 0;
        for (const b of taken) cover += Math.max(0, Math.min(x + w, b.x + b.w) - Math.max(x, b.x)) * Math.max(0, Math.min(y + h, b.y + b.h) - Math.max(y, b.y));
        if (cover < least) { least = cover; best = [x, y]; if (!cover) return best; }
      }
    return best;
  }
  // Deal every collected prop that is not on the table yet. Props already on the table never move.
  // Returns true if the table was full, so something new had to go on top of other props.
  function deal(state) {
    // Older props that were never laid out (an old save, a test start) go straight to their pile or the shelf.
    const fresh = available(state.stage).filter(id => !state.pieces[id] && retired(state, id));
    for (const id of fresh) state.pieces[id] = { ...lying(items[id].at, id), ...(pileFor(id) ? { pile: pileFor(id) } : { stowed: true }) };
    const crowded = fresh.length ? stack(state) : false;
    return place(state, available(state.stage).filter(id => !state.pieces[id])) || crowded;
  }
  /* Lay a batch of props (new, or back out of a pile) in free spots around everything else,
     keeping any work on them. Arrival order first; if that runs out of room, tallest first,
     which packs tighter. Returns true if something had to go on top of other props. */
  function place(state, ids) {
    const tryOrder = order => {
      const waiting = new Set(order), pieces = Object.fromEntries(Object.entries(state.pieces).filter(([k]) => !waiting.has(k)));
      const trial = { ...state, pieces };
      let full = false;
      for (const id of order) {
        const s = spotFor(trial, items[id]); full = full || s.crowded;
        pieces[id] = { ...(state.pieces[id] || lying(s.at, id)), x: s.at[0], y: s.at[1], rot: 0 };
      }
      return { trial, full };
    };
    if (!ids.length) return false;
    let best = tryOrder(ids);
    if (best.full) { const other = tryOrder([...ids].sort((a, b) => items[b].h - items[a].h)); if (!other.full) best = other; }
    state.pieces = best.trial.pieces; state.table = best.trial.table;
    return best.full;
  }
  // Tidy keeps the work done on props: tally digits, board pieces, marker lines.
  const keepWork = (state, id, piece) => { const k = state.pieces[id] || {}; for (const key of ['wheels', 'tafl', 'marks']) if (k[key]) piece[key] = k[key]; return piece; };

  /* Stacks (DG-11, by age since DG-12). Tidy puts older keepsakes into three piles: postcards,
     maps and paper props. Each pile is fanned so the bottom strip of every card shows (the
     table draws its name there); solid props (coins, tally, comb, ruler, board) are put away
     in the shelf. What the last two locks released stays out, so piles never follow a trail.
     For the last lock every postcard and map stays out: it needs them all. */
  const STRIP = Math.round(0.45 * PPI);
  const PILES = { cards: ['Postcard'], maps: ['Map'], papers: ['Luggage tag', 'Ticket', 'Card', 'Journal page'] };
  const pileFor = id => Object.keys(PILES).find(k => PILES[k].includes(items[id].kind)) || null;
  // Which lock released a prop (-1: it came with the bag), and whether the last lock is next.
  const arrival = id => locks.findIndex(l => l.releases.includes(id));
  const finalRoute = stage => stage >= locks.length - 1;
  function retired(state, id) {
    if (arrival(id) >= state.stage - 2) return false;
    return !(finalRoute(state.stage) && ['Postcard', 'Map'].includes(items[id].kind));
  }
  // A pile's members, top card first (paper props smallest on top), and each one's drop below the pile's top.
  const pileOrder = (ids, name) => name === 'papers' ? [...ids].sort((a, b) => items[a].h - items[b].h) : ids;
  function pileShape(ids) {
    let bottom = 0;
    const rel = ids.map((id, i) => { bottom = i ? bottom + STRIP : items[id].h; return [id, bottom - items[id].h]; });
    const top = Math.min(...rel.map(([, y]) => y));
    return { offsets: rel.map(([id, y]) => [id, y - top]), w: Math.max(...ids.map(id => items[id].w)), h: bottom - top };
  }
  const pileMembers = (state, name) => pileOrder(available(state.stage).filter(id => state.pieces[id]?.pile === name), name);
  // Lay each pile out again from its top-left corner, closing any gap left by a card taken out.
  function repack(state) {
    for (const name of Object.keys(PILES)) {
      const ids = pileMembers(state, name), at = state.piles[name];
      if (!ids.length || !at) { delete state.piles[name]; continue; }
      for (const [id, dy] of pileShape(ids).offsets) Object.assign(state.pieces[id], { x: at[0], y: at[1] + dy, rot: 0 });
    }
  }
  // Tidy: older keepsakes stacked, everything else face up and packed in arrival order, on the
  // smallest table that holds it all.
  function arrange(state) {
    const ids = available(state.stage), stacked = ids.filter(id => retired(state, id));
    const piles = Object.keys(PILES).map(name => ({ name, ids: pileOrder(stacked.filter(id => pileFor(id) === name), name) })).filter(b => b.ids.length);
    const blocks = [...piles.map(b => ({ ...b, ...pileShape(b.ids) })), ...ids.filter(id => !stacked.includes(id)).map(id => ({ id, w: items[id].w, h: items[id].h }))];
    // Piles first, then arrival order; if that does not fit, tallest first, which packs tighter.
    const orders = [blocks, [...blocks].sort((a, b) => b.h - a.h)];
    const tries = [...sizes.map((_, i) => [i, GAP]), ...TIGHTER.map(gap => [sizes.length - 1, gap])];
    for (const [i, gap] of tries) for (const order of orders) {
      const pieces = {}, corners = {};
      let fits = true;
      for (const b of order) {
        const at = freeAt(takenBoxes(pieces), b, sizes[i], gap);
        if (!at) { fits = false; break; }
        if (b.id) { pieces[b.id] = keepWork(state, b.id, lying(at, b.id)); continue; }
        corners[b.name] = at;
        for (const [id, dy] of b.offsets) pieces[id] = keepWork(state, id, { ...lying([at[0], at[1] + dy], id), pile: b.name });
      }
      if (!fits) continue;
      for (const id of stacked) if (!pileFor(id)) pieces[id] = keepWork(state, id, { ...lying(items[id].at, id), stowed: true });
      state.table = i; state.pieces = pieces; state.piles = corners; return;
    }
    state.table = sizes.length - 1; state.piles = {};
    state.pieces = Object.fromEntries(ids.map(id => [id, keepWork(state, id, lying(items[id].at, id))]));
  }
  /* Older props join their piles and solid props go to the shelf; a pile keeps its corner if it
     still clears everything, or takes a free spot. Everything else stays exactly where the player
     left it. Used only for props that were never laid out (an old save, a test start).
     Returns true if the table was full (see spotFor). */
  function stack(state) {
    const ids = available(state.stage), back = ids.filter(id => state.pieces[id]?.pile && !retired(state, id));
    let crowded = false;
    for (const id of back) delete state.pieces[id].pile;
    for (const id of ids) {
      const p = state.pieces[id];
      if (!p || p.pile || p.stowed || !retired(state, id)) continue;
      if (id === 'comb') p.seated = false;
      const name = pileFor(id);
      if (name) Object.assign(p, { pile: name, rot: 0, face: 0 }); else p.stowed = true;
    }
    const waiting = new Set(back);
    const loose = () => Object.entries(state.pieces).filter(([k, p]) => !p.stowed && !p.pile && !waiting.has(k)).map(([k, p]) => footprint(k, p));
    const placed = [];
    for (const name of Object.keys(PILES)) {
      const ids = pileMembers(state, name);
      if (!ids.length) { delete state.piles[name]; continue; }
      const { w, h } = pileShape(ids), taken = [...loose(), ...placed], at = state.piles[name];
      const fits = at && taken.every(b => at[0] + w <= b.x || b.x + b.w <= at[0] || at[1] + h <= b.y || b.y + b.h <= at[1]);
      if (fits) while (state.table < sizes.length - 1 && (at[0] + w + EDGE > sizes[state.table].w || at[1] + h + EDGE > sizes[state.table].h)) state.table++;
      let corner = at;
      if (!fits || at[0] + w > sizes[state.table].w || at[1] + h > sizes[state.table].h) { const s = spotFor(state, { w, h }, taken); corner = s.at; crowded = crowded || s.crowded; }
      state.piles[name] = corner; placed.push({ x: corner[0], y: corner[1], w, h });
    }
    repack(state);
    // Cards back from their piles and the new lock's props share the free space together.
    return place(state, [...back, ...ids.filter(id => !state.pieces[id])]) || crowded;
  }
  // The last lock needs every postcard and map: any in a pile come back out to free spots.
  function bringBack(state) {
    const back = available(state.stage).filter(id => state.pieces[id]?.pile && ['Postcard', 'Map'].includes(items[id].kind));
    for (const id of back) delete state.pieces[id].pile;
    repack(state);
    return back.length ? place(state, back) : false;
  }
  // Take a prop out of its pile or the shelf and lay it in the first free spot (see spotFor).
  function release(state, id) {
    const p = state.pieces[id];
    if (!p) return false;
    const piled = !!p.pile;
    delete p.pile; p.stowed = false;
    if (piled) repack(state);
    if (!items[id].freeRotate) p.rot = 0;
    const b = footprint(id, p), { at: spot } = spotFor(state, b, takenBoxes(state.pieces, id));
    p.x = spot[0] + p.x - b.x; p.y = spot[1] + p.y - b.y;
    return true;
  }
  // Out of its pile where it lies (picked up and dragged off it).
  function unpile(state, id) { const p = state.pieces[id]; if (!p?.pile) return false; delete p.pile; repack(state); return true; }
  // A try at the current lock. A wrong code is remembered (once) in that lock's attempt log.
  function attempt(state, answer) {
    const lock = locks[state.stage], code = String(answer).trim().toUpperCase();
    if (!lock || lock.pending) return false;
    if (code !== lock.answer) {
      const log = state.attempts[state.stage];
      if (/^[0-9A-Z]{3,4}$/.test(code)) { const at = log.indexOf(code); if (at >= 0) log.splice(at, 1); log.push(code); if (log.length > MAX_ATTEMPTS) log.shift(); }
      return false;
    }
    state.stage++;
    return true;
  }
  // If a code opened an earlier lock, which one (its index); otherwise -1.
  const earlierLock = (state, code) => locks.findIndex((l, i) => i < state.stage && l.answer === String(code).trim().toUpperCase());
  // Minutes and hours, for the ending and the shared result.
  const duration = ms => { const m = Math.round(ms / 60000), h = Math.floor(m / 60); return m < 1 ? 'under a minute' : h ? `${h} h ${String(m % 60).padStart(2, '0')} min` : `${m} min`; };
  // The shareable one-line result, Wordle-style: a key per lock opened without hints, a bulb per lock that used them.
  function shareText(state) {
    const used = state.hints.reduce((a, b) => a + b, 0);
    const marks = locks.map((_, i) => i >= state.stage ? '▫️' : state.hints[i] >= 4 ? '🔓' : state.hints[i] ? '💡' : '🗝️').join('');
    return `The Raven Inheritance · ${state.stage}/${locks.length} locks · ${duration(state.played)} · ${used} hint${used === 1 ? '' : 's'}\n${marks}\nescapepack.ca/play/norse/`;
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
  const api = { PPI, table, sizes, items, locks, STORY, MAX_ATTEMPTS, earlierLock, duration, shareText, POCKETS, stack, bringBack, finalRoute, arrival, spotFor, initial, available, fresh, restore, attempt, clamp, deal, arrange, release, unpile, repack, retired, pileMembers, STRIP, footprint, snap, onTable, turnAbout, seatComb, followSeat, combPoints, TAFL, taflSquares, markLines };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LeifGame = api;
})(typeof window === 'undefined' ? globalThis : window);
