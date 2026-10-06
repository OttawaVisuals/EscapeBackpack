'use strict';
(() => {
  const G = window.HikingGame, C = window.HikingClues, L = window.HikingLater, $ = id => document.getElementById(id);
  const KEY = 'escape-backpack.hiking-opening.v1', NS = 'http://www.w3.org/2000/svg';
  let state = G.fresh(), hadSave = false, scale = 1, zoom = 1, selected = 'bottle', inspected = null, z = 2, toastTimer;
  let anchor = null, draft = null, wordDown = null, wordMoved = false, savedFocused = null;
  try { const raw = localStorage.getItem(KEY); if (raw) { state = G.restore(JSON.parse(raw)); hadSave = true; } } catch (_) { /* Keep fresh state and show storage status on the next save. */ }
  function save() {
    delete state.tidied;
    try { localStorage.setItem(KEY, JSON.stringify(state)); $('save-status').textContent = 'Saved on this browser'; }
    catch (_) { $('save-status').textContent = 'Browser save unavailable · use Save / load'; }
  }
  function toast(message) { $('toast').textContent = message; $('toast').classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => $('toast').classList.remove('show'), 4000); }
  function el(tag, className, text) { const node = document.createElement(tag); if (className) node.className = className; if (text !== undefined) node.textContent = text; return node; }
  function button(text, action, className) { const b = el('button', className, text); b.type = 'button'; b.addEventListener('click', action); return b; }
  function piece(id) {
    if (!state.pieces[id]) G.place(state, id);
    const p = state.pieces[id];
    if (!Number.isInteger(p.face)) p.face = 0;
    return p;
  }
  function note(back = false) {
    const n = el('div', 'note-paper' + (back ? ' note-back' : ''));
    if (back) return n;
    n.innerHTML = '<h3>Hello me!</h3><div class="note-copy"><p>As you know, my ADHD (Attention-Deficit/Hyperactivity Disorder) makes me <u>FORGET</u> things.</p><p>For our <u>FAMILY</u> camping trip this week, Juno asked me to <u>LOCK</u> her favourite plushy in the “special <u>BACKPACK</u>”. With the stress of the trip/packing/driving, I might not remember how to open it. But I prepared for this! Clues are hidden to <u>HELP</u> unlock the plushy.</p><p><u>BEST</u> of luck!</p><p class="signoff">Cheers!</p></div>';
    return n;
  }
  function bottle(face) {
    const b = el('div', 'bottle-art');
    b.innerHTML = '<div class="bottle-cap"></div><div class="bottle-neck"></div><div class="bottle-body"><span class="bottle-brand">TRAIL COMPANION</span></div>';
    const image = new Image(); image.src = G.stickers[face]; image.alt = 'Animal sticker on the water bottle'; image.draggable = false;
    b.querySelector('.bottle-body').append(image);
    return b;
  }
  function overlay(lines = state.lines, preview = null) {
    const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 16 15'); svg.setAttribute('preserveAspectRatio', 'none'); svg.setAttribute('aria-hidden', 'true');
    svg.classList.add('word-overlay');
    for (const [i, points] of [...lines, ...(preview ? [preview] : [])].entries()) {
      const line = document.createElementNS(NS, 'line');
      for (const [name, value] of Object.entries({ x1: points[1] + .5, y1: points[0] + .5, x2: points[3] + .5, y2: points[2] + .5 })) line.setAttribute(name, value);
      line.classList.add('word-line'); if (i === lines.length) line.classList.add('preview-line'); svg.append(line);
    }
    return svg;
  }
  function sheet(back = false) {
    if (back) { const reverse = el('div', 'sheet-paper sheet-back'); reverse.append(L.sticker('IV', '#2f6fbf')); return reverse; }
    const page = el('div', 'sheet-paper'), word = el('div', 'mini-word-grid');
    page.append(el('h3', '', 'Today’s Word Search'));
    G.grid.forEach(row => [...row].forEach(letter => word.append(el('span', '', letter)))); word.append(overlay()); page.append(word);
    page.append(el('h3', 'sudoku-heading', 'Today’s Sudoku'));
    const row = el('div', 'mini-sudoku-row'), grid = el('div', 'mini-sudoku');
    state.sudoku.forEach((v, i) => grid.append(el('span', i === 2 ? 'blue-cell' : '', v || '')));
    row.append(grid, el('p', '', 'Fill the grid with numbers from 1 to 4. Each column, each row and each of the four 2×2 blocks contains each number exactly once.'));
    page.append(row); return page;
  }
  function art(id) { const p = piece(id); return id === 'bottle' ? bottle(p.face) : id === 'note' ? note(p.face) : id === 'sheet' ? sheet(p.face) : (L.ids.includes(id) ? L : C).art(id, p.face, state); }
  const nameOf = id => id === 'satellite' && state.satellite.built >= G.satellitePages ? G.items.satellite.built : G.items[id].name;
  const kindOf = id => id === 'bottle' ? 'Three sides to explore' : id === 'satellite' && state.satellite.built >= G.satellitePages ? 'Built from the instructions' : piece(id).face ? 'Reverse side' : G.items[id].kind;
  const icons = { bottle: '↻', note: '≋', notepad: '≋', agenda: '≋', blue0: '0', orange4: '4', brown1: '1', red3: '3', cards: '♦', map: '⌖', pouch: '⊟', treasure: '◇', satellite: '✦', calculator: '±' };
  function constrain(id) {
    const p = piece(id), item = G.items[id], sideways = p.rot % 180 !== 0;
    const w = sideways ? item.h : item.w, h = sideways ? item.w : item.h;
    const dx = (item.w - w) / 2, dy = (item.h - h) / 2;
    const table = G.tableSize(state.stage);
    p.x = Math.max(15 - dx, Math.min(table.w - 15 - w - dx, p.x));
    p.y = Math.max(15 - dy, Math.min(table.h - 35 - h - dy, p.y));
  }
  function position(id) {
    const p = piece(id), node = document.querySelector(`.prop[data-id="${id}"]`); if (!node) return;
    node.style.left = p.x + 'px'; node.style.top = p.y + 'px'; node.style.transform = `rotate(${p.rot}deg)`; node.hidden = p.stowed;
  }
  function fit() {
    const frame = $('table-frame'), table = G.tableSize(state.stage); scale = zoom * Math.min((frame.clientWidth - 18) / table.w, (frame.clientHeight - 32) / table.h);
    frame.classList.toggle('zoomed', zoom > 1); $('zoom-out').disabled = zoom <= 1; $('zoom-in').disabled = zoom >= 4; $('zoom-fit').disabled = zoom === 1;
    $('table').style.width = table.w + 'px'; $('table').style.height = table.h + 'px';
    $('table').style.transform = `scale(${scale})`; $('table-fit').style.width = `${table.w * scale}px`; $('table-fit').style.height = `${table.h * scale}px`;
  }
  function select(id, raise = true) {
    selected = id;
    document.querySelectorAll('.prop').forEach(node => { node.classList.toggle('selected', node.dataset.id === id); if (raise && node.dataset.id === id) node.style.zIndex = ++z; });
    $('selected-name').textContent = id ? nameOf(id) : 'Your camp table';
    $('selected-kind').textContent = id ? kindOf(id) : 'Choose an item from your finds';
    for (const key of ['inspect', 'flip', 'rotate', 'stow']) $(key).disabled = !id;
    $('flip').disabled = !id || G.items[id].faces < 2;
    $('flip').innerHTML = (id === 'bottle' ? 'Turn' : 'Flip') + ' <kbd>F</kbd>';
    document.querySelectorAll('.shelf-item').forEach(node => node.setAttribute('aria-pressed', String(node.dataset.id === id)));
  }
  const SHELF_GROUPS = [
    ['Notes & papers', ['note', 'sheet', 'grandparents', 'newspaper', 'iss', 'periodic', 'equation', 'instructions', 'notepad', 'agenda', 'cards', 'map']],
    ['Lego', ['blue0', 'orange4', 'brown1', 'red3', 'flat', 'square', 'cube', 'satellite']],
    ['Bags of Lego parts', ['hobbies', 'jobs', 'pets', 'faces', 'hair', 'names']]
  ];
  const shelfGroup = id => (SHELF_GROUPS.find(([, ids]) => ids.includes(id)) || ['Things'])[0];
  const shelfOpen = new Set(); let shelfStage = null;
  function drawShelf(entries) {
    if (shelfStage !== state.stage) { shelfOpen.clear(); for (const id of state.stage ? G.locks[state.stage - 1].releases : ['bottle']) shelfOpen.add(shelfGroup(id)); shelfStage = state.stage; }
    const groups = new Map([...SHELF_GROUPS.map(([name]) => [name, []]), ['Things', []]]);
    for (const [id, node] of entries) groups.get(shelfGroup(id)).push(node);
    $('shelf').replaceChildren();
    for (const [name, nodes] of groups) {
      if (!nodes.length) continue;
      const open = shelfOpen.has(name), group = el('div', 'shelf-group'), toggle = button('', () => { open ? shelfOpen.delete(name) : shelfOpen.add(name); drawShelf(entries); }, 'group-toggle');
      toggle.setAttribute('aria-expanded', String(open)); toggle.setAttribute('aria-label', `${name}: ${nodes.length}`);
      toggle.append(el('span', 'chev', '›'), el('span', '', name), el('span', 'n', String(nodes.length)));
      group.append(toggle); if (open) group.append(...nodes); $('shelf').append(group);
    }
  }
  function drawTable() {
    $('pieces').replaceChildren(); const shelfEntries = [];
    for (const id of G.available(state.stage, state.found)) {
      const item = G.items[id], p = piece(id), node = el('div', 'prop');
      node.dataset.id = id; node.tabIndex = 0; node.setAttribute('role', 'button'); node.setAttribute('aria-label', `${nameOf(id)}. Enter to inspect; F to turn; R to rotate; arrow keys to move.`);
      node.style.width = `${item.w}px`; node.style.height = `${item.h}px`;
      const artwork = el('div', 'object-art'); artwork.append(art(id));
      const caption = el('div', 'prop-caption'); caption.append(el('span', '', nameOf(id)));
      node.append(artwork, caption); $('pieces').append(node); constrain(id); position(id);
      node.addEventListener('pointerdown', event => startDrag(event, id, node));
      node.addEventListener('dblclick', () => inspect(id));
      node.addEventListener('focus', () => select(id));
      node.addEventListener('keydown', event => {
        if (event.key.startsWith('Arrow')) {
          event.preventDefault(); const d = event.shiftKey ? 25 : 5;
          p.x += event.key === 'ArrowRight' ? d : event.key === 'ArrowLeft' ? -d : 0;
          p.y += event.key === 'ArrowDown' ? d : event.key === 'ArrowUp' ? -d : 0;
          constrain(id); position(id); save();
        }
      });
      const shelf = button('', () => { piece(id).stowed = false; drawTable(); select(id); save(); }, 'shelf-item' + (p.stowed ? ' stowed' : ''));
      shelf.dataset.id = id;
      shelf.append(el('span', 'shelf-icon', icons[id] || (item.bag ? '⁘' : '▦')));
      const label = el('span', '', nameOf(id)); label.append(el('small', '', p.stowed ? 'Put away · click to bring back' : 'On the table')); shelf.append(label); shelfEntries.push([id, shelf]);
    }
    drawShelf(shelfEntries);
    $('item-count').textContent = String(G.available(state.stage, state.found).length).padStart(2, '0');
    if (!G.available(state.stage, state.found).includes(selected) || (selected && piece(selected).stowed)) selected = null;
    select(selected, false); fit();
  }
  function startDrag(event, id, node) {
    if (event.button !== 0) return;
    select(id); node.focus({ preventScroll: true }); node.setPointerCapture(event.pointerId);
    const p = piece(id), start = { x: event.clientX, y: event.clientY, px: p.x, py: p.y }; let moved = false;
    function move(e) {
      const dx = (e.clientX - start.x) / scale, dy = (e.clientY - start.y) / scale;
      if (Math.abs(dx) + Math.abs(dy) < 4 && !moved) return;
      moved = true; node.classList.add('dragging'); p.x = start.px + dx; p.y = start.py + dy; constrain(id); position(id);
    }
    function end(e) { node.classList.remove('dragging'); node.removeEventListener('pointermove', move); node.removeEventListener('pointerup', end); node.removeEventListener('pointercancel', end); if (node.hasPointerCapture(e.pointerId)) node.releasePointerCapture(e.pointerId); save(); }
    node.addEventListener('pointermove', move); node.addEventListener('pointerup', end); node.addEventListener('pointercancel', end);
  }
  function turn(id, direction = 1) {
    if (!id || G.items[id].faces < 2) return; const p = piece(id); p.face = (p.face + direction + G.items[id].faces) % G.items[id].faces;
    const freed = id === 'grandparents' && p.face === 1 && G.discover(state, 'newspaper'), tidied = state.tidied;
    drawTable(); if (inspected === id) renderInspector(); save();
    if (freed) toast(`${tidied ? 'The table was rearranged to make room. ' : ''}A newspaper clipping was tucked inside the card. It’s on your table now.`);
  }
  function rotate() { if (!selected) return; const p = piece(selected); p.rot = (p.rot + 90) % 360; constrain(selected); position(selected); save(); }
  function inspect(id) {
    if (!G.available(state.stage, state.found).includes(id)) return;
    savedFocused = document.activeElement; inspected = id; select(id); anchor = draft = null; renderInspector(); $('inspector').showModal();
  }
  function closeInspector() { $('inspector').close(); }
  $('inspector').addEventListener('close', () => { if ($('inspector').open) return; inspected = null; anchor = draft = wordDown = null; drawTable(); savedFocused?.isConnected && savedFocused.focus({ preventScroll: true }); });
  function renderInspector() {
    const id = inspected, item = G.items[id], p = piece(id); $('inspector-title').textContent = nameOf(id); $('inspector-kind').textContent = item.origin;
    $('inspect-flip').hidden = item.faces < 2;
    $('inspect-flip').textContent = id === 'bottle' ? 'Turn bottle ↻' : id === 'grandparents' ? (p.face ? 'Close card' : 'Open card') : p.face ? 'Show front' : 'Turn over';
    $('inspector-content').replaceChildren();
    if (id === 'bottle') {
      const view = el('div', 'bottle-view'), display = el('div', 'bottle-display'); display.append(bottle(p.face));
      const info = el('div', 'bottle-information'); info.append(el('p', 'eyebrow', 'LOOK A LITTLE CLOSER'), el('h3', '', 'Something familiar.'));
      info.append(el('p', '', 'The bottle has a different animal sticker on each side. Turn it to see them all.'));
      const detail = el('div', 'bottle-detail'), image = new Image(); image.src = G.stickers[p.face]; image.alt = 'Close-up of the original animal sticker'; detail.append(image); info.append(detail, el('p', 'sticker-caption', 'Sticker close-up'));
      const controls = el('div', 'turn-controls');
      const prev = button('←', () => turn(id, -1)); prev.setAttribute('aria-label', 'Previous side');
      const next = button('→', () => turn(id)); next.setAttribute('aria-label', 'Next side');
      controls.append(prev, el('span', '', `${p.face + 1} / 3`), next); info.append(controls); view.append(display, info); $('inspector-content').append(view);
    } else if (id === 'note') { const view = el('div', 'note-view'); view.append(note(p.face)); $('inspector-content').append(view); }
    else if (id === 'sheet') {
      if (p.face) { const view = el('div', 'paper-back-view'); view.append(sheet(true)); $('inspector-content').append(view); }
      else buildPuzzles();
    } else if (L.ids.includes(id)) $('inspector-content').append(L.inspect(id, p.face, state, { save, toast, refresh: renderInspector, redraw: drawTable }));
    else $('inspector-content').append(C.inspect(id, p.face, state, save));
  }
  function wordPoint(event, board) {
    const box = board.getBoundingClientRect();
    return [Math.max(0, Math.min(14, Math.floor((event.clientY - box.top) / box.height * 15))), Math.max(0, Math.min(15, Math.floor((event.clientX - box.left) / box.width * 16)))];
  }
  function showLines() {
    const board = $('word-board'); if (!board) return;
    board.querySelector('svg')?.remove(); board.append(overlay(state.lines, draft));
    board.querySelectorAll('.letter-cell').forEach((node, i) => node.classList.toggle('anchor', !!anchor && Math.floor(i / 16) === anchor[0] && i % 16 === anchor[1]));
    $('line-count').textContent = `${state.lines.length} ${state.lines.length === 1 ? 'mark' : 'marks'}`;
    $('undo-mark').disabled = !state.lines.length; $('clear-marks').disabled = !state.lines.length;
  }
  function finishLine(start, end) {
    if (G.markLine(state, [...start, ...end])) { anchor = draft = null; $('word-status').textContent = 'Mark saved. Select the same endpoints again to erase it.'; save(); }
    else { anchor = start; draft = null; $('word-status').textContent = 'Choose a horizontal, vertical or diagonal line.'; }
    showLines();
  }
  function buildPuzzles() {
    anchor = draft = wordDown = null;
    const workbench = el('div', 'puzzle-workbench'), reference = el('aside', 'reference-note');
    reference.append(el('p', 'eyebrow', 'KEEP YOUR NOTE NEARBY'), note());
    const page = el('section', 'puzzle-page'); page.append(el('h3', '', 'Today’s Word Search'), el('p', 'control-help', 'Drag from first to last letter, or click the two ends. Markings can go in any direction.'));
    const board = el('div', 'word-board'); board.id = 'word-board'; board.setAttribute('aria-label', 'Word search, 15 rows and 16 columns. Use arrow keys to move, Enter to select each end.');
    const cells = el('div', 'word-cells');
    G.grid.forEach((row, r) => [...row].forEach((letter, c) => {
      const cell = el('button', 'letter-cell', letter); cell.type = 'button'; cell.dataset.row = r; cell.dataset.col = c; cell.tabIndex = r === 0 && c === 0 ? 0 : -1;
      cell.setAttribute('aria-label', `${letter}, row ${r + 1}, column ${c + 1}`);
      cell.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); if (anchor) finishLine(anchor, [r, c]); else { anchor = [r, c]; $('word-status').textContent = 'Start selected. Choose the other end.'; showLines(); } }
        if (event.key.startsWith('Arrow')) {
          event.preventDefault(); const nr = Math.max(0, Math.min(14, r + (event.key === 'ArrowDown' ? 1 : event.key === 'ArrowUp' ? -1 : 0))), nc = Math.max(0, Math.min(15, c + (event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0)));
          cells.querySelectorAll('button').forEach(b => b.tabIndex = -1); const next = cells.children[nr * 16 + nc]; next.tabIndex = 0; next.focus();
        }
      });
      cells.append(cell);
    }));
    board.append(cells);
    board.addEventListener('pointerdown', event => {
      if (event.button !== 0) return; event.preventDefault(); wordDown = wordPoint(event, board); wordMoved = false; board.setPointerCapture(event.pointerId);
      const cell = cells.children[wordDown[0] * 16 + wordDown[1]]; cells.querySelectorAll('button').forEach(b => b.tabIndex = -1); cell.tabIndex = 0; cell.focus({ preventScroll: true });
    });
    board.addEventListener('pointermove', event => {
      if (!wordDown) return; const end = wordPoint(event, board); if (end[0] !== wordDown[0] || end[1] !== wordDown[1]) wordMoved = true;
      draft = G.validLine([...wordDown, ...end]) ? [...wordDown, ...end] : null; showLines();
    });
    board.addEventListener('pointerup', event => {
      if (!wordDown) return; const end = wordPoint(event, board);
      if (wordMoved) finishLine(wordDown, end);
      else if (anchor) { if (anchor[0] === end[0] && anchor[1] === end[1]) { anchor = null; $('word-status').textContent = 'Selection cancelled.'; } else finishLine(anchor, end); }
      else { anchor = end; $('word-status').textContent = 'Start selected. Click the other end of your line.'; }
      wordDown = draft = null; if (board.hasPointerCapture(event.pointerId)) board.releasePointerCapture(event.pointerId); showLines();
    });
    board.addEventListener('pointercancel', () => { wordDown = draft = null; showLines(); });
    page.append(board);
    const controls = el('div', 'puzzle-controls');
    const undo = button('Undo last mark', () => { state.lines.pop(); save(); showLines(); $('word-status').textContent = 'Last mark removed.'; }); undo.id = 'undo-mark';
    let clearArmed = false;
    const clear = button('Clear markings', () => {
      if (!clearArmed) { clearArmed = true; clear.textContent = 'Confirm clear'; $('word-status').textContent = 'Click Confirm clear to erase every marking. Sudoku entries are kept.'; return; }
      state.lines = []; anchor = draft = null; clearArmed = false; save(); showLines(); clear.textContent = 'Clear markings'; $('word-status').textContent = 'Markings cleared.';
    }); clear.id = 'clear-marks';
    const count = el('span'); count.id = 'line-count'; controls.append(undo, clear, count); page.append(controls);
    const status = el('p'); status.id = 'word-status'; status.setAttribute('role', 'status'); page.append(status);
    const section = el('section', 'sudoku-section'); section.append(el('h3', '', 'Today’s Sudoku'));
    const row = el('div', 'sudoku-row'), sudoku = el('div', 'sudoku-grid'); sudoku.setAttribute('role', 'group'); sudoku.setAttribute('aria-label', 'Sudoku, four rows and four columns');
    state.sudoku.forEach((value, i) => {
      const input = el('input', 'sudoku-cell' + (i === 2 ? ' blue-cell' : '')); input.type = 'text'; input.inputMode = 'numeric'; input.maxLength = 1; input.pattern = '[1-4]'; input.autocomplete = 'off'; input.value = value || ''; input.readOnly = !!G.givens[i]; input.dataset.cell = i;
      input.setAttribute('aria-label', `Sudoku row ${Math.floor(i / 4) + 1}, column ${i % 4 + 1}${i === 2 ? ', blue cell' : ''}${G.givens[i] ? ', given ' + value : ''}`);
      if (input.readOnly) input.tabIndex = -1;
      input.addEventListener('focus', () => { if (!input.readOnly) input.select(); });
      input.addEventListener('input', () => { input.value = input.value.replace(/[^1-4]/g, '').slice(-1); state.sudoku[i] = input.value ? Number(input.value) : 0; save(); });
      input.addEventListener('keydown', event => {
        if (!event.key.startsWith('Arrow')) return; event.preventDefault(); const step = event.key === 'ArrowLeft' ? -1 : event.key === 'ArrowRight' ? 1 : event.key === 'ArrowUp' ? -4 : 4;
        let next = i + step; while (next >= 0 && next < 16 && G.givens[next]) next += step;
        if (next >= 0 && next < 16) sudoku.children[next].focus();
      });
      sudoku.append(input);
    });
    const rules = el('div', 'sudoku-rules'); rules.innerHTML = '<p>Fill the grid with numbers from <b>1 to 4</b>.</p><p>Each column, each row and each of the four 2×2 blocks contains each number exactly once.</p><p class="small">Click an empty cell and type. Backspace erases a guess. Printed numbers stay fixed.</p>';
    row.append(sudoku, rules); section.append(row); page.append(section); workbench.append(reference, page); $('inspector-content').append(workbench); showLines();
  }
  /* The padlock's wheels: digits or letters. Each wheel has a ▲ (next: 5 → 6) and a ▼ (back) button; dragging up
     or scrolling also turns it. With the keyboard, type the character (focus moves on) or use ↑ ↓; ← → move between wheels. */
  const DIGITS = '0123456789', LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  let dialChars = DIGITS, dialVals = [], dialStage = null;
  const dialWheels = () => [...$('dial').querySelectorAll('.wheel')];
  function buildDial(length, letters) {
    dialChars = letters ? LETTERS : DIGITS; dialVals = Array(length).fill(0);
    $('dial').setAttribute('aria-label', `${letters ? 'Letter' : 'Number'} wheels: ${length}`);
    $('dial').replaceChildren(...dialVals.map((_, i) => {
      const w = button('', () => {}, 'wheel'); w.type = 'button';
      w.setAttribute('role', 'spinbutton'); w.setAttribute('aria-label', `Wheel ${i + 1} of ${length}`);
      w.append(el('span', 'prev'), el('span', 'cur'), el('span', 'next')); w.firstChild.setAttribute('aria-hidden', 'true'); w.lastChild.setAttribute('aria-hidden', 'true');
      wireWheel(w, i);
      const turnButton = (d, label) => {
        const b = button('', () => { turnWheel(i, d); w.focus({ preventScroll: true }); }, 'turn'); b.type = 'button'; b.tabIndex = -1;
        b.setAttribute('aria-label', `Wheel ${i + 1}: ${label}`); b.innerHTML = '<svg viewBox="0 0 12 8" aria-hidden="true"><path d="M1 7 6 2l5 5"/></svg>'; return b;
      };
      const col = el('div', 'wheel-col'); col.append(turnButton(1, 'next'), w, turnButton(-1, 'back')); return col;
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
  function turnWheel(i, d) {
    const n = dialChars.length; dialVals[i] = ((dialVals[i] + d) % n + n) % n; paintWheel(i, d);
    if ($('lock-message').className === 'error') { $('lock-message').textContent = ''; $('lock-message').className = ''; }
  }
  function setDial(i, ch) { const k = dialChars.indexOf(ch.toUpperCase()); if (k < 0) return false; dialVals[i] = k; paintWheel(i, 1); return true; }
  function wireWheel(w, i) {
    let drag = null;
    w.addEventListener('pointerdown', e => { if (e.button !== 0) return; try { w.setPointerCapture(e.pointerId); } catch (_) { /* pointer gone */ } drag = { last: e.clientY }; });
    w.addEventListener('pointermove', e => { if (!drag) return; const dy = e.clientY - drag.last; if (Math.abs(dy) >= 14) { turnWheel(i, dy < 0 ? 1 : -1); drag.last = e.clientY; } });
    w.addEventListener('pointerup', () => { drag = null; }); w.addEventListener('pointercancel', () => { drag = null; });
    w.addEventListener('wheel', e => { e.preventDefault(); turnWheel(i, e.deltaY > 0 ? 1 : -1); }, { passive: false });
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
  // Hints: Hint 1, 2, 3 and Solution open independently; the save keeps the furthest one opened.
  let hintsStage = null; const hintsOpen = new Set();
  function drawHints() {
    if (state.stage >= G.locks.length) { $('hints').replaceChildren(); hintsStage = null; return; }
    if (hintsStage !== state.stage) { hintsOpen.clear(); hintsStage = state.stage; }
    const labels = ['Hint 1', 'Hint 2', 'Hint 3', 'Solution'], row = el('div', 'hint-tabs');
    const texts = G.locks[state.stage].hints.map((text, i) => { const p = el('p', 'hint'); p.id = `hint-${i}`; p.hidden = !hintsOpen.has(i); p.append(el('b', '', `${labels[i]} · `), text); return p; });
    labels.forEach((label, i) => {
      const b = button(label, () => {
        const open = !hintsOpen.has(i); if (open) hintsOpen.add(i); else hintsOpen.delete(i);
        texts[i].hidden = !open; b.setAttribute('aria-expanded', String(open));
        if (open && state.hints[state.stage] < i + 1) { state.hints[state.stage] = i + 1; save(); }
      }, i === 3 ? 'solution' : '');
      b.type = 'button'; b.setAttribute('aria-expanded', String(hintsOpen.has(i))); b.setAttribute('aria-controls', `hint-${i}`); row.append(b);
    });
    $('hints').replaceChildren(row, ...texts);
  }
  function drawProgress() {
    $('progress-count').textContent = `${state.stage} / ${G.locks.length}`;
    $('chapter').textContent = state.stage >= G.locks.length ? 'ALL LOCKS OPEN' : `LOCK ${state.stage + 1} OF ${G.locks.length}`;
    if ($('progress').children.length !== G.locks.length) {
      $('progress').replaceChildren();
      G.locks.forEach((lock, i) => { const row = el('li'), label = el('span', 'sr-only', lock.name); label.append(el('small', '', 'Locked')); row.append(el('span', 'step-number', i + 1), label); $('progress').append(row); });
    }
    [...$('progress').children].forEach((node, i) => {
      const status = i < state.stage ? 'Opened' : i === state.stage ? 'Your next lock' : 'Locked';
      node.className = i < state.stage ? 'done' : i === state.stage ? 'current' : ''; node.title = `Lock ${i + 1} · ${G.locks[i].name} · ${status}`;
      node.querySelector('.step-number').textContent = i < state.stage ? '✓' : i + 1; node.querySelector('small').textContent = ` · ${status}`;
    });
    $('lock-panel').hidden = state.stage >= G.locks.length; $('complete').hidden = state.stage < G.locks.length;
    if (state.stage < G.locks.length) {
      const lock = G.locks[state.stage]; $('lock-number').textContent = `LOCK ${String(state.stage + 1).padStart(2, '0')}`; $('lock-name').textContent = lock.name;
      $('lock-prompt').textContent = lock.prompt;
      $('combination-label').textContent = `${lock.answer.length === 4 ? 'FOUR' : 'THREE'}-${lock.letters ? 'LETTER' : 'DIGIT'} COMBINATION`;
      if (dialStage !== state.stage) { buildDial(lock.answer.length, !!lock.letters); dialStage = state.stage; $('padlock').classList.remove('unlocked', 'wrong'); }
    }
    drawHints();
  }
  let opening = false;
  $('lock-form').addEventListener('submit', async event => {
    event.preventDefault(); if (opening) return; const value = $('combination').value;
    if (!G.unlock(state, value)) {
      $('lock-message').textContent = 'Still locked. Take another look at your clues.'; $('lock-message').className = 'error';
      const pad = $('padlock'); pad.classList.remove('wrong'); void pad.offsetWidth; pad.classList.add('wrong'); return;
    }
    opening = true; $('padlock').classList.add('unlocked'); $('lock-message').className = ''; $('lock-message').textContent = 'Click! The lock springs open.';
    await new Promise(r => setTimeout(r, matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 420)); opening = false;
    const opened = G.locks[state.stage - 1];
    const tidied = state.tidied;
    $('combination').value = ''; $('lock-message').textContent = ''; $('lock-message').className = ''; selected = opened.selected; drawTable(); drawProgress(); save();
    if (tidied) toast('The table was rearranged to make room for the new items.');
    $('arrival-label').textContent = `LOCK ${state.stage} OPEN`;
    $('arrival-title').textContent = opened.title; $('arrival-text').textContent = opened.message;
    $('arrival-close').textContent = state.stage < G.locks.length ? 'Explore the new clues →' : 'Back to the table →'; $('arrival').showModal();
  });
  $('notes').value = state.notes; $('notes').addEventListener('input', () => { state.notes = $('notes').value; save(); });
  $('inspect').addEventListener('click', () => selected && inspect(selected));
  $('flip').addEventListener('click', () => turn(selected)); $('rotate').addEventListener('click', rotate);
  $('stow').addEventListener('click', () => { if (selected) { piece(selected).stowed = true; selected = null; drawTable(); save(); } });
  $('tidy').addEventListener('click', () => {
    G.layout(state); selected = null; drawTable(); save(); toast('Table tidied. Everything is back on the table and your puzzle work is kept.');
  });
  const setZoom = z => { zoom = Math.max(1, Math.min(4, Math.round(z * 100) / 100)); fit(); };
  $('zoom-in').addEventListener('click', () => setZoom(zoom * 1.25)); $('zoom-out').addEventListener('click', () => setZoom(zoom / 1.25)); $('zoom-fit').addEventListener('click', () => setZoom(1));
  $('fullscreen').addEventListener('click', () => { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen?.().catch(() => toast('Full screen is not available here.')); });
  document.addEventListener('fullscreenchange', () => { $('fullscreen').textContent = document.fullscreenElement ? 'Exit full screen' : 'Full screen'; });
  $('inspect-flip').addEventListener('click', () => turn(inspected)); $('close-inspector').addEventListener('click', closeInspector);
  // Game menu in the masthead (save or load a copy, start again).
  const closeMenu = () => { $('game-menu').hidden = true; $('game-btn').setAttribute('aria-expanded', 'false'); };
  $('game-btn').addEventListener('click', e => { e.stopPropagation(); const open = $('game-menu').hidden; $('game-menu').hidden = !open; $('game-btn').setAttribute('aria-expanded', String(open)); });
  $('game-menu').addEventListener('click', closeMenu);
  document.addEventListener('click', e => { if (!e.target.closest('.menu-wrap')) closeMenu(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('game-menu').hidden) { closeMenu(); $('game-btn').focus(); } });
  $('how-to').addEventListener('click', () => $('intro').showModal()); $('begin').addEventListener('click', () => { $('intro').close(); save(); });
  $('arrival-close').addEventListener('click', () => $('arrival').close());
  $('restart').addEventListener('click', () => $('restart-dialog').showModal());
  $('restart-confirm').addEventListener('click', () => { state = G.fresh(); selected = 'bottle'; $('notes').value = ''; $('combination').value = ''; $('lock-message').textContent = ''; $('restart-dialog').close(); dialStage = null; drawTable(); drawProgress(); save(); $('intro').showModal(); });
  document.querySelectorAll('[data-close]').forEach(b => b.addEventListener('click', () => b.closest('dialog').close()));
  $('save-copy').addEventListener('click', () => { $('save-text').value = JSON.stringify(state, null, 2); $('save-result').textContent = ''; $('save-dialog').showModal(); });
  $('select-save').addEventListener('click', () => { $('save-text').focus(); $('save-text').select(); $('save-result').textContent = 'Press Ctrl+C (or ⌘C) to copy. Keep the text in a file or note.'; });
  $('download-save').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' }), url = URL.createObjectURL(blob), a = el('a');
    a.href = url; a.download = 'hiking-backpack-save.json'; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000); $('save-result').textContent = 'Download requested. If no file appears, use Select text to keep a copy.';
  });
  function loadText(text) {
    try { if (text.length > 100000) throw new Error('This save is too large.'); const incoming = G.restore(JSON.parse(text)); state = incoming; selected = 'bottle'; $('notes').value = state.notes; $('combination').value = ''; $('lock-message').textContent = ''; dialStage = null; drawTable(); drawProgress(); save(); $('save-dialog').close(); toast('Your Hiking game is restored.'); }
    catch (_) { $('save-result').textContent = 'Could not load this copy. Choose a valid Hiking opening save.'; }
  }
  $('load-text').addEventListener('click', () => loadText($('save-text').value));
  $('choose-save').addEventListener('click', () => { $('save-file').value = ''; $('save-file').click(); });
  $('save-file').addEventListener('change', async () => { const file = $('save-file').files[0]; if (!file) return; if (file.size > 100000) { $('save-result').textContent = 'This save file is too large.'; return; } try { loadText(await file.text()); } catch (_) { $('save-result').textContent = 'Could not read this file.'; } });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && $('inspector').open && (anchor || wordDown)) { event.preventDefault(); anchor = draft = wordDown = null; showLines(); $('word-status').textContent = 'Selection cancelled.'; return; }
    if (event.defaultPrevented || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName) || event.ctrlKey || event.metaKey || event.altKey) return;
    if (document.querySelector('dialog[open]')) { if ($('inspector').open && event.key.toLowerCase() === 'f') { event.preventDefault(); turn(inspected); } return; }
    if (event.key.toLowerCase() === 'f') { event.preventDefault(); turn(selected); }
    if (event.key.toLowerCase() === 'r') { event.preventDefault(); rotate(); }
    if (event.key === 'Enter' && document.activeElement?.classList.contains('prop')) { event.preventDefault(); inspect(selected); }
    if (event.key === '+' || event.key === '=') { event.preventDefault(); setZoom(zoom * 1.25); }
    if (event.key === '-') { event.preventDefault(); setZoom(zoom / 1.25); }
    if (event.key === '0') { event.preventDefault(); setZoom(1); }
  });
  new ResizeObserver(fit).observe($('table-frame'));
  drawTable(); drawProgress();
  if (new URLSearchParams(location.search).get('design') === '1' && $('design-notes')) { $('design-notes').showModal(); $('design-notes').scrollTop = 0; }
  else if (!hadSave) $('intro').showModal();
  else save();
})();
