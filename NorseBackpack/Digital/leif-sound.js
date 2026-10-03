/* Sound for the online edition, synthesised with the Web Audio API: no audio files to load.
   Effects (padlock clicks, paper, the pocket opening) are on by default; the ambience (wind,
   sea and a crackling hearth) is off until the player turns it on. Settings stay in this
   browser. Browsers only allow sound after the first click or key press. */
(function (root) {
  const KEY = 'escape-backpack.sound';
  let settings = { fx: true, amb: false };
  try { Object.assign(settings, JSON.parse(localStorage.getItem(KEY)) || {}); } catch (_) { /* defaults */ }
  let ctx = null, master = null, ambience = null, noiseBuffer = null;

  function audio() {
    if (ctx) { if (ctx.state === 'suspended') ctx.resume(); return ctx; }
    const AC = root.AudioContext || root.webkitAudioContext; if (!AC) return null;
    ctx = new AC(); master = ctx.createGain(); master.gain.value = 0.55; master.connect(ctx.destination);
    noiseBuffer = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const data = noiseBuffer.getChannelData(0); for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    return ctx;
  }
  // A burst of filtered noise: clicks, paper and thuds are all shaped from this.
  function noise({ at = 0, dur = 0.05, freq = 2000, q = 1, type = 'bandpass', gain = 0.4, attack = 0.002 }) {
    const a = audio(); if (!a) return;
    const t = a.currentTime + at, src = a.createBufferSource(), f = a.createBiquadFilter(), g = a.createGain();
    src.buffer = noiseBuffer; src.playbackRate.value = 0.8 + Math.random() * 0.4;
    f.type = type; f.frequency.value = freq; f.Q.value = q;
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(gain, t + attack); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(f); f.connect(g); g.connect(master); src.start(t, Math.random()); src.stop(t + dur + 0.05);
  }
  function tone({ at = 0, dur = 0.4, freq = 440, type = 'sine', gain = 0.2, slide = 0 }) {
    const a = audio(); if (!a) return;
    const t = a.currentTime + at, o = a.createOscillator(), g = a.createGain();
    o.type = type; o.frequency.setValueAtTime(freq, t); if (slide) o.frequency.exponentialRampToValueAtTime(freq * slide, t + dur);
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(gain, t + 0.01); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(master); o.start(t); o.stop(t + dur + 0.05);
  }
  const effects = {
    tick: () => noise({ dur: 0.025, freq: 3800, q: 6, gain: 0.25 }),
    paper: () => { noise({ dur: 0.18, freq: 2600, q: 0.7, gain: 0.22, attack: 0.03 }); noise({ at: 0.08, dur: 0.12, freq: 4200, q: 0.8, gain: 0.12 }); },
    drop: () => noise({ dur: 0.08, freq: 500, q: 1.2, type: 'lowpass', gain: 0.35 }),
    wrong: () => { noise({ dur: 0.07, freq: 900, q: 3, gain: 0.45 }); tone({ at: 0.02, dur: 0.18, freq: 140, type: 'triangle', gain: 0.18, slide: 0.8 }); },
    unlock: () => { noise({ dur: 0.04, freq: 3000, q: 4, gain: 0.5 }); noise({ at: 0.09, dur: 0.06, freq: 1800, q: 5, gain: 0.45 }); tone({ at: 0.1, dur: 0.12, freq: 1250, type: 'triangle', gain: 0.08 }); },
    open: () => { noise({ dur: 0.5, freq: 900, q: 0.6, type: 'lowpass', gain: 0.25, attack: 0.12 }); [523.25, 659.25, 783.99].forEach((f, i) => tone({ at: 0.15 + i * 0.11, dur: 1.2, freq: f, gain: 0.07 })); },
    whoosh: () => noise({ dur: 0.35, freq: 1400, q: 0.5, gain: 0.12, attack: 0.15 }),
    chapter: () => [392, 493.88, 587.33, 783.99].forEach((f, i) => tone({ at: i * 0.16, dur: 1.6, freq: f, type: 'triangle', gain: 0.06 }))
  };
  function play(name) { if (!settings.fx || !effects[name]) return; try { effects[name](); } catch (_) { /* sound must never break play */ } }

  /* Ambience: wind-and-sea swells (slowly moving filtered noise) under a soft hearth crackle. */
  function startAmbience() {
    const a = audio(); if (!a || ambience) return;
    const out = a.createGain(); out.gain.setValueAtTime(0, a.currentTime); out.gain.linearRampToValueAtTime(0.32, a.currentTime + 3); out.connect(master);
    const src = a.createBufferSource(); src.buffer = noiseBuffer; src.loop = true;
    const low = a.createBiquadFilter(); low.type = 'lowpass'; low.frequency.value = 420;
    const swell = a.createGain(); swell.gain.value = 0.5;
    const lfo = a.createOscillator(), depth = a.createGain(); lfo.frequency.value = 0.09; depth.gain.value = 0.35; lfo.connect(depth); depth.connect(swell.gain);
    const lfo2 = a.createOscillator(), depth2 = a.createGain(); lfo2.frequency.value = 0.05; depth2.gain.value = 180; lfo2.connect(depth2); depth2.connect(low.frequency);
    src.connect(low); low.connect(swell); swell.connect(out); src.start(); lfo.start(); lfo2.start();
    let timer = null;
    const crackle = () => {
      if (!ambience) return;
      const t = a.currentTime;
      for (let i = 0, n = 1 + Math.floor(Math.random() * 3); i < n; i++) {
        const s = a.createBufferSource(), f = a.createBiquadFilter(), g = a.createGain(), at = t + Math.random() * 0.25;
        s.buffer = noiseBuffer; f.type = 'highpass'; f.frequency.value = 1500 + Math.random() * 2500;
        g.gain.setValueAtTime(0.05 + Math.random() * 0.07, at); g.gain.exponentialRampToValueAtTime(0.0001, at + 0.02 + Math.random() * 0.03);
        s.connect(f); f.connect(g); g.connect(out); s.start(at, Math.random()); s.stop(at + 0.08);
      }
      timer = setTimeout(crackle, 120 + Math.random() * 900);
    };
    ambience = { stop() { clearTimeout(timer); out.gain.linearRampToValueAtTime(0, a.currentTime + 1.2); setTimeout(() => { src.stop(); lfo.stop(); lfo2.stop(); out.disconnect(); }, 1400); } };
    crackle();
  }
  function stopAmbience() { ambience?.stop(); ambience = null; }
  function set(changes) {
    Object.assign(settings, changes);
    try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (_) { /* this browser only */ }
    if (settings.amb) startAmbience(); else stopAmbience();
  }
  // The first gesture unlocks audio; start the ambience then if it was left on.
  const wake = () => { if (settings.amb) startAmbience(); else if (settings.fx) audio(); };
  root.addEventListener?.('pointerdown', wake, { once: true }); root.addEventListener?.('keydown', wake, { once: true });
  root.LeifSound = { play, set, get settings() { return { ...settings }; } };
})(window);
