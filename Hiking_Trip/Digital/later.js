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
  // A clear bag with its label; the drawn dots give way to a render of the real parts inside (lego-minifigs.js, DG-H29).
  function bag(id) {
    const name = G.items[id].bag, b = el('div', 'parts-bag'), bits = el('span', 'bag-bits');
    b.append(el('span', 'bag-label', name[0].toUpperCase() + name.slice(1)), bits);
    legoMinifigs().then(m => m.bagPicture(name)).then(url => {
      const img = new Image(); img.src = url; img.alt = ''; img.className = 'bag-render'; img.draggable = false;
      bits.replaceWith(img); b.classList.add('rendered');
    }, () => {});
    return b;
  }
  // 3D parts (lego-minifigs.js), loaded on first use; the lists below work without them.
  const legoMinifigs = () => import('./lego-minifigs.js?v=2');
  const legoData = () => import('./lego-minifigs-data.js?v=2');
  // The parts sit in a grid, one row per bag and one column per neighbour; players swap parts within a row (DG-H35).
  function workbench(state, ctx) {
    const view = el('div', 'figure-workbench'), side = el('aside', 'figure-reference'), main = el('section', 'figure-stands');
    if (have(state, 'notepad')) { side.append(el('p', 'eyebrow', 'YOUR NOTEPAD')); const list = el('div', 'riddle-mini'); G.riddle.forEach((line, i) => list.append(el('p', i ? '' : 'riddle-intro', line))); side.append(list); }
    const bags = G.partOrder.filter(b => have(state, b));
    const help = el('p', 'control-help', bags.length < 6 ? `Bags found: ${bags.length} of 6. More parts may turn up later.` : 'All six bags are here. Drag a part onto another in its row to swap them.');
    const scene = el('div', 'stand-scene lego3d-canvas'), grid = el('div', 'part-grid'), selects = {};
    let model = null, D = null;
    const syncLists = () => { for (const b of bags) state.figures.forEach((fig, i) => { selects[b][i].value = fig[b] || ''; }); };
    const atStart = () => !!D && bags.every(b => state.figures.every((fig, i) => fig[b] === D.ORDER[b][i]));
    const refreshReset = () => { resetButton.disabled = atStart() || !D; };
    grid.append(el('span'), ...state.figures.map((_, i) => el('b', 'part-col', `Column ${i + 1}`)));
    for (const b of bags) {
      grid.append(el('span', 'part-row', G.parts[b].label)); selects[b] = [];
      state.figures.forEach((fig, i) => {
        const select = el('select'); select.setAttribute('aria-label', `${G.parts[b].label}, column ${i + 1}`);
        for (const [value, text] of G.parts[b].options) select.append(new Option(text, value, false, fig[b] === value));
        select.addEventListener('change', () => {
          if (!select.value) return;
          const j = state.figures.findIndex(f => f[b] === select.value);
          if (j >= 0 && j !== i) state.figures[j][b] = fig[b];       // swap with the column that had it
          fig[b] = select.value; ctx.save(); syncLists(); refreshReset(); model?.update();
        });
        selects[b][i] = select; grid.append(select);
      });
    }
    // 3D: drag parts onto each other; the lists stay behind a button for keyboard players.
    const listsButton = button('Use lists instead', () => { const show = grid.hidden; grid.hidden = !show; listsButton.textContent = show ? 'Hide the lists' : 'Use lists instead'; });
    listsButton.hidden = true;
    const resetButton = button('Reset the grid', () => {
      for (const fig of state.figures) for (const b of bags) delete fig[b];
      D.arrange(state.figures, bags); ctx.save(); syncLists(); refreshReset(); model?.update();
    }, 'reset-figures');
    resetButton.disabled = true;
    main.append(help, scene, el('div', 'figure-buttons'), grid); main.querySelector('.figure-buttons').append(listsButton, resetButton);
    const bagLabels = Object.fromEntries(bags.map(b => [b, b[0].toUpperCase() + b.slice(1)]));
    const partNames = Object.fromEntries(bags.map(b => [b, Object.fromEntries(G.parts[b].options)]));
    legoData().then(d => { D = d; d.arrange(state.figures, bags); ctx.save(); syncLists(); refreshReset(); });
    legoMinifigs().then(m => m.mount(scene, { figures: state.figures, bags, labels: bagLabels, names: partNames, onChange: () => { ctx.save(); syncLists(); refreshReset(); } })).then(v => {
      model = v; view.classList.add('has-3d'); grid.hidden = true; listsButton.hidden = false;
    }, err => { console.error(err); scene.remove(); });
    view.classList.toggle('no-side', !side.children.length); view.append(...(side.children.length ? [side] : []), main); return view;
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
    if (state.satellite.built < G.satellitePages) {
      // A clear bag of the real pieces, as for the minifig bags (DG-H29); the drawn dots stay until the render is ready.
      const b = el('div', 'parts-bag satellite-bag'), bits = el('span', 'bag-bits');
      b.append(el('span', 'bag-label', 'Satellite'), bits);
      legoSatellite().then(m => m.bagPicture()).then(url => {
        const img = new Image(); img.src = url; img.alt = ''; img.className = 'bag-render'; img.draggable = false;
        bits.replaceWith(img); b.classList.add('rendered');
      }, () => {});
      return b;
    }
    const wrap = el('div', 'satellite-built lego-thumb'), img = image('satellite-model.jpg', 'The finished Lego satellite');
    wrap.append(img);
    legoSatellite().then(m => m.picture()).then(url => { img.src = url; wrap.classList.add('rendered'); }, err => console.error(err));
    return wrap;
  }
  function buildView(state, ctx) {
    const sat = state.satellite, view = el('div', 'build-view build-3d'), stageBox = el('div', 'build-stage lego3d-canvas'), pic = el('div', 'build-page'), info = el('div', 'build-info');
    const eyebrow = el('p', 'eyebrow'), title = el('h3'), note = el('p', 'muted'), progress = el('div', 'build-progress'), add = button('', () => {}, 'primary');
    const help = el('div', 'lego3d-help', 'Drag to turn · scroll to zoom'); stageBox.append(help);
    // Option: drag the pieces onto their outlines instead of letting the button drop them in. Remembered in this browser.
    const mode = el('label', 'build-mode'), drag = el('input'); drag.type = 'checkbox';
    try { drag.checked = localStorage.getItem('satellite-drag') === '1'; } catch { /* storage blocked: stays off */ }
    mode.append(drag, el('span', '', 'Drag the pieces myself'));
    const words = el('div', 'build-words'); words.append(eyebrow, title, note, mode); info.append(words, progress, add);
    view.append(pic, stageBox, info);
    let model = null;
    const finishPage = () => { sat.built++; ctx.save(); ctx.redraw(); show(); };
    const startDrag = () => {
      if (!model || !drag.checked || sat.built >= G.satellitePages) return;
      help.textContent = 'Drag a piece onto its glowing outline · drag the table to turn · scroll to zoom';
      model.manual.start(sat.built, { onProgress: (n, total) => { note.textContent = n ? `Placed ${n} of ${total}. Keep going.` : `Drag the ${total} piece${total > 1 ? 's' : ''} on the table onto the glowing outlines.`; }, onDone: finishPage });
    };
    const show = () => {
      const done = sat.built >= G.satellitePages, page = sat.built + 2;
      progress.style.setProperty('--done', sat.built / G.satellitePages);
      view.classList.toggle('built', done);
      if (done) {
        pic.replaceChildren(); eyebrow.textContent = 'ALL 11 PAGES'; title.textContent = 'Your satellite is built.';
        note.textContent = 'It’s on your table. You can set it on a flat card like the real model.'; add.hidden = mode.hidden = true; return;
      }
      pic.replaceChildren(image(`sat-${String(page).padStart(2, '0')}.jpg`, `Satellite instructions, page ${page}`));
      eyebrow.textContent = `PAGE ${page} OF 11`; title.textContent = sat.built ? 'Keep building.' : 'Build the satellite.';
      if (drag.checked) { note.textContent = 'Drag the pieces on the table onto the glowing outlines.'; add.textContent = 'Place them for me'; }
      else { note.textContent = 'Follow the instructions one page at a time.'; add.textContent = `Add the pieces on page ${page}`; help.textContent = 'Drag to turn · scroll to zoom'; }
      startDrag();
    };
    add.addEventListener('click', () => {
      if (sat.built >= G.satellitePages) return;
      if (drag.checked && model) { model.manual.solve(); return; }   // drops what is left in place, then onDone moves to the next page
      model?.add(sat.built); finishPage();
    });
    drag.addEventListener('change', () => {
      try { localStorage.setItem('satellite-drag', drag.checked ? '1' : '0'); } catch { /* ignore */ }
      model?.manual.cancel(sat.built); show();
    });
    legoSatellite().then(m => m.mount(stageBox, { built: sat.built })).then(v => { model = v; startDrag(); }, err => {
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

  /* ---------- Cube (lock 7): six pieces in 3D, loaded on first use (lego-cube.js, DG-H31) ---------- */
  const legoCube = () => import('./lego-cube.js');
  function cubeArt(state) {
    const wrap = el('div', 'lego-thumb'), img = document.createElement('img');
    img.alt = ''; img.draggable = false; wrap.append(img);
    legoCube().then(m => m.picture(G, state.cube)).then(url => { img.src = url; })
      .catch(() => { wrap.classList.add('failed'); wrap.textContent = G.items.cube.name; });
    return wrap;
  }
  function cubeView(state, ctx) {
    const view = el('div', 'lego3d-view cube-3d'), canvasBox = el('div', 'lego3d-canvas'), bar = el('div', 'lego3d-bar');
    bar.append(el('p', 'lego3d-status', 'Loading…')); view.append(canvasBox, bar);
    legoCube().then(m => m.mount(canvasBox, { cube: state.cube, G, bar, onChange: () => ctx.save() }))
      .catch(err => { console.error(err); view.replaceChildren(el('p', 'lego-error', 'The 3D puzzle could not load. Check the internet connection, then close and reopen it.')); });
    return view;
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

  // The four numbers in 3D (lego-numbers.js, DG-H30); the drawn digits stay as the fallback.
  const legoIds = Object.keys(legoColours), legoNumbers = () => import('./lego-numbers.js');
  function numberArt(id) {
    const wrap = el('div', 'lego-number'), digit = legoDigit(id); wrap.append(digit);
    legoNumbers().then(m => m.picture(id)).then(url => {
      const img = new Image(); img.src = url; img.alt = G.items[id].name; img.draggable = false; digit.replaceWith(img); wrap.classList.add('rendered');
    }, () => {});
    return wrap;
  }
  function numberView(id) {
    const view = el('div', 'lego-view'), stage = el('div', 'lego-number-stage lego3d-canvas'), digit = legoDigit(id);
    view.append(digit);
    legoNumbers().then(m => { view.replaceChildren(stage); stage.append(el('div', 'lego3d-help', 'Drag to turn · scroll to zoom')); return m.mount(stage, id); })
      .then(() => view.classList.add('rendered'), err => { console.error(err); view.replaceChildren(digit); });
    return view;
  }
  function art(id, face, state) {
    if (legoIds.includes(id)) return numberArt(id);
    if (G.items[id].bag) return bag(id);
    if (id === 'flat' || id === 'square') return legoThumb(id, state);
    if (id === 'instructions') { const b = el('div', 'booklet'); b.append(image('sat-01.jpg', 'Cover of the satellite instructions')); return b; }
    if (id === 'equation') { if (!face) return equationFront(); const wrap = el('div', 'equation-paper back'); wrap.append(scribbleCard(state, false)); return wrap; }
    if (id === 'cube') return cubeArt(state);
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
    if (legoIds.includes(id)) return numberView(id);
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
