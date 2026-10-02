'use strict';
(() => {
  const G = window.LeifGame;
  const $ = id => document.getElementById(id);
  const KEY = 'escape-backpack.leif.v1';
  const SNAP = 12; // screen pixels: edges this close pull together while dragging (Alt turns it off)
  let state = G.fresh(), hadSave = false, storageOK = true;
  try { const saved = localStorage.getItem(KEY); if (saved) { state = G.restore(JSON.parse(saved)); hadSave = true; } } catch (_) { storageOK = false; }
  // Design testing only, on this computer: Leif.html?lock=7 starts a fresh game at lock 7 (past locks still being built).
  const startAt = Number(new URLSearchParams(location.search).get('lock'));
  if (startAt >= 1 && startAt <= G.locks.length + 1 && ['localhost', '127.0.0.1', ''].includes(location.hostname)) { state = G.fresh(); state.stage = Math.floor(startAt) - 1; hadSave = true; history.replaceState(null, '', location.pathname); }
  let selected = null, scale = 1, z = 5, toastTimer, viewerId = null, compareId = '', relaid = false, opening = false, markerOn = false;
  const elements = new Map();
  const available = () => G.available(state.stage);
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); storageOK = true; }
    catch (_) { storageOK = false; }
    $('save-status').textContent = storageOK ? 'Saved on this browser' : 'Browser save unavailable · use Save a copy';
  }
  function toast(message) { $('toast').textContent = message; $('toast').classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => $('toast').classList.remove('show'), 5200); }
  function pieceState(id) {
    if (!state.pieces[id]) state.pieces[id] = { x: G.items[id].at[0], y: G.items[id].at[1], rot: 0, face: 0, stowed: false };
    return state.pieces[id];
  }
  function displayName(id) {
    const name = G.items[id].name, same = available().filter(k => G.items[k].name === name);
    return same.length > 1 ? `${name} ${same.indexOf(id) + 1}` : name;
  }
  const faceName = (id, face) => { const it = G.items[id], n = it.faces?.length || 1; return it.faceNames?.[face] || (n > 2 ? `face ${face + 1} of ${n}` : face ? 'back' : 'front'); };
  function artwork(id, face = 0, width = G.items[id].w) {
    const item = G.items[id];
    if (item.widget === 'tally') return tallyElement(id, width);
    if (item.widget === 'tafl') return taflElement(id, width);
    if (item.marker && !face) return markedMap(id);
    if (item.crop) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', item.crop.join(' ')); svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', item.name);
      const img = document.createElementNS(svg.namespaceURI, 'image');
      img.setAttribute('href', '../Props/_Renders/Luggage_Tag_Inserts_Sheet.png'); img.setAttribute('width', '1530'); img.setAttribute('height', '1980'); svg.append(img); return svg;
    }
    const img = new Image(); img.src = item.faces[Math.min(face, item.faces.length - 1)];
    img.alt = `${item.name} · ${faceName(id, face)}`; img.draggable = false;
    img.addEventListener('error', () => toast(`Could not load ${item.name}. Keep this page with the Norse artwork folders.`), { once: true }); return img;
  }
  function constrain(id) {
    const p = pieceState(id), T = G.sizes[state.table];
    if (!Number.isFinite(p.x) || !Number.isFinite(p.y)) [p.x, p.y] = G.items[id].at;
    const b = G.footprint(id, p);
    p.x += Math.max(0, 12 - b.x) - Math.max(0, b.x + b.w - (T.w - 12));
    p.y += Math.max(0, 12 - b.y) - Math.max(0, b.y + b.h - (T.h - 12));
  }
  function position(id) {
    const el = elements.get(id), p = pieceState(id); if (!el) return;
    el.style.left = p.x + 'px'; el.style.top = p.y + 'px'; el.style.transform = `rotate(${p.rot}deg)`; el.hidden = p.stowed; if (id === 'comb') el.classList.toggle('seated', !!p.seated);
    if (id === 'AD' && state.pieces.comb?.seated) { G.followSeat(state); position('comb'); }
    refreshLens(); if (id === selected) placeTurnHandle();
  }
  function select(id, raise = true) {
    selected = id;
    elements.forEach((el, key) => el.classList.toggle('selected', key === id));
    if (id && raise) { elements.get(id).style.zIndex = ++z; if (id === 'AD' && state.pieces.comb?.seated && elements.get('comb')) elements.get('comb').style.zIndex = ++z; }
    $('selected-name').textContent = id ? displayName(id) : 'Your table';
    if (id) $('selected-type').textContent = `${G.items[id].kind} · ${faceName(id, pieceState(id).face)}` + (G.items[id].freeRotate ? ` · ${(Math.round(pieceState(id).rot * 10) / 10).toFixed(1)}°` : '');
    else $('selected-type').innerHTML = 'Drag to arrange · double-click to inspect · <kbd>M</kbd> magnifier';
    $('stow').disabled = !id;
    document.querySelectorAll('.shelf-item').forEach(el => el.setAttribute('aria-pressed', el.dataset.id === id ? 'true' : 'false'));
    placeTurnHandle();
  }
  function flip(id) {
    if (!id || !(G.items[id].faces?.length > 1)) return;
    const p = pieceState(id); p.face = (p.face + 1) % G.items[id].faces.length; if (id === 'comb') p.seated = false;
    elements.get(id).replaceChildren(artwork(id, p.face)); position(id); trySeat(id); select(id, false); save();
    if ($('viewer').open) renderViewer();
  }
  function rotate(id) { if (!id) return; const p = pieceState(id); p.rot = (p.rot + 90) % 360; if (id === 'comb') p.seated = false; constrain(id); position(id); trySeat(id); select(id, false); save(); if ($('viewer').open) renderViewer(); }
  // Try to settle Aud's comb after the comb or AD has been put down, turned or flipped.
  let combTipShown = false;
  function trySeat(id) {
    if ((id !== 'comb' && id !== 'AD') || !elements.get('comb') || !elements.get('AD')) return;
    const was = !!state.pieces.comb.seated;
    if (G.seatComb(state, Math.max(8, 14 / scale))) { position('comb'); elements.get('comb').style.zIndex = ++z; if (!was && !combTipShown) { combTipShown = true; toast('The comb settles into place.'); } }
  }
  function buildTable() {
    hideTools(); relaid = G.deal(state); if (relaid && !opening) setTimeout(() => toast('There was no room left, so Liv’s keepsakes have been laid out again.'), 900);
    elements.forEach(el => el.remove()); elements.clear();
    for (const id of available()) {
      const item = G.items[id], p = pieceState(id), el = document.createElement('button');
      el.type = 'button'; el.className = 'piece'; el.dataset.id = id;
      el.setAttribute('aria-label', `${item.name}. Select, then Inspect to read. Arrow keys move; F turns over; R rotates.`);
      el.style.width = item.w + 'px'; el.style.height = item.h + 'px';
      el.append(artwork(id, p.face)); $('table').append(el); elements.set(id, el); constrain(id); position(id);
      el.addEventListener('click', () => { select(id); showTools(id); });
      el.addEventListener('pointerenter', e => { if (e.pointerType !== 'touch') hoverTools(id); });
      el.addEventListener('pointerleave', () => { clearTimeout(switchTimer); hideToolsSoon(); });
      el.addEventListener('dblclick', () => openViewer(id));
      el.addEventListener('keydown', e => {
        if (G.items[id].freeRotate && (e.key === '[' || e.key === ']' || e.key === '{' || e.key === '}')) { e.preventDefault(); turn(id, p.rot + ('[{'.includes(e.key) ? -1 : 1) * (e.shiftKey ? 0.1 : 1)); save(); return; }
        const moves = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
        if (moves[e.key]) { e.preventDefault(); const [dx, dy] = moves[e.key], step = e.shiftKey ? 1 : 15; p.x += dx * step; p.y += dy * step; constrain(id); position(id); select(id); save(); }
        if (e.key.toLowerCase() === 'f') { e.preventDefault(); flip(id); }
        if (e.key.toLowerCase() === 'r') { e.preventDefault(); rotate(id); }
        if (e.key === 'Enter') { e.preventDefault(); openViewer(id); }
      });
      let drag = null;
      el.addEventListener('pointerdown', e => { if (e.button !== 0) return; hideTools(); select(id); el.setPointerCapture(e.pointerId); drag = { x: e.clientX, y: e.clientY, px: p.x, py: p.y }; });
      el.addEventListener('pointermove', e => { if (!drag) return; el.classList.add('lifted'); if (id === 'comb') p.seated = false; p.x = drag.px + (e.clientX - drag.x) / scale; p.y = drag.py + (e.clientY - drag.y) / scale; if (!e.altKey) G.snap(state, id, SNAP / scale); constrain(id); position(id); });
      const endDrag = () => { el.classList.remove('lifted'); if (drag) { drag = null; trySeat(id); save(); } };
      el.addEventListener('pointerup', endDrag); el.addEventListener('pointercancel', endDrag); el.addEventListener('lostpointercapture', endDrag);
    }
    renderShelf(); select(selected && available().includes(selected) ? selected : null); fitTable();
  }
  function renderShelf() {
    $('shelf').replaceChildren(); $('item-count').textContent = available().length;
    for (const id of available()) {
      const item = G.items[id], p = pieceState(id), button = document.createElement('button');
      button.className = p.stowed ? 'shelf-item stowed' : 'shelf-item'; button.dataset.id = id; button.setAttribute('aria-pressed', selected === id ? 'true' : 'false'); button.setAttribute('aria-label', `Bring ${item.name} to table`);
      const thumb = document.createElement('div'); thumb.className = 'shelf-thumb'; thumb.append(artwork(id));
      const name = document.createElement('span'); name.textContent = item.name;
      const status = document.createElement('small'); status.textContent = p.stowed ? 'Put away' : 'On table';
      button.append(thumb, name, status); button.addEventListener('click', () => { p.stowed = false; position(id); select(id); renderShelf(); save(); elements.get(id).scrollIntoView({ block: 'nearest', inline: 'nearest' }); }); $('shelf').append(button);
    }
  }
  /* The whole table always fits its area; the magnifier does the zooming. */
  function fitTable() {
    const box = $('table-scroll'), pad = 12, T = G.sizes[state.table];
    placeShelf(box, T, pad);
    $('table').style.width = T.w + 'px'; $('table').style.height = T.h + 'px';
    scale = Math.max(0.05, Math.min((box.clientWidth - pad * 2) / T.w, (box.clientHeight - pad * 2) / T.h));
    $('table').style.transform = `scale(${scale})`; $('table-size').style.width = T.w * scale + 'px'; $('table-size').style.height = T.h * scale + 'px';
    refreshLens(); placeTurnHandle();
  }
  /* The shelf of keepsakes sits under the table or in a column on its left, whichever leaves the
     bigger table (the table is wide, so the column only wins on short windows). */
  const SHELF_COLUMN = 200; let shelfRow = 110;
  function placeShelf(box, T, pad) {
    const body = document.body, left = body.classList.contains('shelf-left');
    if (innerWidth <= 1000) { body.classList.remove('shelf-left'); return; }
    if (!left) shelfRow = document.querySelector('.inventory').offsetHeight;
    const fit = (w, h) => Math.min((w - pad * 2) / T.w, (h - pad * 2) / T.h), w = box.clientWidth, h = box.clientHeight;
    const other = left ? fit(w + SHELF_COLUMN, h - shelfRow) : fit(w - SHELF_COLUMN, h + shelfRow);
    if (other > fit(w, h) * 1.03) body.classList.toggle('shelf-left');
  }
  function renderProgress() {
    // Locks grouped by trail: finished and future trails fold to one line; the current one lists its locks.
    $('progress').replaceChildren();
    const count = document.createElement('li'); count.className = 'count'; count.textContent = `${state.stage} of ${G.locks.length} locks open`; $('progress').append(count);
    const current = G.locks[Math.min(state.stage, G.locks.length - 1)].leg;
    for (const leg of [...new Set(G.locks.map(l => l.leg))]) {
      const idx = G.locks.map((l, i) => l.leg === leg ? i : -1).filter(i => i >= 0), opened = idx.filter(i => i < state.stage).length;
      const group = document.createElement('li'); group.className = 'leg' + (opened === idx.length ? ' done' : leg === current ? ' current' : '');
      const head = document.createElement('div'); head.className = 'leg-head';
      head.innerHTML = `<span class="num">${opened === idx.length ? '✓' : leg}</span><span></span><small>${opened}/${idx.length}</small>`; head.children[1].textContent = G.legs[leg];
      group.append(head);
      if (leg === current && state.stage < G.locks.length) {
        const list = document.createElement('ol');
        for (const i of idx) { const li = document.createElement('li'); li.className = i < state.stage ? 'done' : i === state.stage ? 'current' : ''; if (i === state.stage) li.setAttribute('aria-current', 'step'); li.textContent = `${i < state.stage ? '✓' : i + 1} · ${G.locks[i].name}`; list.append(li); }
        group.append(list);
      }
      $('progress').append(group);
    }
    const done = state.stage === G.locks.length;
    $('lock-panel').hidden = done; $('complete').hidden = !done;
    const lock = G.locks[Math.min(state.stage, G.locks.length - 1)], length = lock.answer?.length || 4, letters = /[A-Z]/.test(lock.answer || '');
    $('chapter').textContent = `0${lock.leg} / ${G.legs[lock.leg].toUpperCase()}`;
    if (!done) {
      $('lock-number').textContent = `Lock ${state.stage + 1} of ${G.locks.length}`; $('lock-name').textContent = lock.name; $('lock-nudge').textContent = lock.nudge || '';
      const box = $('combination'); box.maxLength = length; box.placeholder = '·'.repeat(length);
      box.pattern = letters ? `[A-Za-z]{${length}}` : `[0-9]{${length}}`; box.inputMode = letters ? 'text' : 'numeric'; box.classList.toggle('letters', letters);
      $('lock-ask').textContent = lock.pending ? 'This lock is still being built: its combination is being set. Your progress is saved in this browser, so you can carry on from here when it’s ready.'
        : letters ? `This one is a word lock: find a ${length === 4 ? 'four' : length}-letter word among Liv’s keepsakes.` : `Find a ${length === 3 ? 'three' : 'four'}-digit combination among Liv’s keepsakes.`;
      box.disabled = !!lock.pending; $('lock-form').querySelector('button[type=submit]').disabled = !!lock.pending; $('hint-next').hidden = !!lock.pending;
    }
    $('lock-message').textContent = ''; $('combination').value = ''; renderHints();
  }
  function renderHints() {
    $('hints').replaceChildren(); if (state.stage >= G.locks.length) return;
    const shown = state.hints[state.stage];
    G.locks[state.stage].hints.slice(0, shown).forEach((text, i) => { const p = document.createElement('p'); p.className = 'hint'; p.textContent = `${i === 3 ? 'Solution' : 'Hint ' + (i + 1)} · ${text}`; $('hints').append(p); });
    $('hint-next').textContent = shown === 0 ? 'Need a hint?' : shown === 3 ? 'Reveal the combination' : shown === 4 ? 'All hints shown' : 'Another hint'; $('hint-next').disabled = shown === 4;
  }
  function openViewer(id) {
    hideTools(); viewerId = id; select(id);
    $('viewer-compare').replaceChildren(new Option('nothing', ''), ...available().filter(k => k !== id && !pieceState(k).stowed).map(k => new Option(displayName(k), k)));
    $('viewer-compare').value = available().includes(compareId) && compareId !== id ? compareId : '';
    if (!$('viewer').open) $('viewer').showModal(); renderViewer(); placeTurnHandle();
  }
  // Draw a prop into a close-up box, fitted to slotW × slotH, as it lies on the table.
  function drawInto(box, id, slotW, slotH) {
    const item = G.items[id], p0 = pieceState(id), p = item.freeRotate ? { ...p0, rot: 0 } : p0, sideways = p.rot % 180 !== 0;
    const boxW = sideways ? item.h : item.w, boxH = sideways ? item.w : item.h, fit = Math.max(0.01, Math.min(slotW / boxW, slotH / boxH));
    box.style.width = boxW * fit + 'px'; box.style.height = boxH * fit + 'px';
    // Widgets (tally, board) draw at a fixed size and scale themselves, so they go in a holder.
    const drawn = artwork(id, p.face, item.w * fit), art = item.widget ? document.createElement('div') : drawn;
    if (item.widget) art.append(drawn);
    Object.assign(art.style, { position: 'absolute', width: item.w * fit + 'px', height: item.h * fit + 'px', left: (boxW - item.w) * fit / 2 + 'px', top: (boxH - item.h) * fit / 2 + 'px', transform: `rotate(${p.rot}deg)` });
    box.replaceChildren(art);
  }
  function renderViewer() {
    if (!viewerId) return;
    const item = G.items[viewerId], side = compareId && compareId !== viewerId && available().includes(compareId) ? compareId : '';
    $('viewer-title').textContent = item.name; $('viewer-flip').disabled = !(item.faces?.length > 1);
    const markable = item.marker && !pieceState(viewerId).face; if (!markable) markerOn = false;
    $('viewer-marker').hidden = !markable; $('viewer-marker').setAttribute('aria-pressed', String(markerOn)); $('viewer-undo').hidden = $('viewer-wipe').hidden = !markerOn;
    $('viewer-scroll').classList.toggle('marking', markerOn);
    const host = $('viewer-scroll'), w = host.clientWidth - 40, h = host.clientHeight - 90;
    $('viewer-side').hidden = !side; host.classList.toggle('comparing', !!side);
    drawInto($('viewer-art'), viewerId, side ? (w - 24) / 2 : w, h);
    if (side) drawInto($('viewer-side'), side, (w - 24) / 2, h); else $('viewer-side').replaceChildren();
    refreshLens();
  }
  $('stow').onclick = () => { if (!selected) return; pieceState(selected).stowed = true; position(selected); select(null); renderShelf(); save(); };
  $('tidy').onclick = () => { G.arrange(state); buildTable(); save(); toast('Everything is face up and laid out again.'); };
  $('lock-form').onsubmit = e => {
    e.preventDefault(); const lock = G.locks[state.stage]; if (!lock) return;
    if (!G.attempt(state, $('combination').value)) { $('lock-message').textContent = 'The lock stays closed. Try another combination.'; $('lock-message').className = 'error'; $('combination').select(); return; }
    $('lock-message').className = ''; selected = lock.releases[0]; opening = true; buildTable(); opening = false; renderProgress(); save(); showOpened(lock);
  };
  $('combination').oninput = () => { const box = $('combination'); box.value = (box.classList.contains('letters') ? box.value.replace(/[^a-z]/gi, '').toUpperCase() : box.value.replace(/[^0-9]/g, '')).slice(0, box.maxLength); };
  $('hint-next').onclick = () => { if (state.stage >= G.locks.length) return; state.hints[state.stage] = Math.min(4, state.hints[state.stage] + 1); renderHints(); save(); };
  $('notes').value = state.notes; $('notes').oninput = () => { state.notes = $('notes').value; save(); };
  $('viewer-compare').onchange = () => { compareId = $('viewer-compare').value; renderViewer(); };
  // Double-click the side prop to swap places, so Flip and Rotate act on it.
  $('viewer-side').title = 'Double-click to swap it with the main view';
  $('viewer-side').addEventListener('dblclick', () => { if (!compareId) return; const main = viewerId; openViewer(compareId); compareId = main; $('viewer-compare').value = main; renderViewer(); });
  $('viewer-flip').onclick = () => flip(viewerId); $('viewer-rotate').onclick = () => rotate(viewerId);
  $('help').onclick = () => $('intro').showModal(); $('begin').onclick = () => { $('intro').close(); select('L1'); save(); openViewer('L1'); };
  document.querySelectorAll('[data-close]').forEach(button => button.onclick = () => button.closest('dialog').close());
  $('review-table').onclick = () => $('table-scroll').scrollIntoView({ block: 'center' });
  $('restart').onclick = () => $('restart-dialog').showModal();
  $('restart-confirm').onclick = () => { state = G.fresh(); selected = null; $('notes').value = ''; $('restart-dialog').close(); buildTable(); renderProgress(); save(); $('intro').showModal(); };
  function openSave(mode) {
    const exporting = mode === 'export';
    $('save-title').textContent = exporting ? 'Keep a copy' : 'Load a saved game';
    $('save-instructions').textContent = exporting ? 'Download a file, or select and copy this text somewhere safe. Either can restore your progress.' : 'Paste your saved game text below, or choose a saved file. Loading replaces this playtest’s current progress.';
    $('save-text').value = exporting ? JSON.stringify(state, null, 2) : '';
    $('save-text').readOnly = exporting; $('save-result').textContent = '';
    $('download-save').hidden = !exporting; $('select-save').hidden = !exporting;
    $('choose-save-file').hidden = exporting; $('load-save-text').hidden = exporting;
    $('save-dialog').showModal();
  }
  $('export-save').onclick = () => openSave('export');
  $('import-save').onclick = () => openSave('import');
  $('select-save').onclick = () => { $('save-text').focus(); $('save-text').select(); };
  $('download-save').onclick = () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' }));
    const a = document.createElement('a'); a.href = url; a.download = 'leifs-trail-save.json'; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    $('save-result').textContent = 'Download requested. If your browser does not save a file, use Select all text and copy it.';
  };
  function loadSavedText(text) {
    try {
      if (text.length > 100000) throw new Error('Too large');
      const raw = JSON.parse(text); if (raw.version !== 1 || !Number.isInteger(raw.stage) || raw.stage < 0 || raw.stage > G.locks.length) throw new Error('Invalid save');
      state = G.restore(raw); selected = null; $('notes').value = state.notes; buildTable(); renderProgress(); save(); $('save-dialog').close(); toast('Your saved game is loaded.');
    } catch (_) { $('save-result').textContent = 'That is not a valid Leif’s trail save. Your current game was kept.'; }
  }
  $('load-save-text').onclick = () => loadSavedText($('save-text').value);
  $('choose-save-file').onclick = () => $('save-file').click();
  $('save-file').onchange = async () => {
    const file = $('save-file').files[0]; if (!file) return;
    try {
      if (file.size > 100000) throw new Error('Too large');
      loadSavedText(await file.text());
    } catch (_) { $('save-result').textContent = 'Could not read that save file. Your game was kept.'; }
    $('save-file').value = '';
  };
  /* Magnifying glass: a round lens that follows the pointer over the table or the close-up.
     It shows a live copy of that surface, scaled up around the point under the pointer. */
  let lensOn = false, lensPower = 3, lensAt = null;
  const lensEl = document.createElement('div'), lensContent = document.createElement('div');
  lensEl.id = 'lens'; lensEl.setAttribute('aria-hidden', 'true'); lensEl.hidden = true;
  lensContent.className = 'lens-content'; lensEl.append(lensContent); document.body.append(lensEl);
  const lensSurface = () => !$('viewer').open ? $('table') : lensAt?.target?.closest?.('#viewer-side') && !$('viewer-side').hidden ? $('viewer-side') : $('viewer-art');
  const artSignature = el => [...el.querySelectorAll('img,image')].map(img => img.getAttribute('src') || img.getAttribute('href')).join('|');
  function refreshLens() {
    if (!lensOn) return;
    const surface = lensSurface(); let copy = lensContent.firstElementChild;
    if (!copy || copy.dataset.from !== surface.id || copy.dataset.art !== artSignature(surface) || copy.children.length !== surface.children.length) {
      copy = surface.cloneNode(true); copy.removeAttribute('id'); copy.classList.add('lens-copy');
      copy.dataset.from = surface.id; copy.dataset.art = artSignature(surface); lensContent.replaceChildren(copy);
    } else [...surface.children].forEach((child, i) => { copy.children[i].style.cssText = child.style.cssText; copy.children[i].className = child.className; copy.children[i].hidden = child.hidden; });
    copy.style.cssText = surface.style.cssText; copy.style.transform = 'none';
    copy.style.width = surface.offsetWidth + 'px'; copy.style.height = surface.offsetHeight + 'px';
    placeLens();
  }
  function placeLens() {
    if (!lensOn || !lensAt) return;
    const host = $('viewer').open ? $('viewer') : document.body;
    if (lensEl.parentNode !== host) host.append(lensEl);
    const surface = lensSurface(), r = surface.getBoundingClientRect(), { x, y } = lensAt;
    const outside = x < r.left || x > r.right || y < r.top || y > r.bottom || !lensAt.target?.closest?.('#table-scroll,#viewer-scroll');
    if (!surface.offsetWidth || outside) { lensEl.hidden = true; return; }
    lensEl.hidden = false;
    const size = lensEl.offsetWidth, onScreen = r.width / surface.offsetWidth, k = onScreen * lensPower;
    const lx = (x - r.left) / onScreen, ly = (y - r.top) / onScreen;
    lensEl.style.left = x - size / 2 + 'px'; lensEl.style.top = y - size / 2 + 'px';
    lensContent.style.transform = `translate(${size / 2 - lx * k}px,${size / 2 - ly * k}px) scale(${k})`;
  }
  function setLens(on) {
    lensOn = on; document.body.classList.toggle('magnifying', on); if (on) { hideTools(); if (markerOn) { markerOn = false; renderViewer(); } }
    for (const id of ['magnify', 'viewer-magnify']) $(id).setAttribute('aria-pressed', String(on));
    if (on) refreshLens(); else { lensEl.hidden = true; lensContent.replaceChildren(); }
  }
  document.addEventListener('pointermove', e => { if (!lensOn) return; lensAt = { x: e.clientX, y: e.clientY, target: e.target }; placeLens(); });
  for (const id of ['table-scroll', 'viewer-scroll']) {
    $(id).addEventListener('wheel', e => {
      if (!lensOn || lensEl.hidden) return; e.preventDefault();
      lensPower = G.clamp(lensPower * (e.deltaY < 0 ? 1.15 : 1 / 1.15), 1.5, 10, 3); placeLens();
    }, { passive: false });
    $(id).addEventListener('pointerleave', () => { lensEl.hidden = true; });
  }
  $('magnify').onclick = $('viewer-magnify').onclick = () => setLens(!lensOn);
  document.addEventListener('keydown', e => {
    if (e.target.closest?.('input,textarea,select') || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key.toLowerCase() === 'm') { e.preventDefault(); setLens(!lensOn); }
    if (e.key === 'Escape' && lensOn && !document.querySelector('dialog[open]')) setLens(false);
  });
  $('viewer').addEventListener('close', () => { lensContent.replaceChildren(); document.body.append(lensEl); lensEl.hidden = true; refreshLens(); });

  /* Full screen: the table and the backpack only. Where the browser refuses real
     full screen, the page-filling layout still applies. */
  async function setExpanded(on) {
    document.body.classList.toggle('expanded', on);
    $('expand').setAttribute('aria-pressed', String(on)); $('expand').textContent = on ? 'Exit full screen' : 'Full screen';
    fitTable();
    try {
      if (on && !document.fullscreenElement) await document.documentElement.requestFullscreen();
      if (!on && document.fullscreenElement) await document.exitFullscreen();
    } catch (_) { /* Not allowed here; keep the CSS layout. */ }
    fitTable();
  }
  $('expand').onclick = () => setExpanded(!document.body.classList.contains('expanded'));
  document.addEventListener('fullscreenchange', () => { if (!document.fullscreenElement && document.body.classList.contains('expanded')) setExpanded(false); });
  /* Refit whenever the table's area changes size: window resize, full screen, panel changes. */
  new ResizeObserver(fitTable).observe($('table-scroll'));
  /* Prop tools: a small bar over the prop under the pointer (or the one last tapped)
     with Zoom, Rotate, Flip and Move. */
  let toolsFor = null, toolsTimer = null, switchTimer = null, moving = null, swallowClick = false;
  /* Hovering a prop shows its bar at once, unless another prop's bar is open: then it
     switches only if the pointer rests on the new prop, so crossing an overlapping
     prop on the way up to the bar does not steal it. A click switches at once. */
  function hoverTools(id) {
    clearTimeout(switchTimer);
    if (!toolsFor || toolsFor === id || $('prop-tools').hidden) { showTools(id); return; }
    clearTimeout(toolsTimer); switchTimer = setTimeout(() => showTools(id), 400);
  }
  function showTools(id) {
    if (lensOn || moving || document.querySelector('dialog[open]') || !elements.get(id) || pieceState(id).stowed) return;
    clearTimeout(toolsTimer); clearTimeout(switchTimer); toolsFor = id;
    const t = $('prop-tools'), item = G.items[id];
    t.querySelector('[data-tool="flip"]').disabled = !(item.faces?.length > 1);
    $('tools-name').textContent = displayName(id); t.setAttribute('aria-label', `${displayName(id)}: actions`);
    t.hidden = false; placeTools();
  }
  function placeTools() {
    if (!toolsFor) return;
    const t = $('prop-tools'), r = elements.get(toolsFor).getBoundingClientRect(), box = $('table-scroll').getBoundingClientRect();
    const w = t.offsetWidth, h = t.offsetHeight;
    const x = Math.min(box.right - w - 4, Math.max(box.left + 4, r.left + r.width / 2 - w / 2));
    let y = r.top - h - 6;
    if (y < box.top + 4) y = Math.min(r.bottom + 6, box.bottom - h - 4);
    t.style.left = x + 'px'; t.style.top = y + 'px';
  }
  function hideTools() { clearTimeout(toolsTimer); clearTimeout(switchTimer); toolsFor = null; $('prop-tools').hidden = true; }
  function hideToolsSoon() { clearTimeout(toolsTimer); toolsTimer = setTimeout(hideTools, 300); }
  $('prop-tools').addEventListener('pointerenter', () => { clearTimeout(toolsTimer); clearTimeout(switchTimer); });
  $('prop-tools').addEventListener('pointerleave', hideToolsSoon);
  $('prop-tools').addEventListener('click', e => {
    const tool = e.target.closest('[data-tool]')?.dataset.tool, id = toolsFor;
    if (!tool || !id) return;
    if (tool === 'zoom') openViewer(id);
    if (tool === 'rotate') { rotate(id); placeTools(); }
    if (tool === 'flip') { flip(id); placeTools(); }
  });

  /* Move: press Move and drag, or click Move and the prop follows the pointer until the
     next click. Escape puts it back where it was. */
  const tablePoint = e => { const r = $('table').getBoundingClientRect(); return [(e.clientX - r.left) / scale, (e.clientY - r.top) / scale]; };
  $('prop-tools').querySelector('[data-tool="move"]').addEventListener('pointerdown', e => {
    if (e.button !== 0 || !toolsFor) return;
    e.preventDefault();
    const id = toolsFor, p = pieceState(id), [tx, ty] = tablePoint(e);
    hideTools(); select(id);
    moving = { id, dx: tx - p.x, dy: ty - p.y, from: [p.x, p.y], sx: e.clientX, sy: e.clientY, dragged: false };
    if (id === 'comb') p.seated = false;
    document.body.classList.add('moving'); elements.get(id).classList.add('lifted'); placeTurnHandle();
  });
  document.addEventListener('pointermove', e => {
    if (!moving) return;
    const p = pieceState(moving.id), [tx, ty] = tablePoint(e);
    p.x = tx - moving.dx; p.y = ty - moving.dy; if (!e.altKey) G.snap(state, moving.id, SNAP / scale); constrain(moving.id); position(moving.id);
    if (Math.hypot(e.clientX - moving.sx, e.clientY - moving.sy) > 5) moving.dragged = true;
  });
  function endMove(cancel) {
    if (!moving) return;
    const { id, from } = moving, p = pieceState(id);
    if (cancel) { [p.x, p.y] = from; constrain(id); position(id); }
    moving = null; document.body.classList.remove('moving'); elements.get(id)?.classList.remove('lifted'); trySeat(id); placeTurnHandle(); save();
    if (elements.get(id)?.matches(':hover')) showTools(id);
  }
  document.addEventListener('pointerup', () => { if (moving?.dragged) endMove(); });
  document.addEventListener('pointerdown', e => { if (moving) { e.preventDefault(); e.stopPropagation(); endMove(); swallowClick = true; } }, true);
  document.addEventListener('click', e => { if (swallowClick) { swallowClick = false; e.preventDefault(); e.stopPropagation(); } }, true);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && moving) { e.preventDefault(); endMove(true); } });
  $('viewer').addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key.toLowerCase() === 'r') { e.preventDefault(); rotate(viewerId); }
    if (e.key.toLowerCase() === 'f') { e.preventDefault(); flip(viewerId); }
  });
  // Move from the close-up: back to the table carrying the prop, centred on the pointer.
  $('viewer-move').onclick = e => {
    const id = viewerId, p = pieceState(id), item = G.items[id];
    $('viewer').close(); p.stowed = false; select(id);
    moving = { id, dx: item.w / 2, dy: item.h / 2, from: [p.x, p.y], sx: e.clientX, sy: e.clientY, dragged: false };
    document.body.classList.add('moving'); elements.get(id).classList.add('lifted');
    const [tx, ty] = tablePoint(e); p.x = tx - moving.dx; p.y = ty - moving.dy; constrain(id); position(id);
    toast('Click where it goes. Esc puts it back.');
  };

  /* Turn handle: a round knob at the far end of a freely turning prop (the ruler) while it is
     selected. Dragging it turns the prop about its pivot (the ruler's 0 mark); Shift snaps to 15°. */
  const turnHandle = $('turn-handle');
  function turn(id, rot) { const p = pieceState(id); G.turnAbout(id, p, rot, pivotUnits(id)); constrain(id); position(id); select(id, false); }
  const pivotUnits = id => { const it = G.items[id]; return [it.pivot[0] * it.w, it.pivot[1] * it.h]; };
  const toScreen = ([tx, ty]) => { const r = $('table').getBoundingClientRect(); return [r.left + tx * scale, r.top + ty * scale]; };
  function placeTurnHandle() {
    const id = selected, it = id && G.items[id];
    if (!it?.freeRotate || pieceState(id).stowed || moving || document.querySelector('dialog[open]')) { turnHandle.hidden = true; return; }
    const [x, y] = toScreen(G.onTable(id, pieceState(id), [it.handle[0] * it.w, it.handle[1] * it.h]));
    turnHandle.hidden = false; turnHandle.style.left = x + 'px'; turnHandle.style.top = y + 'px';
  }
  let turning = null, turnTipShown = false;
  turnHandle.addEventListener('pointerdown', e => {
    if (e.button !== 0 || !selected) return;
    e.preventDefault(); e.stopPropagation(); try { turnHandle.setPointerCapture(e.pointerId); } catch (_) { /* pointer already gone */ } hideTools();
    const [px, py] = toScreen(G.onTable(selected, pieceState(selected), pivotUnits(selected)));
    turning = { id: selected, px, py, from: pieceState(selected).rot, start: Math.atan2(e.clientY - py, e.clientX - px) * 180 / Math.PI };
    elements.get(selected).classList.add('lifted');
  });
  turnHandle.addEventListener('pointermove', e => {
    if (!turning) return;
    let rot = turning.from + Math.atan2(e.clientY - turning.py, e.clientX - turning.px) * 180 / Math.PI - turning.start;
    if (e.shiftKey) rot = Math.round(rot / 15) * 15;
    turn(turning.id, rot);
  });
  const endTurn = () => { if (!turning) return; elements.get(turning.id)?.classList.remove('lifted'); turning = null; save(); };
  turnHandle.addEventListener('pointerup', endTurn); turnHandle.addEventListener('pointercancel', endTurn); turnHandle.addEventListener('lostpointercapture', endTurn);
  turnHandle.addEventListener('keydown', e => { if (selected && (e.key === '[' || e.key === ']')) { e.preventDefault(); turn(selected, pieceState(selected).rot + (e.key === '[' ? -1 : 1) * (e.shiftKey ? 0.1 : 1)); save(); } });
  const showTurnTip = () => { if (!turnTipShown && G.items[selected]?.freeRotate) { turnTipShown = true; toast('Drag the round handle to turn the ruler around its 0 mark. Shift: 15° steps. [ and ]: one degree.'); } };
  document.addEventListener('click', e => { if (e.target.closest?.('.piece')) showTurnTip(); });
  $('viewer').addEventListener('close', () => { placeTurnHandle(); for (const id of [viewerId, compareId]) if (id && (G.items[id]?.widget || G.items[id]?.marker) && elements.get(id)) elements.get(id).replaceChildren(artwork(id, pieceState(id).face)); });
  $('table').addEventListener('transitionend', e => { if (e.target === $('table')) placeTurnHandle(); }); // after the zoom animation settles

  /* The treasure tally: four ten-sided wheels with seven-segment digits (PR-24), drawn in
     3D like the prototype. Drag a wheel up or down, or scroll over it, to turn it. */
  const SEGMENTS = ['abcdef', 'bc', 'abged', 'abgcd', 'fgbc', 'afgcd', 'afgedc', 'abc', 'abcdefg', 'abcdfg'];
  function segs(v) {
    const w = 3.4, h = 5.6, t = 0.7;
    const R = { a: [-w / 2, -h / 2, w, t], b: [w / 2 - t, -h / 2, t, h / 2], c: [w / 2 - t, 0, t, h / 2], d: [-w / 2, h / 2 - t, w, t], e: [-w / 2, 0, t, h / 2], f: [-w / 2, -h / 2, t, h / 2], g: [-w / 2, -t / 2, w, t] };
    return [...SEGMENTS[v]].map(s => `<rect x="${R[s][0]}" y="${R[s][1]}" width="${R[s][2]}" height="${R[s][3]}"/>`).join('');
  }
  function setWheel(ring, a, settle) {
    const prism = ring.querySelector('.prism'); prism.classList.toggle('settle', !!settle); prism.style.transform = `rotateX(${a}deg)`; ring.dataset.a = a;
    ring.querySelectorAll('.shade').forEach((s, k) => { const t = (a + 36 * k) * Math.PI / 180; s.style.opacity = Math.min(0.85, 1.3 * (1 - Math.cos(t)) + (Math.sin(t) < 0 ? 0.06 : 0)).toFixed(3); });
  }
  function tallyElement(id, width) {
    const p = pieceState(id), wrap = document.createElement('div');
    if (!Array.isArray(p.wheels)) p.wheels = [0, 0, 0, 0];
    wrap.className = 'tally'; wrap.style.transform = `scale(${width / 500})`;
    let html = '<div class="shadow"></div><div class="row"><div class="cap"></div>';
    for (let i = 0; i < 4; i++) {
      html += `<div class="ring" data-i="${i}" title="Drag up or down, or scroll, to turn"><div class="prism">`;
      for (let k = 0; k < 10; k++) html += `<div class="facet" style="transform: rotateX(${36 * k}deg) translateZ(91.44px)"><svg viewBox="-4.625 -3.71 9.25 7.42"><g transform="translate(-0.25 0)">${segs((10 - k) % 10)}</g></svg><div class="shade"></div></div>`;
      html += '</div></div>';
    }
    wrap.innerHTML = html + '<div class="cap"></div></div>';
    wrap.querySelectorAll('.ring').forEach((ring, i) => {
      setWheel(ring, p.wheels[i] * 36);
      const settle = () => { const digit = ((Math.round(Number(ring.dataset.a) / 36) % 10) + 10) % 10; p.wheels[i] = digit; setWheel(ring, digit * 36, true); refreshLens(); save(); if (wrap.closest('#viewer')) refreshPiece(id); };
      let turnDrag = null;
      ring.addEventListener('pointerdown', e => {
        if (e.button !== 0) return; e.stopPropagation(); select(id); hideTools();
        try { ring.setPointerCapture(e.pointerId); } catch (_) { /* pointer already gone */ }
        turnDrag = { x: e.clientX, y: e.clientY, a: Number(ring.dataset.a), step: Math.max(4, ring.getBoundingClientRect().height / 4) };
      });
      ring.addEventListener('pointermove', e => {
        if (!turnDrag) return;
        const t = pieceState(id).rot * Math.PI / 180, along = -(e.clientX - turnDrag.x) * Math.sin(t) + (e.clientY - turnDrag.y) * Math.cos(t);
        setWheel(ring, turnDrag.a - along / turnDrag.step * 36);
      });
      const end = () => { if (turnDrag) { turnDrag = null; settle(); } };
      ring.addEventListener('pointerup', end); ring.addEventListener('pointercancel', end); ring.addEventListener('lostpointercapture', end);
      ring.addEventListener('wheel', e => { if (lensOn) return; e.preventDefault(); e.stopPropagation(); setWheel(ring, Number(ring.dataset.a) + (e.deltaY < 0 ? 36 : -36)); settle(); }, { passive: false });
    });
    return wrap;
  }

  /* Hnefatafl board (PR-08, PZ-01): 11 × 11 squares, columns A–K and rows 1–11 as on Liv's
     sheet, corners and throne marked, with a tray of 16 dark pieces, 6 light pieces and the
     king below. Drag a piece onto a square; drag it off the board to put it back in the tray.
     No rules are enforced, as with the real board. */
  const TAFL_M = 18, TAFL_TRAY = 452;
  const COLS = 'ABCDEFGHIJK';
  function taflElement(id, width) {
    const it = G.items[id], p = pieceState(id), cell = (it.w - 2 * TAFL_M) / 11;
    if (!Array.isArray(p.tafl)) p.tafl = G.taflSquares();
    const wrap = document.createElement('div'); wrap.className = 'tafl';
    Object.assign(wrap.style, { width: it.w + 'px', height: it.h + 'px', transform: `scale(${width / it.w})` });
    const corner = (c, r) => (c === 0 || c === 10) && (r === 0 || r === 10);
    let svg = `<svg class="tafl-grid" viewBox="0 0 ${it.w} ${it.w}" style="width:${it.w}px;height:${it.w}px">`; // inline size: prop SVGs are otherwise stretched to fill
    for (let r = 0; r < 11; r++) for (let c = 0; c < 11; c++) {
      const x = TAFL_M + c * cell, y = TAFL_M + r * cell, special = corner(c, r) || (c === 5 && r === 5);
      svg += `<rect x="${x}" y="${y}" width="${cell}" height="${cell}" class="${special ? 'special' : ''}"/>`;
      if (special) svg += `<path d="M${x + cell / 2} ${y + cell * 0.2} L${x + cell * 0.8} ${y + cell / 2} L${x + cell / 2} ${y + cell * 0.8} L${x + cell * 0.2} ${y + cell / 2} Z" class="mark"/>`;
    }
    for (let c = 0; c < 11; c++) svg += `<text x="${TAFL_M + (c + 0.5) * cell}" y="${TAFL_M - 5}">${COLS[c]}</text>`;
    for (let r = 0; r < 11; r++) svg += `<text x="${TAFL_M / 2}" y="${TAFL_M + (r + 0.5) * cell + 3}">${11 - r}</text>`;
    wrap.innerHTML = svg + '</svg><div class="tafl-tray"></div><button type="button" class="tafl-clear">Clear the board</button>';
    const at = sq => [TAFL_M + (COLS.indexOf(sq[0]) + 0.5) * cell, TAFL_M + (11 - Number(sq.slice(1)) + 0.5) * cell];
    const trayAt = i => [16 + (i % 13) * 32 + 14, TAFL_TRAY + 8 + Math.floor(i / 13) * 34 + 14];
    const tokens = G.TAFL.map((kind, i) => {
      const t = document.createElement('div'); t.className = `tafl-piece ${kind}`; t.dataset.i = i; wrap.append(t); return t;
    });
    const place = () => tokens.forEach((t, i) => { const [x, y] = p.tafl[i] ? at(p.tafl[i]) : trayAt(i); t.style.left = x + 'px'; t.style.top = y + 'px'; t.classList.toggle('on-board', !!p.tafl[i]); });
    place();
    // Screen movement → board units, whatever the board's turn and zoom.
    const toLocal = (dx, dy) => {
      const rot = pieceState(id).rot, a = -rot * Math.PI / 180, r = wrap.getBoundingClientRect();
      const s = r.width / (rot % 180 ? it.h : it.w);
      return [(dx * Math.cos(a) - dy * Math.sin(a)) / s, (dx * Math.sin(a) + dy * Math.cos(a)) / s];
    };
    tokens.forEach((t, i) => {
      let drag = null;
      t.addEventListener('pointerdown', e => {
        if (e.button !== 0) return; e.stopPropagation(); e.preventDefault(); select(id); hideTools();
        try { t.setPointerCapture(e.pointerId); } catch (_) { /* pointer already gone */ }
        drag = { x: e.clientX, y: e.clientY, from: (p.tafl[i] ? at(p.tafl[i]) : trayAt(i)) }; t.classList.add('lifted');
      });
      t.addEventListener('pointermove', e => {
        if (!drag) return; const [lx, ly] = toLocal(e.clientX - drag.x, e.clientY - drag.y);
        t.style.left = drag.from[0] + lx + 'px'; t.style.top = drag.from[1] + ly + 'px';
      });
      const drop = e => {
        if (!drag) return;
        const [lx, ly] = toLocal(e.clientX - drag.x, e.clientY - drag.y), x = drag.from[0] + lx, y = drag.from[1] + ly;
        const c = Math.floor((x - TAFL_M) / cell), r = Math.floor((y - TAFL_M) / cell);
        drag = null; t.classList.remove('lifted');
        if (c >= 0 && c < 11 && r >= 0 && r < 11) { const sq = COLS[c] + (11 - r); if (!p.tafl.some((s, k) => s === sq && k !== i)) p.tafl[i] = sq; }
        else if (y > TAFL_M + 11 * cell) p.tafl[i] = null;
        place(); refreshLens(); save(); if (wrap.closest('#viewer')) refreshPiece(id);
      };
      t.addEventListener('pointerup', drop); t.addEventListener('pointercancel', e => { drag && (drag = null, t.classList.remove('lifted'), place()); });
    });
    const clear = wrap.querySelector('.tafl-clear');
    clear.addEventListener('pointerdown', e => e.stopPropagation());
    clear.addEventListener('click', e => { e.stopPropagation(); p.tafl = G.taflSquares(); place(); refreshLens(); save(); if (wrap.closest('#viewer')) refreshPiece(id); });
    return wrap;
  }

  /* Lock open: a pop-up names what arrived and what to look at next; the new props glow
     for a few seconds once it closes. */
  function showOpened(lock) {
    const n = G.locks.indexOf(lock) + 1, next = G.locks[state.stage];
    $('opened-eyebrow').textContent = `Lock ${n} open`;
    $('opened-title').textContent = lock.name;
    $('opened-what').textContent = lock.message + (relaid ? ' There was no room left, so everything has been laid out again.' : '');
    $('opened-next').textContent = !next ? 'That was the last lock. Liv’s note is waiting beside the backpack.'
      : next.pending ? 'The next lock is still being built. Your progress is saved here.'
      : next.leg !== lock.leg ? `${G.legs[next.leg]} starts here. ${next.nudge || ''}` : (next.nudge || '');
    $('opened').showModal(); $('opened-go').focus();
  }
  $('opened-go').onclick = () => $('opened').close();
  $('opened').addEventListener('close', () => {
    const lock = G.locks[state.stage - 1]; if (!lock) return;
    const glow = lock.releases.map(id => elements.get(id)).filter(Boolean);
    glow.forEach(el => el.classList.add('arrived')); setTimeout(() => glow.forEach(el => el.classList.remove('arrived')), 4500);
    if (state.stage === G.locks.length) $('complete').scrollIntoView({ block: 'nearest' }); else $('combination').focus();
  });

  /* Wet-erase marker (PZ-06): in a map's close-up, drag to draw a straight line. Lines are
     stored as fractions of the map, so they show at any size and on the table too. */
  const MARK_WIDTH = 0.06 * 88; // about 1.5 mm, in table units
  function markedMap(id) {
    const it = G.items[id], p = pieceState(id), wrap = document.createElement('div');
    wrap.className = 'marked';
    const img = new Image(); img.src = it.faces[0]; img.alt = `${it.name} · front`; img.draggable = false;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', `0 0 ${it.w} ${it.h}`); svg.setAttribute('preserveAspectRatio', 'none'); svg.classList.add('marks');
    svg.innerHTML = (p.marks || []).map(([a, b, c, d]) => `<line x1="${a * it.w}" y1="${b * it.h}" x2="${c * it.w}" y2="${d * it.h}" stroke-width="${MARK_WIDTH}"/>`).join('');
    wrap.append(img, svg); return wrap;
  }
  // Pointer position as a fraction of the main close-up prop, whatever its turn.
  function mapFraction(e) {
    const it = G.items[viewerId], p = pieceState(viewerId), box = $('viewer-art').getBoundingClientRect(), art = $('viewer-art').firstElementChild;
    const s = parseFloat(art.style.width) / it.w, a = -p.rot * Math.PI / 180, dx = e.clientX - (box.left + box.width / 2), dy = e.clientY - (box.top + box.height / 2);
    const lx = (dx * Math.cos(a) - dy * Math.sin(a)) / s + it.w / 2, ly = (dx * Math.sin(a) + dy * Math.cos(a)) / s + it.h / 2;
    return [Math.min(1, Math.max(0, lx / it.w)), Math.min(1, Math.max(0, ly / it.h))];
  }
  let drawing = null;
  // Keep the table copy in step with work done in the close-up.
  const refreshPiece = id => { if (elements.get(id)) elements.get(id).replaceChildren(artwork(id, pieceState(id).face)); };
  $('viewer-art').addEventListener('pointerdown', e => {
    if (!markerOn || e.button !== 0) return; e.preventDefault();
    try { $('viewer-art').setPointerCapture(e.pointerId); } catch (_) { /* pointer already gone */ }
    const it = G.items[viewerId], from = mapFraction(e), svg = $('viewer-art').querySelector('svg.marks'), line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('stroke-width', MARK_WIDTH); line.classList.add('drawing'); svg.append(line);
    drawing = { from, line, it };
    const set = to => { line.setAttribute('x1', from[0] * it.w); line.setAttribute('y1', from[1] * it.h); line.setAttribute('x2', to[0] * it.w); line.setAttribute('y2', to[1] * it.h); };
    set(from); drawing.set = set;
  });
  $('viewer-art').addEventListener('pointermove', e => { if (drawing) drawing.set(mapFraction(e)); });
  const endLine = e => {
    if (!drawing) return; const { from, line } = drawing, to = mapFraction(e); drawing = null; line.remove();
    if (Math.hypot(to[0] - from[0], to[1] - from[1]) > 0.004) { const p = pieceState(viewerId); p.marks = G.markLines([...(p.marks || []), [...from, ...to]]); save(); refreshPiece(viewerId); }
    renderViewer();
  };
  $('viewer-art').addEventListener('pointerup', endLine); $('viewer-art').addEventListener('pointercancel', () => { if (drawing) { drawing.line.remove(); drawing = null; } });
  $('viewer-marker').onclick = () => { markerOn = !markerOn; if (markerOn && lensOn) setLens(false); renderViewer(); };
  $('viewer-undo').onclick = () => { const p = pieceState(viewerId); p.marks = (p.marks || []).slice(0, -1); save(); refreshPiece(viewerId); renderViewer(); };
  $('viewer-wipe').onclick = () => { const p = pieceState(viewerId); if (!(p.marks || []).length) return; p.marks = []; save(); refreshPiece(viewerId); renderViewer(); toast('The map is wiped clean.'); };
  $('viewer').addEventListener('close', () => { markerOn = false; });

  window.addEventListener('resize', () => { hideTools(); fitTable(); if ($('viewer').open) renderViewer(); });
  buildTable(); renderProgress(); save(); if (!hadSave) $('intro').showModal();
})();
