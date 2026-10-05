/* Player props for locks 3–4. Images are extracted/copied from the physical game.
   The newspaper crop comes directly from NewsClipping.docx, not an answer crop.
   The backs carry two of the lock 5 values, as in the physical solution: v on the clipping, GM on the calculator. */
(function (root) {
  'use strict';
  const G = root.HikingGame;
  const element = (tag, cls, text) => { const node = document.createElement(tag); if (cls) node.className = cls; if (text !== undefined) node.textContent = text; return node; };
  const image = (src, alt) => { const node = new Image(); node.src = `assets/${src}`; node.alt = alt; node.draggable = false; return node; };
  const issText = 'I was looking at the stars tonight and saw something that seemed to defy the laws of KNoWN PHYSiCs. Upon closer look, it was actually the International Space Station. We decided to create our own little satellite made out of Legos.';
  function grandparents(face) {
    const card = element('div', 'grandparents-card' + (face ? ' card-inside' : ''));
    if (!face) {
      card.innerHTML = '<div class="card-border"><span class="card-sprig" aria-hidden="true">❧</span><h3>Thank<br><em>You!</em></h3><p>To Juno</p><span class="card-sprig bottom" aria-hidden="true">❧</span></div>';
      return card;
    }
    card.innerHTML = '<h3>Hello Juno!</h3><div class="grandparents-message"><p>Thank you again for taking us on our first escape room last week! We had so much fun! So much so, that we created our own puzzles out of Legos.</p><p>Your dad will give them to you one at a time. Start with the blue square, then the brown flatter one and you can end with the big cube. For the first two, you will have to use the piece on top to help you solve them.</p><p>PS: Look what we found: your dog is famous! He was featured in today’s journal. Such a good boy!</p><p class="card-signature">Cheers,<br>Gran and Pops</p></div>';
    const drawings = element('div', 'lego-sketches');
    drawings.append(image('lego-square.png', 'Drawing of the small square Lego puzzle'), image('lego-flat.png', 'Drawing of the flat Lego puzzle'), image('lego-cube.png', 'Drawing of the cube Lego puzzle'));
    card.append(drawings); return card;
  }
  function newspaper() {
    const paper = element('article', 'news-paper');
    paper.append(element('h3', '', 'Good Boy Given Award for Helping Geese'));
    const photo = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    // Word srcRect: left 20.862%, top 24.010%, right 22.139%, bottom 15.495%.
    // The source image also has a revealing headline outside this printed crop.
    photo.setAttribute('viewBox', '191.09592 219.9316 522.11084 554.1342'); photo.classList.add('news-photo'); photo.setAttribute('role', 'img'); photo.setAttribute('aria-label', 'Photograph of the husky wearing a collar and name tag');
    const pic = document.createElementNS(photo.namespaceURI, 'image'); pic.setAttribute('href', 'assets/newspaper-dog.jpg'); pic.setAttribute('width', '916'); pic.setAttribute('height', '916'); photo.append(pic); paper.append(photo);
    paper.append(element('p', '', 'A white Siberian Husky has been given an award by the mayor for helping a group of Canada Geese cross the local main road.'), element('p', '', 'The nine-year old Husky was observed herding a group of Geese at a crosswalk so they could reach the local river safely.'));
    return paper;
  }
  // A handwritten value on the back of a prop.
  function scribbledBack(cls, text) { const back = element('div', `scribbled-back ${cls}`); back.append(element('p', 'scribbled-value', text)); return back; }
  function iss() {
    const paper = element('article', 'iss-paper'); paper.append(image('iss-drawing.png', 'Drawing of the International Space Station'), element('p', '', issText)); return paper;
  }
  function calculatorCover(state) {
    const body = element('div', 'calculator-cover'); body.append(element('p', 'calc-brand', 'POCKET CALCULATOR'), element('div', 'calc-screen', state.calculator.result || '0'));
    const keys = element('div', 'calc-mini-keys'); 'C ( ) ⌫ 7 8 9 ÷ 4 5 6 × 1 2 3 − 0 . = +'.split(' ').forEach(key => keys.append(element('span', key === '=' ? 'equals' : '', key))); body.append(keys); return body;
  }
  function art(id, face, state) {
    if (id === 'grandparents') return grandparents(face);
    if (id === 'newspaper') return face ? scribbledBack('news-back', `v = ${G.values.v}`) : newspaper();
    if (id === 'iss') return iss();
    if (id === 'periodic') { const sheet = element('div', 'periodic-sheet'); sheet.append(image('periodic-table.png', 'Periodic table of the elements')); return sheet; }
    if (id === 'calculator') return face ? scribbledBack('calc-back', `GM = ${G.values.GM}`) : calculatorCover(state);
  }
  function calculator(state, onChange) {
    const body = element('form', 'working-calculator'); body.setAttribute('aria-label', 'Pocket calculator');
    body.append(element('p', 'calc-brand', 'POCKET CALCULATOR'));
    const label = element('label', 'calc-label', 'Calculation'), input = element('input', 'calc-expression'); input.type = 'text'; input.inputMode = 'text'; input.maxLength = 160; input.autocomplete = 'off'; input.spellcheck = false; input.setAttribute('aria-label', 'Calculation'); input.placeholder = 'Type a calculation'; input.value = state.calculator.expression; label.append(input); body.append(label);
    const result = element('output', 'calc-result', state.calculator.result || '0'); result.setAttribute('aria-label', 'Result'); result.setAttribute('aria-live', 'polite'); body.append(result);
    const status = element('p', 'calc-status'); status.setAttribute('role', 'status'); body.append(status);
    function update() { state.calculator.expression = input.value; state.calculator.result = ''; result.textContent = '—'; status.textContent = ''; onChange(); }
    function solve() {
      try { state.calculator.result = String(G.calculate(input.value)); result.textContent = state.calculator.result; status.textContent = ''; onChange(); }
      catch (error) { result.textContent = '—'; state.calculator.result = ''; status.textContent = error.message; onChange(); }
    }
    input.addEventListener('input', () => { input.value = input.value.replace(/[^\d+\-*/×÷−().,\s]/g, ''); update(); });
    body.addEventListener('submit', event => { event.preventDefault(); solve(); });
    const keys = element('div', 'calc-keypad');
    for (const key of ['C','(',')','⌫','7','8','9','÷','4','5','6','×','1','2','3','−','0','.','=','+']) {
      const b = element('button', key === '=' ? 'primary' : '', key); b.type = 'button';
      if (key === 'C') b.setAttribute('aria-label', 'Clear calculation'); if (key === '⌫') b.setAttribute('aria-label', 'Delete last character'); if (key === '=') b.setAttribute('aria-label', 'Calculate result');
      b.addEventListener('click', () => {
        if (key === '=') { solve(); return; }
        const start = input.selectionStart ?? input.value.length, end = input.selectionEnd ?? input.value.length;
        if (key === 'C') input.value = '';
        else if (key === '⌫') input.value = input.value.slice(0, start === end ? Math.max(0, start - 1) : start) + input.value.slice(end);
        else input.value = (input.value.slice(0, start) + key + input.value.slice(end)).slice(0, 160);
        update(); input.focus(); const next = key === 'C' ? 0 : key === '⌫' ? Math.max(0, start - (start === end ? 1 : 0)) : start + 1; input.setSelectionRange(next, next);
      }); keys.append(b);
    }
    body.append(keys, element('p', 'calc-help', 'Type or use the keys. Enter calculates.')); return body;
  }
  function zoomControls(onZoom) {
    let zoom = 1;
    const bar = element('div', 'document-tools'), label = element('span', '', '100%'); label.setAttribute('aria-live', 'polite');
    const minus = element('button', '', '−'), plus = element('button', '', '+'), fit = element('button', '', 'Fit');
    minus.type = plus.type = fit.type = 'button'; minus.setAttribute('aria-label', 'Zoom out'); plus.setAttribute('aria-label', 'Zoom in'); fit.setAttribute('aria-label', 'Fit to view');
    const apply = value => { zoom = Math.min(3, Math.max(.25, value)); label.textContent = `${Math.round(zoom * 100)}%`; minus.disabled = zoom <= .25; plus.disabled = zoom >= 3; onZoom(zoom); };
    minus.addEventListener('click', () => apply(zoom - .25)); plus.addEventListener('click', () => apply(zoom + .25));
    bar.append(element('span', 'zoom-instruction', 'Zoom to inspect · scroll to explore'), minus, label, plus, fit);
    return { bar, fit, apply };
  }
  function documentView(id, face, state) {
    const view = element('div', 'document-view'), scroll = element('div', 'document-scroll'), stage = element('div', 'document-stage'), page = element('div', 'document-page');
    const size = id === 'grandparents' ? {w:590,h:face ? 735 : 520} : id === 'newspaper' ? {w:530,h:770} : id === 'calculator' ? {w:320,h:460} : {w:550,h:630};
    page.style.width = `${size.w}px`; page.style.height = `${size.h}px`; page.append(art(id, face, state)); stage.append(page); scroll.append(stage);
    const controls = zoomControls(zoom => { stage.style.width = `${size.w * zoom}px`; stage.style.height = `${size.h * zoom}px`; page.style.transform = `scale(${zoom})`; });
    function fit() { controls.apply(Math.min(1, (scroll.clientWidth - 42) / size.w, (scroll.clientHeight - 38) / size.h)); }
    controls.fit.addEventListener('click', fit); view.append(controls.bar, scroll); requestAnimationFrame(fit); return view;
  }
  function periodicView(state, onChange) {
    const view = element('div', 'periodic-workbench'), side = element('aside', 'science-reference');
    side.append(element('p', 'eyebrow', 'YOUR ISS NOTE'), element('p', 'science-note', issText));
    const calc = element('details', 'inline-calculator'); calc.append(element('summary', '', 'Use the pocket calculator'), calculator(state, onChange)); side.append(calc);
    const right = element('section', 'periodic-reference'), scroll = element('div', 'periodic-scroll'), table = image('periodic-table.png', 'Original periodic table. Atomic numbers are at the top left of each element.');
    const controls = zoomControls(zoom => { table.style.width = `${zoom * 100}%`; }); controls.fit.addEventListener('click', () => controls.apply(1)); controls.apply(1);
    scroll.append(table); right.append(controls.bar, scroll); view.append(side, right); return view;
  }
  function inspect(id, face, state, onChange) {
    if (id === 'periodic') return periodicView(state, onChange);
    if (id === 'calculator' && face) return documentView(id, face, state);
    if (id === 'calculator') { const view = element('div', 'calculator-view'); view.append(calculator(state, onChange)); return view; }
    return documentView(id, face, state);
  }
  root.HikingClues = { art, inspect };
})(window);
