// Blue square Lego puzzle (lock 7): slide the red tile into the slot under the bridge, then use it to drag the bridge
// and push two orange tiles out; the last one has a 5 on it. Built from assets/lego-square-step0…4.ldr. Design record: DG-H23.
import { definePuzzle } from './lego-puzzle.js';

export const { load, picture, mount } = definePuzzle({
  files: [0, 1, 2, 3, 4].map(i => new URL(`assets/lego-square-step${i}.ldr`, import.meta.url)),
  rules: {
    limitAll: 1,                                         // every loose piece moves at most one stud
    stayInside: false,                                   // pieces may stick out of the sides
    lateral: true,                                       // the red tile can be slid sideways while it is in
    handPush: (ref, files) => !!files[ref.file],         // the bridge (a submodel) can be pushed directly
    winPart: movers => movers.at(-1).find(i => movers.slice(0, -1).every(s => !s.includes(i)))   // the tile that moves only in the last step
  },
  label: { text: '5', on: 'win' },                       // written on the end of the orange tile that slides out last
  messages: {
    start: 'Click the red tile on top to pick it up.',
    held: 'Point at a hole in the side and click to slide the red tile in.',
    inserted: 'The tile is in. Slide it with ◀ ▶, push it further in, or click it to pull it out. You can also push the bridge.',
    solved: 'The orange tile slides out of the side. There’s a 5 written on it.'
  }
});
