'use strict';
(() => {
  const G = window.LeifGame;
  const $ = id => document.getElementById(id);
  const KEY = 'escape-backpack.leif.v1';
  let state = G.fresh(), hadSave = false, storageOK = true;
  try { const saved = localStorage.getItem(KEY); if (saved) { state = G.restore(JSON.parse(saved)); hadSave = true; } } catch (_) { storageOK = false; }
  let selected = null, scale = 1, z = 5, toastTimer, viewerId = null, lightScale = 1;
  const elements = new Map();
  const available = () => G.available(state.stage);
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); storageOK = true; }
    catch (_) { storageOK = false; }
    $('save-status').textContent = storageOK ? 'Saved on this browser' : 'Browser save unavailable · use Save a copy';
  }
  function toast(message) { $('toast').textContent = message; $('toast').classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => $('toast').classList.remove('show'), 5200); }
  function pieceState(id) {
    if (!state.pieces[id]) state.pieces[id] = { x: G.items[id].at[0], y: G.items[id].at[1], rot: 0, back: false, stowed: false };
    return state.pieces[id];
  }
  function artwork(id, back = false) {
    const item = G.items[id];
    if (item.crop) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', item.crop.join(' ')); svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', item.name);
      const img = document.createElementNS(svg.namespaceURI, 'image');
      img.setAttribute('href', '../Props/_Renders/Luggage_Tag_Inserts_Sheet.png'); img.setAttribute('width', '1530'); img.setAttribute('height', '1980'); svg.append(img); return svg;
    }
    const img = new Image(); img.src = item.faces[back && item.faces.length > 1 ? 1 : 0];
    img.alt = `${item.name} · ${back ? 'back' : 'front'}`; img.draggable = false;
    img.addEventListener('error', () => toast(`Could not load ${item.name}. Keep this page with the Norse artwork folders.`), { once: true }); return img;
  }
  function constrain(id) {
    const p = pieceState(id), item = G.items[id], sideways = p.rot % 180 !== 0;
    const extraX = sideways ? (item.h - item.w) / 2 : 0, extraY = sideways ? (item.w - item.h) / 2 : 0;
    p.x = G.clamp(p.x, 12 + extraX, 1388 - item.w - extraX, item.at[0]);
    p.y = G.clamp(p.y, 12 + extraY, 1038 - item.h - extraY, item.at[1]);
  }
  function position(id) {
    const el = elements.get(id), p = pieceState(id); if (!el) return;
    el.style.left = p.x + 'px'; el.style.top = p.y + 'px'; el.style.transform = `rotate(${p.rot}deg)`; el.hidden = p.stowed;
  }
  function select(id, raise = true) {
    selected = id;
    elements.forEach((el, key) => el.classList.toggle('selected', key === id));
    if (id && raise) elements.get(id).style.zIndex = ++z;
    $('selected-name').textContent = id ? G.items[id].name : 'Your table';
    $('selected-type').textContent = id ? `${G.items[id].kind} · ${pieceState(id).back ? 'back' : 'front'}` : 'Select a keepsake to inspect it';
    for (const name of ['inspect', 'rotate', 'stow']) $(name).disabled = !id;
    $('flip').disabled = !id || !(G.items[id].faces?.length > 1);
    document.querySelectorAll('.shelf-item').forEach(el => el.setAttribute('aria-pressed', el.dataset.id === id ? 'true' : 'false'));
  }
  function flip(id) {
    if (!id || !(G.items[id].faces?.length > 1)) return;
    const p = pieceState(id); p.back = !p.back;
    elements.get(id).replaceChildren(artwork(id, p.back)); select(id, false); save();
    if ($('viewer').open) renderViewer();
  }
  function rotate(id) { if (!id) return; const p = pieceState(id); p.rot = (p.rot + 90) % 360; constrain(id); position(id); save(); }
  function buildTable() {
    elements.forEach(el => el.remove()); elements.clear();
    for (const id of available()) {
      const item = G.items[id], p = pieceState(id), el = document.createElement('button');
      el.type = 'button'; el.className = 'piece'; el.dataset.id = id;
      el.setAttribute('aria-label', `${item.name}. Select, then Inspect to read. Arrow keys move; F turns over; R rotates.`);
      el.style.width = item.w + 'px'; el.style.height = item.h + 'px';
      el.append(artwork(id, p.back)); $('table').append(el); elements.set(id, el); constrain(id); position(id);
      el.addEventListener('click', () => select(id));
      el.addEventListener('dblclick', () => openViewer(id));
      el.addEventListener('keydown', e => {
        const moves = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
        if (moves[e.key]) { e.preventDefault(); const [dx, dy] = moves[e.key], step = e.shiftKey ? 1 : 15; p.x += dx * step; p.y += dy * step; constrain(id); position(id); select(id); save(); }
        if (e.key.toLowerCase() === 'f') { e.preventDefault(); flip(id); }
        if (e.key.toLowerCase() === 'r') { e.preventDefault(); rotate(id); }
        if (e.key === 'Enter') { e.preventDefault(); openViewer(id); }
      });
      let drag = null;
      el.addEventListener('pointerdown', e => { if (e.button !== 0) return; select(id); el.setPointerCapture(e.pointerId); drag = { x: e.clientX, y: e.clientY, px: p.x, py: p.y }; });
      el.addEventListener('pointermove', e => { if (!drag) return; p.x = drag.px + (e.clientX - drag.x) / scale; p.y = drag.py + (e.clientY - drag.y) / scale; constrain(id); position(id); });
      const endDrag = () => { if (drag) { drag = null; save(); } };
      el.addEventListener('pointerup', endDrag); el.addEventListener('pointercancel', endDrag); el.addEventListener('lostpointercapture', endDrag);
    }
    renderShelf(); select(selected && available().includes(selected) ? selected : null); fitTable();
  }
  function renderShelf() {
    $('shelf').replaceChildren(); $('item-count').textContent = available().length;
    for (const id of available()) {
      const item = G.items[id], p = pieceState(id), button = document.createElement('button');
      button.className = 'shelf-item'; button.dataset.id = id; button.setAttribute('aria-pressed', selected === id ? 'true' : 'false'); button.setAttribute('aria-label', `Bring ${item.name} to table`);
      const thumb = document.createElement('div'); thumb.className = 'shelf-thumb'; thumb.append(artwork(id));
      const name = document.createElement('span'); name.textContent = item.name;
      const status = document.createElement('small'); status.textContent = p.stowed ? 'Put away' : 'On table';
      button.append(thumb, name, status); button.addEventListener('click', () => { p.stowed = false; position(id); select(id); renderShelf(); save(); elements.get(id).scrollIntoView({ block: 'nearest', inline: 'nearest' }); }); $('shelf').append(button);
    }
  }
  function fitTable() {
    scale = Math.max(0.2, ($('table-scroll').clientWidth - 2) / 1400) * Number($('table-zoom').value);
    $('table').style.transform = `scale(${scale})`; $('table-size').style.width = 1400 * scale + 'px'; $('table-size').style.height = 1050 * scale + 'px';
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
    if (!done) { $('lock-number').textContent = `Lock ${state.stage + 1} of ${G.locks.length}`; $('lock-name').textContent = G.locks[state.stage].name; }
    $('lock-message').textContent = ''; $('combination').value = ''; renderHints();
  }
  function renderHints() {
    $('hints').replaceChildren(); if (state.stage >= G.locks.length) return;
    const shown = state.hints[state.stage];
    G.locks[state.stage].hints.slice(0, shown).forEach((text, i) => { const p = document.createElement('p'); p.className = 'hint'; p.textContent = `${i === 3 ? 'Solution' : 'Hint ' + (i + 1)} · ${text}`; $('hints').append(p); });
    $('hint-next').textContent = shown === 0 ? 'Need a hint?' : shown === 3 ? 'Reveal the combination' : shown === 4 ? 'All hints shown' : 'Another hint'; $('hint-next').disabled = shown === 4;
  }
  function openViewer(id) {
    viewerId = id; select(id); $('viewer-zoom').value = '1'; $('viewer').showModal(); renderViewer();
  }
  function renderViewer() {
    if (!viewerId) return;
    const item = G.items[viewerId]; $('viewer-title').textContent = item.name; $('viewer-flip').disabled = !(item.faces?.length > 1);
    const host = $('viewer-scroll'), availableW = host.clientWidth - 40, availableH = host.clientHeight - 40;
    const fit = Math.min(availableW / item.w, availableH / item.h) * Number($('viewer-zoom').value);
    $('viewer-art').style.width = Math.max(1, item.w * fit) + 'px'; $('viewer-art').style.height = Math.max(1, item.h * fit) + 'px';
    $('viewer-art').replaceChildren(artwork(viewerId, pieceState(viewerId).back));
  }
  function openLight() {
    const cards = available().filter(id => G.items[id].kind === 'Postcard');
    if (cards.length < 2) { toast('The lamp is ready. You need another postcard to try a pair.'); return; }
    if (state.light.top === state.light.bottom) { state.light.top = cards.at(-2); state.light.bottom = cards.at(-1); }
    for (const [id, key] of [['light-top', 'top'], ['light-bottom', 'bottom']]) {
      $(id).replaceChildren(...cards.map(cardId => { const option = document.createElement('option'); option.value = cardId; option.textContent = G.items[cardId].name; return option; })); $(id).value = state.light[key];
    }
    $('light-zoom').value = '1'; $('light-pan').value = '0'; $('light-dialog').showModal(); renderLight(); save();
  }
  function renderLight() {
    const l = state.light, windowEl = $('light-window');
    lightScale = windowEl.clientWidth / 1900 * Number($('light-zoom').value);
    const pan = Number($('light-pan').value);
    $('light-scene').style.transform = `translate(${windowEl.clientWidth / 2 - (950 + pan) * lightScale}px,${windowEl.clientHeight / 2 - 1250 * lightScale}px) scale(${lightScale})`;
    const top = $('light-upper'), bottom = $('light-lower');
    top.src = G.items[l.top].faces[l.topBack ? 1 : 0]; top.style.left = 200 + l.dx + 'px'; top.style.top = 200 + l.dy + 'px'; top.style.transform = `rotate(${l.rotation}deg)`;
    bottom.src = G.items[l.bottom].faces[l.bottomBack ? 1 : 0]; bottom.style.left = '200px'; bottom.style.top = '1250px'; bottom.style.transform = `rotate(${l.bottomRotation}deg)`;
    windowEl.classList.toggle('lit', l.on); $('lamp-toggle').setAttribute('aria-pressed', String(l.on)); $('lamp-toggle').textContent = l.on ? 'Switch lamp off' : 'Switch lamp on';
    $('light-flip-top').textContent = l.topBack ? 'Show picture' : 'Turn over'; $('light-flip-bottom').textContent = l.bottomBack ? 'Show picture' : 'Turn over';
  }
  function moveLight(dx, dy) { state.light.dx = G.clamp(state.light.dx + dx, -600, 600, 110); state.light.dy = G.clamp(state.light.dy + dy, -250, 250, -60); renderLight(); save(); }
  $('inspect').onclick = () => selected && openViewer(selected);
  $('flip').onclick = () => flip(selected); $('rotate').onclick = () => rotate(selected);
  $('stow').onclick = () => { if (!selected) return; pieceState(selected).stowed = true; position(selected); select(null); renderShelf(); save(); };
  $('tidy').onclick = () => { available().forEach(id => { const p = pieceState(id); p.x = G.items[id].at[0]; p.y = G.items[id].at[1]; p.rot = 0; p.stowed = false; }); buildTable(); save(); toast('All collected items are back on the table.'); };
  $('table-zoom').onchange = fitTable;
  $('lock-form').onsubmit = e => {
    e.preventDefault(); const lock = G.locks[state.stage]; if (!lock) return;
    if (!G.attempt(state, $('combination').value)) { $('lock-message').textContent = 'The lock stays closed. Try another combination.'; $('lock-message').className = 'error'; $('combination').select(); return; }
    $('lock-message').className = ''; selected = lock.releases[0]; buildTable(); renderProgress(); save(); toast(lock.message);
    if (state.stage === G.locks.length) $('complete').scrollIntoView({ block: 'nearest' });
    else $('combination').focus();
  };
  $('combination').oninput = () => { $('combination').value = $('combination').value.replace(/[^0-9]/g, '').slice(0, 4); };
  $('hint-next').onclick = () => { if (state.stage >= G.locks.length) return; state.hints[state.stage] = Math.min(4, state.hints[state.stage] + 1); renderHints(); save(); };
  $('notes').value = state.notes; $('notes').oninput = () => { state.notes = $('notes').value; save(); };
  $('viewer-flip').onclick = () => flip(viewerId); $('viewer-zoom').onchange = renderViewer;
  $('light-open').onclick = openLight;
  for (const [id, key] of [['light-top', 'top'], ['light-bottom', 'bottom']]) $(id).onchange = () => {
    const other = key === 'top' ? 'bottom' : 'top';
    if ($(id).value === state.light[other]) { $(id).value = state.light[key]; toast('Choose two different postcards.'); return; }
    state.light[key] = $(id).value; renderLight(); save();
  };
  for (const [id, key] of [['light-rotate-top', 'rotation'], ['light-rotate-bottom', 'bottomRotation']]) $(id).onclick = () => { state.light[key] = (state.light[key] + 180) % 360; renderLight(); save(); };
  for (const [id, key] of [['light-flip-top', 'topBack'], ['light-flip-bottom', 'bottomBack'], ['lamp-toggle', 'on']]) $(id).onclick = () => { state.light[key] = !state.light[key]; renderLight(); save(); };
  $('light-zoom').onchange = renderLight; $('light-pan').oninput = renderLight;
  document.querySelectorAll('[data-nudge]').forEach(button => button.onclick = e => { const [dx, dy] = button.dataset.nudge.split(',').map(Number); moveLight(dx / (e.shiftKey ? 10 : 1), dy / (e.shiftKey ? 10 : 1)); });
  $('light-window').onkeydown = e => { const moves = { ArrowLeft: [-10, 0], ArrowRight: [10, 0], ArrowUp: [0, -10], ArrowDown: [0, 10] }; if (!moves[e.key]) return; e.preventDefault(); const [dx, dy] = moves[e.key]; moveLight(dx / (e.shiftKey ? 10 : 1), dy / (e.shiftKey ? 10 : 1)); };
  let lightDrag;
  $('light-window').onpointerdown = e => { if (e.button !== 0) return; e.currentTarget.setPointerCapture(e.pointerId); lightDrag = { x: e.clientX, y: e.clientY, dx: state.light.dx, dy: state.light.dy }; };
  $('light-window').onpointermove = e => { if (!lightDrag) return; state.light.dx = G.clamp(lightDrag.dx + (e.clientX - lightDrag.x) / lightScale, -600, 600, 110); state.light.dy = G.clamp(lightDrag.dy + (e.clientY - lightDrag.y) / lightScale, -250, 250, -60); renderLight(); };
  const endLightDrag = () => { lightDrag = null; save(); };
  $('light-window').onpointerup = endLightDrag; $('light-window').onpointercancel = endLightDrag; $('light-window').onlostpointercapture = endLightDrag;
  $('light-reset').onclick = () => { Object.assign(state.light, { rotation: 0, bottomRotation: 0, dx: 110, dy: -60, topBack: false, bottomBack: false }); renderLight(); save(); };
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
      const raw = JSON.parse(text); if (raw.version !== 1 || !Number.isInteger(raw.stage) || raw.stage < 0 || raw.stage > 3) throw new Error('Invalid save');
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
  window.addEventListener('resize', () => { fitTable(); if ($('viewer').open) renderViewer(); if ($('light-dialog').open) renderLight(); });
  buildTable(); renderProgress(); save(); if (!hadSave) $('intro').showModal();
})();
