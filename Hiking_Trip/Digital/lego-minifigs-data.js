// Lock 8 minifigs: how the user's Stud.io export (assets/lego-minifigs.ldr) splits into the six bags. No Three.js
// here, so lego.test.mjs can check it against the export. Used by lego-minifigs.js. Design record: DG-H27.

// Which bag each part of the export comes from (DG-H27: the beard goes with the grey hair).
export const BAG = {
  jobs: ['bl_973pb4534c01.dat copy', 'bl_973pb3863c01.dat', 'bl_973pb5011c01.dat copy', 'bl_973pb5515c03.dat copy', 'bl_973pb2017c01.dat copy',
    '73200b-f1.dat', 'bl_970c01pb67.dat', 'bl_970c00pb1512.dat'],
  faces: ['bl_3626cpb2144.dat', 'bl_28621pb0205.dat', 'bl_28621pb0170.dat', '3626cp7i.dat', '3626cpnb.dat'],
  hair: ['21268.dat', '93223.dat', '13785.dat', '36806.dat', '26139.dat', 'bl_44751.dat'],
  hobbies: ['25975p01.dat', '2599.dat', '93552p05.dat', '30089.dat', '98138.dat', '93559.dat'],
  pets: ['33320.dat', '36756pb01.dat', '41835.dat', 'bl_2889pb01.dat', '13786pb01.dat']
};
// The solved figures as exported, by the name printed on each base (the option values in game-data.js `parts`).
export const SOLVED = {
  DICK: { jobs: 'coat', faces: 'beard', hair: 'grey', hobbies: 'guitar', pets: 'frog' },
  MADY: { jobs: 'chef', faces: 'stars', hair: 'orange', hobbies: 'flippers', pets: 'rat' },
  JUNE: { jobs: 'ranger', faces: 'plain', hair: 'black', hobbies: 'brush', pets: 'bird' },
  RICH: { jobs: 'suit', faces: 'mark', hair: 'blonde', hobbies: 'camera', pets: 'dog' },
  BART: { jobs: 'vest', faces: 'scar', hair: 'blue', hobbies: 'stick', pets: 'cat' }
};
// The custom name bases (Stud.io custom parts “Dick_Name” … on a 3 × 4 tile, 88646).
export const NAME_FILES = { 'm72907a53_20251025_031040.dat': 'DICK', 'm72907a53_20251025_062604.dat': 'MADY', 'm72907a53_20251025_062553.dat': 'JUNE', 'm72907a53_20251025_062613.dat': 'RICH', 'm72907a53_20251025_062623.dat': 'BART' };
// Loose parts on the workbench (DG-H28): one row per bag, from the stands towards the player; tall parts sit at the
// back so they hide nothing.
export const ROWS = ['jobs', 'pets', 'hobbies', 'hair', 'faces', 'names'];
// Each row has its own order, and every other row is shifted half a place, so no column lines up a solved neighbour.
export const ORDER = {
  jobs: ['suit', 'coat', 'chef', 'vest', 'ranger'], pets: ['cat', 'rat', 'frog', 'bird', 'dog'],
  hobbies: ['brush', 'flippers', 'stick', 'guitar', 'camera'], hair: ['grey', 'blonde', 'blue', 'orange', 'black'],
  faces: ['stars', 'scar', 'mark', 'plain', 'beard'], names: ['MADY', 'JUNE', 'RICH', 'DICK', 'BART']
};
