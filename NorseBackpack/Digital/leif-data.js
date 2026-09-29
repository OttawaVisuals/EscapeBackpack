/* Player assets reuse the physical edition. Sequence: PC-18, 29 September 2026.
   This friends-only prototype checks answers locally; source is not spoiler-proof. */
(function (root) {
  const postcard = (slug) => ['Front', 'Back'].map(side => `../Web/Postcards/Postcard_${slug}_${side}.webp`);
  const items = {
    L1: { name: "L’Anse aux Meadows", kind: 'Postcard', faces: postcard('L1_LAnse'), w: 440, h: 308, at: [80, 100] },
    tagA: { name: 'Luggage tag · Vinland', kind: 'Luggage tag', crop: [460, 260, 610, 356], w: 320, h: 187, at: [640, 110] },
    tagB: { name: 'Luggage tag · Rouen', kind: 'Luggage tag', crop: [460, 735, 610, 356], w: 320, h: 187, at: [660, 390] },
    ticket: { name: 'Brattahlíð museum ticket', kind: 'Ticket', faces: ['../Props/_Renders/Museum_Ticket_Front.png', '../Props/_Renders/Museum_Ticket_Back.png'], w: 125, h: 344, at: [1090, 120] },
    L2: { name: 'Battle Harbour', kind: 'Postcard', faces: postcard('L2_Battle_Harbour'), w: 440, h: 308, at: [130, 480] },
    L3: { name: 'Baffin Island', kind: 'Postcard', faces: postcard('L3_Baffin_Island'), w: 440, h: 308, at: [700, 690] },
    LD: { name: 'Brattahlíð', kind: 'Postcard', faces: postcard('LD_Brattahlid'), w: 440, h: 308, at: [70, 610] },
    map: { name: 'Leif’s sea chart', kind: 'Map', faces: ['../Props/_Renders/Trail_Map_1_Leif_Print.png'], w: 480, h: 621, at: [740, 220] },
    R2: { name: 'Rouen', kind: 'Postcard', faces: postcard('R2_Rouen'), w: 440, h: 308, at: [110, 210] },
    rolloMap: { name: 'Rollo’s trail map', kind: 'Map', faces: ['../Props/_Renders/Trail_Map_2_Rollo_Print.png'], w: 480, h: 621, at: [710, 240] },
    rouenTicket: { name: 'Rouen museum ticket', kind: 'Ticket', faces: ['../Props/RouenTicket/Rouen_Ticket_Front_300dpi.png', '../Props/RouenTicket/Rouen_Ticket_Back_300dpi.png'], w: 160, h: 350, at: [1180, 120] }
  };
  const locks = [
    { name: 'Main compartment', answer: '1021', releases: ['L2', 'L3'], message: 'Inside are two more postcards from Liv.', hints: [
      'Look at both luggage tags and both sides of the first postcard.',
      'Each tag has a street number. The postcard is from the first stop of Liv’s journey. Which tag matches that place?',
      'Use the Vinland tag’s street number first, followed by the Rouen tag’s street number.',
      'The combination is 1021.'
    ] },
    { name: 'Lower front pocket', answer: '1576', releases: ['LD', 'map'], message: 'A postcard from Greenland and Leif’s sea chart were tucked inside.', hints: [
      'Read the two new postcards. What do they both say about the sky?',
      'Try bringing the two illustrated skies together under the light. You can turn and slide the cards.',
      'Put Battle Harbour above Baffin Island, both picture-side up. Turn Battle Harbour upside down and bring their top edges together. Magnify the meeting edges.',
      'The joined cloud fragments read 1576.'
    ] },
    { name: 'Rollo’s pouch', answer: '3212', releases: ['R2', 'rolloMap', 'rouenTicket'], message: 'Leif’s leg is complete. Liv’s journey continues with Rollo.', hints: [
      'Inspect every detail on the Brattahlíð postcard, including the small print. Keep the sea chart and museum ticket nearby.',
      '“Series F, No. 1” points to a square on the chart. What animal is there?',
      'The animal is a bear. Spell its name using the visitor index on the back of the museum ticket, taking one digit per letter.',
      'B → 3, E → 2, A → 1, R → 2. The combination is 3212.'
    ] }
  ];
  const initial = ['L1', 'tagA', 'tagB', 'ticket'];
  const available = stage => [...initial, ...locks.slice(0, stage).flatMap(lock => lock.releases)];
  const fresh = () => ({ version: 1, stage: 0, pieces: {}, hints: [0, 0, 0], notes: '', light: { top: 'L1', bottom: 'L1', rotation: 0, bottomRotation: 0, topBack: false, bottomBack: false, dx: 110, dy: -60, on: false } });
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
      state.pieces[id] = { x: clamp(p.x, 10, 1400 - items[id].w - 10, items[id].at[0]), y: clamp(p.y, 10, 1050 - items[id].h - 10, items[id].at[1]), rot: [0, 90, 180, 270].includes(p.rot) ? p.rot : 0, back: !!p.back && items[id].faces?.length === 2, stowed: !!p.stowed };
    }
    const l = raw.light;
    if (l && typeof l === 'object') {
      const cards = available(state.stage).filter(id => items[id].kind === 'Postcard');
      for (const key of ['top', 'bottom']) if (cards.includes(l[key])) state.light[key] = l[key];
      for (const key of ['rotation', 'bottomRotation']) state.light[key] = l[key] === 180 ? 180 : 0;
      for (const key of ['on', 'topBack', 'bottomBack']) state.light[key] = !!l[key];
      state.light.dx = clamp(l.dx, -600, 600, 110);
      state.light.dy = clamp(l.dy, -250, 250, -60);
    }
    return state;
  }
  function attempt(state, answer) {
    if (state.stage >= locks.length || String(answer).trim() !== locks[state.stage].answer) return false;
    state.stage++;
    return true;
  }
  const api = { items, locks, initial, available, fresh, restore, attempt, clamp };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LeifGame = api;
})(typeof window === 'undefined' ? globalThis : window);
