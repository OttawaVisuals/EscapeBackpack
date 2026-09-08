import fs from 'node:fs';
const dir = new URL('./', import.meta.url);
const read = path => fs.readFileSync(new URL(path, dir), 'utf8');
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
export function paperSection(marked) {
  const layout = JSON.parse(read('QR_Patch_Prototype/aurora-qr-layoutV2.json'));
  const pdf = fs.readFileSync(new URL('../output/pdf/Aurora_V2_Paper_Prototype.pdf', dir)).toString('base64');
  const briefPdf = fs.readFileSync(new URL('../output/pdf/Aurora_Emergency_Briefing.pdf', dir)).toString('base64');
  const briefing = read('QR_Patch_Prototype/Briefing_Refined_Draft.txt');
  const options = read('QR_Patch_Prototype/Placement_Clue_Options.md');
  const cells = layout.patches.flatMap(p => p.cells);
  const colors = ['#a84420','#226b67','#7357a1','#245e99','#96701c','#a23e70'];
  const outlines = layout.patches.map((p,i) => {
    const set = new Set(p.cells.map(([r,c]) => `${r},${c}`));
    return p.cells.map(([r,c]) => {
      let path = '';
      for (const [dr,dc,edge] of [[-1,0,`M${c} ${r}h1`],[1,0,`M${c} ${r+1}h1`],[0,-1,`M${c} ${r}v1`],[0,1,`M${c+1} ${r}v1`]])
        if (!set.has(`${r+dr},${c+dc}`)) path += edge;
      return `<rect x="${c}" y="${r}" width="1" height="1" fill="${colors[i]}" fill-opacity=".16"/><path d="${path}" fill="none" stroke="${colors[i]}" stroke-width=".12"/>`;
    }).join('');
  }).join('');
  const grid = Array.from({length:26},(_,i)=>`<path d="M${i} 0v25M0 ${i}h25" stroke="#d8dee4" stroke-width=".04"/>`).join('');
  const corners = [[0,0],[18,0],[0,18]].map(([x,y])=>`<rect x="${x}" y="${y}" width="7" height="7" fill="#16253c"/><rect x="${x+1}" y="${y+1}" width="5" height="5" fill="white"/><rect x="${x+2}" y="${y+2}" width="3" height="3" fill="#16253c"/>`).join('');
  const thumbs = layout.patches.map((p,i)=> {
    const rows=p.cells.map(c=>c[0]), cols=p.cells.map(c=>c[1]);
    const r0=Math.min(...rows), c0=Math.min(...cols), w=Math.max(...cols)-c0+1, h=Math.max(...rows)-r0+1;
    const squares=p.cells.map(([r,c])=>`<rect x="${c-c0}" y="${r-r0}" width="1" height="1" fill="${layout.targetMatrix[r*25+c]?'black':'white'}" stroke="#aaa" stroke-width=".025"/>`).join('');
    return `<div class="card"><strong style="color:${colors[i]}">Patch ${p.id}</strong><svg viewBox="-1 -1 ${w+2} ${h+2}" role="img" aria-label="V2 patch ${p.id} pattern" style="width:100%;height:100px;display:block;margin-top:12px">${squares}</svg></div>`;
  }).join('');
  return `<div class="reader" style="margin:24px 0">
    <span class="tag">V2 · ready for paper testing</span><h2>Print it. Assemble it. Test it.</h2>
    <p>Five pages: refined briefing, base QR, six cutout patches, maintenance diagram and facilitator instructions.</p>
    <div class="toolbar"><a href="data:application/pdf;base64,${pdf}" download="Aurora_V2_Paper_Prototype.pdf">Download printable PDF</a><a href="data:application/pdf;base64,${briefPdf}" download="Aurora_Emergency_Briefing.pdf">Download styled briefing only</a><a href="data:text/plain;charset=utf-8,${encodeURIComponent(briefing)}" download="Briefing_Refined_Draft.txt">Download briefing text</a><a href="data:application/json;charset=utf-8,${encodeURIComponent(JSON.stringify(layout,null,2))}" download="aurora-qr-layoutV2.json">Download V2 editor layout</a></div>
    <p><strong>Print single-sided at 100% / Actual size.</strong> Check both 50 mm rulers. Give players pages 1, 2 and 4 plus the cut patches from page 3. Keep page 5.</p>
    <p class="notetext">3 mm squares · 75 mm QR face · 99 mm including its white border. Use opaque paper and adhesive underneath. Screen previews are not print templates.</p>
    <div class="intro"><strong>Opening sequence</strong><p>Briefing → find panel, patches and diagram → match shapes → transfer all six → scan → HAROLD.</p></div>
    <div class="maplayout"><div class="visual"><svg viewBox="-2 -2 29 29" role="img" aria-label="Maintenance diagram showing the six V2 patch outlines and three orientation corners">${grid}${corners}${outlines}</svg><p class="notetext">Designer preview uses colour to distinguish adjacent patches. The player PDF uses monochrome outlines and numbered coordinates.</p></div><div><h3>Recommended: match the maintenance diagram</h3><p>Match each loose patch to its outline. Keep the printed side up and transfer it to the same rows and columns on the QR panel.</p><p>This is a simple opening assembly task. The three corner markers establish orientation; players need no QR knowledge.</p><p><strong>Physical test still needed:</strong> some strips are only 3 mm wide. Check cutting, positioning and scanning separately.</p><p class="notetext">${cells.length} patch squares cover all 58 changed squares. Some five-patch combinations already decode HAROLD; accepted for this cooperative prototype.</p></div></div>
    <details><summary>See all six V2 patch patterns</summary><div class="prose"><div class="grid3">${thumbs}</div></div></details>
    <details><summary>Read the revised HAROLD briefing</summary><div class="prose">${briefing.split(/\r?\n\s*\r?\n/).filter(Boolean).map(p=>`<p>${escape(p).replaceAll('\n','<br>')}</p>`).join('')}<p class="notetext">The original briefing is preserved. Only the final transmission breaks off; essential instructions remain readable.</p></div></details>
    <details><summary>Placement clues: recommended version, two alternatives and hints</summary><div class="prose">${marked.parse(options)}</div></details>
    <p class="notetext">The PDF patterns were checked against V2. Actual phone-camera performance and deployment of /coms and /Harold remain unverified. To edit this exact prototype, import the V2 layout downloaded above into the editor below.</p>
  </div>`;
}
