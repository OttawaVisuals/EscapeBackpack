const { test } = require('node:test');
const assert = require('node:assert/strict');
const { preferences, clockRuns } = require('./experience.js');

test('presentation preferences tolerate missing and corrupt data without enabling sound', () => {
  for (const value of [null, false, 'bad', [], { effects: 'true', ambience: 1, motion: null }]) {
    assert.deepEqual(preferences(value), { effects: false, ambience: false, motion: true });
  }
  assert.deepEqual(preferences({ effects: true, ambience: false, motion: false, stage: 10 }), { effects: true, ambience: false, motion: false });
});

test('title, pause, idle, hidden page and completion each stop play time', () => {
  const running = { hidden: false, idle: false, title: false, paused: false, done: false };
  assert.equal(clockRuns(running), true);
  for (const reason of Object.keys(running)) assert.equal(clockRuns({ ...running, [reason]: true }), false, reason);
});
