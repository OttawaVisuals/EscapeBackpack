/* Props for locks 5–10, plus the later items found with locks 1–4.
   Nothing here checks an answer: puzzles show what the player built, and the player reads the result. */
(function (root) {
  'use strict';
  const G = root.HikingGame, NS = 'http://www.w3.org/2000/svg';
  const el = (tag, cls, text) => { const node = document.createElement(tag); if (cls) node.className = cls; if (text !== undefined) node.textContent = text; return node; };
  const svg = (tag, attrs = {}, text) => { const node = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v); if (text !== undefined) node.textContent = text; return node; };
  const image = (src, alt) => { const node = new Image(); node.src = `assets/${src}`; node.alt = alt; node.draggable = false; return node; };
  const button = (text, action, cls) => { const b = el('button', cls, text); b.type = 'button'; b.addEventListener('click', action); return b; };
  const have = (state, id) => G.available(state.stage, state.found).includes(id);
  const dataUri = markup => `url("data:image/svg+xml,${encodeURIComponent(markup)}")`;

  /* ---------- Lego numbers ---------- */
  const digits = { 0: ['111', '101', '101', '101', '111'], 1: ['010', '110', '010', '010', '111'], 3: ['111', '001', '011', '001', '111'], 4: ['101', '101', '111', '001', '001'] };
  const legoColours = { blue0: ['#1f5fa8', '#3f82cc', 0], orange4: ['#d86a1c', '#f08a3c', 4], brown1: ['#6b3f26', '#8d5a3b', 1], red3: ['#b3241f', '#d8423a', 3] };
  function legoDigit(id) {
    const [dark, light, digit] = legoColours[id], s = svg('svg', { viewBox: '0 0 96 160', class: 'lego-digit', role: 'img', 'aria-label': G.items[id].name });
    digits[digit].forEach((row, r) => [...row].forEach((on, c) => {
      if (on !== '1') return;
      const x = 3 + c * 30, y = 6 + r * 30;
      s.append(svg('rect', { x, y, width: 30, height: 30, rx: 2, fill: light, stroke: dark, 'stroke-width': 2 }), svg('circle', { cx: x + 15, cy: y + 15, r: 8, fill: light, stroke: dark, 'stroke-width': 2 }));
    }));
    return s;
  }

  /* ---------- Coloured order stickers (lock 10) ---------- */
  function sticker(numeral, colour) { const s = el('span', 'order-sticker', numeral); s.style.background = colour; return s; }

  /* ---------- Bags of Lego parts and the neighbours workbench (lock 8) ---------- */
  function bag(id) { const b = el('div', 'parts-bag'); b.append(el('span', 'bag-label', G.items[id].bag[0].toUpperCase() + G.items[id].bag.slice(1)), el('span', 'bag-bits')); return b; }
  const hairColour = { grey: '#a9a9a6', blue: '#2d55c8', black: '#26272b', blonde: '#f2d36b', orange: '#e2702a' };
  const outfitColour = { coat: '#f4f4ef', vest: '#ec7a26', ranger: '#78936a', suit: '#e9edf2', chef: '#fbfbf7' };
  const petColour = { frog: '#3e9a48', cat: '#222', bird: '#c9b48c', dog: '#8b8f93', rat: '#4a4a4a' };
  function minifig(fig) {
    const s = svg('svg', { viewBox: '0 0 120 206', class: 'minifig', 'aria-hidden': 'true' });
    s.append(svg('rect', { x: 8, y: 160, width: 104, height: 24, rx: 4, fill: '#222' }));
    if (fig.names) s.append(svg('text', { x: 60, y: 177, 'text-anchor': 'middle', fill: '#fff', 'font-size': 13, 'font-family': 'Segoe UI, sans-serif', 'letter-spacing': 2 }, fig.names));
    s.append(svg('rect', { x: 40, y: 112, width: 40, height: 46, fill: '#3b4a6b' }), svg('line', { x1: 60, y1: 120, x2: 60, y2: 158, stroke: '#2b3550', 'stroke-width': 2 }));
    s.append(svg('path', { d: 'M36 70h48l6 44H30z', fill: fig.jobs ? outfitColour[fig.jobs] : '#d8d6cc', stroke: '#8c8a80', 'stroke-width': 1.5, 'stroke-dasharray': fig.jobs ? '' : '4 3' }));
    if (fig.jobs === 'vest') s.append(svg('rect', { x: 38, y: 92, width: 44, height: 5, fill: '#f6e04a' }));
    if (fig.jobs === 'chef') for (const y of [80, 92, 104]) s.append(svg('circle', { cx: 54, cy: y, r: 2, fill: '#777' }), svg('circle', { cx: 66, cy: y, r: 2, fill: '#777' }));
    if (fig.jobs === 'coat') s.append(svg('path', { d: 'M60 72v40M50 72l10 14 10-14', stroke: '#5b9bb8', 'stroke-width': 3, fill: 'none' }));
    if (fig.jobs === 'suit') s.append(svg('circle', { cx: 52, cy: 84, r: 5, fill: '#c94f3a' }));
    s.append(svg('circle', { cx: 60, cy: 50, r: 21, fill: '#f6cf3a', stroke: '#b8961f', 'stroke-width': 1.5 }));
    const face = fig.faces;
    s.append(svg('circle', { cx: 53, cy: 47, r: 2.4, fill: '#222' }), svg('circle', { cx: 67, cy: 47, r: 2.4, fill: '#222' }));
    s.append(svg('path', { d: face === 'plain' ? 'M50 56q10 9 20 0' : 'M52 57q8 5 16 0', stroke: '#222', 'stroke-width': 2, fill: 'none' }));
    if (face === 'beard') s.append(svg('path', { d: 'M40 52q20 34 40 0q-6 12-20 12t-20-12z', fill: '#9a9a96' }));
    if (face === 'scar') s.append(svg('path', { d: 'M46 39l7 7M48 44l3-3', stroke: '#9b3d2a', 'stroke-width': 2 }));
    if (face === 'mark') s.append(svg('ellipse', { cx: 71, cy: 55, rx: 4, ry: 3, fill: '#a5643f' }));
    if (face === 'stars') s.append(svg('path', { d: 'M70 54l1.5 3 3 .4-2.2 2 .6 3-2.9-1.5-2.9 1.5.6-3-2.2-2 3-.4z', fill: '#2e5fb5' }));
    if (fig.hair) {
      s.append(svg('path', { d: 'M38 46q0-26 22-26t22 26q-6-12-22-12t-22 12z', fill: hairColour[fig.hair] }));
      if (fig.hair === 'black') s.append(svg('path', { d: 'M38 46q-4 30 4 44h-6q-6-20 2-44zM82 46q4 30-4 44h6q6-20-2-44z', fill: hairColour.black }));
      if (fig.hair === 'orange') s.append(svg('circle', { cx: 78, cy: 24, r: 9, fill: hairColour.orange }));
    } else s.append(svg('path', { d: 'M38 46q0-26 22-26t22 26', fill: 'none', stroke: '#8c8a80', 'stroke-dasharray': '4 3' }));
    if (face === 'plain') s.append(svg('rect', { x: 39, y: 33, width: 42, height: 5, rx: 2, fill: '#8a5a32' }));   // the headband is printed on this head
    if (fig.hobbies) s.append(svg('text', { x: 60, y: 200, 'text-anchor': 'middle', 'font-size': 12, fill: '#3d4a3a', 'font-family': 'Segoe UI, sans-serif' }, `holding: ${G.parts.hobbies.options.find(([v]) => v === fig.hobbies)[1].toLowerCase()}`));
    if (fig.pets) s.append(svg('ellipse', { cx: 100, cy: 150, rx: 13, ry: 8, fill: petColour[fig.pets] }), svg('circle', { cx: 110, cy: 143, r: 6, fill: petColour[fig.pets] }));
    return s;
  }
  // 3D figures (lego-minifigs.js), loaded on first use; the drawings above stay as the fallback.
  const legoMinifigs = () => import('./lego-minifigs.js');
  function workbench(state, ctx) {
    const view = el('div', 'figure-workbench'), side = el('aside', 'figure-reference'), main = el('section', 'figure-stands');
    if (have(state, 'notepad')) { side.append(el('p', 'eyebrow', 'YOUR NOTEPAD')); const list = el('div', 'riddle-mini'); G.riddle.forEach((line, i) => list.append(el('p', i ? '' : 'riddle-intro', line))); side.append(list); }
    else side.append(el('p', 'eyebrow', 'LEGO PARTS'), el('p', 'muted', 'Five stands and the bags of parts you have found. Put the parts together however you like.'));
    const bags = G.partOrder.filter(b => have(state, b)), missing = G.partOrder.filter(b => !have(state, b));
    main.append(el('p', 'control-help', bags.length < 6 ? `Bags found: ${bags.length} of 6. More parts may turn up later.` : 'All six bags are here. Choose a part for each stand; a part already on another stand moves over.'));
    const scene = el('div', 'stand-scene lego3d-canvas'), row = el('div', 'stand-row'), selects = [];
    scene.append(el('div', 'lego3d-help', 'Drag a figure to turn it'));
    let model = null;
    state.figures.forEach((fig, i) => {
      const stand = el('div', 'stand'); stand.append(minifig(fig));
      selects[i] = {};
      for (const b of bags) {
        const label = el('label', 'part-pick'), select = el('select'); label.append(el('span', '', G.parts[b].label), select);
        select.append(new Option('—', ''));
        for (const [value, text] of G.parts[b].options) select.append(new Option(text, value, false, fig[b] === value));
        select.addEventListener('change', () => {
          const moved = [];
          state.figures.forEach((other, j) => { if (j !== i && select.value && other[b] === select.value) { delete other[b]; selects[j][b].value = ''; moved.push(j); } });
          if (select.value) fig[b] = select.value; else delete fig[b];
          ctx.save();
          if (model) [i, ...moved].forEach(j => model.update(j)); else ctx.refresh();
        });
        selects[i][b] = select;
        stand.append(label);
      }
      row.append(stand);
    });
    main.append(scene, row);
    if (missing.length) main.append(el('p', 'small-note', `Not found yet: ${missing.map(b => `“${b[0].toUpperCase() + b.slice(1)}”`).join(', ')}.`));
    legoMinifigs().then(m => m.mount(scene, { figures: state.figures })).then(v => { model = v; view.classList.add('has-3d'); }, err => { console.error(err); scene.remove(); });
    view.append(side, main); return view;
  }

  /* ---------- Satellite (locks 4–5) ---------- */
  // Solution pose, in the coordinates of the back of the ISS note (807 × 727).
  const rings = { S: [257, 142], plus: [128, 348], X: [677, 240], I: [434, 645] };
  const tail = [200, 240], tip = [740, 565], centre = [550, 451];
  function shorten([x1, y1], [x2, y2], by) { const l = Math.hypot(x2 - x1, y2 - y1), dx = (x2 - x1) / l * by, dy = (y2 - y1) / l * by; return { x1: x1 + dx, y1: y1 + dy, x2: x2 - dx, y2: y2 - dy }; }
  function satelliteShape() {
    const g = svg('g', { class: 'satellite-shape' }), angle = Math.atan2(tip[1] - tail[1], tip[0] - tail[0]) * 180 / Math.PI;
    const along = t => [tail[0] + (tip[0] - tail[0]) * t, tail[1] + (tip[1] - tail[1]) * t];
    g.append(svg('line', { x1: tail[0], y1: tail[1], x2: tip[0], y2: tip[1], stroke: '#83898e', 'stroke-width': 13, 'stroke-linecap': 'round' }));
    g.append(svg('line', { ...shorten(rings.S, rings.plus, 50), stroke: '#83898e', 'stroke-width': 10 }), svg('line', { ...shorten(rings.X, rings.I, 50), stroke: '#83898e', 'stroke-width': 10 }));
    for (const t of [0.17, 0.33]) { const [x, y] = along(t); g.append(svg('rect', { x: x - 34, y: y - 34, width: 68, height: 68, rx: 4, fill: '#8f8a45', stroke: '#5f5b2c', 'stroke-width': 3, transform: `rotate(${angle} ${x} ${y})` })); }
    const armAngle = Math.atan2(rings.I[1] - rings.X[1], rings.I[0] - rings.X[0]) * 180 / Math.PI;
    for (const d of [-112, 112]) {
      const len = Math.hypot(rings.I[0] - rings.X[0], rings.I[1] - rings.X[1]), ex = (rings.I[0] - rings.X[0]) / len, ey = (rings.I[1] - rings.X[1]) / len, x = centre[0] + ex * d, y = centre[1] + ey * d;
      g.append(svg('rect', { x: x - 50, y: y - 30, width: 100, height: 60, rx: 3, fill: '#24376b', stroke: '#101a38', 'stroke-width': 3, transform: `rotate(${armAngle} ${x} ${y})` }));
      for (let k = -30; k <= 30; k += 20) g.append(svg('line', { x1: x + k, y1: y - 28, x2: x + k, y2: y + 28, stroke: '#5b75b8', 'stroke-width': 2, transform: `rotate(${armAngle} ${x} ${y})` }));
    }
    g.append(svg('rect', { x: centre[0] - 62, y: centre[1] - 44, width: 124, height: 88, rx: 6, fill: '#f2f1ea', stroke: '#2c3440', 'stroke-width': 3, transform: `rotate(${angle} ${centre[0]} ${centre[1]})` }));
    g.append(svg('rect', { x: centre[0] - 40, y: centre[1] - 22, width: 50, height: 44, rx: 3, fill: '#23324f', transform: `rotate(${angle} ${centre[0]} ${centre[1]})` }));
    const [tx, ty] = along(0.9); g.append(svg('circle', { cx: tx, cy: ty, r: 38, fill: '#e1782d', stroke: '#8c4211', 'stroke-width': 3 }), svg('circle', { cx: tx, cy: ty, r: 19, fill: '#f6f3ea' }));
    for (const [x, y] of Object.values(rings)) g.append(svg('circle', { cx: x, cy: y, r: 50, fill: 'none', stroke: '#1e2227', 'stroke-width': 14 }), svg('circle', { cx: x, cy: y, r: 43, fill: 'none', stroke: '#4f565e', 'stroke-width': 2 }));
    return g;
  }
  // The 3D model seen from above (lego-satellite.js), placed so its four magnifier lenses sit on the rings' solution
  // positions: the best rotation, scale and shift over every way of matching lenses to rings. Cached once rendered.
  let topCache;
  function satelliteTop() {
    topCache ??= legoSatellite().then(m => m.topView()).then(({ url, size, lenses }) => {
      const targets = [rings.S, rings.plus, rings.X, rings.I];
      let best = null;
      for (const order of permutations([0, 1, 2, 3])) {
        const w = order.map(i => targets[i]), n = lenses.length;
        const zc = lenses.reduce((a, p) => [a[0] + p[0] / n, a[1] + p[1] / n], [0, 0]), wc = w.reduce((a, p) => [a[0] + p[0] / n, a[1] + p[1] / n], [0, 0]);
        let re = 0, im = 0, den = 0;
        lenses.forEach((p, i) => { const ax = p[0] - zc[0], ay = p[1] - zc[1], bx = w[i][0] - wc[0], by = w[i][1] - wc[1]; re += bx * ax + by * ay; im += by * ax - bx * ay; den += ax * ax + ay * ay; });
        const a = [re / den, im / den], b = [wc[0] - (a[0] * zc[0] - a[1] * zc[1]), wc[1] - (a[1] * zc[0] + a[0] * zc[1])];
        const err = lenses.reduce((e, p, i) => e + Math.hypot(a[0] * p[0] - a[1] * p[1] + b[0] - w[i][0], a[1] * p[0] + a[0] * p[1] + b[1] - w[i][1]), 0);
        if (!best || err < best.err) best = { a, b, err };
      }
      return { url, size, ...best };
    });
    return topCache.then(({ url, size, a, b }) => svg('image', { href: url, width: size, height: size, class: 'satellite-shape satellite-photo', transform: `matrix(${a[0]} ${a[1]} ${-a[1]} ${a[0]} ${b[0]} ${b[1]})` }));
  }
  const permutations = list => list.length < 2 ? [list] : list.flatMap((x, i) => permutations([...list.slice(0, i), ...list.slice(i + 1)]).map(rest => [x, ...rest]));
  // The back of the ISS note: the scribbles from 3. ISS Formula.docx, positioned as on the printed card.
  const scribbles = [
    [45, ['A', 48], ['F', 105], ['T', 160], ['E', 285], ['-', 330], ['3', 380], ['&', 440], ['#', 488], ['8', 560], ['q', 600]],
    [145, ['G', 48], ['(', 150], ['f', 186], ['S', 257], ['Y', 330], ['H', 392], ['h', 420], ['%', 495], ['2', 528], ['!', 635], ['\\', 745]],
    [245, ['@', 48], ['(', 180], ['3', 220], ['+', 312], ['$', 370], ['_', 465], ['R', 510], ['X', 677], ['b', 750]],
    [348, ['<', 40], ['+', 128], ['O', 225], ['W', 330], ['}', 415], ['"', 495], ['#', 540], ['5', 600], ['%', 700], ['1', 765]],
    [545, ['T', 48], ['*', 100], ['@', 195], ['F', 310], ['1', 390], ['O', 440], ['+', 540], ['#', 600], ['?', 728]],
    [645, ['P', 45], ['>', 100], ['…', 165], ['$', 300], ['3', 335], ['I', 434], ['O', 500], ['Q', 570], ['X', 650]]
  ];
  function scribbleCard(state, interactive, ctx) {
    const s = svg('svg', { viewBox: '0 0 807 727', class: 'scribble-card', role: 'img', 'aria-label': 'The back of the ISS note, covered in scribbled letters, numbers and symbols, with two short red marks' });
    s.append(svg('rect', { width: 807, height: 727, fill: '#fffdf7' }));
    for (const [y, ...chars] of scribbles) for (const [ch, x] of chars) s.append(svg('text', { x, y: y + 16, 'text-anchor': 'middle', class: 'scribble' }, ch));
    s.append(svg('path', { d: 'M 214 112 A 52 52 0 0 1 300 112', stroke: '#c0221b', 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round' }));
    s.append(svg('line', { x1: 717, y1: 606, x2: 765, y2: 525, stroke: '#c0221b', 'stroke-width': 8, 'stroke-linecap': 'round' }));
    const sat = state.satellite;
    if (sat.on && sat.built >= G.satellitePages) {
      const g = svg('g', { transform: `translate(${sat.x} ${sat.y}) rotate(${sat.rot} 470 400)`, class: interactive ? 'satellite-overlay movable' : 'satellite-overlay' });
      s.append(g);
      satelliteTop().then(top => g.append(top), () => g.append(satelliteShape()));
      if (interactive) {
        g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button'); g.setAttribute('aria-label', 'Lego satellite. Drag, or use the arrow keys, to move it.');
        g.addEventListener('pointerdown', event => {
          event.preventDefault(); g.setPointerCapture(event.pointerId); const box = s.getBoundingClientRect(), k = 807 / box.width, start = { x: event.clientX, y: event.clientY, sx: sat.x, sy: sat.y };
          const move = e => { sat.x = Math.round(Math.max(-600, Math.min(600, start.sx + (e.clientX - start.x) * k))); sat.y = Math.round(Math.max(-600, Math.min(600, start.sy + (e.clientY - start.y) * k))); g.setAttribute('transform', `translate(${sat.x} ${sat.y}) rotate(${sat.rot} 470 400)`); };
          const end = () => { g.removeEventListener('pointermove', move); g.removeEventListener('pointerup', end); g.removeEventListener('pointercancel', end); ctx.save(); };
          g.addEventListener('pointermove', move); g.addEventListener('pointerup', end); g.addEventListener('pointercancel', end);
        });
        g.addEventListener('keydown', event => {
          const d = event.shiftKey ? 10 : 2, keys = { ArrowLeft: [-d, 0], ArrowRight: [d, 0], ArrowUp: [0, -d], ArrowDown: [0, d] }; if (!keys[event.key]) return;
          event.preventDefault(); sat.x += keys[event.key][0]; sat.y += keys[event.key][1]; g.setAttribute('transform', `translate(${sat.x} ${sat.y}) rotate(${sat.rot} 470 400)`); ctx.save();
        });
      }
    }
    return s;
  }
  function equationFront() {
    const paper = el('article', 'equation-paper');
    paper.append(el('p', '', 'After seeing the ISS at night, I was curious to find out at what altitude it is flying. I remember the equation to calculate it, but I seem to have forgotten the different values for it. I might have scribbled them somewhere.'));
    const formula = el('div', 'formula'); formula.innerHTML = '<i>h</i> = <span class="fraction"><span><i>GM</i></span><span><i>v</i><sup>2</sup></span></span> − <i>R</i><sub>e</sub>'; paper.append(formula);
    const legend = el('ul', 'legend'); for (const t of ['GM = standard gravitational parameter [km³/s²]', 'v = orbital velocity of the ISS [km/s]', 'Re = mean radius of the Earth [km]']) legend.append(el('li', '', t)); paper.append(legend);
    paper.append(el('p', 'equation-correction', 'The equation is slightly wrong and needs a small correction. I just need to build the satellite to get the right answer.'));
    return paper;
  }
  function equationBack(state, ctx) {
    const view = el('div', 'scribble-view'), tools = el('div', 'document-tools'), sat = state.satellite, built = sat.built >= G.satellitePages;
    if (built) {
      tools.append(button(sat.on ? 'Lift the satellite off' : 'Set the satellite on this side', () => { sat.on = !sat.on; ctx.save(); ctx.refresh(); }, sat.on ? '' : 'primary'));
      if (sat.on) {
        const rotate = d => () => { sat.rot = (sat.rot + d + 360) % 360; ctx.save(); ctx.refresh(); };
        tools.append(button('⟲ Turn', rotate(-5)), el('span', 'rotation-readout', `${sat.rot}°`), button('Turn ⟳', rotate(5)), el('span', 'zoom-instruction', 'Drag the satellite to move it · arrow keys nudge it'));
      }
    } else tools.append(el('span', 'zoom-instruction', 'Scribbles, and two little red marks.'));
    const frame = el('div', 'scribble-frame'); frame.append(scribbleCard(state, true, ctx));
    view.append(tools, frame); return view;
  }
  // 3D satellite (lego-satellite.js), loaded on first use; the photo and the page images remain the fallback.
  const legoSatellite = () => import('./lego-satellite.js');
  function satelliteArt(state) {
    if (state.satellite.built < G.satellitePages) { const b = el('div', 'parts-bag satellite-bag'); b.append(el('span', 'bag-label', 'Satellite'), el('span', 'bag-bits')); return b; }
    const wrap = el('div', 'satellite-built lego-thumb'), img = image('satellite-model.jpg', 'The finished Lego satellite');
    wrap.append(img);
    legoSatellite().then(m => m.picture()).then(url => { img.src = url; wrap.classList.add('rendered'); }, err => console.error(err));
    return wrap;
  }
  function buildView(state, ctx) {
    const sat = state.satellite, view = el('div', 'build-view build-3d'), stageBox = el('div', 'build-stage lego3d-canvas'), pic = el('div', 'build-page'), info = el('div', 'build-info');
    const eyebrow = el('p', 'eyebrow'), title = el('h3'), note = el('p', 'muted'), progress = el('div', 'build-progress'), add = button('', () => {}, 'primary');
    stageBox.append(el('div', 'lego3d-help', 'Drag to turn · scroll to zoom'));
    const words = el('div', 'build-words'); words.append(eyebrow, title, note); info.append(words, progress, add);
    view.append(pic, stageBox, info);
    let model = null;
    const show = () => {
      const done = sat.built >= G.satellitePages, page = sat.built + 2;
      progress.style.setProperty('--done', sat.built / G.satellitePages);
      view.classList.toggle('built', done);
      if (done) {
        pic.replaceChildren(); eyebrow.textContent = 'ALL 11 PAGES'; title.textContent = 'Your satellite is built.';
        note.textContent = 'It’s on your table. You can set it on a flat card like the real model.'; add.hidden = true; return;
      }
      pic.replaceChildren(image(`sat-${String(page).padStart(2, '0')}.jpg`, `Satellite instructions, page ${page}`));
      eyebrow.textContent = `PAGE ${page} OF 11`; title.textContent = sat.built ? 'Keep building.' : 'Build the satellite.';
      note.textContent = 'Follow the instructions one page at a time.'; add.textContent = `Add the pieces on page ${page}`;
    };
    add.addEventListener('click', () => {
      if (sat.built >= G.satellitePages) return;
      model?.add(sat.built);
      sat.built++; ctx.save(); ctx.redraw(); show();
    });
    legoSatellite().then(m => m.mount(stageBox, { built: sat.built })).then(v => { model = v; }, err => {
      console.error(err); view.classList.add('no-3d');
      stageBox.replaceChildren(el('p', 'lego-error', 'The 3D model could not load. Check the internet connection; the instructions still work.'));
    });
    show();
    return view;
  }
  function instructionsView() {
    let page = 1; const view = el('div', 'booklet-view'), tools = el('div', 'document-tools'), scroll = el('div', 'document-scroll booklet-scroll'), pic = image('sat-01.jpg', 'Satellite instructions, page 1'), label = el('span', '', '1 / 11');
    const show = () => { pic.src = `assets/sat-${String(page).padStart(2, '0')}.jpg`; pic.alt = `Satellite instructions, page ${page}`; label.textContent = `${page} / 11`; prev.disabled = page === 1; next.disabled = page === 11; };
    const prev = button('← Page', () => { page--; show(); }), next = button('Page →', () => { page++; show(); });
    let zoom = 1; const zoomBy = d => () => { zoom = Math.min(2.5, Math.max(1, zoom + d)); pic.style.width = `${zoom * 100}%`; };
    tools.append(prev, label, next, el('span', 'zoom-instruction', 'Zoom'), button('−', zoomBy(-.5)), button('+', zoomBy(.5)));
    scroll.append(pic); view.append(tools, scroll); show(); return view;
  }

  /* ---------- Square and flat Lego puzzles (lock 7): 3D, loaded on first use (lego-square.js, lego-flat.js) ---------- */
  const lego = { square: () => import('./lego-square.js'), flat: () => import('./lego-flat.js') };
  function legoThumb(id, state) {
    const wrap = el('div', 'lego-thumb'), img = document.createElement('img');
    img.alt = ''; wrap.append(img);
    lego[id]().then(m => m.picture(state.push[id].actions)).then(url => { img.src = url; })
      .catch(() => { wrap.classList.add('failed'); wrap.textContent = G.items[id].name; });
    return wrap;
  }
  function legoView(id, state, ctx) {
    const view = el('div', 'lego-flat-view');
    lego[id]().then(m => m.mount(view, { actions: state.push[id].actions, onChange: actions => { state.push[id].actions = actions; ctx.save(); } }))
      .catch(err => { console.error(err); view.replaceChildren(el('p', 'lego-error', 'The 3D puzzle could not load. Check the internet connection, then close and reopen it.')); });
    return view;
  }

  /* ---------- Cube pieces (lock 7) ---------- */
  const cubeColours = { a: '#c43a2f', b: '#2f6fbf', c: '#3d9a4f', d: '#e0a12c' };
  const cubePicture = dataUri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280"><rect width="280" height="280" fill="#f4f1e6"/><g fill="#e2dccb">' + Array.from({ length: 16 }, (_, i) => `<circle cx="${35 + (i % 4) * 70}" cy="${35 + Math.floor(i / 4) * 70}" r="13"/>`).join('') + '</g><g font-family="Arial Black,Arial,sans-serif" font-weight="900" fill="#1d2a3a" text-anchor="middle"><text x="72" y="222" font-size="205">5</text><text x="140" y="172" font-size="70">+</text><text x="208" y="222" font-size="205">3</text></g></svg>');
  // A cell of a turned piece at local [r, c] shows the picture slice of the same cell in the solved frame, turned with the piece.
  function cubeCell(id, r, c, rot) {
    const cell = el('span', 'cube-cell'), art = el('span', 'cube-art'), local = G.pieceCells(id, 0, 0, rot);
    const [sr, sc] = G.cubePieces[id][local.findIndex(([lr, lc]) => lr === r && lc === c)];
    art.style.backgroundImage = cubePicture; art.style.backgroundPosition = `${sc * 100 / 3}% ${sr * 100 / 3}%`; art.style.transform = `rotate(${rot * 90}deg)`;
    cell.style.borderColor = cubeColours[id]; cell.append(art); return cell;
  }
  function pieceShape(id, rot) {
    const cells = G.pieceCells(id, 0, 0, rot), rows = Math.max(...cells.map(([r]) => r)) + 1, cols = Math.max(...cells.map(([, c]) => c)) + 1, shape = el('span', 'cube-shape');
    shape.style.gridTemplateColumns = `repeat(${cols}, var(--cell, 1fr))`; shape.style.gridTemplateRows = `repeat(${rows}, var(--cell, 1fr))`; shape.style.aspectRatio = `${cols} / ${rows}`;
    for (const [r, c] of cells) { const cell = cubeCell(id, r, c, rot); cell.style.gridRow = r + 1; cell.style.gridColumn = c + 1; shape.append(cell); }
    return shape;
  }
  function cubePile() { const pile = el('div', 'cube-pile'); for (const [id, rot] of [['a', 1], ['b', 0], ['c', 3], ['d', 2]]) { const p = pieceShape(id, rot); p.classList.add(`pile-${id}`); pile.append(p); } return pile; }
  function cubeView(state, ctx) {
    const view = el('div', 'cube-view'), tray = el('div', 'cube-tray'), frame = el('div', 'cube-frame'), status = el('p', 'push-status'); status.setAttribute('role', 'status');
    const turns = { a: 1, b: 0, c: 3, d: 2 }; let chosen = null;
    function draw() {
      tray.replaceChildren(); frame.replaceChildren();
      for (const id of Object.keys(G.cubePieces)) {
        if (state.cube[id]) continue;
        const b = el('button', 'cube-piece' + (chosen === id ? ' chosen' : '')); b.type = 'button'; b.setAttribute('aria-label', `Piece ${'abcd'.indexOf(id) + 1}${chosen === id ? ', picked up' : ''}`);
        b.append(pieceShape(id, turns[id])); b.addEventListener('click', () => { chosen = chosen === id ? null : id; status.textContent = chosen ? 'Click a square in the frame to set the piece’s top-left corner there. Turn it first if you like.' : ''; draw(); }); tray.append(b);
      }
      const filled = {};
      for (const [id, [r, c, rot]] of Object.entries(state.cube)) G.pieceCells(id, r, c, rot).forEach(([cr, cc]) => { filled[cr * 4 + cc] = [id, cr - r, cc - c, rot]; });
      for (let i = 0; i < 16; i++) {
        const r = Math.floor(i / 4), c = i % 4, slot = el('button', 'cube-slot'); slot.type = 'button'; slot.setAttribute('aria-label', `Frame row ${r + 1}, column ${c + 1}${filled[i] ? ', filled' : ''}`);
        if (filled[i]) { const [id, lr, lc, rot] = filled[i]; slot.append(cubeCell(id, lr, lc, rot)); slot.classList.add('filled'); }
        slot.addEventListener('click', () => {
          if (filled[i] && !chosen) { const id = filled[i][0]; turns[id] = state.cube[id][2]; delete state.cube[id]; chosen = id; status.textContent = 'Piece picked up.'; ctx.save(); draw(); return; }
          if (!chosen) { status.textContent = 'Pick a piece first.'; return; }
          const problem = G.placeCube(state, chosen, r, c, turns[chosen]);
          if (problem) { status.textContent = problem; return; }
          status.textContent = Object.keys(state.cube).length === 4 ? 'All four pieces are in the frame.' : 'Piece placed.'; chosen = null; ctx.save(); draw();
        });
        frame.append(slot);
      }
      rotateButton.disabled = !chosen;
    }
    const rotateButton = button('Turn piece ↻', () => { if (chosen) { turns[chosen] = (turns[chosen] + 1) % 4; draw(); } });
    const tools = el('div', 'document-tools'); tools.append(rotateButton, el('span', 'zoom-instruction', 'Pick a piece, turn it, then click the frame · click a placed piece to lift it'));
    const bench = el('div', 'cube-bench'); bench.append(frame, tray); view.append(tools, bench, status); draw(); return view;
  }

  /* ---------- Tile boards: jigsaw (lock 6) and map (lock 9) ---------- */
  const otterFront = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd3ea"/><stop offset="1" stop-color="#e5f3f1"/></linearGradient></defs><rect width="800" height="600" fill="url(#sky)"/><circle cx="660" cy="105" r="58" fill="#f6c843"/><path d="M0 300 L120 170 L230 290 L340 150 L470 300 L590 190 L800 330 V600 H0Z" fill="#6c9a7a"/><path d="M0 340 L90 260 L170 330 L260 250 L360 340 L800 360 V600 H0Z" fill="#4f7d5f"/>' +
    [60, 150, 700, 760].map(x => `<path d="M${x} 380 l-34 70 h68z M${x} 340 l-28 60 h56z" fill="#2f5b3e"/><rect x="${x - 6}" y="450" width="12" height="22" fill="#6b4a2f"/>`).join('') +
    '<path d="M0 430 Q200 400 400 440 T800 430 V600 H0Z" fill="#3e88b8"/><path d="M40 480 q40-12 80 0 M520 470 q40-12 80 0 M260 540 q40-12 80 0 M620 545 q40-12 80 0" stroke="#bfe3f3" stroke-width="6" fill="none" stroke-linecap="round"/>' +
    '<ellipse cx="400" cy="440" rx="150" ry="60" fill="#8a5a36"/><ellipse cx="400" cy="420" rx="120" ry="70" fill="#a26c42"/><ellipse cx="400" cy="440" rx="80" ry="45" fill="#e8c9a0"/><circle cx="400" cy="300" r="92" fill="#a26c42"/><circle cx="322" cy="232" r="24" fill="#8a5a36"/><circle cx="478" cy="232" r="24" fill="#8a5a36"/><ellipse cx="400" cy="330" rx="62" ry="46" fill="#e8c9a0"/><circle cx="365" cy="285" r="11" fill="#222"/><circle cx="435" cy="285" r="11" fill="#222"/><circle cx="369" cy="281" r="3" fill="#fff"/><circle cx="439" cy="281" r="3" fill="#fff"/><ellipse cx="400" cy="318" rx="20" ry="13" fill="#3a2a22"/><path d="M380 345 q20 18 40 0" stroke="#3a2a22" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M350 330 h-50 M352 342 h-46 M450 330 h50 M448 342 h46" stroke="#5a3d28" stroke-width="3"/>' +
    '<path d="M310 220 Q400 120 490 220 Z" fill="#d23c3c"/><rect x="300" y="210" width="200" height="26" rx="13" fill="#f7f4ea"/><circle cx="400" cy="128" r="18" fill="#f7f4ea"/><ellipse cx="320" cy="430" rx="34" ry="22" fill="#8a5a36"/><ellipse cx="480" cy="430" rx="34" ry="22" fill="#8a5a36"/><path d="M455 405 l60 -12 l-10 30 z" fill="#f0a63a"/><circle cx="530" cy="400" r="5" fill="#222"/></svg>';
  const otterBack = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect width="800" height="600" fill="#f5f2ea"/><g font-family="Segoe Print,Comic Sans MS,cursive" font-size="78" fill="#26303a" text-anchor="middle"><text x="400" y="150">Card numbers</text><text x="400" y="330">of Canadian-born</text><text x="400" y="505">players</text></g></svg>';
  function tileBoard(kind, state, ctx, opts = {}) {
    const def = G.boards[kind], list = state[kind], board = el('div', `tile-board ${kind}-board`), flipped = !!opts.flipped;
    board.style.gridTemplateColumns = `repeat(${def.cols}, 1fr)`;
    const front = kind === 'otter' ? dataUri(otterFront) : 'url("assets/map-full.jpg")', back = dataUri(otterBack);
    let chosen = null;
    for (let pos = 0; pos < list.length; pos++) {
      const r = Math.floor(pos / def.cols), c = pos % def.cols;
      // Turned over, the board reads mirrored: the tile at (r, c) shows the back of the tile in (r, cols−1−c).
      const tile = flipped ? list[r * def.cols + (def.cols - 1 - c)] : list[pos], tr = Math.floor(tile / def.cols), tc = tile % def.cols;
      const b = el('button', 'board-tile'); b.type = 'button'; b.dataset.pos = pos;
      b.style.backgroundImage = flipped ? back : front; b.style.backgroundSize = `${def.cols * 100}% ${def.rows * 100}%`;
      b.style.backgroundPosition = `${(flipped ? def.cols - 1 - tc : tc) * 100 / (def.cols - 1)}% ${tr * 100 / (def.rows - 1)}%`;
      b.setAttribute('aria-label', `${kind === 'otter' ? 'Puzzle' : 'Map'} piece in row ${r + 1}, column ${c + 1}`);
      if (flipped || opts.locked) b.disabled = true;
      else b.addEventListener('click', () => {
        if (chosen === null) { chosen = pos; b.classList.add('chosen'); opts.status && (opts.status.textContent = 'Now click the spot to swap it with.'); return; }
        if (chosen !== pos) { [list[chosen], list[pos]] = [list[pos], list[chosen]]; ctx.save(); }
        chosen = null; opts.status && (opts.status.textContent = ''); opts.redraw();
      });
      board.append(b);
    }
    return board;
  }
  function otterView(state, ctx) {
    let flipped = false; const view = el('div', 'board-view'), holder = el('div', 'board-holder'), status = el('p', 'push-status'), tools = el('div', 'document-tools'); status.setAttribute('role', 'status');
    const flip = button('Turn the puzzle over ↻', () => { flipped = !flipped; draw(); });
    const draw = () => { holder.replaceChildren(tileBoard('otter', state, ctx, { flipped, status, redraw: draw })); flip.textContent = flipped ? 'Turn it back over ↻' : 'Turn the puzzle over ↻'; status.textContent = flipped ? 'You are looking at the back. Turn it back over to move pieces.' : ''; };
    tools.append(flip, el('span', 'zoom-instruction', 'Click a piece, then the spot to swap it with'));
    view.append(tools, holder, status); draw(); return view;
  }
  function otterArt() { const box = el('div', 'puzzle-box'); const pic = el('div', 'puzzle-box-art'); pic.style.backgroundImage = dataUri(otterFront); box.append(pic, el('span', '', '12 PIECES')); return box; }
  function mapView(state, ctx) {
    let pen = false, last = null; const view = el('div', 'board-view map-view'), holder = el('div', 'board-holder'), status = el('p', 'push-status'), tools = el('div', 'document-tools'); status.setAttribute('role', 'status');
    const penButton = button('Draw on the map ✎', () => { pen = !pen; last = null; draw(); });
    const undo = button('Undo line', () => { state.mapLines.pop(); ctx.save(); draw(); }), clear = button('Clear lines', () => { state.mapLines = []; ctx.save(); draw(); });
    function draw() {
      const wrap = el('div', 'map-wrap'); wrap.append(tileBoard('map', state, ctx, { locked: pen, status, redraw: draw }));
      const lines = svg('svg', { viewBox: '0 0 1000 1000', preserveAspectRatio: 'none', class: 'map-lines' + (pen ? ' drawing' : '') });
      for (const [x1, y1, x2, y2] of state.mapLines) lines.append(svg('line', { x1, y1, x2, y2 }));
      if (last) lines.append(svg('circle', { cx: last[0], cy: last[1], r: 6, class: 'pen-dot' }));
      if (pen) lines.addEventListener('click', e => {
        const box = lines.getBoundingClientRect(), p = [Math.round((e.clientX - box.left) / box.width * 1000), Math.round((e.clientY - box.top) / box.height * 1000)].map(n => Math.max(0, Math.min(1000, n)));
        if (last && state.mapLines.length < 200) { state.mapLines.push([...last, ...p]); ctx.save(); }
        last = p; draw();
      });
      wrap.append(lines); holder.replaceChildren(wrap);
      penButton.textContent = pen ? 'Stop drawing' : 'Draw on the map ✎'; penButton.classList.toggle('primary', pen);
      undo.disabled = clear.disabled = !state.mapLines.length;
      status.textContent = pen ? (last ? 'Click the next point. Stop drawing to lift the pen.' : 'Click where your line starts.') : '';
    }
    tools.append(penButton, undo, clear, el('span', 'zoom-instruction', 'Swap pieces: click one, then another'));
    view.append(tools, holder, status); draw(); return view;
  }
  function mapArt() { const stack = el('div', 'map-stack'); for (let i = 0; i < 3; i++) { const t = el('span', 'map-piece'); t.style.backgroundImage = 'url("assets/map-full.jpg")'; t.style.backgroundPosition = `${[50, 0, 100][i]}% ${[50, 100, 0][i]}%`; stack.append(t); } return stack; }

  /* ---------- Hockey cards (lock 6) ---------- */
  const cardColours = ['#2a4d8f', '#7a2e3b', '#1f6b5c', '#4c3a7a', '#a5542a'];
  function hockeyCard(card, i, back) {
    const node = el('div', 'hockey-card' + (back ? ' back' : '')); node.style.setProperty('--band', cardColours[i % cardColours.length]);
    if (back) { node.append(el('p', 'card-no', `#${card.number}`), el('p', 'card-name', card.name), el('p', 'card-label', 'BORN'), el('p', 'card-born', card.born), el('p', 'card-label', 'POSITION'), el('p', 'card-born', card.position)); return node; }
    const pic = el('div', 'card-portrait');
    node.append(el('p', 'card-set', 'WOMEN’S HOCKEY · PLAYER CARD'), pic, el('p', 'card-name', card.name), el('p', 'card-no', `#${card.number}`)); return node;
  }
  function cardsView() {
    const view = el('div', 'cards-view'), grid = el('div', 'cards-grid'), turned = new Set();
    view.append(el('p', 'control-help', 'Click a card to turn it over.'));
    const draw = () => { grid.replaceChildren(); G.hockey.forEach((card, i) => { const b = el('button', 'card-button'); b.type = 'button'; b.setAttribute('aria-label', `${card.name}, ${turned.has(i) ? 'back' : 'front'}. Click to turn over.`); b.append(hockeyCard(card, i, turned.has(i))); b.addEventListener('click', () => { turned.has(i) ? turned.delete(i) : turned.add(i); draw(); grid.children[i].focus(); }); grid.append(b); }); };
    view.append(grid); draw(); return view;
  }
  function cardsArt() { const stack = el('div', 'card-stack'); stack.append(hockeyCard(G.hockey[3], 3, false)); return stack; }

  /* ---------- Papers: notepad, agenda, pouch, treasure bag ---------- */
  function notepad(face) {
    const pad = el('article', 'notepad-paper' + (face ? ' pad-back' : ''));
    if (face) { pad.append(el('span', 'pad-brand', 'NOTES'), sticker('I', '#e0761f')); return pad; }
    G.riddle.forEach((line, i) => pad.append(el('p', i ? 'riddle-line' : 'riddle-intro', line))); return pad;
  }
  const schedule = [['6 am', ''], ['7 am', ''], ['8 am', ''], ['9 am', 'Sleep in!'], ['10 am', ''], ['11 am', 'Cook birthday brunch'], ['12 pm', 'Clean up for the party'], ['1 pm', 'Buy birthday cake'], ['2 pm', 'Get birthday hats'], ['3 pm', 'Pick up chairs at the Park Ranger’s house'], ['4 pm', 'Buy gift(s)'], ['5 pm', 'Pick up streamers at Bobby the cat’s house'], ['6 pm', 'Grab ice creams on the way back'], ['7 pm', 'Party Time!'], ['8 pm', ''], ['9 pm', ''], ['10 pm', '']];
  function agenda(face) {
    const page = el('article', 'agenda-paper' + (face ? ' agenda-back' : ''));
    if (face) { page.append(sticker('III', '#c0261f')); return page; }
    const head = el('div', 'agenda-head'); head.append(el('span', '', 'Date: 6 / 3'), el('strong', '', 'DAILY SCHEDULE')); page.append(head);
    const table = el('div', 'agenda-rows'); for (const [time, text] of schedule) { const row = el('div', 'agenda-row'); row.append(el('span', '', time), el('span', 'handwriting', text)); table.append(row); } page.append(table);
    page.append(el('p', 'agenda-notes handwriting', 'Notes: Today is a BIG day! It’s Juno’s birthday! I just need to run some errands.')); return page;
  }
  function pouchArt(state) {
    const p = el('div', 'pouch-art'); p.append(el('span', 'pouch-zip'), el('span', 'pouch-zip two'));
    const locksRow = el('div', 'pouch-locks'); for (let i = 5; i < 9; i++) locksRow.append(el('span', 'mini-lock' + (state.stage > i ? ' open' : ''), String(i + 1))); p.append(locksRow); return p;
  }
  function treasureArt(state) { const t = el('div', 'treasure-art'); t.append(el('span', 'treasure-tie'), el('span', 'mini-lock' + (state.stage >= 10 ? ' open' : ''), '10')); return t; }
  function pocketsView(id, state) {
    const view = el('div', 'pockets-view'), list = el('ul', 'pocket-list');
    view.append(id === 'pouch' ? pouchArt(state) : treasureArt(state));
    const rows = id === 'pouch' ? [5, 6, 7, 8] : [9];
    for (const i of rows) list.append(el('li', state.stage > i ? 'open' : '', `${G.locks[i].name.replace('Pouch · ', '')}: lock ${i + 1}, ${state.stage > i ? 'open' : state.stage === i ? 'your next lock' : 'locked'}`));
    view.append(list, el('p', 'muted', 'Each lock is in your backpack panel. Open them in order.')); return view;
  }

  /* ---------- Shared document view with zoom ---------- */
  function documentView(node, size) {
    const view = el('div', 'document-view'), scroll = el('div', 'document-scroll'), stage = el('div', 'document-stage'), page = el('div', 'document-page');
    page.style.width = `${size.w}px`; page.style.height = `${size.h}px`; page.append(node); stage.append(page); scroll.append(stage);
    let zoom = 1; const tools = el('div', 'document-tools'), label = el('span', '', '100%');
    const apply = value => { zoom = Math.min(3, Math.max(.25, value)); label.textContent = `${Math.round(zoom * 100)}%`; stage.style.width = `${size.w * zoom}px`; stage.style.height = `${size.h * zoom}px`; page.style.transform = `scale(${zoom})`; };
    const fit = () => apply(Math.min(1, (scroll.clientWidth - 42) / size.w, (scroll.clientHeight - 38) / size.h));
    tools.append(el('span', 'zoom-instruction', 'Zoom to inspect · scroll to explore'), button('−', () => apply(zoom - .25)), label, button('+', () => apply(zoom + .25)), button('Fit', fit));
    view.append(tools, scroll); requestAnimationFrame(fit); return view;
  }

  const legoIds = Object.keys(legoColours);
  function art(id, face, state) {
    if (legoIds.includes(id)) { const wrap = el('div', 'lego-number'); wrap.append(legoDigit(id)); return wrap; }
    if (G.items[id].bag) return bag(id);
    if (id === 'flat' || id === 'square') return legoThumb(id, state);
    if (id === 'instructions') { const b = el('div', 'booklet'); b.append(image('sat-01.jpg', 'Cover of the satellite instructions')); return b; }
    if (id === 'equation') { if (!face) return equationFront(); const wrap = el('div', 'equation-paper back'); wrap.append(scribbleCard(state, false)); return wrap; }
    if (id === 'cube') return cubePile();
    if (id === 'pouch') return pouchArt(state);
    if (id === 'treasure') return treasureArt(state);
    if (id === 'satellite') return satelliteArt(state);
    if (id === 'otter') return otterArt();
    if (id === 'cards') return cardsArt();
    if (id === 'notepad') return notepad(face);
    if (id === 'agenda') return agenda(face);
    if (id === 'map') return mapArt();
  }
  function inspect(id, face, state, ctx) {
    if (legoIds.includes(id)) { const view = el('div', 'lego-view'); view.append(legoDigit(id)); return view; }
    if (G.items[id].bag) return workbench(state, ctx);
    if (id === 'flat' || id === 'square') return legoView(id, state, ctx);
    if (id === 'instructions') return instructionsView();
    if (id === 'equation') return face ? equationBack(state, ctx) : documentView(equationFront(), { w: 560, h: 520 });
    if (id === 'cube') return cubeView(state, ctx);
    if (id === 'pouch' || id === 'treasure') return pocketsView(id, state);
    if (id === 'satellite') return buildView(state, ctx);
    if (id === 'otter') return otterView(state, ctx);
    if (id === 'cards') return cardsView();
    if (id === 'notepad') return documentView(notepad(face), { w: 520, h: 760 });
    if (id === 'agenda') return documentView(agenda(face), { w: 480, h: 700 });
    if (id === 'map') return mapView(state, ctx);
  }
  root.HikingLater = { art, inspect, sticker, ids: Object.keys(G.items).filter(id => !['bottle', 'note', 'sheet', 'grandparents', 'newspaper', 'iss', 'periodic', 'calculator'].includes(id)) };
})(window);
