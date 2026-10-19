/* Presentation, optional synthesised audio and player preferences. No puzzle answers. */
(function (root) {
  'use strict';
  const defaults = { effects: false, ambience: false, motion: true };
  function preferences(value) {
    const p = value && typeof value === 'object' ? value : {};
    return Object.fromEntries(Object.entries(defaults).map(([key, fallback]) => [key, typeof p[key] === 'boolean' ? p[key] : fallback]));
  }
  function clockRuns({ hidden, idle, title, paused, done }) { return !hidden && !idle && !title && !paused && !done; }
  function init() {
    const $ = id => document.getElementById(id), key = 'escape-backpack.hiking-preferences.v1';
    let prefs = preferences(), context, master, fire, air, active = false, ringUntil = 0, suspendTimer;
    try { prefs = preferences(JSON.parse(localStorage.getItem(key))); } catch (_) { /* Defaults work without storage. */ }
    function persist() { try { localStorage.setItem(key, JSON.stringify(prefs)); } catch (_) { /* Preferences remain for this visit. */ } }
    function audio() {
      const Audio = window.AudioContext || window.webkitAudioContext;
      if (!Audio) return false;
      if (!context) {
        context = new Audio(); master = context.createGain(); master.gain.value = .22; master.connect(context.destination);
        // Soft, filtered noise: no files, network calls or recurring timers.
        const buffer = context.createBuffer(1, context.sampleRate * 4, context.sampleRate), data = buffer.getChannelData(0);
        let brown = 0;
        for (let i = 0; i < data.length; i++) { brown = (brown + (Math.random() * 2 - 1) * .02) / 1.02; data[i] = brown * 3; }
        fire = context.createBufferSource(); fire.buffer = buffer; fire.loop = true;
        const filter = context.createBiquadFilter(); filter.type = 'lowpass'; filter.frequency.value = 650;
        air = context.createGain(); air.gain.value = 0; fire.connect(filter); filter.connect(air); air.connect(master); fire.start();
      }
      return true;
    }
    function syncAudio(gesture = false) {
      clearTimeout(suspendTimer);
      if (!prefs.effects && !prefs.ambience) { context?.suspend().catch(() => {}); return; }
      if (gesture) { try { if (!audio()) return; } catch (_) { return; } }
      if (!context) return;
      if (!active || document.hidden) {
        air.gain.setTargetAtTime(0, context.currentTime, .1);
        const remaining = document.hidden ? 0 : Math.max(0, ringUntil - context.currentTime) * 1000;
        if (remaining) suspendTimer = setTimeout(() => { ringUntil = 0; context.suspend().catch(() => {}); }, remaining);
        else { ringUntil = 0; context.suspend().catch(() => {}); }
        return;
      }
      if (gesture) context.resume().catch(() => {});
      air.gain.setTargetAtTime(prefs.ambience ? .22 : 0, context.currentTime, .3);
    }
    function apply() {
      document.documentElement.classList.toggle('reduced-motion', !prefs.motion);
      $('setting-effects').checked = prefs.effects; $('setting-ambience').checked = prefs.ambience; $('setting-motion').checked = prefs.motion;
      $('intro-sound').checked = prefs.effects || prefs.ambience;
      $('sound-toggle').setAttribute('aria-pressed', String(prefs.effects || prefs.ambience));
      $('sound-toggle').textContent = prefs.effects || prefs.ambience ? 'Sound on' : 'Sound off';
    }
    for (const name of Object.keys(defaults)) $('setting-' + name).addEventListener('change', e => {
      prefs[name] = e.target.checked; persist(); apply(); syncAudio(true); if (name === 'effects') cue('select');
    });
    function toggleSound(on) { prefs.effects = prefs.ambience = on; persist(); apply(); syncAudio(true); cue('select'); }
    $('intro-sound').addEventListener('change', e => toggleSound(e.target.checked));
    $('sound-toggle').addEventListener('click', () => toggleSound(!(prefs.effects || prefs.ambience)));
    function cue(kind) {
      if (!prefs.effects || !active || document.hidden) return;
      try {
        if (!audio() || context.state !== 'running') return;
        if (kind === 'finish') ringUntil = context.currentTime + 1.3;
        const notes = kind === 'finish' ? [523.25, 659.25, 783.99, 1046.5] : kind === 'unlock' ? [392, 523.25, 659.25] : kind === 'wrong' ? [164.81, 146.83] : kind === 'wheel' ? [700] : [440];
        const step = ['finish', 'unlock'].includes(kind) ? .14 : .055;
        notes.forEach((frequency, i) => {
          const at = context.currentTime + i * step, osc = context.createOscillator(), gain = context.createGain();
          osc.type = kind === 'wheel' ? 'triangle' : 'sine'; osc.frequency.value = frequency;
          gain.gain.setValueAtTime(0, at); gain.gain.linearRampToValueAtTime(kind === 'wheel' ? .06 : .35, at + .008);
          gain.gain.exponentialRampToValueAtTime(.0001, at + (kind === 'finish' ? .7 : .2));
          osc.connect(gain); gain.connect(master); osc.start(at); osc.stop(at + .8);
          osc.onended = () => { osc.disconnect(); gain.disconnect(); };
        });
      } catch (_) { /* Audio support never blocks play. */ }
    }
    // Resume only after an input gesture, including a return from another tab.
    document.addEventListener('pointerdown', () => syncAudio(true), { passive: true });
    document.addEventListener('keydown', () => syncAudio(true), { passive: true });
    document.addEventListener('visibilitychange', () => syncAudio());
    apply();
    return {
      cue,
      setActive(on, gesture = false) { active = on; syncAudio(gesture); },
      motion() { return prefs.motion && !matchMedia('(prefers-reduced-motion: reduce)').matches; },
      progress(state, locks) {
        const done = state.stage === locks.length;
        $('trail-fill').style.width = `${state.stage / locks.length * 100}%`;
        $('trail-progress').setAttribute('aria-valuenow', state.stage);
        $('trail-progress').setAttribute('aria-valuetext', `${state.stage} of ${locks.length} locks opened`);
        $('trail-status').textContent = done ? 'Adventure complete' : `${state.stage} of ${locks.length} locks opened`;
        $('camp-chapter').textContent = done ? 'A happy ending' : state.stage === 0 ? 'The trail begins' : state.stage < 5 ? 'Follow the clues' : state.stage < 9 ? 'Deeper into the backpack' : 'One last mystery';
        $('camp-objective').textContent = done ? 'Juno’s plushy is free. Take a moment by the fire.' : 'Your mission: free Juno’s favourite plushy.';
        $('pause-progress').textContent = done ? 'All ten locks opened' : `Lock ${state.stage + 1} · ${locks[state.stage].name}`;
        $('intro-resume').hidden = state.played === 0 && state.stage === 0;
        $('intro-resume').textContent = done ? 'Adventure complete · return to your camp table' : `Your saved adventure · ${state.stage} / ${locks.length} locks open`;
        $('begin-label').textContent = state.played || state.stage ? 'Return to camp' : 'Begin your adventure';
        $('ending-summary').textContent = `${locks.length} locks. One very happy reunion.`;
        $('final-stats').replaceChildren(...[...$('ending-stats').childNodes].map(n => n.cloneNode(true)));
        document.body.classList.toggle('adventure-complete', done);
      },
      reveal(ids) {
        for (const id of ids) {
          const node = document.querySelector(`.prop[data-id="${id}"]`); if (!node) continue;
          node.classList.add('new-find'); setTimeout(() => node.classList.remove('new-find'), 2200);
        }
      }
    };
  }
  const api = { preferences, clockRuns, init };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.HikingExperience = api;
})(typeof window === 'undefined' ? globalThis : window);
