// Real Lego parts for Three.js, from a pack made by tools/pack-lego.mjs (part shapes and Stud.io prints).
// Unlike lego3d.js `partMesh` (boxes for the push puzzles), these are the library shapes, so minifigs, bars and
// clips look like the real thing. Coordinates are LDraw (y down); put objects under lego3d.js `createScene().root`.
import * as THREE from 'three';
import { mergeVertices, toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';
import { toMatrix4 } from './lego3d.js';

const CREASE = THREE.MathUtils.degToRad(38);   // LDraw primitives use 16 or 48 segments: smooth those, keep box edges sharp

export async function loadPack(url) {
  const base = new URL('.', new URL(url, location.href));
  const json = await (await fetch(url, { cache: 'no-cache' })).json();   // small; always checked, so a repack shows up
  const floats = new Float32Array(await (await fetch(new URL(json.bin, base))).arrayBuffer());
  const slice = (off, len) => floats.subarray(off, off + len);

  const materials = new Map(), geometries = new Map(), textures = new Map(), loads = [];
  const colourOf = key => json.colours[key] || { value: '#999999', edge: '#333333', alpha: 255, finish: '' };
  function material(key) {
    if (materials.has(key)) return materials.get(key);
    const c = colourOf(key), m = new THREE.MeshStandardMaterial({ color: new THREE.Color(c.value), roughness: 0.32, metalness: 0 });
    if (c.finish === 'PEARLESCENT' || c.finish === 'METAL') Object.assign(m, { metalness: 0.55, roughness: 0.3 });
    if (c.finish === 'CHROME') Object.assign(m, { metalness: 0.9, roughness: 0.15 });
    if (c.alpha < 255) Object.assign(m, { transparent: true, opacity: Math.max(0.35, c.alpha / 255), depthWrite: false });
    materials.set(key, m);
    return m;
  }
  function edgeMaterial(key) {
    const k = 'line:' + key;
    if (!materials.has(k)) materials.set(k, new THREE.LineBasicMaterial({ color: new THREE.Color(colourOf(key).edge), transparent: true, opacity: 0.45 }));
    return materials.get(k);
  }
  function texture(id) {
    if (!textures.has(id)) {
      let t;
      loads.push(new Promise(done => { t = new THREE.TextureLoader().load(new URL(json.textures[id], base).href, done, undefined, done); }));
      t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
      textures.set(id, new THREE.MeshStandardMaterial({ map: t, transparent: true, roughness: 0.4, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2, depthWrite: false }));
    }
    return textures.get(id);
  }
  function geometry(key, build) {
    if (!geometries.has(key)) geometries.set(key, build());
    return geometries.get(key);
  }
  const smooth = (pos, uv) => {
    let g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    if (uv) g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
    g = uv ? mergeVertices(g, 1e-3) : mergeVertices(g, 1e-3);
    return toCreasedNormals(g, CREASE);
  };
  // Colour key of a group in a part placed with `colour` (16 = the placed colour, 24 = its edge colour).
  const keyFor = (code, colour) => code === '16' ? String(colour) : code === '24' ? 'e' + colour : code;

  // One library part as a Group (meshes share geometry and materials with every other copy).
  function part(file, colour) {
    const p = json.parts[file], g = new THREE.Group();
    if (!p) { console.warn('Part not in pack:', file); return g; }
    p.tris.forEach(([code, off, len], i) => {
      const mesh = new THREE.Mesh(geometry(`${file}:t${i}`, () => smooth(slice(off, len))), material(keyFor(code, colour)));
      mesh.castShadow = mesh.receiveShadow = true; g.add(mesh);
    });
    p.tex.forEach(([id, off, len, uvOff, uvLen], i) => {
      const mesh = new THREE.Mesh(geometry(`${file}:x${i}`, () => smooth(slice(off, len), slice(uvOff, uvLen))), texture(id));
      mesh.renderOrder = 1; g.add(mesh);
    });
    p.edges.forEach(([code, off, len], i) => {
      const geo = geometry(`${file}:e${i}`, () => new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(slice(off, len), 3)));
      g.add(new THREE.LineSegments(geo, edgeMaterial(keyFor(code, colour))));
    });
    g.userData.file = file;
    return g;
  }

  // A reference from the model (a part, or a submodel such as the telescope or a posed torso), placed by its matrix.
  function build(ref, inherited = 16) {
    const colour = ref.color === 16 ? inherited : ref.color;
    const kids = json.files[ref.file];
    let o;
    if (kids) { o = new THREE.Group(); for (const k of kids) o.add(build(k, colour)); }
    else o = part(ref.file, colour);
    o.matrixAutoUpdate = false; o.matrix.copy(toMatrix4(ref.m));
    o.userData.ref = ref;
    return o;
  }

  // Average vertex of a part's triangles in one colour group (e.g. the lens of a magnifying glass), in part space.
  function centroid(file, code) {
    const s = [0, 0, 0]; let n = 0;
    for (const [c, off, len] of json.parts[file]?.tris || []) if (c === code) for (let i = off; i < off + len; i += 3) { s[0] += floats[i]; s[1] += floats[i + 1]; s[2] += floats[i + 2]; n++; }
    return n ? s.map(v => v / n) : null;
  }

  // Resolves once every print used so far has loaded (for still pictures).
  const ready = () => Promise.all(loads);

  return { json, main: json.files[json.main], files: json.files, part, build, material, centroid, ready };
}

// World-space bounding box of an object built in LDraw space (call after it is added under the scene root).
export function boundsOf(object) {
  object.updateWorldMatrix(true, true);
  return new THREE.Box3().setFromObject(object);
}
