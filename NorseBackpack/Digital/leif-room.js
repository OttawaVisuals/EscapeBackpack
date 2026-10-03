/* "Play together": the connection to a shared room on the escapepack-rooms worker.
   leif.js decides what to share; this file only connects, reconnects with back-off, and
   queues changes made while the connection is down (they are sent, merged, on reconnect). */
(function (root) {
  const ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  const newCode = () => Array.from(crypto.getRandomValues(new Uint8Array(6)), b => ALPHABET[b % ALPHABET.length]).join('');
  const validCode = code => /^[A-HJ-NP-Z2-9]{6}$/.test(code);
  const COLORS = ['#E0A26A', '#7FB8E8', '#B9A3E8', '#8FD19E', '#F08A8A', '#F2D06B', '#6ED3C9', '#E89BC8'];

  class Room {
    /* on: { welcome(game, peers, you), state(patch, full, who), peers(list), cursor(who, x, y),
            move(who, id, x, y, rot), event(who, kind, lock), status('connecting'|'live'|'retrying'|'closed', detail) } */
    constructor(server, code, me, on, game = 'norse') {
      Object.assign(this, { server: server.replace(/\/+$/, ''), code, me, on, game, ws: null, pending: null, tries: 0, left: false, live: false });
      this.connect();
    }
    connect() {
      this.on.status?.('connecting');
      let ws;
      try { ws = new WebSocket(`${this.server}/room/${this.code}?game=${this.game}`); } catch (e) { this.retry(); return; }
      this.ws = ws;
      ws.onopen = () => ws.send(JSON.stringify({ t: 'hello', name: this.me.name, color: this.me.color }));
      ws.onmessage = e => {
        let m; try { m = JSON.parse(e.data); } catch (_) { return; }
        if (m.t === 'welcome') {
          this.tries = 0; this.live = true; this.you = m.you; this.on.status?.('live');
          this.on.welcome?.(m.game, m.peers, m.you);
          if (this.pending) { const patch = this.pending; this.pending = null; this.sendState(patch); }
        } else if (m.t === 'state') this.on.state?.(m.patch, m.full, m);
        else if (m.t === 'peers') this.on.peers?.(m.peers);
        else if (m.t === 'cursor') this.on.cursor?.(m, m.x, m.y);
        else if (m.t === 'move') this.on.move?.(m, m.id, m.x, m.y, m.rot);
        else if (m.t === 'event') this.on.event?.(m, m.kind, m.lock);
        else if (m.t === 'error') this.on.status?.('live', m.message);
      };
      ws.onclose = e => { this.live = false; if (this.left) return; if (e.code === 1008 || e.code === 4003) { this.on.status?.('closed', 'This room is not available.'); return; } this.retry(); };
      ws.onerror = () => { /* onclose follows */ };
    }
    retry() {
      this.on.status?.('retrying');
      const wait = Math.min(15000, 1000 * 2 ** this.tries++);
      clearTimeout(this.timer); this.timer = setTimeout(() => { if (!this.left) this.connect(); }, wait);
    }
    send(obj) { if (this.live && this.ws?.readyState === 1) { this.ws.send(JSON.stringify(obj)); return true; } return false; }
    // State changes are never lost: while offline they merge into one pending patch.
    sendState(patch, full = false) {
      if (full) this.pending = null;
      if (this.send({ t: 'state', patch, full })) return;
      if (full || !this.pending) { this.pending = patch; return; }
      for (const [k, v] of Object.entries(patch)) this.pending[k] = k === 'pieces' ? { ...(this.pending.pieces || {}), ...v } : v;
    }
    leave() { this.left = true; clearTimeout(this.timer); try { this.ws?.close(1000, 'Left'); } catch (_) { /* gone */ } this.on.status?.('closed'); }
  }
  root.LeifRoom = { Room, newCode, validCode, COLORS };
})(window);
