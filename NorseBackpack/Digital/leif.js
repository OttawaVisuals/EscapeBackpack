'use strict';
(() => {
  const G = window.LeifGame;
  const $ = id => document.getElementById(id);
  const KEY = 'escape-backpack.leif.v1';
  const SNAP = 12; // screen pixels: edges this close pull together while dragging (Alt turns it off)
  let state = G.fresh(), hadSave = false, storageOK = true;
  try { const saved = localStorage.getItem(KEY); if (saved) { state = G.restore(JSON.parse(saved)); hadSave = true; } } catch (_) { storageOK = false; }
  let selected = null, scale = 1, z = 5, toastTimer, viewerId = null;
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
  const faceName = (id, face) => { const n = G.items[id].faces?.length || 1; return n > 2 ? `face ${face + 1} of ${n}` : face ? 'back' : 'front'; };
  function artwork(id, face = 0) {
    const item = G.items[id];
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
    const p = pieceState(id), item = G.items[id], sideways = p.rot % 180 !== 0;
    const extraX = sideways ? (item.h - item.w) / 2 : 0, extraY = sideways ? (item.w - item.h) / 2 : 0;
    const T = G.sizes[state.table];
    p.x = G.clamp(p.x, 12 + extraX, T.w - 12 - item.w - extraX, item.at[0]);
    p.y = G.clamp(p.y, 12 + extraY, T.h - 12 - item.h - extraY, item.at[1]);
  }
  function position(id) {
    const el = elements.get(id), p = pieceState(id); if (!el) return;
    el.style.left = p.x + 'px'; el.style.top = p.y + 'px'; el.style.transform = `rotate(${p.rot}deg)`; el.hidden = p.stowed; refreshLens();
  }
  function select(id, raise = true) {
    selected = id;
    elements.forEach((el, key) => el.classList.toggle('selected', key === id));
    if (id && raise) elements.get(id).style.zIndex = ++z;
    $('selected-name').textContent = id ? G.items[id].name : 'Your table';
    if (id) $('selected-type').textContent = `${G.items[id].kind} · ${faceName(id, pieceState(id).face)}`;
    else $('selected-type').innerHTML = 'Drag to arrange · double-click to inspect · <kbd>M</kbd> magnifier';
    $('stow').disabled = !id;
    document.querySelectorAll('.shelf-item').forEach(el => el.setAttribute('aria-pressed', el.dataset.id === id ? 'true' : 'false'));
  }
  function flip(id) {
    if (!id || !(G.items[id].faces?.length > 1)) return;
    const p = pieceState(id); p.face = (p.face + 1) % G.items[id].faces.length;
    elements.get(id).replaceChildren(artwork(id, p.face)); select(id, false); save();
    if ($('viewer').open) renderViewer();
  }
  function rotate(id) { if (!id) return; const p = pieceState(id); p.rot = (p.rot + 90) % 360; constrain(id); position(id); save(); if ($('viewer').open) renderViewer(); }
  function buildTable() {
    hideTools(); G.deal(state);
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
        const moves = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
        if (moves[e.key]) { e.preventDefault(); const [dx, dy] = moves[e.key], step = e.shiftKey ? 1 : 15; p.x += dx * step; p.y += dy * step; constrain(id); position(id); select(id); save(); }
        if (e.key.toLowerCase() === 'f') { e.preventDefault(); flip(id); }
        if (e.key.toLowerCase() === 'r') { e.preventDefault(); rotate(id); }
        if (e.key === 'Enter') { e.preventDefault(); openViewer(id); }
      });
      let drag = null;
      el.addEventListener('pointerdown', e => { if (e.button !== 0) return; hideTools(); select(id); el.setPointerCapture(e.pointerId); drag = { x: e.clientX, y: e.clientY, px: p.x, py: p.y }; });
      el.addEventListener('pointermove', e => { if (!drag) return; el.classList.add('lifted'); p.x = drag.px + (e.clientX - drag.x) / scale; p.y = drag.py + (e.clientY - drag.y) / scale; if (!e.altKey) G.snap(state, id, SNAP / scale); constrain(id); position(id); });
      const endDrag = () => { el.classList.remove('lifted'); if (drag) { drag = null; save(); } };
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
    $('table').style.width = T.w + 'px'; $('table').style.height = T.h + 'px';
    scale = Math.max(0.05, Math.min((box.clientWidth - pad * 2) / T.w, (box.clientHeight - pad * 2) / T.h));
    $('table').style.transform = `scale(${scale})`; $('table-size').style.width = T.w * scale + 'px'; $('table-size').style.height = T.h * scale + 'px';
    refreshLens();
  }
  function renderProgress() {
    $('progress').replaceChildren();
    G.locks.forEach((lock, i) => {
      const li = document.createElement('li'), number = document.createElement('span'); number.className = 'num'; number.textContent = i < state.stage ? '✓' : i + 1;
      li.className = i < state.stage ? 'done' : i === state.stage ? 'current' : '';
      if (i === state.stage) li.setAttribute('aria-current', 'step'); li.append(number, document.createTextNode(lock.name)); $('progress').append(li);
    });
    const done = state.stage === G.locks.length;
    $('lock-panel').hidden = done; $('complete').hidden = !done;
    const lock = G.locks[Math.min(state.stage, G.locks.length - 1)], digits = lock.answer.length;
    $('chapter').textContent = `0${lock.leg} / ${G.legs[lock.leg].toUpperCase()}`;
    if (!done) {
      $('lock-number').textContent = `Lock ${state.stage + 1} of ${G.locks.length}`; $('lock-name').textContent = lock.name;
      $('combination').maxLength = digits; $('combination').pattern = `[0-9]{${digits}}`; $('combination').placeholder = '·'.repeat(digits);
      $('lock-ask').textContent = `Find a ${digits === 3 ? 'three' : 'four'}-digit combination among Liv’s keepsakes.`;
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
    hideTools(); viewerId = id; select(id); $('viewer').showModal(); renderViewer();
  }
  function renderViewer() {
    if (!viewerId) return;
    const item = G.items[viewerId], p = pieceState(viewerId), sideways = p.rot % 180 !== 0;
    $('viewer-title').textContent = item.name; $('viewer-flip').disabled = !(item.faces?.length > 1);
    const host = $('viewer-scroll'), boxW = sideways ? item.h : item.w, boxH = sideways ? item.w : item.h;
    const fit = Math.max(0.01, Math.min((host.clientWidth - 40) / boxW, (host.clientHeight - 90) / boxH));
    $('viewer-art').style.width = boxW * fit + 'px'; $('viewer-art').style.height = boxH * fit + 'px';
    const art = artwork(viewerId, p.face);
    Object.assign(art.style, { position: 'absolute', width: item.w * fit + 'px', height: item.h * fit + 'px', left: (boxW - item.w) * fit / 2 + 'px', top: (boxH - item.h) * fit / 2 + 'px', transform: `rotate(${p.rot}deg)` });
    $('viewer-art').replaceChildren(art); refreshLens();
  }
  $('stow').onclick = () => { if (!selected) return; pieceState(selected).stowed = true; position(selected); select(null); renderShelf(); save(); };
  $('tidy').onclick = () => { G.arrange(state); buildTable(); save(); toast('Everything is face up and laid out again.'); };
  $('lock-form').onsubmit = e => {
    e.preventDefault(); const lock = G.locks[state.stage]; if (!lock) return;
    if (!G.attempt(state, $('combination').value)) { $('lock-message').textContent = 'The lock stays closed. Try another combination.'; $('lock-message').className = 'error'; $('combination').select(); return; }
    $('lock-message').className = ''; selected = lock.releases[0]; buildTable(); renderProgress(); save(); toast(lock.message);
    if (state.stage === G.locks.length) $('complete').scrollIntoView({ block: 'nearest' });
    else $('combination').focus();
  };
  $('combination').oninput = () => { $('combination').value = $('combination').value.replace(/[^0-9]/g, '').slice(0, $('combination').maxLength); };
  $('hint-next').onclick = () => { if (state.stage >= G.locks.length) return; state.hints[state.stage] = Math.min(4, state.hints[state.stage] + 1); renderHints(); save(); };
  $('notes').value = state.notes; $('notes').oninput = () => { state.notes = $('notes').value; save(); };
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
  const lensSurface = () => $('viewer').open ? $('viewer-art') : $('table');
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
    lensOn = on; document.body.classList.toggle('magnifying', on); if (on) hideTools();
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
    t.setAttribute('aria-label', `${item.name}: actions`);
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
    document.body.classList.add('moving'); elements.get(id).classList.add('lifted');
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
    moving = null; document.body.classList.remove('moving'); elements.get(id)?.classList.remove('lifted'); save();
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

  window.addEventListener('resize', () => { hideTools(); fitTable(); if ($('viewer').open) renderViewer(); });
  buildTable(); renderProgress(); save(); if (!hadSave) $('intro').showModal();
})();
