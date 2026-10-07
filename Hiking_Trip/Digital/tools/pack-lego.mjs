// Packs a Stud.io LDraw export into a small asset the browser can draw with real part shapes and prints.
//   node Hiking_Trip/Digital/tools/pack-lego.mjs <export.ldr> <name>
// Writes assets/lego-<name>.pack.json (colours, parts, the model and its steps) and assets/lego-<name>.pack.bin
// (geometry). Parts come from the Stud.io install: its custom parts, the LDraw library, then its unofficial library.
// Prints are Stud.io textures (0 PE_TEX_PATH / 0 PE_TEX_INFO): either UV-mapped triangles (faces, torsos, animals)
// or a flat projection (custom name tiles, the satellite's gold panels). Prints are written as assets/lego-tex-<hash>.png.
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, basename } from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';

const STUDIO = process.env.STUDIO_LDRAW || 'C:/Program Files/Studio 2.0/ldraw';
const CUSTOM = process.env.STUDIO_CUSTOM || join(process.env.LOCALAPPDATA || '', 'Stud.io/CustomParts/parts');
// The LDraw library first: Stud.io places parts by it. Stud.io's UnOfficial copies of library parts can have a different
// origin (hair 26139 there sits one brick higher), so UnOfficial only supplies what the library lacks (bl_ prints, *tex).
const ROOTS = [CUSTOM, `${STUDIO}/parts`, `${STUDIO}/p`, `${STUDIO}/UnOfficial/parts`, `${STUDIO}/UnOfficial/p`];
const OUT = new URL('../assets/', import.meta.url);
const TEX_MAX = 512;   // longest side of a packed texture, in pixels

// ---- Library lookup: lower-case relative path → file, first root wins ----
const index = new Map();
function walk(root, dir = root) {
  let names; try { names = readdirSync(dir); } catch { return; }
  for (const n of names) {
    const full = join(dir, n);
    if (statSync(full).isDirectory()) { walk(root, full); continue; }
    const rel = full.slice(root.length + 1).replace(/\\/g, '/').toLowerCase();
    if (!index.has(rel)) index.set(rel, full);
  }
}
ROOTS.forEach(r => walk(r));
const cache = new Map();
function libraryFile(name) {
  const key = name.replace(/\\/g, '/').toLowerCase();
  if (cache.has(key)) return cache.get(key);
  const path = index.get(key);
  const lines = path ? readFileSync(path, 'utf8').split(/\r?\n/) : null;
  cache.set(key, lines);
  return lines;
}

// ---- Colours from Stud.io's LDConfig ----
const colours = {};
for (const line of readFileSync(`${STUDIO}/LDConfig.ldr`, 'utf8').split(/\r?\n/)) {
  const m = line.match(/^0 !COLOUR\s+(\S+)\s+CODE\s+(\d+)\s+VALUE\s+#(\w+)\s+EDGE\s+#(\w+)(.*)$/);
  if (!m) continue;
  const alpha = +(m[5].match(/ALPHA\s+(\d+)/)?.[1] ?? 255);
  colours[m[2]] = { name: m[1], value: '#' + m[3], edge: '#' + m[4], alpha, finish: /CHROME|PEARLESCENT|METAL/.exec(m[5])?.[0] || '' };
}
const edgeOf = code => colours[code]?.edge || '#333333';

// ---- 3 × 4 matrices as [x y z a b c d e f g h i] (LDraw order) ----
const I = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];
function mul(A, B) {
  const [ax, ay, az, a, b, c, d, e, f, g, h, i] = A, [bx, by, bz, p, q, r, s, t, u, v, w, x] = B;
  return [ax + a * bx + b * by + c * bz, ay + d * bx + e * by + f * bz, az + g * bx + h * by + i * bz,
    a * p + b * s + c * v, a * q + b * t + c * w, a * r + b * u + c * x,
    d * p + e * s + f * v, d * q + e * t + f * w, d * r + e * u + f * x,
    g * p + h * s + i * v, g * q + h * t + i * w, g * r + h * u + i * x];
}
const apply = (M, x, y, z) => [M[0] + M[3] * x + M[4] * y + M[5] * z, M[1] + M[6] * x + M[7] * y + M[8] * z, M[2] + M[9] * x + M[10] * y + M[11] * z];
const det = M => M[3] * (M[7] * M[11] - M[8] * M[10]) - M[4] * (M[6] * M[11] - M[8] * M[9]) + M[5] * (M[6] * M[10] - M[7] * M[9]);
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = a => { const l = Math.hypot(...a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };

// ---- Textures ----
const textures = [], textureIds = new Map(), warnings = new Set();
function addTexture(b64) {
  const hash = createHash('sha1').update(b64).digest('hex').slice(0, 12);
  if (textureIds.has(hash)) return textureIds.get(hash);
  const file = `lego-tex-${hash}.png`, path = new URL(file, OUT);
  writeFileSync(path, Buffer.from(b64, 'base64'));
  // Shrink large prints with Pillow (keeps transparency).
  execFileSync('python', ['-c', `import sys\nfrom PIL import Image\nim=Image.open(sys.argv[1]); im.load()\nif max(im.size)>${TEX_MAX}: im.thumbnail((${TEX_MAX},${TEX_MAX}), Image.LANCZOS)\nim.save(sys.argv[1], optimize=True)`, path.pathname.replace(/^\/(\w:)/, '$1')]);
  textureIds.set(hash, textures.length); textures.push(file);
  return textures.length - 1;
}

// ---- Flattening one part into coloured triangles, textured triangles and edge lines (part space) ----
// colour 16 stays 16 (the colour the part is placed with) and 24 stays 24 (its edge colour) unless a subfile fixes it.
function resolveColour(code, current) {
  if (code === 16) return current;
  if (code === 24) return current === 16 ? 24 : 'e' + current;
  return code;
}
function flattenPart(name) {
  const out = { tris: new Map(), tex: [], edges: new Map(), hands: [] };
  const push = (map, key, ...nums) => { if (!map.has(key)) map.set(key, []); map.get(key).push(...nums); };
  // active: the texture drawn on this subtree ({ id, planar } or null). decls: textures aimed further down, each with
  // its path of type-1 line indices relative to this file (-1 = this file's own triangles).
  function visit(lines, M, colour, invert, active, decls) {
    let ccw = true, certified = false, invertNext = false, pending = [], typeOne = 0;
    decls = decls.slice();
    const own = () => { const t = decls.find(d => d.path.length === 1 && d.path[0] === -1); return t ? makeTex(t, M) : active; };
    for (const raw of lines) {
      const p = raw.trim().split(/\s+/);
      if (p[0] === '0') {
        if (p[1] === 'BFC') {
          if (p.includes('CERTIFY')) certified = true;
          if (p.includes('CW')) ccw = false; if (p.includes('CCW')) ccw = true;
          if (p.includes('INVERTNEXT')) invertNext = true;
        } else if (p[1] === 'PE_TEX_PATH') pending = p.slice(2).map(Number);
        else if (p[1] === 'PE_TEX_INFO') decls.push({ path: pending, id: addTexture(p.at(-1)), nums: p.slice(2, -1).map(Number) });
        else if (p[1]?.startsWith('PE_TEX')) warnings.add(`${name}: ${p[1]} not supported`);
        continue;
      }
      const type = +p[0];
      if (type === 1) {
        const code = +p[1], m = p.slice(2, 14).map(Number), file = p.slice(14).join(' ');
        const childM = mul(M, m), childInvert = invert !== invertNext, k = typeOne++;
        invertNext = false;
        if (file.toLowerCase() === '3820.dat') out.hands.push(childM.map(v => Math.round(v * 1000) / 1000));   // minifig hand: where held items go
        const sub = libraryFile(file);
        if (!sub) { warnings.add(`${name}: missing ${file}`); continue; }
        const aimed = decls.filter(d => d.path[0] === k).map(d => ({ ...d, path: d.path.slice(1) }));
        const hit = aimed.find(d => d.path.length === 0);
        visit(sub, childM, resolveColour(code, colour), childInvert, hit ? makeTex(hit, childM) : active, aimed.filter(d => d.path.length));
        continue;
      }
      invertNext = false;
      const code = resolveColour(+p[1], colour), n = p.slice(2).map(Number);
      if (type === 2) { push(out.edges, code, ...apply(M, n[0], n[1], n[2]), ...apply(M, n[3], n[4], n[5])); continue; }
      if (type !== 3 && type !== 4) continue;
      const k = type, verts = [];
      let uvs = null;
      for (let v = 0; v < k; v++) verts.push(apply(M, n[v * 3], n[v * 3 + 1], n[v * 3 + 2]));
      if (n.length >= k * 5) { uvs = []; for (let v = 0; v < k; v++) uvs.push([n[k * 3 + v * 2], n[k * 3 + v * 2 + 1]]); }
      // Winding: make every triangle counter-clockwise in part space (only for certified files).
      const flip = certified && ((!ccw) !== (det(M) < 0) !== invert);
      const tex = own();
      for (const tri of k === 3 ? [[0, 1, 2]] : [[0, 1, 2], [0, 2, 3]]) {
        const t = flip ? [tri[0], tri[2], tri[1]] : tri, pts = t.map(i => verts[i]);
        push(out.tris, code, ...pts.flat());
        if (!tex) continue;
        const uv = tex.planar ? planarUV(tex.planar, pts) : uvs && t.map(i => uvs[i]);
        if (uv) out.tex.push({ id: tex.id, code, pos: pts.flat(), uv: uv.flat() });
      }
    }
  }
  const top = libraryFile(name);
  if (!top) { warnings.add(`missing part ${name}`); return null; }
  visit(top, I, 16, false, null, []);
  return out;
}

// Planar projection (custom Stud.io parts): PE_TEX_INFO x y z a b c d e f g h i x1 y1 x2 y2.
// (x y z) and the matrix place a box in the textured subfile's space; its middle axis is the thin one (the printed
// face is perpendicular to it). The picture covers (x1..x2, y2..y1) measured from the box centre along the other
// two axes, in part units. Checked against the name tiles (name band along the front edge, readable from the front).
function makeTex(t, M) {
  if (t.nums.length < 16) return { id: t.id, planar: null };
  const [x, y, z, a, b, c, d, e, f, g, h, i, x1, y1, x2, y2] = t.nums;
  const C = apply(M, x, y, z);
  const axis = col => { const v = [M[3] * col[0] + M[4] * col[1] + M[5] * col[2], M[6] * col[0] + M[7] * col[1] + M[8] * col[2], M[9] * col[0] + M[10] * col[1] + M[11] * col[2]]; return v; };
  const U = axis([a, d, g]), V = axis([b, e, h]), W = axis([c, f, i]);
  return { id: t.id, planar: { C, eu: norm(U), ev: norm(V), ew: norm(W), hv: Math.hypot(...V) / 2 + 0.6, bounds: [x1, y1, x2, y2] } };
}
function planarUV(pl, pts) {
  const n = norm(cross(sub(pts[1], pts[0]), sub(pts[2], pts[0])));
  if (Math.abs(dot(n, pl.ev)) < 0.7) return null;                       // only faces looking along the thin axis
  if (pts.some(p => Math.abs(dot(sub(p, pl.C), pl.ev)) > pl.hv)) return null;
  const [x1, y1, x2, y2] = pl.bounds;
  return pts.map(p => {
    const d = sub(p, pl.C), u = dot(d, pl.eu), w = -dot(d, pl.ew);
    return [(u - x1) / (x2 - x1), 1 - (w - y2) / (y1 - y2)];
  });
}

// ---- The model: its own files (main model, submodels such as the telescope or a posed torso) and steps ----
function parseModel(text) {
  const files = {}; let cur = null, main = null, step = 0;
  for (const raw of text.split(/\r?\n/)) {
    const p = raw.trim().split(/\s+/);
    if (p[0] === '0' && p[1] === 'FILE') { cur = p.slice(2).join(' ').toLowerCase(); files[cur] = []; main ??= cur; step = 0; continue; }
    if (p[0] === '0' && p[1] === 'STEP') { step++; continue; }
    if (p[0] === '1' && cur) files[cur].push({ color: +p[1], m: p.slice(2, 14).map(Number), file: p.slice(14).join(' ').toLowerCase(), step });
  }
  return { files, main };
}

// Several exports can share one pack (the four Lego numbers): each one's main model is filed under its own file name
// (exports from Stud.io often share the same model name), and json.models lists them.
const args = process.argv.slice(2), name = args.pop(), inputs = args;
if (!inputs.length || !name) { console.error('usage: node pack-lego.mjs <export.ldr> [<export2.ldr> …] <name>'); process.exit(1); }
const input = inputs.join(', ');
const model = { files: {}, main: null, models: {} };
for (const path of inputs) {
  const one = parseModel(readFileSync(path, 'utf8')), key = basename(path).replace(/\.ldr$/i, '').toLowerCase();
  const rename = f => f === one.main && inputs.length > 1 ? key : f;
  for (const [f, refs] of Object.entries(one.files)) model.files[rename(f)] = refs.map(r => ({ ...r, file: rename(r.file) }));
  model.models[key] = rename(one.main); model.main ??= rename(one.main);
}
const used = new Set(), codes = new Set();
for (const refs of Object.values(model.files)) for (const r of refs) { if (!model.files[r.file]) used.add(r.file); codes.add(r.color); }

// Geometry goes into one Float32 buffer; each group records [offset, length] in floats.
const floats = [];
const store = arr => { const off = floats.length; for (const v of arr) floats.push(Math.round(v * 1000) / 1000); return [off, arr.length]; };
const parts = {};
let triangles = 0;
for (const file of [...used].sort()) {
  const flat = flattenPart(file);
  if (!flat) continue;
  const part = { tris: [], tex: [], edges: [] };
  if (flat.hands.length) part.hands = flat.hands;
  for (const [code, arr] of flat.tris) { part.tris.push([String(code), ...store(arr)]); triangles += arr.length / 9; if (typeof code === 'number') codes.add(code); }
  for (const [code, arr] of flat.edges) { part.edges.push([String(code), ...store(arr)]); if (typeof code === 'number') codes.add(code); }
  const byTex = new Map();
  for (const t of flat.tex) { const k = t.id; if (!byTex.has(k)) byTex.set(k, { pos: [], uv: [] }); byTex.get(k).pos.push(...t.pos); byTex.get(k).uv.push(...t.uv); }
  for (const [id, g] of byTex) part.tex.push([id, ...store(g.pos), ...store(g.uv)]);
  parts[file] = part;
}
const colourTable = {};
for (const c of codes) if (colours[c]) colourTable[c] = colours[c]; else if (c !== 16 && c !== 24) warnings.add(`unknown colour ${c}`);
for (const c of Object.keys(colourTable)) colourTable['e' + c] = { value: colours[c].edge, edge: colours[c].edge, alpha: 255, finish: '' };

// The geometry link carries its content hash, so browsers fetch it again after a repack.
const bin = Buffer.from(new Float32Array(floats).buffer), binHash = createHash('sha1').update(bin).digest('hex').slice(0, 10);
const json = { source: inputs.map(p => basename(p)).join(', '), main: model.main, models: model.models, files: model.files, parts, colours: colourTable, textures, bin: `lego-${name}.pack.bin?v=${binHash}` };
writeFileSync(new URL(`lego-${name}.pack.json`, OUT), JSON.stringify(json));
writeFileSync(new URL(`lego-${name}.pack.bin`, OUT), bin);
console.log(`${name}: ${used.size} parts, ${Math.round(triangles)} triangles, ${textures.length} textures, ${(floats.length * 4 / 1e6).toFixed(2)} MB geometry`);
for (const w of warnings) console.warn('warning:', w);
