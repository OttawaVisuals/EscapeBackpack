'use strict';
(() => {
  const G = window.LeifGame;
  const $ = id => document.getElementById(id);
  const KEY = 'escape-backpack.leif.v1', ROOM_KEY = 'escape-backpack.leif.room', NAME_KEY = 'escape-backpack.name', TIPS_KEY = 'escape-backpack.tips';
  const FORMSPREE = 'https://formspree.io/f/xaqavoan'; // the site's feedback form
  const SNAP = 12; // screen pixels: edges this close pull together while dragging (Alt turns it off)
  let state = G.fresh(), hadSave = false, storageOK = true;
  try { const saved = localStorage.getItem(KEY); if (saved) { state = G.restore(JSON.parse(saved)); hadSave = true; } } catch (_) { storageOK = false; }
  const params = new URLSearchParams(location.search), onThisComputer = ['localhost', '127.0.0.1', ''].includes(location.hostname);
  // Design testing only, on this computer: Leif.html?lock=7 starts a fresh game at lock 7.
  const startAt = Number(params.get('lock'));
  if (startAt >= 1 && startAt <= G.locks.length + 1 && onThisComputer) { state = G.fresh(); state.stage = Math.floor(startAt) - 1; hadSave = true; history.replaceState(null, '', location.pathname); }
  // Play together: the rooms worker's address from the page, or ?rooms=ws://localhost:8787 while testing here.
  const ROOMS = (onThisComputer && params.get('rooms')) || document.querySelector('meta[name=rooms-server]')?.content.trim() || '';
  let room = null, roomCode = '', peers = [], synced = null;
  let dragging = null, gesture = null, lastTap = {}, zoom = 1;
  let selected = null, scale = 1, z = 5, toastTimer, viewerId = null, compareId = '', opening = false, markerOn = false, busy = false;
  const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wait = ms => new Promise(r => setTimeout(r, reduceMotion() ? 0 : ms));
  const elements = new Map();
  const available = () => G.available(state.stage);
  const store = (key, value) => { try { localStorage.setItem(key, value); return true; } catch (_) { return false; } };
  const fetchStore = key => { try { return localStorage.getItem(key); } catch (_) { return null; } };
  // Solo games save in this browser; in a room the table is also shared, and saved separately.
  function save() {
    storageOK = store(room ? ROOM_KEY : KEY, JSON.stringify(room ? { code: roomCode, state } : state));
    $('save-status').textContent = room ? 'Shared with your room' : storageOK ? 'Saved on this browser' : 'Browser save unavailable · use Save a copy';
    if (room) shareChanges();
  }
  const track = (name, props = {}) => { try { window.zaraz?.track?.(name, { game: 'norse-online', ...props }); } catch (_) { /* analytics never blocks play */ } };
  const sound = name => window.LeifSound?.play(name);
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
    el.classList.toggle('piled', !!p.pile); el.classList.toggle('noted', !!state.itemNotes[id]); if (p.pile) el.style.zIndex = -1 - G.pileMembers(state, p.pile).indexOf(id);
    if (id === 'AD' && state.pieces.comb?.seated) { G.followSeat(state); position('comb'); }
    refreshLens(); if (id === selected) placeTurnHandle();
  }
  function select(id, raise = true) {
    selected = id;
    elements.forEach((el, key) => el.classList.toggle('selected', key === id));
    if (id && raise && !pieceState(id).pile) { elements.get(id).style.zIndex = ++z; if (id === 'AD' && state.pieces.comb?.seated && elements.get('comb')) elements.get('comb').style.zIndex = ++z; }
    $('selected-name').textContent = id ? displayName(id) : 'Your table';
    if (id) $('selected-type').textContent = `${G.items[id].kind} · ${faceName(id, pieceState(id).face)}` + (G.items[id].freeRotate ? ` · ${(Math.round(pieceState(id).rot * 10) / 10).toFixed(1)}°` : '');
    else $('selected-type').innerHTML = 'Drag to arrange · double-click to inspect · <kbd>M</kbd> magnifier';
    $('stow').disabled = !id;
    document.querySelectorAll('.shelf-item').forEach(el => el.setAttribute('aria-pressed', el.dataset.id === id ? 'true' : 'false'));
    placeTurnHandle();
  }
  function positionAll() { elements.forEach((_, id) => position(id)); renderPileTags(); }
  // Out of its pile or the shelf into the first free spot (the table grows if it must).
  function pullOut(id) {
    G.release(state, id); positionAll(); fitTable();
    const el = elements.get(id); el.style.zIndex = ++z; select(id); renderShelf(); save();
    el.classList.add('arrived'); setTimeout(() => el.classList.remove('arrived'), 2800);
    el.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }
  // Picked up off its pile: it stays where it is and the pile closes up.
  function lift(id) { if (!G.unpile(state, id)) return; positionAll(); elements.get(id).style.zIndex = ++z; }
  function flip(id) {
    if (!id || !(G.items[id].faces?.length > 1)) return;
    const p = pieceState(id); p.face = (p.face + 1) % G.items[id].faces.length; if (id === 'comb') p.seated = false;
    elements.get(id).replaceChildren(artwork(id, p.face)); position(id); trySeat(id); select(id, false); save(); sound('paper');
    if ($('viewer').open) { renderViewer(); doneTip('flip'); setTimeout(() => tip('magnifier', $('viewer-magnify'), 'Small print? Turn on the magnifier (M) and move it over the card. Scroll over the lens to change its strength.'), 300); }
  }
  function rotate(id) { if (!id) return; if (pieceState(id).pile) pullOut(id); const p = pieceState(id); p.rot = (p.rot + 90) % 360; if (id === 'comb') p.seated = false; constrain(id); position(id); trySeat(id); select(id, false); save(); if ($('viewer').open) renderViewer(); }
  // Try to settle Aud's comb after the comb or AD has been put down, turned or flipped.
  let combTipShown = false;
  function trySeat(id) {
    if ((id !== 'comb' && id !== 'AD') || !elements.get('comb') || !elements.get('AD')) return;
    const was = !!state.pieces.comb.seated;
    if (G.seatComb(state, Math.max(8, 14 / scale))) { position('comb'); elements.get('comb').style.zIndex = ++z; if (!was && !combTipShown) { combTipShown = true; toast('The comb settles into place.'); } }
  }
  function buildTable() {
    hideTools(); const crowded = G.deal(state); if (crowded && !opening) setTimeout(() => toast('The table is full, so some keepsakes lie on top of others. Tidy table makes room.'), 900);
    elements.forEach(el => el.remove()); elements.clear();
    for (const id of available()) {
      const item = G.items[id], p = pieceState(id), el = document.createElement('button');
      el.type = 'button'; el.className = 'piece'; el.dataset.id = id;
      el.setAttribute('aria-label', `${item.name}. Select, then Inspect to read. Arrow keys move; F turns over; R rotates.`);
      el.style.width = item.w + 'px'; el.style.height = item.h + 'px'; el.dataset.name = displayName(id);
      el.append(artwork(id, p.face)); $('table').append(el); elements.set(id, el); constrain(id); position(id);
      el.addEventListener('click', e => {
        if (p.pile && e.clientY > el.getBoundingClientRect().bottom - G.STRIP * scale) { hideTools(); pullOut(id); return; }
        select(id); showTools(id);
      });
      el.addEventListener('pointerenter', e => { if (e.pointerType !== 'touch') hoverTools(id); });
      el.addEventListener('pointerleave', () => { clearTimeout(switchTimer); hideToolsSoon(); });
      el.addEventListener('dblclick', () => openViewer(id));
      el.addEventListener('keydown', e => {
        if (G.items[id].freeRotate && (e.key === '[' || e.key === ']' || e.key === '{' || e.key === '}')) { e.preventDefault(); turn(id, p.rot + ('[{'.includes(e.key) ? -1 : 1) * (e.shiftKey ? 0.1 : 1)); save(); return; }
        const moves = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
        if (moves[e.key]) { e.preventDefault(); lift(id); const [dx, dy] = moves[e.key], step = e.shiftKey ? 1 : 15; p.x += dx * step; p.y += dy * step; constrain(id); position(id); select(id); save(); }
        if (e.key.toLowerCase() === 'f') { e.preventDefault(); flip(id); }
        if (e.key.toLowerCase() === 'r') { e.preventDefault(); rotate(id); }
        if (e.key === 'Enter') { e.preventDefault(); openViewer(id); }
      });
      let drag = null;
      el.addEventListener('pointerdown', e => {
        if (e.button !== 0 || (lensOn && e.pointerType !== 'mouse')) return;
        hideTools(); select(id); el.setPointerCapture(e.pointerId); drag = { x: e.clientX, y: e.clientY, px: p.x, py: p.y, moved: false }; dragging = id;
      });
      el.addEventListener('pointermove', e => {
        if (!drag || gesture?.type === 'pinch') return;
        if (!drag.moved && Math.hypot(e.clientX - drag.x, e.clientY - drag.y) < 4) return;
        drag.moved = true; lift(id); el.classList.add('lifted'); if (id === 'comb') p.seated = false;
        p.x = drag.px + (e.clientX - drag.x) / scale; p.y = drag.py + (e.clientY - drag.y) / scale;
        if (!e.altKey) G.snap(state, id, SNAP / scale); constrain(id); position(id); shareMove(id);
      });
      const endDrag = e => {
        el.classList.remove('lifted'); if (!drag) return;
        const moved = drag.moved; drag = null; dragging = null;
        if (moved) { trySeat(id); save(); sound('drop'); tip('arrange', el, 'Put things wherever helps you think. Edges that come close snap together. R rotates; on a tablet, hold a keepsake and twist with a second finger.'); return; }
        // A double tap opens the close-up (touch screens have no double-click).
        if (e?.type === 'pointerup' && e.pointerType === 'touch') { const now = Date.now(); if (lastTap.id === id && now - lastTap.at < 350) { lastTap = {}; openViewer(id); } else lastTap = { id, at: now }; }
      };
      el.addEventListener('pointerup', endDrag); el.addEventListener('pointercancel', endDrag); el.addEventListener('lostpointercapture', endDrag);
    }
    renderShelf(); renderPileTags(); select(selected && available().includes(selected) ? selected : null); fitTable();
    return crowded;
  }
  /* Keepsakes shelf, grouped by kind, never by trail (which cards belong together is part of the
     final riddle). Groups holding what the last lock brought are open; the others fold to one
     chip each, so the row stays short as the game goes on. */
  const KINDS = [['Postcards', ['Postcard']], ['Maps', ['Map']], ['Tickets & papers', ['Luggage tag', 'Ticket', 'Card', 'Journal page']]];
  const kindGroup = id => (KINDS.find(([, kinds]) => kinds.includes(G.items[id].kind)) || ['Objects'])[0];
  const shelfOpen = new Set(); let shelfStage = null;
  function renderShelf() {
    $('shelf').replaceChildren(); $('item-count').textContent = available().length;
    if (shelfStage !== state.stage) { shelfOpen.clear(); for (const id of state.stage ? G.locks[state.stage - 1].releases : G.available(0)) shelfOpen.add(kindGroup(id)); shelfStage = state.stage; }
    const groups = new Map([...KINDS.map(([name]) => [name, []]), ['Objects', []]]);
    for (const id of available()) groups.get(kindGroup(id)).push(id);
    for (const [leg, ids] of groups) {
      if (!ids.length) continue;
      const group = document.createElement('div'); group.className = 'shelf-group';
      const open = shelfOpen.has(leg), toggle = document.createElement('button');
      toggle.type = 'button'; toggle.className = 'group-toggle'; toggle.setAttribute('aria-expanded', String(open));
      toggle.innerHTML = '<span class="chev" aria-hidden="true">›</span><span></span><span class="n"></span>';
      toggle.children[1].textContent = leg; toggle.children[2].textContent = ids.length;
      toggle.setAttribute('aria-label', `${leg}: ${ids.length} keepsakes`);
      toggle.onclick = () => { open ? shelfOpen.delete(leg) : shelfOpen.add(leg); renderShelf(); };
      group.append(toggle);
      if (open) for (const id of ids) group.append(shelfItem(id));
      $('shelf').append(group);
    }
  }
  function shelfItem(id) {
    const item = G.items[id], p = pieceState(id), button = document.createElement('button');
    button.className = p.stowed ? 'shelf-item stowed' : 'shelf-item'; button.dataset.id = id; button.setAttribute('aria-pressed', selected === id ? 'true' : 'false');
    button.setAttribute('aria-label', p.stowed ? `${item.name}: put away. Bring it to the table` : p.pile ? `${item.name}: in a pile. Take it out` : `${item.name}: on the table. Find it`);
    const thumb = document.createElement('div'); thumb.className = 'shelf-thumb'; thumb.append(artwork(id));
    const name = document.createElement('span'); name.textContent = displayName(id);
    if (p.pile) button.classList.add('piled');
    button.append(thumb, name);
    button.addEventListener('click', () => { if (p.stowed || p.pile) { pullOut(id); return; } select(id); elements.get(id).style.zIndex = ++z; elements.get(id).scrollIntoView({ block: 'nearest', inline: 'nearest' }); flash(id); });
    return button;
  }
  const flash = id => { const el = elements.get(id); if (!el) return; el.classList.remove('arrived'); void el.offsetWidth; el.classList.add('arrived'); setTimeout(() => el.classList.remove('arrived'), 4300); };

  /* Piles: a tag on each pile names it and how many it holds; clicking lists its cards. */
  const PILE_NAMES = { cards: 'Postcards', maps: 'Maps', papers: 'Tickets & tags' }, PILE_SHORT = { cards: 'Cards', maps: 'Maps', papers: 'Papers' };
  function renderPileTags() {
    const table = $('table'); table.querySelectorAll('.pile-tag').forEach(t => t.remove());
    for (const [name, at] of Object.entries(state.piles || {})) {
      const ids = G.pileMembers(state, name); if (!ids.length || !at) continue;
      const tag = document.createElement('button'); tag.type = 'button'; tag.className = 'pile-tag'; tag.dataset.pile = name;
      tag.setAttribute('aria-haspopup', 'menu'); tag.setAttribute('aria-label', `${PILE_NAMES[name]} pile: ${ids.length}. Choose one to take out`);
      tag.innerHTML = '<span></span><span class="count"></span><span aria-hidden="true">▾</span>'; tag.children[0].textContent = PILE_SHORT[name]; tag.title = `${PILE_NAMES[name]}: choose one to take out`; tag.children[1].textContent = ids.length;
      Object.assign(tag.style, { left: at[0] + 10 + 'px', top: at[1] + 10 + 'px', transform: `scale(${1 / scale})`, transformOrigin: '0 0', zIndex: ++z });
      tag.addEventListener('pointerdown', e => e.stopPropagation());
      tag.addEventListener('click', e => { e.stopPropagation(); openPileMenu(name, tag); });
      table.append(tag);
    }
  }
  function openPileMenu(name, anchor) {
    const menu = $('pile-menu'), ids = G.pileMembers(state, name);
    menu.replaceChildren(Object.assign(document.createElement('div'), { className: 'menu-title', textContent: `${PILE_NAMES[name]} · take one out` }));
    for (const id of ids) {
      const b = document.createElement('button'); b.type = 'button'; b.setAttribute('role', 'menuitem');
      const thumb = document.createElement('span'); thumb.className = 'thumb'; thumb.append(artwork(id));
      b.append(thumb, document.createTextNode(displayName(id)));
      b.onclick = () => { closePileMenu(); pullOut(id); };
      menu.append(b);
    }
    const r = anchor.getBoundingClientRect(); menu.hidden = false;
    menu.style.left = Math.min(innerWidth - menu.offsetWidth - 8, r.left) + 'px';
    menu.style.top = Math.min(innerHeight - menu.offsetHeight - 8, r.bottom + 6) + 'px';
    menu.querySelector('[role=menuitem]')?.focus();
  }
  function closePileMenu() { $('pile-menu').hidden = true; }
  document.addEventListener('pointerdown', e => { if (!$('pile-menu').hidden && !e.target.closest('#pile-menu')) closePileMenu(); });
  $('pile-menu').addEventListener('keydown', e => {
    const items = [...$('pile-menu').querySelectorAll('[role=menuitem]')], i = items.indexOf(document.activeElement);
    if (e.key === 'Escape') { e.preventDefault(); closePileMenu(); }
    if (e.key === 'ArrowDown') { e.preventDefault(); items[(i + 1) % items.length]?.focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); items[(i - 1 + items.length) % items.length]?.focus(); }
  });

  /* At zoom 1 ("Fit") the whole table fits its area. Zoom in with + and −, Ctrl+scroll or a
     pinch; drag the empty table to pan. focus: a screen point [x, y] that stays put while
     zooming; anchor: the table point that should end up under it (pinch keeps it). */
  const tableAt = ([x, y]) => { const r = $('table').getBoundingClientRect(); return [(x - r.left) / scale, (y - r.top) / scale]; };
  function fitTable(focus, anchor) {
    const box = $('table-scroll'), pad = 12, T = G.sizes[state.table];
    placeShelf(box, T, pad);
    const keep = focus && (anchor || tableAt(focus));
    $('table').style.width = T.w + 'px'; $('table').style.height = T.h + 'px';
    scale = Math.max(0.05, Math.min((box.clientWidth - pad * 2) / T.w, (box.clientHeight - pad * 2) / T.h)) * zoom;
    $('table').style.transform = `scale(${scale})`; $('table').classList.toggle('readable-strips', G.STRIP * scale >= 14);
    $('table').querySelectorAll('.pile-tag,.remote-cursor').forEach(t => { t.style.transform = `scale(${1 / scale})`; }); $('table-size').style.width = T.w * scale + 'px'; $('table-size').style.height = T.h * scale + 'px';
    if (keep) { const r = $('table').getBoundingClientRect(); box.scrollLeft += r.left + keep[0] * scale - focus[0]; box.scrollTop += r.top + keep[1] * scale - focus[1]; }
    $('zoom-fit').textContent = zoom === 1 ? 'Fit' : Math.round(zoom * 100) + '%'; $('zoom-out').disabled = zoom <= 1; $('zoom-in').disabled = zoom >= MAX_ZOOM;
    box.classList.toggle('zoomed', zoom > 1); refreshLens(); placeTurnHandle(); placeTip();
  }
  const MAX_ZOOM = 5, ZOOM_STEPS = [1, 1.5, 2, 3, 4, 5];
  function setZoom(next, focus, anchor) {
    next = Math.min(MAX_ZOOM, Math.max(1, next)); if (Math.abs(next - zoom) < 0.002 && !anchor) return;
    const r = $('table-scroll').getBoundingClientRect(); zoom = next; hideTools();
    document.body.classList.add('zooming'); fitTable(focus || [r.left + r.width / 2, r.top + r.height / 2], anchor);
    clearTimeout(setZoom.timer); setZoom.timer = setTimeout(() => document.body.classList.remove('zooming'), 120);
  }
  $('zoom-in').onclick = () => setZoom(ZOOM_STEPS.find(v => v > zoom + 0.01) || MAX_ZOOM);
  $('zoom-out').onclick = () => setZoom([...ZOOM_STEPS].reverse().find(v => v < zoom - 0.01) || 1);
  $('zoom-fit').onclick = () => setZoom(1);
  $('table-scroll').addEventListener('wheel', e => { if (!e.ctrlKey || (lensOn && !lensEl.hidden)) return; e.preventDefault(); setZoom(zoom * (e.deltaY < 0 ? 1.15 : 1 / 1.15), [e.clientX, e.clientY]); }, { passive: false });
  /* Gestures on the table: drag the empty table to pan; two fingers pinch to zoom (and pan), or,
     while one finger holds a keepsake, a second finger twisting turns it. */
  const touches = new Map(), angleOf = (a, b) => Math.atan2(b.y - a.y, b.x - a.x) * 180 / Math.PI, gap = (a, b) => Math.hypot(b.x - a.x, b.y - a.y);
  const onBackground = t => !t.closest('.piece,.pile-tag,button,input,.unlock-banner,.tafl,.tally');
  $('table-scroll').addEventListener('pointerdown', e => {
    if (e.pointerType === 'touch') touches.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const box = $('table-scroll');
    if (touches.size === 2) {
      e.preventDefault(); e.stopPropagation();
      const [a, b] = [...touches.values()], mid = [(a.x + b.x) / 2, (a.y + b.y) / 2];
      gesture = dragging && !lensOn ? { type: 'twist', id: dragging, a0: angleOf(a, b), rot0: pieceState(dragging).rot, turns: 0 }
        : { type: 'pinch', d0: gap(a, b), z0: zoom, anchor: tableAt(mid) };
      return;
    }
    if (touches.size <= 1 && onBackground(e.target) && (e.button === 0 || e.pointerType === 'touch') && !(lensOn && e.pointerType !== 'mouse')) {
      gesture = { type: 'pan', x: e.clientX, y: e.clientY, sl: box.scrollLeft, st: box.scrollTop, id: e.pointerId };
      if (zoom > 1) box.classList.add('panning');
    }
  }, true);
  document.addEventListener('pointermove', e => {
    if (touches.has(e.pointerId)) touches.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (!gesture) return;
    const box = $('table-scroll');
    if (gesture.type === 'pan' && e.pointerId === gesture.id) { box.scrollLeft = gesture.sl - (e.clientX - gesture.x); box.scrollTop = gesture.st - (e.clientY - gesture.y); return; }
    if (touches.size < 2) return;
    const [a, b] = [...touches.values()];
    if (gesture.type === 'pinch') setZoom(gesture.z0 * gap(a, b) / gesture.d0, [(a.x + b.x) / 2, (a.y + b.y) / 2], gesture.anchor);
    if (gesture.type === 'twist') {
      let turn = angleOf(a, b) - gesture.a0; turn = ((turn + 540) % 360) - 180;
      if (G.items[gesture.id].freeRotate) { turn(gesture.id, gesture.rot0 + turn); return; }
      const steps = Math.round(turn / 90);
      if (steps !== gesture.turns && Math.abs(turn - steps * 90) < 35) { const n = ((steps - gesture.turns) % 4 + 4) % 4; for (let i = 0; i < n; i++) rotate(gesture.id); gesture.turns = steps; sound('tick'); }
    }
  });
  const endGesture = e => {
    touches.delete(e.pointerId); $('table-scroll').classList.remove('panning');
    if (gesture && (gesture.type === 'pan' ? e.pointerId === gesture.id : touches.size < 2)) { if (gesture.type === 'twist') save(); gesture = null; }
  };
  document.addEventListener('pointerup', endGesture); document.addEventListener('pointercancel', endGesture);
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
  /* The backpack, drawn with its real pockets (each lock names one). The pocket whose lock is
     next glows; pockets with a lock still to come show a padlock; emptied pockets hang open. */
  const LOCK = (x, y) => `<g transform="translate(${x} ${y})"><g class="lk"><path d="M-3.6 -1V-4.4a3.6 3.6 0 0 1 7.2 0V-1"/><rect x="-5.6" y="-1.4" width="11.2" height="8.6" rx="1.6"/></g></g>`;
  const BAG = `<svg viewBox="0 0 260 232" role="group" aria-labelledby="bag-title"><title id="bag-title">Backpack</title>
    <path d="M110 40C110 12 150 12 150 40" fill="none" stroke="#7A5232" stroke-width="7" stroke-linecap="round"/>
    <path d="M80 48L58 66M180 48L204 60" stroke="#7A5232" stroke-width="2.5"/>
    <g class="pocket" data-pocket="lowerLeft"><title>Lower left pocket</title><path class="zone fabric-light" d="M74 128H58Q48 128 48 140V180Q48 192 60 192H76Z"/><ellipse class="mouth" cx="62" cy="131" rx="11" ry="3"/>${LOCK(61, 158)}</g>
    <g class="pocket" data-pocket="lowerRight"><title>Lower right pocket</title><path class="zone fabric-light" d="M186 128H202Q212 128 212 140V180Q212 192 200 192H184Z"/><ellipse class="mouth" cx="198" cy="131" rx="11" ry="3"/>${LOCK(199, 158)}</g>
    <g class="pocket" data-pocket="main"><title>Main compartment</title><rect class="zone fabric" x="70" y="36" width="120" height="162" rx="26"/><ellipse class="mouth" cx="130" cy="41" rx="46" ry="6"/>${LOCK(130, 100)}</g>
    <g class="pocket" data-pocket="insideMiddle"><title>Inside middle pocket</title><rect class="zone inside" x="90" y="110" width="80" height="26" rx="6"/><ellipse class="mouth" cx="130" cy="112" rx="32" ry="3"/>${LOCK(130, 121)}</g>
    <g class="pocket" data-pocket="lowerFront"><title>Lower front pocket</title><rect class="zone fabric-light" x="86" y="142" width="88" height="50" rx="11"/><path class="stitch" d="M92 158H168"/><ellipse class="mouth" cx="130" cy="146" rx="38" ry="4"/>${LOCK(130, 171)}</g>
    <g class="pocket" data-pocket="insideTop"><title>Inside top pocket</title><path class="zone fabric-light" d="M70 62Q70 36 96 36H164Q190 36 190 62V84Q130 98 70 84Z"/><path class="stitch" d="M76 80Q130 93 184 80"/><ellipse class="mouth" cx="130" cy="88" rx="42" ry="4"/>${LOCK(130, 60)}</g>
    <g aria-hidden="true" pointer-events="none"><rect class="leather" x="98" y="38" width="9" height="56" rx="2"/><rect class="leather" x="153" y="38" width="9" height="56" rx="2"/><rect class="buckle" x="96" y="72" width="13" height="11" rx="2"/><rect class="buckle" x="151" y="72" width="13" height="11" rx="2"/></g>
    <g class="pocket" data-pocket="rolloPouch"><title>Rollo’s pouch</title><path class="zone fabric-light" d="M38 70Q34 63 44 63H62Q72 63 68 70L72 104Q72 118 53 118Q34 118 34 104Z"/><path d="M40 70H66" stroke="#7A5232" stroke-width="2"/><ellipse class="mouth" cx="53" cy="66" rx="12" ry="3"/>${LOCK(53, 92)}</g>
    <g class="pocket" data-pocket="boardBag"><title>Board bag</title><rect class="zone fabric-light" x="190" y="58" width="50" height="52" rx="4"/><path class="stitch" d="M198 66H232V102H198Z"/><ellipse class="mouth" cx="215" cy="61" rx="21" ry="3"/>${LOCK(215, 86)}</g>
    <g class="pocket" data-pocket="largePouch"><title>Large pouch</title><rect class="zone fabric-light" x="76" y="200" width="108" height="28" rx="14"/><path d="M98 200V228M162 200V228" stroke="#7A5232" stroke-width="5"/><ellipse class="mouth" cx="180" cy="214" rx="4" ry="11"/>${LOCK(130, 212)}</g>
  </svg>`;
  function renderBag() {
    if (!$('bag').firstElementChild) {
      $('bag').innerHTML = BAG;
      $('bag').addEventListener('click', e => { if (e.target.closest('.pocket.current')) $('dial').querySelector('.wheel')?.focus(); });
      $('bag').addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('.pocket.current')) { e.preventDefault(); $('dial').querySelector('.wheel')?.focus(); } });
    }
    const current = G.locks[state.stage]?.pocket;
    $('bag').querySelectorAll('.pocket').forEach(g => {
      const id = g.dataset.pocket, idx = G.locks.map((l, i) => l.pocket === id ? i : -1).filter(i => i >= 0);
      const done = idx.filter(i => i < state.stage).length, left = idx.length - done;
      g.classList.toggle('current', id === current); g.classList.toggle('open', left === 0); g.classList.remove('opening');
      const words = left === 0 ? 'open' : id === current ? `locked: lock ${state.stage + 1} is next` : done ? `locked again: ${left} lock${left > 1 ? 's' : ''} to come` : 'locked';
      g.querySelector('title').textContent = `${G.POCKETS[id]} · ${words}`;
      if (id === current) { g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button'); g.setAttribute('aria-label', `${G.POCKETS[id]}: try its lock`); }
      else { g.removeAttribute('tabindex'); g.removeAttribute('role'); g.removeAttribute('aria-label'); }
    });
    $('bag-title').textContent = `Backpack: ${state.stage} of ${G.locks.length} locks open` + (current ? `. Next: ${G.POCKETS[current]}.` : '.');
  }
  function renderProgress() {
    renderBag(); $('lock-count').textContent = `${state.stage} of ${G.locks.length} open`;
    const done = state.stage === G.locks.length;
    $('lock-panel').hidden = done; $('complete').hidden = !done;
    const lock = G.locks[Math.min(state.stage, G.locks.length - 1)], length = lock.answer?.length || 4, letters = /[A-Z]/.test(lock.answer || '');
    $('chapter').textContent = done ? `ALL ${G.locks.length} LOCKS OPEN` : G.finalRoute(state.stage) ? 'THE FINAL ROUTE' : `LOCK ${state.stage + 1} OF ${G.locks.length}`;
    $('padlock').classList.remove('unlocked', 'wrong');
    if (!done) {
      $('lock-number').textContent = `Lock ${state.stage + 1} of ${G.locks.length}`; $('lock-name').textContent = lock.name; $('lock-nudge').textContent = lock.nudge || '';
      buildDial(length, letters, !!lock.pending);
      $('lock-ask').textContent = lock.pending ? 'This lock is still being built: its combination is being set. Your progress is saved in this browser, so you can carry on from here when it’s ready.'
        : letters ? `A word lock: turn the wheels to a ${length === 4 ? 'four' : length}-letter word hidden among Liv’s keepsakes.` : `Turn the wheels to a ${length === 3 ? 'three' : 'four'}-digit combination hidden among Liv’s keepsakes.`;
      $('lock-form').querySelector('button[type=submit]').disabled = !!lock.pending; $('hint-next').hidden = !!lock.pending;
    }
    $('lock-message').textContent = ''; $('lock-message').className = ''; renderHints(); renderAttempts();
    if (done) renderComplete();
    $('fb-medallion').closest('label').hidden = !done;
  }
  // The codes already tried on this lock, newest first.
  function renderAttempts() {
    const log = state.attempts[state.stage] || [], box = $('attempts'); box.replaceChildren();
    if (!log.length || state.stage >= G.locks.length) return;
    const label = document.createElement('span'); label.textContent = `Tried (${log.length}):`; box.append(label);
    [...log].reverse().slice(0, 8).forEach(code => { const c = document.createElement('code'); c.textContent = code; box.append(c); });
    if (log.length > 8) { const more = document.createElement('span'); more.textContent = `+${log.length - 8} more`; more.title = [...log].reverse().slice(8).join(', '); box.append(more); }
  }
  /* The ending: Liv's letter, the journey in numbers, and things to take away. */
  const totalHints = () => state.hints.reduce((a, b) => a + b, 0), totalTries = () => state.attempts.reduce((a, l) => a + l.length, 0);
  function renderComplete() {
    const letter = $('ending-letter'); letter.replaceChildren(...[...G.STORY.ending, G.STORY.signature].map(t => Object.assign(document.createElement('p'), { textContent: t })));
    const stats = [['Time', G.duration(state.played)], ['Hints', String(totalHints())], ['Wrong tries', String(totalTries())], ['Locks', `${state.stage} of ${G.locks.length}`]];
    $('ending-stats').replaceChildren(...stats.flatMap(([k, v]) => [Object.assign(document.createElement('dt'), { textContent: k }), Object.assign(document.createElement('dd'), { textContent: v })]));
    $('team-name').value = state.team || '';
  }
  $('copy-result').onclick = async () => {
    const text = G.shareText(state);
    try { await navigator.clipboard.writeText(text); toast('Copied. Paste it wherever you like: no answers are included.'); }
    catch (_) { $('save-text').value = text; openSave('export'); $('save-title').textContent = 'Your result'; $('save-instructions').textContent = 'Select and copy this text.'; $('save-text').value = text; }
  };
  $('team-name').oninput = () => { state.team = $('team-name').value.replace(/\s+/g, ' ').slice(0, 40); saveSoon(); };
  function saveSoon() { clearTimeout(saveSoon.t); saveSoon.t = setTimeout(save, 600); }
  $('print-cert').onclick = () => {
    $('cert-name').textContent = state.team.trim() || 'A determined traveller';
    $('cert-stats').textContent = `${new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })} · ${G.duration(state.played)} · ${totalHints()} hint${totalHints() === 1 ? '' : 's'}`;
    $('cert-medallion').src = G.items.medallion.faces[0];
    track('certificate_printed'); setTimeout(() => print(), 150);
  };
  $('open-feedback-end').onclick = () => openFeedback();
  /* The padlock's wheels: digits or letters. Each wheel has a ▲ (next: 5 → 6) and a ▼ (back)
     button; dragging up or scrolling also turns it forward. With the keyboard, type the character
     (focus moves on), or use the arrow keys (↑ next, ↓ back). */
  const DIGITS = '0123456789', LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  let dialChars = DIGITS, dialVals = [];
  function buildDial(length, letters, disabled) {
    dialChars = letters ? LETTERS : DIGITS; dialVals = Array(length).fill(0);
    $('dial').setAttribute('aria-label', `${letters ? 'Letter' : 'Number'} wheels: ${length}`);
    $('dial').replaceChildren(...dialVals.map((_, i) => {
      const w = document.createElement('button'); w.type = 'button'; w.className = 'wheel'; w.disabled = disabled;
      w.setAttribute('role', 'spinbutton'); w.setAttribute('aria-label', `Wheel ${i + 1} of ${length}`);
      w.innerHTML = '<span class="prev" aria-hidden="true"></span><span class="cur"></span><span class="next" aria-hidden="true"></span>';
      wireWheel(w, i);
      const turn = (d, label) => {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'turn'; b.tabIndex = -1; b.disabled = disabled;
        b.setAttribute('aria-label', `Wheel ${i + 1}: ${label}`); b.innerHTML = '<svg viewBox="0 0 12 8" aria-hidden="true"><path d="M1 7 6 2l5 5"/></svg>';
        b.addEventListener('click', () => { turnWheel(i, d); w.focus({ preventScroll: true }); }); return b;
      };
      const col = document.createElement('div'); col.className = 'wheel-col';
      col.append(turn(1, 'next'), w, turn(-1, 'back')); return col;
    }));
    dialVals.forEach((_, i) => paintWheel(i));
  }
  function paintWheel(i, dir) {
    const w = dialWheels()[i], n = dialChars.length, v = dialVals[i];
    w.querySelector('.prev').textContent = dialChars[(v + n - 1) % n]; w.querySelector('.cur').textContent = dialChars[v]; w.querySelector('.next').textContent = dialChars[(v + 1) % n];
    w.setAttribute('aria-valuenow', v); w.setAttribute('aria-valuemin', 0); w.setAttribute('aria-valuemax', n - 1); w.setAttribute('aria-valuetext', dialChars[v]);
    if (dir) { w.style.setProperty('--dir', dir > 0 ? '10px' : '-10px'); w.classList.remove('spin'); void w.offsetWidth; w.classList.add('spin'); }
    $('combination').value = dialVals.map(k => dialChars[k]).join('');
  }
  const dialWheels = () => [...$('dial').querySelectorAll('.wheel')];
  function turnWheel(i, d) {
    const n = dialChars.length; dialVals[i] = ((dialVals[i] + d) % n + n) % n; paintWheel(i, d); sound('tick');
    if ($('lock-message').className === 'error') { $('lock-message').textContent = ''; $('lock-message').className = ''; }
  }
  function setDial(i, ch) { const k = dialChars.indexOf(ch.toUpperCase()); if (k < 0) return false; const d = k === dialVals[i] ? 0 : 1; dialVals[i] = k; paintWheel(i, d); return true; }
  function wireWheel(w, i) {
    let drag = null;
    w.addEventListener('pointerdown', e => { if (e.button !== 0 || w.disabled) return; try { w.setPointerCapture(e.pointerId); } catch (_) { /* gone */ } drag = { last: e.clientY }; });
    w.addEventListener('pointermove', e => {
      if (!drag) return; const dy = e.clientY - drag.last;
      if (Math.abs(dy) >= 14) { turnWheel(i, dy < 0 ? 1 : -1); drag.last = e.clientY; }
    });
    w.addEventListener('pointerup', () => { drag = null; });
    w.addEventListener('pointercancel', () => { drag = null; });
    w.addEventListener('click', e => e.preventDefault());
    w.addEventListener('wheel', e => { if (w.disabled) return; e.preventDefault(); turnWheel(i, e.deltaY > 0 ? 1 : -1); }, { passive: false });
    w.addEventListener('keydown', e => {
      const wheels = dialWheels();
      if (e.key === 'ArrowUp') { e.preventDefault(); turnWheel(i, 1); }
      else if (e.key === 'ArrowDown') { e.preventDefault(); turnWheel(i, -1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); wheels[i + 1]?.focus(); }
      else if (e.key === 'ArrowLeft' || e.key === 'Backspace') { e.preventDefault(); wheels[i - 1]?.focus(); }
      else if (e.key === 'Enter') { e.preventDefault(); $('lock-form').requestSubmit(); }
      else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey && setDial(i, e.key)) { e.preventDefault(); (wheels[i + 1] || $('lock-form').querySelector('[type=submit]')).focus(); }
    });
  }
  $('dial').addEventListener('paste', e => {
    const text = (e.clipboardData?.getData('text') || '').toUpperCase().split('').filter(c => dialChars.includes(c));
    if (!text.length) return; e.preventDefault();
    const start = Math.max(0, dialWheels().indexOf(document.activeElement));
    text.slice(0, dialVals.length - start).forEach((c, k) => setDial(start + k, c));
  });
  function renderHints() {
    $('hints').replaceChildren(); if (state.stage >= G.locks.length) return;
    const shown = state.hints[state.stage];
    G.locks[state.stage].hints.slice(0, shown).forEach((text, i) => { const p = document.createElement('p'); p.className = 'hint'; const b = document.createElement('b'); b.textContent = (i === 3 ? 'Solution' : 'Hint ' + (i + 1)) + ' · '; p.append(b, text); $('hints').append(p); });
    $('hint-next').textContent = shown === 0 ? 'Need a hint?' : shown === 3 ? 'Reveal the combination' : shown === 4 ? 'All hints shown' : 'Another hint'; $('hint-next').disabled = shown === 4;
  }
  function openViewer(id) {
    hideTools(); viewerId = id; select(id);
    $('viewer-compare').replaceChildren(new Option('Choose a keepsake…', ''), ...available().filter(k => k !== id && !pieceState(k).stowed).map(k => new Option(displayName(k), k)));
    $('viewer-compare').value = available().includes(compareId) && compareId !== id ? compareId : '';
    if (!$('viewer').open) $('viewer').showModal(); renderViewer(); placeTurnHandle(); renderViewerNote();
    doneTip('tools'); if (G.items[id].faces?.length > 1) setTimeout(() => tip('flip', $('viewer-flip'), 'Liv writes on the back of everything. Flip it over.'), 350);
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
  $('stow').onclick = () => { if (!selected) return; G.unpile(state, selected); pieceState(selected).stowed = true; positionAll(); select(null); renderShelf(); save(); };
  $('tidy').onclick = () => {
    G.arrange(state); buildTable(); save();
    toast(Object.keys(state.piles).length ? 'Older keepsakes are stacked: use a pile’s tag to take a card out. Solid keepsakes are on the Keepsakes shelf.' : 'Everything is face up and laid out again.');
  };
  /* Opening a lock: the shackle springs, the pocket opens, and what was inside flies out of it
     to its place on the table. A short banner says what arrived; the final route and the end get a card of their own. */
  $('lock-form').onsubmit = async e => {
    e.preventDefault(); const lock = G.locks[state.stage]; if (!lock || busy) return;
    const code = $('combination').value;
    doneTip('padlock');
    if (!G.attempt(state, code)) {
      const earlier = G.earlierLock(state, code);
      $('lock-message').textContent = earlier >= 0 ? `That code opened lock ${earlier + 1}, the ${G.locks[earlier].name.toLowerCase().replace(/, .*$/, '')}. This lock needs a different one.` : 'The lock stays closed. Try another combination.';
      $('lock-message').className = 'error'; sound('wrong'); renderAttempts(); save();
      const pad = $('padlock'); pad.classList.remove('wrong'); void pad.offsetWidth; pad.classList.add('wrong'); return;
    }
    const i = state.stage - 1;
    track('lock_opened', { lock: i + 1, seconds: Math.round(state.lockTime[i] / 1000), hints: state.hints[i], tries: state.attempts[i].length, room: !!room });
    if (state.stage === G.locks.length) track('game_completed', { minutes: Math.round(state.played / 60000), room: !!room });
    await presentUnlock(lock, true);
  };
  /* A lock opening, here or (in a room) on someone else's screen: the shackle springs, the
     pocket opens, and what was inside flies out to its place on the table. A banner says what
     arrived and asks how the puzzle was; the final route and the end get a card of their own. */
  async function presentUnlock(lock, local, by) {
    busy = true; hideBanner(); closePileMenu();
    const index = G.locks.indexOf(lock), chapter = G.finalRoute(index + 1);
    const pocket = $('bag').querySelector(`.pocket[data-pocket="${lock.pocket}"]`), from = pocket.getBoundingClientRect();
    if (local) { $('padlock').classList.add('unlocked'); $('lock-message').className = ''; $('lock-message').textContent = 'Click! The lock springs open.'; sound('unlock'); await wait(380); }
    pocket.classList.remove('current'); pocket.classList.add('opening'); sound('open'); await wait(650);
    const size = state.table;
    let crowded = local && index + 1 === G.locks.length - 1 ? G.bringBack(state) : false;
    if (local) selected = lock.releases[0];
    opening = true; crowded = buildTable() || crowded; opening = false; renderProgress(); renderPins();
    if (local) save();
    if (state.table !== size) await wait(650);
    sound('whoosh'); await flyIn(lock.releases.filter(id => !pieceState(id).stowed && !pieceState(id).pile), from);
    const glow = lock.releases.map(id => elements.get(id)).filter(Boolean);
    glow.forEach(el => el.classList.add('arrived')); setTimeout(() => glow.forEach(el => el.classList.remove('arrived')), 4500);
    showBanner(`Lock ${index + 1} open · ${lock.name}`, (by ? `${by} opened it. ` : '') + lock.message
      + (crowded ? ' The table is full, so some lie on top of others: Tidy table makes room.' : ''), index);
    busy = false;
    if (chapter) showChapter(lock); else if (local) $('dial').querySelector('.wheel')?.focus();
  }
  // Each new prop flies from the pocket's place on the backpack to where it lies on the table.
  function flyIn(ids, from) {
    if (reduceMotion() || !from.width) return Promise.resolve();
    const cx = from.left + from.width / 2, cy = from.top + from.height / 2;
    return Promise.all(ids.map((id, i) => new Promise(done => {
      const el = elements.get(id); if (!el || el.hidden) return done();
      const r = el.getBoundingClientRect(), ghost = document.createElement('div'), k = Math.min(0.3, 44 / Math.max(r.width, r.height));
      ghost.className = 'fly'; ghost.append(el.firstElementChild.cloneNode(true));
      Object.assign(ghost.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' });
      if (G.items[id].round) ghost.style.borderRadius = '50%';
      el.classList.add('in-flight'); document.body.append(ghost);
      const anim = ghost.animate([
        { transform: `translate(${cx - r.left - r.width * k / 2}px,${cy - r.top - r.height * k / 2}px) scale(${k})`, opacity: 0 },
        { opacity: 1, offset: 0.15 },
        { transform: 'translate(0,0) scale(1)', opacity: 1 }
      ], { duration: 820, delay: i * 120, easing: 'cubic-bezier(.2,.75,.25,1)', fill: 'backwards' });
      anim.onfinish = anim.oncancel = () => { ghost.remove(); el.classList.remove('in-flight'); done(); };
    })));
  }
  let bannerTimer;
  function showBanner(title, text, rateLock) {
    $('banner-title').textContent = title; $('banner-text').textContent = text; $('unlock-banner').hidden = false;
    const rate = $('rate'); rate.hidden = !(rateLock >= 0); rate.dataset.lock = rateLock;
    rate.querySelectorAll('button').forEach(b => b.remove());
    if (rateLock >= 0) for (let n = 1; n <= 5; n++) {
      const b = document.createElement('button'); b.type = 'button'; b.textContent = '★'; b.setAttribute('aria-label', `${n} of 5`); b.setAttribute('aria-pressed', String(state.ratings[rateLock] === n));
      b.classList.toggle('on', n <= state.ratings[rateLock]);
      b.onclick = () => { state.ratings[rateLock] = n; save(); track('puzzle_rated', { lock: rateLock + 1, rating: n }); rate.querySelectorAll('button').forEach((x, k) => { x.classList.toggle('on', k < n); x.setAttribute('aria-pressed', String(k + 1 === n)); }); clearTimeout(bannerTimer); bannerTimer = setTimeout(hideBanner, 2500); };
      rate.append(b);
    }
    clearTimeout(bannerTimer); bannerTimer = setTimeout(hideBanner, 16000);
  }
  function hideBanner() { clearTimeout(bannerTimer); $('unlock-banner').hidden = true; }
  $('banner-close').onclick = hideBanner;
  $('hint-next').onclick = () => { if (state.stage >= G.locks.length) return; state.hints[state.stage] = Math.min(4, state.hints[state.stage] + 1); renderHints(); save(); $('hints').lastElementChild?.scrollIntoView({ block: 'nearest', behavior: reduceMotion() ? 'auto' : 'smooth' }); };
  $('notes').value = state.notes; $('notes').oninput = () => { state.notes = $('notes').value; save(); };
  $('viewer-compare').onchange = () => { compareId = $('viewer-compare').value; renderViewer(); };
  // Double-click the side prop to swap places, so Flip and Rotate act on it.
  $('viewer-side').title = 'Double-click to swap it with the main view';
  $('viewer-side').addEventListener('dblclick', () => { if (!compareId) return; const main = viewerId; openViewer(compareId); compareId = main; $('viewer-compare').value = main; renderViewer(); });
  $('viewer-flip').onclick = () => flip(viewerId); $('viewer-rotate').onclick = () => rotate(viewerId);
  $('help').onclick = () => { $('intro').showModal(); $('begin').focus(); }; $('begin').onclick = () => $('intro').close();
  document.querySelectorAll('[data-close]').forEach(button => button.onclick = () => button.closest('dialog').close());
  $('review-table').onclick = () => $('table-scroll').scrollIntoView({ block: 'center' });
  $('restart').onclick = () => $('restart-dialog').showModal();
  $('restart-confirm').onclick = () => { state = G.fresh(); selected = null; $('notes').value = ''; $('restart-dialog').close(); buildTable(); renderProgress(); renderPins(); save(); openUnpack(); };
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
    const a = document.createElement('a'); a.href = url; a.download = 'raven-inheritance-save.json'; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    $('save-result').textContent = 'Download requested. If your browser does not save a file, use Select all text and copy it.';
  };
  function loadSavedText(text) {
    try {
      if (text.length > 100000) throw new Error('Too large');
      const raw = JSON.parse(text); if (raw.version !== 1 || !Number.isInteger(raw.stage) || raw.stage < 0 || raw.stage > G.locks.length) throw new Error('Invalid save');
      state = G.restore(raw); selected = null; $('notes').value = state.notes; buildTable(); renderProgress(); save(); $('save-dialog').close(); toast('Your saved game is loaded.');
    } catch (_) { $('save-result').textContent = 'That is not a valid saved game. Your current game was kept.'; }
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
    // Under a finger, the lens sits above it so the finger does not hide what it shows.
    lensEl.style.left = x - size / 2 + 'px'; lensEl.style.top = y - size / 2 - (lensAt.touch ? size * 0.62 : 0) + 'px';
    lensContent.style.transform = `translate(${size / 2 - lx * k}px,${size / 2 - ly * k}px) scale(${k})`;
  }
  function setLens(on) {
    lensOn = on; document.body.classList.toggle('magnifying', on); if (on) { hideTools(); if (markerOn) { markerOn = false; renderViewer(); } }
    for (const id of ['magnify', 'viewer-magnify']) $(id).setAttribute('aria-pressed', String(on));
    if (on) { refreshLens(); doneTip('magnifier'); } else { lensEl.hidden = true; lensContent.replaceChildren(); }
  }
  document.addEventListener('pointermove', e => { if (!lensOn) return; lensAt = { x: e.clientX, y: e.clientY, target: e.target, touch: e.pointerType === 'touch' }; placeLens(); });
  document.addEventListener('pointerdown', e => { if (!lensOn || e.pointerType === 'mouse') return; lensAt = { x: e.clientX, y: e.clientY, target: e.target, touch: true }; placeLens(); }, true);
  for (const id of ['table-scroll', 'viewer-scroll']) {
    $(id).addEventListener('wheel', e => {
      if (!lensOn || lensEl.hidden) return; e.preventDefault();
      lensPower = G.clamp(lensPower * (e.deltaY < 0 ? 1.15 : 1 / 1.15), 1.5, 10, 3); placeLens();
    }, { passive: false });
    $(id).addEventListener('pointerleave', () => { lensEl.hidden = true; });
  }
  $('magnify').onclick = $('viewer-magnify').onclick = () => setLens(!lensOn);
  document.addEventListener('keydown', e => {
    if (e.defaultPrevented || e.target.closest?.('input,textarea,select,.wheel') || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key.toLowerCase() === 'm') { e.preventDefault(); setLens(!lensOn); }
    if (!document.querySelector('dialog[open]') && ['+', '=', '-', '0'].includes(e.key)) { e.preventDefault(); (e.key === '0' ? $('zoom-fit') : e.key === '-' ? $('zoom-out') : $('zoom-in')).click(); }
    if (e.key === 'Escape' && lensOn && !document.querySelector('dialog[open]')) setLens(false);
    if (e.key === 'Escape' && !$('unlock-banner').hidden && !document.querySelector('dialog[open]')) hideBanner();
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
    hideTools(); lift(id); select(id);
    moving = { id, dx: tx - p.x, dy: ty - p.y, from: [p.x, p.y], sx: e.clientX, sy: e.clientY, dragged: false };
    if (id === 'comb') p.seated = false;
    document.body.classList.add('moving'); elements.get(id).classList.add('lifted'); placeTurnHandle();
  });
  document.addEventListener('pointermove', e => {
    if (!moving) return;
    const p = pieceState(moving.id), [tx, ty] = tablePoint(e);
    p.x = tx - moving.dx; p.y = ty - moving.dy; if (!e.altKey) G.snap(state, moving.id, SNAP / scale); constrain(moving.id); position(moving.id); shareMove(moving.id);
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
    if (e.ctrlKey || e.metaKey || e.altKey || e.target.closest('input,textarea,select')) return;
    if (e.key.toLowerCase() === 'r') { e.preventDefault(); rotate(viewerId); }
    if (e.key.toLowerCase() === 'f') { e.preventDefault(); flip(viewerId); }
  });
  // Move from the close-up: back to the table carrying the prop, centred on the pointer.
  $('viewer-move').onclick = e => {
    const id = viewerId, p = pieceState(id), item = G.items[id];
    $('viewer').close(); lift(id); p.stowed = false; position(id); select(id);
    moving = { id, dx: item.w / 2, dy: item.h / 2, from: [p.x, p.y], sx: e.clientX, sy: e.clientY, dragged: false };
    document.body.classList.add('moving'); elements.get(id).classList.add('lifted');
    const [tx, ty] = tablePoint(e); p.x = tx - moving.dx; p.y = ty - moving.dy; constrain(id); position(id);
    toast('Click where it goes. Esc puts it back.');
  };

  /* Turn handle: a round knob at the far end of a freely turning prop (the ruler) while it is
     selected. Dragging it turns the prop about its pivot (the ruler's 0 mark); Shift snaps to 15°. */
  const turnHandle = $('turn-handle');
  function turn(id, rot) { const p = pieceState(id); G.turnAbout(id, p, rot, pivotUnits(id)); constrain(id); position(id); select(id, false); shareMove(id); }
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

  /* The final route and the end get a card; ordinary locks only get the banner. */
  function showChapter(lock) {
    const next = G.locks[state.stage], last = !next;
    $('opened-no').textContent = last ? '✦' : String(state.stage + 1);
    $('opened-eyebrow').textContent = `Lock ${G.locks.indexOf(lock) + 1} open · ${lock.name}`;
    $('opened-title').textContent = last ? 'The last pocket opens' : 'The final route';
    $('opened-what').textContent = last ? lock.message : next.nudge || '';
    $('opened-next').textContent = last ? 'That was the last lock. Liv’s note is waiting beside the backpack.'
      : next.pending ? 'The next lock is still being built. Your progress is saved here.'
      : 'Every postcard and map is on the table. Everything else stays where you left it.';
    const note = last ? [...G.STORY.ending, G.STORY.signature] : [];
    $('opened-liv').replaceChildren(...note.map(t => Object.assign(document.createElement('p'), { textContent: t }))); $('opened-liv').hidden = !note.length;
    $('opened-medallion').hidden = !last; if (last) $('opened-medallion').src = G.items.medallion.faces[0];
    if (last) $('opened-next').textContent = 'The medallion is on your table. Your journey, a result to share and a certificate are beside the backpack.';
    $('opened-go').textContent = last ? 'See your journey' : 'Begin the final route →';
    sound('chapter'); $('opened').showModal(); $('opened-go').focus();
  }
  $('opened-go').onclick = () => $('opened').close();
  $('opened').addEventListener('close', () => {
    if (state.stage === G.locks.length) $('complete').scrollIntoView({ block: 'nearest' }); else $('dial').querySelector('.wheel')?.focus();
    setTimeout(laterTips, 600);
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

  /* Notebook: free notes (yours alone) and notes pinned to keepsakes (shared in a room).
     The keepsakes tab lists every postcard as it arrives, with its note. */
  for (const tab of ['notes', 'pins']) $('tab-' + tab).onclick = () => {
    for (const t of ['notes', 'pins']) { $('tab-' + t).setAttribute('aria-selected', String(t === tab)); $('pane-' + t).hidden = t !== tab; }
    if (tab === 'pins') renderPins();
  };
  function renderPins() {
    const noted = Object.keys(state.itemNotes).filter(id => available().includes(id));
    $('pin-count').textContent = noted.length ? `(${noted.length})` : '';
    if ($('pane-pins').hidden) return;
    const list = $('pins'); list.replaceChildren();
    const ids = [...available().filter(id => G.items[id].kind === 'Postcard'), ...noted.filter(id => G.items[id].kind !== 'Postcard')];
    let leg = null;
    for (const id of ids) {
      const l = G.items[id].kind === 'Postcard' ? 'Postcards' : 'Other keepsakes';
      if (l !== leg) { leg = l; list.append(Object.assign(document.createElement('h3'), { textContent: l })); }
      const b = document.createElement('button'); b.type = 'button'; b.className = 'pin' + (state.itemNotes[id] ? ' has' : '');
      b.append(Object.assign(document.createElement('strong'), { textContent: displayName(id) }), Object.assign(document.createElement('span'), { textContent: state.itemNotes[id] || 'Add a note' }));
      b.onclick = () => { openViewer(id); setNoteOpen(true); };
      list.append(b);
    }
  }
  let noteOpen = false;
  function setNoteOpen(on) { noteOpen = on; renderViewerNote(); if (on) $('viewer-note-text').focus(); }
  function renderViewerNote() {
    const id = viewerId; if (!id) return;
    $('viewer-note-btn').setAttribute('aria-pressed', String(noteOpen)); $('viewer-note').hidden = !noteOpen;
    $('viewer-note-btn').classList.toggle('has-note', !!state.itemNotes[id]);
    if (!noteOpen) return;
    $('viewer-note-name').textContent = displayName(id); $('viewer-note-shared').textContent = room ? 'Everyone in your room sees this note.' : '';
    if (document.activeElement !== $('viewer-note-text')) $('viewer-note-text').value = state.itemNotes[id] || '';
  }
  $('viewer-note-btn').onclick = () => setNoteOpen(!noteOpen);
  $('viewer-note-text').oninput = () => {
    const id = viewerId, text = $('viewer-note-text').value.slice(0, 1000);
    if (text.trim()) state.itemNotes[id] = text; else delete state.itemNotes[id];
    position(id); $('viewer-note-btn').classList.toggle('has-note', !!text.trim()); renderPins(); saveSoon();
  };
  $('viewer').addEventListener('close', () => { noteOpen = false; $('viewer-note').hidden = true; if (tipEl?.closest('dialog')) dropTip(); setTimeout(() => tip('padlock', $('dial'), 'Found a code? Turn the wheels (or type it) and press Open. Hints are just below if you get stuck.'), 400); });

  /* Tips: one small bubble at a time, shown the first time each thing is useful. They never
     give away a puzzle: only how to handle the keepsakes. "No more tips" turns them all off. */
  let tipsSeen; try { tipsSeen = new Set(JSON.parse(fetchStore(TIPS_KEY) || '[]')); } catch (_) { tipsSeen = new Set(); }
  let tipEl = null, tipId = null, tipAnchor = null;
  function tip(id, anchor, text) {
    if (tipsSeen.has('off') || tipsSeen.has(id) || tipEl || !anchor?.isConnected || anchor.hidden || !anchor.offsetWidth) return;
    const dialog = anchor.closest('dialog'), open = document.querySelector('dialog[open]');
    if (open && open !== dialog) return;
    tipEl = document.createElement('div'); tipEl.className = 'tip'; tipEl.setAttribute('role', 'status'); tipId = id; tipAnchor = anchor;
    tipEl.innerHTML = '<p></p><div class="tip-actions"><button type="button" class="tip-ok">Got it</button><button type="button" class="text-button tip-off">No more tips</button></div>';
    tipEl.querySelector('p').textContent = text;
    tipEl.querySelector('.tip-ok').onclick = () => doneTip(id);
    tipEl.querySelector('.tip-off').onclick = () => { tipsSeen.add('off'); doneTip(id); };
    (dialog || document.body).append(tipEl); placeTip();
  }
  function placeTip() {
    if (!tipEl) return;
    if (!tipAnchor?.isConnected) { dropTip(); return; }
    const r = tipAnchor.getBoundingClientRect(), w = tipEl.offsetWidth, h = tipEl.offsetHeight;
    const below = r.bottom + h + 16 < innerHeight;
    tipEl.classList.toggle('above', !below);
    tipEl.style.left = Math.max(8, Math.min(innerWidth - w - 8, r.left + r.width / 2 - w / 2)) + 'px';
    tipEl.style.top = (below ? r.bottom + 12 : Math.max(8, r.top - h - 12)) + 'px';
    tipEl.style.setProperty('--arrow', Math.max(14, Math.min(w - 14, r.left + r.width / 2 - parseFloat(tipEl.style.left))) + 'px');
  }
  function dropTip() { tipEl?.remove(); tipEl = null; tipId = null; tipAnchor = null; }
  function doneTip(id) {
    if (!tipsSeen.has(id)) { tipsSeen.add(id); store(TIPS_KEY, JSON.stringify([...tipsSeen])); }
    if (tipId === id || tipsSeen.has('off')) dropTip();
  }
  // A tip that waits for a moment without dialogs: piles, once there are some.
  function laterTips() {
    const tag = $('table').querySelector('.pile-tag');
    if (tag) tip('piles', tag, 'Older keepsakes are stacked in piles. Use a pile’s tag to take a card back out.');
  }
  addEventListener('resize', placeTip); $('table-scroll').addEventListener('scroll', placeTip);

  /* The opening: Liv's letter, then unbuckling the bag sends the first keepsakes to the table. */
  const letterParas = lines => lines.map(t => Object.assign(document.createElement('p'), { textContent: t }));
  function openUnpack() {
    $('letter-text').replaceChildren(...letterParas(G.STORY.letter));
    $('unpack-bag').innerHTML = BAG.replace(' role="group" aria-labelledby="bag-title"', ' aria-hidden="true"').replace(/<title[^>]*>[^<]*<\/title>/g, '');
    $('unpack-together').textContent = ROOMS ? 'together on your own devices (Play together, top right)' : 'together around one screen';
    $('unpack').showModal(); $('unbuckle').focus();
  }
  $('unbuckle').onclick = async () => {
    const pocket = $('unpack-bag').querySelector('.pocket[data-pocket="main"]');
    sound('unlock'); pocket?.classList.add('opening'); $('unpack').classList.add('opening'); await wait(700); sound('open');
    const from = pocket?.getBoundingClientRect() || { width: 0 };
    $('unpack').close(); $('unpack').classList.remove('opening'); save();
    sound('whoosh'); await flyIn(G.initial, from);
    setTimeout(() => tip('tools', elements.get('L1'), 'Liv’s first postcard. Hover over it (or tap it) for its tools, or double-click (double-tap) for a close-up.'), 300);
  };
  $('unpack').addEventListener('cancel', e => e.preventDefault()); // Esc does not skip the letter by accident
  $('unpack-help').onclick = () => { $('intro').showModal(); $('begin').focus(); };

  /* Sound: effects and ambience switches in the header. */
  function renderSound() {
    const s = window.LeifSound?.settings || { fx: false, amb: false };
    $('sound-fx').checked = s.fx; $('sound-amb').checked = s.amb;
    $('sound-btn').classList.toggle('muted', !s.fx && !s.amb); $('sound-btn').title = !s.fx && !s.amb ? 'Sound is off' : 'Sound';
  }
  $('sound-btn').onclick = e => { e.stopPropagation(); const open = $('sound-menu').hidden; $('sound-menu').hidden = !open; $('sound-btn').setAttribute('aria-expanded', String(open)); };
  $('sound-fx').onchange = () => { window.LeifSound?.set({ fx: $('sound-fx').checked }); renderSound(); sound('tick'); };
  $('sound-amb').onchange = () => { window.LeifSound?.set({ amb: $('sound-amb').checked }); renderSound(); };
  document.addEventListener('pointerdown', e => { if (!$('sound-menu').hidden && !e.target.closest('.sound-wrap')) { $('sound-menu').hidden = true; $('sound-btn').setAttribute('aria-expanded', 'false'); } });
  $('sound-menu').addEventListener('keydown', e => { if (e.key === 'Escape') { $('sound-menu').hidden = true; $('sound-btn').focus(); } });
  if (!window.LeifSound) $('sound-btn').closest('.sound-wrap').hidden = true;

  /* Play time: counted only while the page is visible and someone has touched it in the last
     five minutes, so a game left open overnight does not count. Personal: never shared. */
  let lastInput = Date.now(), lastTick = Date.now(), ticks = 0;
  for (const type of ['pointerdown', 'keydown', 'wheel']) document.addEventListener(type, () => { lastInput = Date.now(); }, { passive: true, capture: true });
  setInterval(() => {
    const now = Date.now(), dt = Math.min(now - lastTick, 20000); lastTick = now;
    if (document.visibilityState !== 'visible' || now - lastInput > 300000 || state.stage >= G.locks.length) return;
    state.played += dt; state.lockTime[state.stage] += dt;
    if (++ticks % 3 === 0) save();
  }, 5000);

  /* Feedback, sent to the same Formspree form as the site's feedback page. */
  function openFeedback() { $('fb-result').textContent = ''; $('fb-send').disabled = false; $('feedback-form').hidden = false; $('feedback-dialog').showModal(); $('fb-message').focus(); }
  $('open-feedback').onclick = () => openFeedback();
  function statsText() {
    const lines = G.locks.map((l, i) => i < state.stage ? `Lock ${i + 1} (${l.name}): ${G.duration(state.lockTime[i])}, ${state.hints[i]} hint${state.hints[i] === 1 ? '' : 's'}, ${state.attempts[i].length} wrong ${state.attempts[i].length === 1 ? 'try' : 'tries'}, rated ${state.ratings[i] || '–'}/5` : null).filter(Boolean);
    const now = state.stage < G.locks.length ? `Now on lock ${state.stage + 1} (${G.duration(state.lockTime[state.stage])} so far, ${state.hints[state.stage]} hints, ${state.attempts[state.stage].length} wrong tries)` : 'Finished';
    return [`${state.stage}/${G.locks.length} locks · ${G.duration(state.played)} played${room ? ` · in a room of ${peers.length}` : ''} · ${innerWidth}×${innerHeight}${matchMedia('(pointer: coarse)').matches ? ' touch' : ''}`, ...lines, now].join('\n');
  }
  $('feedback-form').onsubmit = async e => {
    e.preventDefault(); if (!$('feedback-form').reportValidity()) return;
    const body = { game: 'norse-online', rating: $('fb-rating').value, email: $('fb-email').value.trim(), medallion: $('fb-medallion').checked && state.stage === G.locks.length ? 'yes' : 'no', _subject: 'The Raven Inheritance · online playtest feedback',
      message: $('fb-message').value.trim() + ($('fb-stats').checked ? `\n\n--- Game stats ---\n${statsText()}` : '') };
    $('fb-send').disabled = true; $('fb-result').textContent = 'Sending…';
    try {
      const r = await fetch(FORMSPREE, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body) });
      if (!r.ok) throw new Error(r.status === 429 ? 'busy' : 'failed');
      track('feedback_submitted', { rating: body.rating || 'none' });
      $('fb-result').textContent = 'Thank you. It’s on its way to us.'; $('feedback-form').reset(); setTimeout(() => $('feedback-dialog').close(), 1800);
    } catch (err) { $('fb-result').textContent = err.message === 'busy' ? 'Too many messages right now. Please try again in a minute.' : 'We couldn’t send it. Check your connection and try again.'; $('fb-send').disabled = false; }
  };

  /* Play together: one shared table per room. The shared part of the game is the table,
     the locks, hints, tried codes, pinned notes and the certificate name; each player keeps
     their own notebook, play time and ratings. Only what changed is sent. */
  const SHARED = ['stage', 'table', 'pieces', 'piles', 'hints', 'attempts', 'itemNotes', 'team'];
  const clone = v => JSON.parse(JSON.stringify(v)), sharedPart = s => clone(Object.fromEntries(SHARED.map(k => [k, s[k]])));
  const personal = () => ({ notes: state.notes, played: state.played, lockTime: state.lockTime, ratings: state.ratings });
  const myColor = (() => { let c = Number(fetchStore(NAME_KEY + '.color')); if (!(c >= 0 && c < 8)) { c = Math.floor(Math.random() * 8); store(NAME_KEY + '.color', String(c)); } return c; })();
  function shareChanges() {
    if (!room || !synced) return;
    const now = sharedPart(state), patch = {};
    for (const k of SHARED) {
      if (k !== 'pieces') { if (JSON.stringify(now[k]) !== JSON.stringify(synced[k])) patch[k] = now[k]; continue; }
      const changed = {}; for (const [id, p] of Object.entries(now.pieces)) if (JSON.stringify(p) !== JSON.stringify(synced.pieces?.[id])) changed[id] = p;
      if (Object.keys(changed).length) patch.pieces = changed;
    }
    synced = now; if (Object.keys(patch).length) room.sendState(patch);
  }
  let lastMove = 0;
  function shareMove(id) { if (!room) return; const now = Date.now(); if (now - lastMove < 70) return; lastMove = now; const p = pieceState(id); room.send({ t: 'move', id, x: Math.round(p.x), y: Math.round(p.y), rot: p.rot }); }
  // Someone else changed the shared table: apply it, animating a lock they opened.
  function applyShared(patch, full, who) {
    const base = full ? {} : { ...sharedPart(state), ...patch, pieces: { ...state.pieces, ...(patch.pieces || {}) } };
    const next = G.restore({ version: 1, ...(full ? patch : base), ...personal() });
    synced = sharedPart(next);
    if (next.stage !== state.stage) {
      const opened = next.stage === state.stage + 1 ? G.locks[state.stage] : null;
      state = next; store(ROOM_KEY, JSON.stringify({ code: roomCode, state }));
      if (opened && !busy) presentUnlock(opened, false, who?.name || 'Someone');
      else { buildTable(); renderProgress(); renderPins(); }
      return;
    }
    let rebuild = next.table !== state.table || JSON.stringify(next.piles) !== JSON.stringify(state.piles);
    const touched = [];
    for (const [id, np] of Object.entries(next.pieces)) {
      const cur = state.pieces[id];
      if (!cur) { state.pieces[id] = np; rebuild = true; continue; }
      if (id === dragging || id === moving?.id || JSON.stringify(cur) === JSON.stringify(np)) continue;
      if (cur.stowed !== np.stowed || cur.pile !== np.pile) rebuild = true;
      const art = ['face', 'marks', 'wheels', 'tafl', 'seated'].some(k => JSON.stringify(cur[k]) !== JSON.stringify(np[k]));
      for (const k of Object.keys(cur)) if (!(k in np)) delete cur[k];
      Object.assign(cur, np); touched.push([id, art]);
    }
    for (const k of ['table', 'piles', 'hints', 'attempts', 'itemNotes', 'team']) state[k] = next[k];
    store(ROOM_KEY, JSON.stringify({ code: roomCode, state }));
    if (rebuild) buildTable();
    else for (const [id, art] of touched) { if (art) refreshPiece(id); elements.get(id)?.classList.add('remote'); position(id); setTimeout(() => elements.get(id)?.classList.remove('remote'), 200); }
    renderHints(); renderAttempts(); renderShelf(); renderPins(); renderViewerNote(); fitTable();
    if (state.stage === G.locks.length) renderComplete();
    if ($('viewer').open && touched.some(([id]) => id === viewerId || id === compareId)) renderViewer();
  }
  // Live drags and pointers, not saved.
  function remoteMove(who, id, x, y, rot) {
    const p = state.pieces[id], el = elements.get(id);
    if (!p || !el || id === dragging || id === moving?.id) return;
    Object.assign(p, { x, y, rot }); el.classList.add('remote'); position(id);
  }
  const cursors = new Map();
  function remoteCursor(who, x, y) {
    let c = cursors.get(who.from);
    if (!c) {
      c = document.createElement('div'); c.className = 'remote-cursor'; c.setAttribute('aria-hidden', 'true');
      c.innerHTML = '<svg viewBox="0 0 24 24"><path d="M3 2l7 19 2.6-7.6L20 11z"/></svg><span></span>';
      cursors.set(who.from, c); $('table').append(c);
    }
    c.style.setProperty('--c', LeifRoom.COLORS[who.color] || '#E0A26A'); c.querySelector('span').textContent = who.name;
    Object.assign(c.style, { left: x + 'px', top: y + 'px', transform: `scale(${1 / scale})` }); c.classList.remove('idle');
    clearTimeout(c.timer); c.timer = setTimeout(() => c.classList.add('idle'), 5000);
  }
  let lastCursor = 0;
  $('table-scroll').addEventListener('pointermove', e => {
    if (!room || e.pointerType === 'touch' && !dragging) return;
    const now = Date.now(); if (now - lastCursor < 80) return; lastCursor = now;
    const [x, y] = tableAt([e.clientX, e.clientY]), T = G.sizes[state.table];
    if (x >= 0 && y >= 0 && x <= T.w && y <= T.h) room.send({ t: 'cursor', x: Math.round(x), y: Math.round(y) });
  });
  function renderRoom(status) {
    const inRoom = !!room;
    $('together').hidden = !ROOMS || inRoom; $('room-chip').hidden = !inRoom;
    $('room-out').hidden = inRoom; $('room-in').hidden = !inRoom;
    if (!inRoom) return;
    const link = `${location.origin}${location.pathname}?room=${roomCode}`;
    $('room-code-big').textContent = roomCode; $('room-link').textContent = link; $('room-link').href = link;
    $('room-label').textContent = `${roomCode} · ${peers.length || 1}`;
    $('room-dots').replaceChildren(...peers.slice(0, 5).map(p => { const d = document.createElement('i'); d.style.background = LeifRoom.COLORS[p.color]; d.title = p.name; return d; }));
    $('room-peers').replaceChildren(...peers.map(p => { const li = document.createElement('li'); const d = document.createElement('i'); d.style.background = LeifRoom.COLORS[p.color]; li.append(d, document.createTextNode(p.name + (p.id === room.you ? ' (you)' : ''))); return li; }));
    if (status) $('room-status').textContent = status;
    $('room-chip').classList.toggle('offline', !room.live);
    for (const [id, c] of cursors) if (!peers.some(p => p.id === id)) { c.remove(); cursors.delete(id); }
  }
  function openRoomDialog(code) {
    $('room-name').value = fetchStore(NAME_KEY) || ''; $('room-code').value = code || ''; $('room-error').textContent = '';
    renderRoom(); $('room-dialog').showModal(); (room ? $('room-copy') : $('room-name').value ? (code ? $('room-join') : $('room-create')) : $('room-name')).focus();
  }
  function joinRoom(code, create) {
    const name = $('room-name').value.replace(/\s+/g, ' ').trim().slice(0, 24) || fetchStore(NAME_KEY);
    if (!name) { $('room-error').textContent = 'Add your name first, so the others know who is moving things.'; $('room-name').focus(); return; }
    store(NAME_KEY, name);
    if (room) room.leave();
    roomCode = code; synced = null; peers = [];
    history.replaceState(null, '', `${location.pathname}?room=${code}${params.get('rooms') ? `&rooms=${encodeURIComponent(params.get('rooms'))}` : ''}`);
    try { const cached = JSON.parse(fetchStore(ROOM_KEY)); if (!create && cached?.code === code) { state = G.restore({ ...cached.state, ...personal() }); buildTable(); renderProgress(); } } catch (_) { /* no cache */ }
    room = new LeifRoom.Room(ROOMS, code, { name, color: myColor }, {
      welcome(game, list) {
        peers = list;
        if (game && Object.keys(game).length) { state = G.restore({ version: 1, ...game, ...personal() }); synced = sharedPart(state); selected = null; buildTable(); renderProgress(); renderPins(); save(); }
        else { synced = sharedPart(state); room.sendState(synced, true); save(); }
        renderRoom('Connected.'); track('room_joined', { players: list.length, created: !!create });
      },
      state: (patch, full, who) => applyShared(patch, full, who),
      peers(list) { const joined = list.filter(p => !peers.some(q => q.id === p.id) && p.id !== room.you); peers = list; renderRoom(); joined.forEach(p => toast(`${p.name} joined the table.`)); },
      cursor: remoteCursor, move: remoteMove,
      status(s, detail) { renderRoom(detail || { connecting: 'Connecting…', live: 'Connected.', retrying: 'Connection lost. Trying again…', closed: '' }[s]); }
    });
    renderRoom('Connecting…'); $('save-status').textContent = 'Shared with your room';
  }
  function leaveRoom() {
    room?.leave(); room = null; synced = null; roomCode = ''; peers = [];
    cursors.forEach(c => c.remove()); cursors.clear();
    history.replaceState(null, '', location.pathname);
    try { const solo = fetchStore(KEY); state = solo ? G.restore(JSON.parse(solo)) : G.fresh(); } catch (_) { state = G.fresh(); }
    selected = null; $('notes').value = state.notes; buildTable(); renderProgress(); renderPins(); renderRoom(); save(); toast('You left the room. This is your own game again.');
  }
  $('together').onclick = () => openRoomDialog(); $('room-chip').onclick = () => openRoomDialog();
  $('room-create').onclick = () => { joinRoom(LeifRoom.newCode(), true); if (room) renderRoom('Room started. Share the link.'); };
  $('room-join').onclick = () => {
    const code = $('room-code').value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    if (!LeifRoom.validCode(code)) { $('room-error').textContent = 'Room codes are six letters and numbers, like K7P2QX.'; $('room-code').focus(); return; }
    joinRoom(code, false);
  };
  $('room-code').addEventListener('keydown', e => { if (e.key === 'Enter') $('room-join').click(); });
  $('room-copy').onclick = async () => { try { await navigator.clipboard.writeText($('room-link').href); toast('Link copied. Send it to the others.'); } catch (_) { getSelection().selectAllChildren($('room-link')); } };
  $('room-leave').onclick = () => { $('room-dialog').close(); leaveRoom(); };

  window.addEventListener('resize', () => { hideTools(); fitTable(); if ($('viewer').open) renderViewer(); });
  buildTable(); renderProgress(); renderPins(); renderSound(); renderRoom(); save();
  const roomParam = (params.get('room') || '').toUpperCase();
  if (ROOMS && LeifRoom.validCode(roomParam)) { if (fetchStore(NAME_KEY)) joinRoom(roomParam, false); else openRoomDialog(roomParam); }
  else if (!hadSave) openUnpack();
  else if (state.stage === 0) setTimeout(() => tip('tools', elements.get('L1'), 'Liv’s first postcard. Hover over it (or tap it) for its tools, or double-click (double-tap) for a close-up.'), 600);
})();
