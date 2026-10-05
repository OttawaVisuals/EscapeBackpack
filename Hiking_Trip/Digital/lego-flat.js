// Flat brown Lego puzzle (lock 7): push the green tile into holes in the sides to free the red piece with a 1.
// Built from the Stud.io exports in assets/lego-flat-step0…3.ldr (start, then one file per push). Design record: DG-H21.
import { definePuzzle } from './lego-puzzle.js';

export const { load, picture, mount } = definePuzzle({
  files: [0, 1, 2, 3].map(i => new URL(`assets/lego-flat-step${i}.ldr`, import.meta.url)),
  rules: { limitByColor: { 25: 1 } },                    // every orange tile is held by a stud: one stud of travel, never out of the box
  label: { text: '1', on: 'goal' },                      // written on the red round tile
  messages: {
    start: 'Click the green tile to pick it up.',
    held: 'Point at a hole in the side and click to slide the green tile in.',
    solved: 'The red piece slides out and drops onto the table. There’s a 1 written on it.'
  }
});
