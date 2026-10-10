// The water bottle in 3D: drag to turn it, scroll or pinch to zoom. Three stickers sit 120° apart around a label band.
import * as THREE from 'three';

const TAU = Math.PI * 2;

function labelTexture(images) {
  const w = 2048, h = 512, c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'), r = 190;
  images.forEach((img, i) => {
    for (const x of [w * i / images.length, w * i / images.length + w]) {
      g.save(); g.beginPath(); g.arc(x, h * 0.46, r, 0, TAU); g.clip();
      g.drawImage(img, x - r, h * 0.46 - r, r * 2, r * 2); g.restore();
      g.strokeStyle = 'rgba(70,80,70,.25)'; g.lineWidth = 3; g.beginPath(); g.arc(x, h * 0.46, r, 0, TAU); g.stroke();
    }
  });
  g.fillStyle = '#6d7d6d'; g.font = '600 26px "Inter Tight", Arial, sans-serif'; g.textAlign = 'center';
  if ('letterSpacing' in g) g.letterSpacing = '8px';
  for (let i = 0; i < images.length; i++) for (const x of [w * i / images.length, w * i / images.length + w]) g.fillText('TRAIL COMPANION', x, h * 0.9);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8; return tex;
}

function loadImage(src) { return new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = no; i.src = src; }); }

// box: element to fill. Resolves to { to(face), dispose() }.
export async function mount(box, { stickers, face = 0, onFace = () => {} }) {
  const images = await Promise.all(stickers.map(loadImage));
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.domElement.className = 'bottle3d-canvas'; box.replaceChildren(renderer.domElement);
  const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(30, 1, 0.1, 50);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a9a88, 1.1));
  const sun = new THREE.DirectionalLight(0xfff3dc, 1.6); sun.position.set(2.5, 4, 5); scene.add(sun);

  // Profile of the bottle, bottom to neck, in a unit where the body radius is 1.
  const pts = [[0, 0], [0.82, 0], [0.97, 0.05], [1, 0.2], [1, 2.55], [0.96, 2.85], [0.62, 3.2], [0.4, 3.42], [0.4, 3.62]].map(([x, y]) => new THREE.Vector2(x, y));
  const bodyMat = new THREE.MeshStandardMaterial({ color: 0xf1f1e4, roughness: 0.38, metalness: 0.05 });
  const bottle = new THREE.Group();
  bottle.add(new THREE.Mesh(new THREE.LatheGeometry(pts, 96), bodyMat));
  const label = new THREE.Mesh(new THREE.CylinderGeometry(1.004, 1.004, 1.6, 96, 1, true), new THREE.MeshStandardMaterial({ map: labelTexture(images), transparent: true, roughness: 0.5, polygonOffset: true, polygonOffsetFactor: -2 }));
  label.position.y = 1.5; bottle.add(label);
  const capMat = new THREE.MeshStandardMaterial({ color: 0x3a4644, roughness: 0.6 });
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.47, 0.47, 0.62, 48), capMat); cap.position.y = 3.86; bottle.add(cap);
  for (let i = 0; i < 48; i++) { const rib = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.5, 0.03), capMat); const a = i / 48 * TAU; rib.position.set(Math.sin(a) * 0.48, 3.86, Math.cos(a) * 0.48); bottle.add(rib); }
  bottle.position.y = -2.05; const pivot = new THREE.Group(); pivot.add(bottle); scene.add(pivot);

  let yaw = -face * TAU / images.length, target = yaw, dist = 9.5, wantDist = 9.5, dragging = false, last = 0, velocity = 0, raf = 0, dead = false;
  const nearest = () => ((Math.round(-yaw / (TAU / images.length)) % images.length) + images.length) % images.length;
  let shown = face;
  const resize = () => { const w = box.clientWidth || 300, h = box.clientHeight || 500; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); };
  const frame = () => {
    if (dead) return;
    if (!dragging) { velocity *= 0.92; target += velocity; }
    yaw += (target - yaw) * (dragging ? 0.6 : 0.18); pivot.rotation.y = yaw;
    dist += (wantDist - dist) * 0.15; camera.position.set(0, 0.2, dist); camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
    if (!dragging && Math.abs(velocity) < 0.0005 && shown !== nearest()) { shown = nearest(); onFace(shown); }
    raf = requestAnimationFrame(frame);
  };
  const el = renderer.domElement; el.style.touchAction = 'none'; el.style.cursor = 'grab';
  const pointers = new Map(); let pinch = 0;
  el.addEventListener('pointerdown', e => { el.setPointerCapture(e.pointerId); pointers.set(e.pointerId, e); dragging = true; last = e.clientX; velocity = 0; el.style.cursor = 'grabbing'; if (pointers.size === 2) { const [a, b] = [...pointers.values()]; pinch = Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY); } });
  el.addEventListener('pointermove', e => {
    if (!pointers.has(e.pointerId)) return; pointers.set(e.pointerId, e);
    if (pointers.size === 2) { const [a, b] = [...pointers.values()], d = Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY); wantDist = Math.min(14, Math.max(4.5, wantDist * pinch / d)); pinch = d; return; }
    const dx = e.clientX - last; last = e.clientX; target += dx * 0.012; velocity = dx * 0.004;
  });
  const up = e => { pointers.delete(e.pointerId); if (!pointers.size) { dragging = false; el.style.cursor = 'grab'; } else last = [...pointers.values()][0].clientX; };
  el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
  el.addEventListener('wheel', e => { e.preventDefault(); wantDist = Math.min(14, Math.max(4.5, wantDist * (1 + Math.sign(e.deltaY) * 0.1))); }, { passive: false });
  el.tabIndex = 0; el.setAttribute('role', 'img'); el.setAttribute('aria-label', 'The water bottle in 3D. Drag, or use the left and right arrow keys, to turn it.');
  el.addEventListener('keydown', e => { if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); target += (e.key === 'ArrowLeft' ? -1 : 1) * 0.25; } });
  const ro = new ResizeObserver(resize); ro.observe(box); resize(); frame();
  return {
    // Swing round to the front of sticker n by the shortest way.
    to(n) { const step = TAU / images.length; let t = -n * step; t += Math.round((target - t) / TAU) * TAU; target = t; velocity = 0; shown = n; },
    dispose() { dead = true; cancelAnimationFrame(raf); ro.disconnect(); renderer.dispose(); },
  };
}
