/* The Raven Inheritance, V2: a box of rune-marked envelopes opened with a cypher wheel (PR-007,
   Full_Adventure.html, 18 Oct 2026). Player assets reuse the physical edition.
   This friends-only prototype checks answers locally; source is not spoiler-proof. */
(function (root) {
  /* Every prop is drawn at its real printed size. Sizes and start positions come from
     table-layout.js (inches), which plans the whole game's table; here they become
     table units. Postcards and maps take their slots in the order they arrive. */
  const L = root.TableLayout || require('./table-layout2.js');
  const PPI = L.PPI;
  const table = { w: L.table.w * PPI, h: L.table.h * PPI };
  const units = ({ w, h, x, y }) => ({ w: Math.round(w * PPI), h: Math.round(h * PPI), at: [Math.round(x * PPI), Math.round(y * PPI)] });
  const cardSlot = n => units(L.cardSlot(n)), mapSlot = n => units(L.mapSlot(n)), slot = key => units(L.props[key]);
  const V2 = f => `./assets/v2/${f}.webp`;
  const postcard = (slug) => ['Front', 'Back'].map(side => `../Web/Postcards/Postcard_${slug}_${side}.webp`);
  const items = {
    // On top of the box from the start: L1 (it gives the first code as a worked example) and Liv's notes card.
    L1: { name: "L’Anse aux Meadows", kind: 'Postcard', faces: postcard('L1_LAnse'), ...cardSlot(1) },
    notes: { name: 'Liv’s notes', kind: 'Card', faces: [V2('Notes_Card')], ...slot('notes') },
    AD: { name: 'Bjarnarhöfn', kind: 'Postcard', faces: postcard('AD_Bjarnarhofn'), ...cardSlot(15) },
    // Aud's comb (PR-19): seats on AD's message side over the two printed ring-and-dots.
    comb: { name: 'Carved comb', kind: 'Comb', faces: ['./assets/Comb_Front.svg', './assets/Comb_Back.svg'], noSnap: true, ...slot('comb') },
    L2: { name: 'Battle Harbour', kind: 'Postcard', faces: postcard('L2_Battle_Harbour'), ...cardSlot(2) },
    L3: { name: 'Baffin Island', kind: 'Postcard', faces: postcard('L3_Baffin_Island'), ...cardSlot(3) },
    H2: { name: 'Staraya Ladoga', kind: 'Postcard', faces: postcard('H2_Staraya_Ladoga'), ...cardSlot(19) },
    H3: { name: 'Kyiv', kind: 'Postcard', faces: postcard('H3_Kyiv'), ...cardSlot(20) },
    HD: { name: 'Constantinople', kind: 'Postcard', faces: postcard('HD_Constantinople'), ...cardSlot(21) },
    A2: { name: 'Hvammur', kind: 'Postcard', faces: postcard('A2_Hvammur'), ...cardSlot(13) },
    audMap: { name: 'The Island Settlement', kind: 'Map', marker: true, faces: [V2('Map_Aud')], ...mapSlot(3) },
    audTicket: { name: 'Aud’s Treasure Museum ticket', kind: 'Ticket', faces: [V2('Aud_Ticket_Front'), V2('Aud_Ticket_Back')], ...slot('audTicket') },
    R1: { name: 'Châlus', kind: 'Postcard', faces: postcard('R1_Chalus'), ...cardSlot(6) },
    R6: { name: 'Roumare Forest', kind: 'Postcard', faces: postcard('R6_Roumare_Forest'), ...cardSlot(7) },
    RD: { name: 'Walcheren', kind: 'Postcard', faces: postcard('RD_Walcheren'), ...cardSlot(8) },
    LD: { name: 'Brattahlíð', kind: 'Postcard', faces: postcard('LD_Brattahlid'), ...cardSlot(4) },
    map: { name: 'The Western Lands', kind: 'Map', marker: true, faces: [V2('Map_Leif')], ...mapSlot(1) },
    ticket: { name: 'Brattahlíð museum ticket', kind: 'Ticket', faces: [V2('Museum_Ticket_Front'), V2('Museum_Ticket_Back')], ...slot('museumTicket') },
    A1: { name: 'Dögurðarnes', kind: 'Postcard', faces: postcard('A1_Dogurdarnes'), ...cardSlot(12) },
    A3: { name: 'Esjuberg', kind: 'Postcard', faces: postcard('A3_Esjuberg'), ...cardSlot(14) },
    // The four-wheel treasure tally (PR-24): digits drawn like the printed seven-segment ring.
    tally: { name: 'Tally', kind: 'Tally', widget: 'tally', noSnap: true, ...slot('tally') },
    R2: { name: 'Rouen', kind: 'Postcard', faces: postcard('R2_Rouen'), ...cardSlot(5) },
    rolloMap: { name: 'The Granted Lands', kind: 'Map', marker: true, faces: [V2('Map_Rollo')], ...mapSlot(2) },
    rouenTicket: { name: 'Rouen museum ticket', kind: 'Ticket', faces: [V2('Rouen_Ticket_Front'), V2('Rouen_Ticket_Back')], ...slot('rouenTicket') },
    R3: { name: 'Bayeux', kind: 'Postcard', faces: postcard('R3_Bayeux'), ...cardSlot(9) },
    R4: { name: 'Winchester', kind: 'Postcard', faces: postcard('R4_Winchester'), ...cardSlot(10) },
    R5: { name: 'Battle', kind: 'Postcard', faces: postcard('R5_Battle'), ...cardSlot(11) },
    // Liv's printed ruler card (PP-025): LONGSHIP scale along the top, SPEAR scale on the other edge.
    // Flip turns it half way round so the SPEAR edge is on top with its 0 at the left. Each face turns about its own 0 mark.
    ruler: { name: 'Liv’s ruler', kind: 'Ruler', faces: [V2('Ruler'), V2('Ruler_Spear')], faceNames: ['LONGSHIP edge up', 'SPEAR edge up'], freeRotate: true,
      pivots: [[54.5 / 961, 8 / 253], [55.5 / 961, 9 / 253]], pivot: [54.5 / 961, 8 / 253], handles: [[0.985, 8 / 253], [0.985, 9 / 253]], handle: [0.985, 8 / 253], ...slot('ruler') },
    H1: { name: 'Oslo', kind: 'Postcard', faces: postcard('H1_Oslo'), ...cardSlot(18) },
    haraldMap: { name: 'The Varangian Road', kind: 'Map', marker: true, faces: [V2('Map_Harald_Front'), V2('Map_Harald_Back')], ...mapSlot(4) },
    // The 11 × 11 board with its 19 dark pieces, 6 light pieces and the king in a tray below.
    board: { name: 'Hnefatafl board', kind: 'Board', widget: 'tafl', ...slot('board') },
    // Its back holds columns I–K in mirror image; online it can also be held up to the light (PZ-008).
    osloTicket: { name: 'Hnefatafl Museum ticket', kind: 'Ticket', faces: [V2('Hnefatafl_Ticket_Front'), V2('Hnefatafl_Ticket_Back'), V2('Hnefatafl_Ticket_Light')], faceNames: ['front', 'back', 'held to the light'], ...slot('hnefataflTicket') },
    H4: { name: 'Hedeby', kind: 'Postcard', faces: postcard('H4_Hedeby'), ...cardSlot(16) },
    H5: { name: 'Sicily', kind: 'Postcard', faces: postcard('H5_Sicily'), ...cardSlot(17) },
    ravenCard: { name: 'Raven’s flights card', kind: 'Card', faces: [V2('Raven_Flights_Card')], ...slot('ravenFlights') },
    H6: { name: 'Patara', kind: 'Postcard', faces: postcard('H6_Patara'), ...cardSlot(22) },
    // Envelope 12 (PP-039): one page of hop tickets per journey, and the three flight bookings between journeys.
    hopLeif: { name: 'Hop tickets · Leif’s journey', kind: 'Hop tickets', faces: [V2('Hop_Tickets_Leif')], ...slot('hopLeif') },
    hopRollo: { name: 'Hop tickets · Rollo’s journey', kind: 'Hop tickets', faces: [V2('Hop_Tickets_Rollo')], ...slot('hopRollo') },
    hopAud: { name: 'Hop tickets · Aud’s journey', kind: 'Hop tickets', faces: [V2('Hop_Tickets_Aud')], ...slot('hopAud') },
    hopHarald: { name: 'Hop tickets · Harald’s journey', kind: 'Hop tickets', faces: [V2('Hop_Tickets_Harald')], ...slot('hopHarald') },
    flight1: { name: 'Booking confirmation', kind: 'Ticket', faces: [V2('Flight_Booking_1')], ...slot('flight1') },
    flight2: { name: 'Booking confirmation', kind: 'Ticket', faces: [V2('Flight_Booking_2')], ...slot('flight2') },
    flight3: { name: 'Booking confirmation', kind: 'Ticket', faces: [V2('Flight_Booking_3')], ...slot('flight3') },
    // Envelope 13: the plane ticket, Liv's last letter and the end-of-game keepsake (50 mm medallion).
    planeTicket: { name: 'Plane ticket', kind: 'Ticket', faces: [V2('Plane_Ticket')], ...slot('planeTicket') },
    finalLetter: { name: 'Liv’s last letter', kind: 'Letter', faces: [V2('Final_Letter')], ...slot('finalLetter') },
    medallion: { name: 'Medallion', kind: 'Medallion', faces: ['./assets/Medallion_Front.webp', './assets/Medallion_Back.webp'], round: true, noSnap: true, ...slot('medallion') }
  };
  // The hoard (PZ-03): 12 loose coins, mixed so the three piles are not handed over sorted.
  const COINS = ['01_dirham_common', '03_denier_common', '05_hedeby_ship', '01_dirham_common', '07_raven', '03_denier_common',
    '02_dirham_rare', '06_york_cross', '01_dirham_common', '04_denier_rare', '03_denier_common', '01_dirham_common'];
  const coinIds = COINS.map((_, i) => 'coin' + (i + 1));
  COINS.forEach((art, i) => { items[coinIds[i]] = { name: 'Coin', kind: 'Coin', faces: [`./assets/Coin_${art}.svg`], round: true, noSnap: true, ...slot(coinIds[i]) }; });
  /* The thirteen envelopes, in play order (Full_Adventure.html, 18 Oct 2026). Envelope N is opened by
     the code that the puzzle before it gives: `answer` is that code, `releases` is what is inside.
     Each step keeps the old field names (lock, answer, releases) so the table logic is unchanged.
     Hints are the records' hints (PZ-001 to PZ-013) word for word; the last entry is the solution. */
  const locks = [
    { nudge: 'Postcard L1 and the cypher wheel lie on top of the box.', name: 'Envelope 1', answer: '1021', releases: ['AD', 'comb'], message: 'A postcard from Bjarnarhöfn and Aud’s carved comb.', hints: [
      'Read the postcard on top of the box: it tells you what to set on the wheel.',
      'Turn the four rings until the left-hand windows show 1 0 2 1.',
      'Read the four runes in the right-hand windows and open the envelope marked with the same runes.'
    ], solution: 'Set 1021 on the wheel. The windows show ᚷᛉᚦᛉ, the runes on envelope 1.' },
    { nudge: 'A postcard from Bjarnarhöfn and Aud’s carved comb.', name: 'Envelope 2', answer: 'BOOK', releases: ['L2', 'L3'], message: 'Two postcards, from Battle Harbour and Baffin Island, and a magnifier: its button is now in the table’s toolbar (key M).', hints: [
      'The two ring-and-dots on the card match the two on the comb.',
      'Line the comb up so its holes sit over the printed dots: handle on the left, teeth over the writing.',
      'Some teeth are broken. Read the first letter you can see on each line they leave open, from top to bottom.'
    ], solution: 'With the comb in place only four lines show: Bjarnarhöfn today, / to follow the / of followers, then claimed land of her / like (the end of “feels like”). Reading the first visible letter of each, top to bottom: B, O, O, K.' },
    { nudge: 'Two postcards, from Battle Harbour and Baffin Island.', name: 'Envelope 3', answer: '1576', releases: ['H2', 'H3', 'HD'], message: 'Three postcards: Staraya Ladoga, Kyiv and Constantinople.', hints: [
      'Read the two new postcards. What do they both say about the sky?',
      'Bring the two skies together. The top edges of the cards matter.',
      'Turn one card upside down and lay it so its top edge meets the other card’s top edge, both picture side up. Look along the join with the magnifier.'
    ], solution: 'Laid top edge to top edge, one card upside down, the cloud fragments across the join read 1576.' },
    { nudge: 'Three postcards: Staraya Ladoga, Kyiv and Constantinople.', name: 'Envelope 4', answer: 'MEAD', releases: ['A2', 'audMap', 'audTicket'], message: 'A postcard from Hvammur, a map of the Island Settlement and a museum ticket.', hints: [
      'Three cards, three words, one drink.',
      'What do you get when honey ferments?',
      'Each card hides its word a different way: read one, count one, look at one.'
    ], solution: 'Staraya Ladoga spells DRINK with the first letter of each of its five sentences. Kyiv’s riddle (sweet but not fruit, gold but not metal, made by thousands, six-sided walls) is HONEY. Constantinople’s picture puzzle (sugar feeding yeast, a bubbling flask) means FERMENTED. A fermented honey drink is MEAD.' },
    { nudge: 'A postcard from Hvammur, a map of the Island Settlement and a museum ticket.', name: 'Envelope 5', answer: '532', releases: ['R1', 'R6', 'RD'], message: 'Three postcards: Châlus, Roumare Forest and Walcheren.', hints: [
      'The Island Settlement map and the Treasure Museum ticket go together: the ticket gives directions, and the Hvammur postcard says what to count on the way.',
      'Start at the northernmost chapel on the map and follow the ticket’s six steps along the roads.',
      'Keep three separate tallies as you go: bridges, fords and gates. On the fifth step, the postcard tells you which road to follow.'
    ], solution: 'Six legs: chapel → chapel (1 bridge), → well (2 fords, 1 bridge), → landing (1 ford, 1 bridge), → standing stone (1 bridge), → village at the crossing, along the forest road (2 gates, 1 bridge), → the wood beyond the ruin (nothing). Totals: 5 bridges, 3 fords, 2 gates: 532.' },
    { nudge: 'Three postcards: Châlus, Roumare Forest and Walcheren.', name: 'Envelope 6', answer: '562', releases: ['LD', 'ticket', 'map'], message: 'A postcard from Brattahlíð, a map of the Western Lands and a museum ticket.', hints: [
      'Look closely at the pictures on three of the postcards. Each message mentions something small in passing.',
      'Count the Viking boats at Walcheren, the wild boars in Roumare Forest and the crossbow bolts at Châlus. Use the magnifier: some hide well. Read Roumare’s message again before you settle on its number.',
      'The Fun Facts on the backs date each place. Put the counts in date order. Liv thinks there were twice as many boars as she saw.'
    ], solution: 'Walcheren 5 boats (before 911), then Roumare 3 boars doubled to 6 (911), then Châlus 2 crossbow bolts (1199): 562.' },
    { nudge: 'A postcard from Brattahlíð, a map of the Western Lands and a museum ticket.', name: 'Envelope 7', answer: '4865', releases: ['A1', 'A3', ...coinIds, 'tally'], message: 'Two postcards, a pouch of coins and a four-wheel tally.', hints: [
      'The chart is not empty. Something is drawn where the card is pointing.',
      'Are you certain which animal that is? Look at its pose and silhouette, not only its location.',
      'It is a wolf. Read W, O, L, F off the index on the back of the museum ticket.'
    ], solution: 'The postcard points to square A6 on the sea chart, where the wolf is drawn. Reading W, O, L, F off the museum ticket’s visitor index gives 4865.' },
    { nudge: 'Two postcards, a pouch of coins and a four-wheel tally.', name: 'Envelope 8', answer: 'SOLE', releases: ['R2', 'rolloMap', 'rouenTicket'], message: 'A postcard from Rouen, a map of the Granted Lands and a museum ticket.', hints: [
      'Your museum ticket has a coin room. Sort the coins into its three groups.',
      'The treasure hunt ended in the wood beyond a ruin. Look at the mark beside it on Aud’s map, then find the same mark on the ticket: only those coins count.',
      'Add up what those coins are worth on the ticket and set the total on the treasure tally.',
      'Turn the whole tally upside down and read the four characters from left to right.'
    ], solution: 'The marked group adds up to 3705, which reads SOLE upside down.' },
    { nudge: 'A postcard from Rouen, a map of the Granted Lands and a museum ticket.', name: 'Envelope 9', answer: '1486', releases: ['R3', 'R4', 'R5', 'ruler'], message: 'Three postcards (Bayeux, Winchester and Battle) and Liv’s ruler.', hints: [
      'Read the Rouen postcard next to the back of the Rouen museum ticket. Some of Liv’s words have a partner on the ticket.',
      'The ticket pairs everyday Saxon words (numbered) with their Norman partners (lettered). A matched pair gives a letter and a number: a square on the Granted Lands map.',
      'Liv mentions fighting, people, poultry and an inn, in that order. For each word, find its square on the map and count the squares to the little drawing for that word.'
    ], solution: 'Fight: 1 square. People (folk): 4. Poultry (hen): 8. Inn: 6. In the postcard’s order the code is 1486.' },
    { nudge: 'Three postcards (Bayeux, Winchester and Battle) and Liv’s ruler.', name: 'Envelope 10', answer: '120', releases: ['H1', 'haraldMap', 'board', 'osloTicket'], message: 'The Oslo postcard, a map of the Varangian Road, a Hnefatafl board with its pieces and a museum ticket.', hints: [
      'The Bayeux, Winchester and Battle postcards each end with a little picture puzzle. Read them as words.',
      'Two of the picture puzzles point to places on the Granted Lands map; the third tells you which scale of the ruler to use.',
      'Measure between those two places on the Granted Lands map, dot to dot, with Liv’s ruler. Use the edge that matches the drawing on the Battle postcard.'
    ], solution: 'Bayeux: cross + bow + lightning bolt = CROSSBOW BOLT, so Châlus. Winchester: tree + tea = TREATY, so Saint-Clair-sur-Epte. Battle: a drawing of a longship, so use the LONGSHIP edge of the ruler (the other edge, SPEAR, is a decoy). Châlus to Saint-Clair-sur-Epte reads 120 on the LONGSHIP edge.' },
    { nudge: 'The Oslo postcard, a map of the Varangian Road, a Hnefatafl board with its pieces and a museum ticket.', name: 'Envelope 11', answer: '2134', releases: ['H4', 'H5', 'ravenCard'], message: 'Two postcards (Hedeby and Sicily) and a card of raven flights.', hints: [
      'The board is eleven columns wide. Count what you can actually see, and think about what the smudge hides.',
      'Something was lying on the ink. It is still in the box, and it is the right shape.',
      'Dark moves first, then the king, four times. The numbered arrows on the back of Harald’s map are the first two dark moves; Liv’s riddle gives the third.',
      'The shield on the museum ticket is also printed on Harald’s map. It marks where the last dark piece goes, and that move frees the way for the king.',
      'The king does not have to run to the top of the column. Try stopping after one square.',
      'F6 → H6 → H7 → K7 → K11, then measure each leg.'
    ], solution: 'Set out the starting position from Liv’s note, with columns I to K taken from the museum ticket. Then play: dark E1 → E6, king F6 → H6; dark H2 → H5, king H6 → H7; dark H10 → H11 (the attacker on the second-highest row steps up to the top row), king H7 → K7; dark K10 → I10 (the shield on Harald’s map is at I10, and moving the piece on K10 frees column K), king K7 → K11. The moves are 2, 1, 3 and 4 squares long: 2134.' },
    { nudge: 'Two postcards (Hedeby and Sicily) and a card of raven flights.', name: 'Envelope 12', answer: '2648', releases: ['H6', 'hopLeif', 'hopRollo', 'hopAud', 'hopHarald', 'flight1', 'flight2', 'flight3'], message: 'The postcard from Patara, the hop tickets for the four journeys and three flight bookings.', hints: [
      'The underlined word on the Sicily postcard matters to the map’s unusual column labels.',
      'Read the columns R, A, V, E, N in that order. On Hedeby’s key, each stem’s left branches select the row; its right branches select the letter.',
      'Use the five decoded letters as perches on the raven’s flights card. Move directly from each letter to the next and read one digit from each flight. Do not add them.'
    ], solution: 'R6 → H, A10 → R, V9 → A, E3 → F, N2 → N: HRAFN. Then H → R = 2, R → A = 6, A → F = 4, F → N = 8: 2648.' },
    // The final riddle (PZ-013): filter the decoys, order each journey from its hop tickets, draw it on its map.
    { nudge: 'The postcard from Patara, the hop tickets for the four journeys and three flight bookings.', name: 'Envelope 13', answer: '1972', releases: ['planeTicket', 'finalLetter', 'medallion'], message: 'A plane ticket, Liv’s last letter and a medallion.', hints: [
      'Liv wrote to retrace only the steps that matter to your family’s history. Only the postcards with her small raven count. Four cards have no raven: set them aside.',
      'Each map shows the stamp of its journey. Put each postcard beside the map with the same stamp. The travel tickets show how Liv got from each stop to the next, so use them to put each journey’s stops in order.',
      'On each map, join the raven stops in that order, skipping any stop without a raven. Each map draws one digit. The flight tickets between the journeys give the order to read the four maps.'
    ], solution: 'Set aside the four postcards with no raven. Match the rest to the maps by their stamps. Chain each journey’s travel tickets to put its stops in order (skip any whose postcard has no raven). On each map, join the raven stops in that order: Leif’s map draws 1, Rollo’s 9, Aud’s 7 and Harald’s 2. The three flight tickets give the order Leif, Rollo, Aud, Harald: 1972.' }
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
  const initial = ['L1', 'notes'];
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
    state.hints = state.hints.map((_, i) => Math.floor(clamp(raw.hints?.[i], 0, 7, 0)));
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
  const TAFL = [...Array(19).fill('dark'), ...Array(6).fill('light'), 'king'];
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
  const PILES = { cards: ['Postcard'], maps: ['Map'], papers: ['Ticket', 'Card', 'Letter', 'Hop tickets'] };
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
    const marks = locks.map((_, i) => i >= state.stage ? '▫️' : state.hints[i] > locks[i].hints.length ? '🔓' : state.hints[i] ? '💡' : '🗝️').join('');
    return `The Raven Inheritance · ${state.stage}/${locks.length} envelopes · ${duration(state.played)} · ${used} hint${used === 1 ? '' : 's'}\n${marks}\nescapepack.ca/play/norse/`;
  }
    /* Aud's comb seats the way the real one does: comb face up, AD message side up, both
     square to each other, and both holes over both printed ring-and-dots (card points from
     Props/Comb). Seated, it travels and turns with the card. */
  const PT = PPI / 72;
  // From assets/comb.json (Props/Comb/build_comb.py); 6 x 4 in AD card since 13 Oct 2026.
  const COMB = { origin: [-16.5, 9.5], holes: [[24, 20], [24, 214]], dots: [[24, 20], [24, 214]] };
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
  /* The cypher wheel (PP-047, Props/CypherWheel/build_cypher_wheel_pdf.py, seed 1021). Four rings carry the
     same 20 symbols: 0-9, a blank (a 3-digit code starts with it) and the nine letters the word codes use.
     Each ring gives every symbol its own rune. Ring I takes the code's first character; the rune windows
     read ring IV to ring I, left to right. Checked against the printed labels in raven2.test.cjs. */
  const WHEEL_SYMBOLS = [...'0123456789', ' ', ...'ABDEKLMOS'];
  const WHEEL_RUNES = [
    { 0: 'ᚲ', 1: 'ᛉ', 2: 'ᛏ', 3: 'ᛟ', 4: 'ᚦ', 5: 'ᚱ', 6: 'ᚠ', 7: 'ᚢ', 8: 'ᛚ', 9: 'ᛈ', ' ': 'ᛇ', A: 'ᛊ', B: 'ᛁ', D: 'ᚹ', E: 'ᛒ', K: 'ᚾ', L: 'ᚺ', M: 'ᚷ', O: 'ᛞ', S: 'ᛖ' },
    { 0: 'ᚦ', 1: 'ᚲ', 2: 'ᛁ', 3: 'ᛊ', 4: 'ᛞ', 5: 'ᛟ', 6: 'ᛉ', 7: 'ᚾ', 8: 'ᛏ', 9: 'ᚹ', ' ': 'ᛖ', A: 'ᚷ', B: 'ᚱ', D: 'ᚢ', E: 'ᛚ', K: 'ᛈ', L: 'ᛒ', M: 'ᚺ', O: 'ᚠ', S: 'ᛇ' },
    { 0: 'ᚷ', 1: 'ᛞ', 2: 'ᛉ', 3: 'ᚹ', 4: 'ᛟ', 5: 'ᚲ', 6: 'ᛏ', 7: 'ᛚ', 8: 'ᚠ', 9: 'ᛈ', ' ': 'ᚺ', A: 'ᛒ', B: 'ᚦ', D: 'ᚱ', E: 'ᛊ', K: 'ᛇ', L: 'ᚾ', M: 'ᛁ', O: 'ᛖ', S: 'ᚢ' },
    { 0: 'ᛁ', 1: 'ᚷ', 2: 'ᛈ', 3: 'ᛊ', 4: 'ᛚ', 5: 'ᚺ', 6: 'ᛒ', 7: 'ᚠ', 8: 'ᚲ', 9: 'ᚹ', ' ': 'ᚾ', A: 'ᛖ', B: 'ᚢ', D: 'ᚱ', E: 'ᛏ', K: 'ᛉ', L: 'ᛇ', M: 'ᛟ', O: 'ᛞ', S: 'ᚦ' }
  ];
  // A code as the four ring settings: the code, blank-padded on the left, one character per ring.
  const ringsOf = code => String(code).toUpperCase().padStart(4, ' ').slice(-4).split('');
  // The four runes the windows show for ring settings (or a code).
  const runesFor = code => { const r = Array.isArray(code) ? code : ringsOf(code); return [3, 2, 1, 0].map(i => WHEEL_RUNES[i][r[i]] || '').join(''); };
  const labels = locks.map(l => runesFor(l.answer));
  // The box holds its envelopes loose: a fixed mixed-up order, so the order of the shelf gives nothing away.
  const BOX_ORDER = [6, 1, 10, 3, 8, 12, 4, 9, 0, 11, 2, 7, 5];
  /* A try at an envelope: the player has set `code` on the wheel and picks one envelope. It opens only if the
     wheel's runes match that envelope's label and it is the next one. A wrong code is remembered (once) in the
     current puzzle's log, unless it is the right code for this puzzle (then the wrong envelope was picked).
     Returns 'open', 'open-done' (already open), 'later' or 'nomatch'. */
  function tryEnvelope(state, code, envelope) {
    const clean = String(code).trim().toUpperCase(), rings = ringsOf(code);
    if (state.stage >= locks.length) return 'open-done';
    if (runesFor(rings) !== labels[envelope]) {
      if (clean !== locks[state.stage].answer && /^[0-9A-Z]{3,4}$/.test(clean)) {
        const log = state.attempts[state.stage], at = log.indexOf(clean);
        if (at >= 0) log.splice(at, 1);
        log.push(clean); if (log.length > MAX_ATTEMPTS) log.shift();
      }
      return 'nomatch';
    }
    if (envelope < state.stage) return 'open-done';
    if (envelope > state.stage) return 'later';
    state.stage++;
    return 'open';
  }
  const api = { WHEEL_SYMBOLS, WHEEL_RUNES, ringsOf, runesFor, labels, BOX_ORDER, tryEnvelope, PPI, table, sizes, items, locks, STORY, MAX_ATTEMPTS, earlierLock, duration, shareText, stack, bringBack, finalRoute, arrival, spotFor, initial, available, fresh, restore, attempt, clamp, deal, arrange, release, unpile, repack, retired, pileMembers, STRIP, footprint, snap, onTable, turnAbout, seatComb, followSeat, combPoints, TAFL, taflSquares, markLines };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LeifGame = api;
})(typeof window === 'undefined' ? globalThis : window);
