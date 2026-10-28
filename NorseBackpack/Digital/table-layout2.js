/* Where every prop of the whole Norse game starts on the digital table, V2 (box, envelopes and
   cypher wheel), at real size. Inches; the game draws PPI table units per inch.
   Sizes of printed props come from raven2-sizes.js (build_raven2_assets.py reads them off the
   print PDFs). Postcards and maps use numbered slots that the game fills in arrival order, never
   by trail or stop, so the layout gives nothing away about the final riddle. The other props are
   shelf-packed into the right-hand column, then a strip along the bottom.
   3D-printed props marked `est` have estimated sizes. */
(function (root) {
  const S = root.RavenSizes || require('./raven2-sizes.js');
  const PPI = 88;
  const table = { w: 64, h: 36.3 };
  // The game's table starts small and grows through these sizes (same shape) as props arrive.
  const sizes = [[27.1, 15.4], [35.7, 20.2], [45.5, 25.8], [54.2, 30.7], [64, 36.3]];
  const mapSlot = n => ({ w: 8.5, h: 11, x: 0.5 + 8.9 * (n - 1), y: 0.5 });
  const cardSlot = n => ({ w: 6, h: 4, x: 0.5 + 6.3 * ((n - 1) % 7), y: 12 + 4.3 * Math.floor((n - 1) / 7) });
  const fixed = {
    board: { w: 5, h: 6.3, est: true },
    tally: { w: 2.46, h: 1.38 },
    comb: { w: 3.993, h: 2.986 },
    medallion: { w: 1.97, h: 1.97 },
    ravenFlights: { w: 4, h: 3 }
  };
  const printed = { notes: 'Notes_Card', audTicket: 'Aud_Ticket_Front', museumTicket: 'Museum_Ticket_Front', rouenTicket: 'Rouen_Ticket_Front',
    hnefataflTicket: 'Hnefatafl_Ticket_Front', flight1: 'Flight_Booking_1', flight2: 'Flight_Booking_2', flight3: 'Flight_Booking_3',
    hopLeif: 'Hop_Tickets_Leif', hopRollo: 'Hop_Tickets_Rollo', hopAud: 'Hop_Tickets_Aud', hopHarald: 'Hop_Tickets_Harald',
    planeTicket: 'Plane_Ticket', finalLetter: 'Final_Letter', ruler: 'Ruler' };
  const sizeOf = {};
  for (const [k, p] of Object.entries(printed)) sizeOf[k] = { w: S[p][0], h: S[p][1] };
  Object.assign(sizeOf, fixed);
  for (let i = 0; i < 12; i++) sizeOf['coin' + (i + 1)] = { w: 1.1, h: 1.1 };
  /* Shelf packing: tallest first, left to right in rows, into the right-hand column (x 45 to the
     table's edge), then into a strip under the postcards (y 29.5 down, x up to 44.8). */
  const GAP = 0.4;
  const regions = [{ x: 45.5, y: 0.5, w: table.w - 46, h: table.h - 1 }, { x: 0.5, y: 29.6, w: 44.3, h: table.h - 30.1 }];
  const props = {};
  const order = Object.keys(sizeOf).sort((a, b) => sizeOf[b].h - sizeOf[a].h || (a < b ? -1 : 1));
  for (const r of regions) { r.rowY = r.y; r.rowH = 0; r.cx = r.x; }
  for (const key of order) {
    const { w, h } = sizeOf[key];
    let done = false;
    for (const r of regions) {
      if (r.cx + w > r.x + r.w + 1e-9) { r.rowY += r.rowH + GAP; r.rowH = 0; r.cx = r.x; }
      if (r.rowY + h > r.y + r.h + 1e-9 || w > r.w) continue;
      props[key] = { ...sizeOf[key], x: Math.round(r.cx * 100) / 100, y: Math.round(r.rowY * 100) / 100 };
      r.cx += w + GAP; r.rowH = Math.max(r.rowH, h); done = true; break;
    }
    if (!done) throw new Error('table-layout2: no room for ' + key);
  }
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
