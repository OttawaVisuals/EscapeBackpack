/* Where every prop of the whole Norse game starts on the digital table, at real size.
   Inches; the game draws PPI table units per inch. Used by leif-data.js (sizes, growth steps),
   Table_Full_Layout.html (design preview) and leif.test.cjs (overlap check).
   Postcards and maps use numbered slots that the game fills in arrival order, never by
   trail or stop, so the layout gives nothing away about the final riddle.
   3D-printed props marked `est` have estimated sizes. */
(function (root) {
  const PPI = 88;
  const table = { w: 52, h: 28 };
  // The game's table starts small and grows through these sizes (same shape) as props arrive.
  const sizes = [[22, 11.85], [29, 15.6], [37, 19.9], [44, 23.7], [52, 28]];
  const mapSlot = n => ({ w: 8.5, h: 11, x: 0.5 + 8.9 * (n - 1), y: 0.5 });
  const cardSlot = n => ({ w: 5, h: 3.5, x: 0.5 + 5.4 * ((n - 1) % 7), y: 12 + 3.9 * Math.floor((n - 1) / 7) });
  const props = {
    journalIconography: { w: 5.83, h: 8.27, x: 38.8, y: 0.5 },
    audTicket: { w: 3, h: 4, x: 38.8, y: 17.84 },
    museumTicket: { w: 2, h: 5.5, x: 42.2, y: 17.84 },
    boardInsert: { w: 4.82, h: 6.12, x: 45.03, y: 0.5 },
    board: { w: 5, h: 6.3, x: 45.03, y: 7.02, est: true },
    hnefataflTicket: { w: 2.6, h: 6.6, x: 45.03, y: 13.72 },
    tagA: { w: 3.54, h: 2.07, x: 48.03, y: 13.72 },
    tagB: { w: 3.54, h: 2.07, x: 48.03, y: 16.19 },
    transition1: { w: 5.4, h: 2.5, x: 5.9, y: 24.2 },
    transition2: { w: 5.4, h: 2.5, x: 11.7, y: 24.2 },
    transition3: { w: 5.4, h: 2.5, x: 17.5, y: 24.2 },
    ravenFlights: { w: 4, h: 3, x: 23.3, y: 24 },
    rouenTicket: { w: 2, h: 3, x: 27.7, y: 24 },
    tally: { w: 2.46, h: 1.38, x: 30.1, y: 24 },
    comb: { w: 2.743, h: 2.611, x: 38.8, y: 25.2 },
    medallion: { w: 1.97, h: 1.97, x: 34, y: 24 },
    ruler: { w: 11.81, h: 0.59, x: 38.8, y: 24.2 }
  };
  for (let i = 0; i < 12; i++) props['coin' + (i + 1)] = { w: 1.1, h: 1.1, x: 36.1 + 1.3 * (i % 2), y: 0.5 + 1.3 * Math.floor(i / 2) };
  // Every start position in the whole game: 4 map slots, 22 postcard slots, the named props.
  const all = () => [
    ...[1, 2, 3, 4].map(n => ['map' + n, mapSlot(n)]),
    ...Array.from({ length: 22 }, (_, i) => ['card' + (i + 1), cardSlot(i + 1)]),
    ...Object.entries(props)
  ];
  const api = { PPI, table, sizes, mapSlot, cardSlot, props, all };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.TableLayout = api;
})(typeof window === 'undefined' ? globalThis : window);
