/* Hiking online: original clues and grids, adapted for a browser.
   Sources and adaptation decisions are recorded in index.html#design-notes.
   This local playtest checks answers in JavaScript; it is not spoiler-proof. */
(function (root) {
  'use strict';
  const grid = [
    'XBRRCMTJWDOAHLKK',
    'WETWTEGROFMMMADD',
    'GJDFAITWASRALRJJ',
    'DKHLSTBMIPXWKJFF',
    'KREDIWITLELOCKPP',
    'YHRSCLBMUWUMDCEE',
    'QORAYHWDSHXAGADD',
    'MPIHEHKYLLHELPMM',
    'ATNHRISAZVFNGKVV',
    'HEGXUFGUIIQCLCLL',
    'MATDVBJXGMDIKAUU',
    'EYCKHTSGUTTSEBWW',
    'ENASNEESRUHESQCC',
    'HOWZWTVZMUURVKII',
    'DNFJAYJNFEQODGFF'
  ];
  // Six fixed entries, and the blue square at row 1, column 3, match the PDF.
  const givens = [0, 0, 0, 0, 4, 2, 0, 1, 1, 0, 2, 4, 0, 0, 0, 0];
  // x/y are fixed starting spots for the first eight props; later props go in the first free space.
  const items = {
    bottle: { name: 'Water bottle', kind: 'Three sides to explore', w: 180, h: 395, x: 490, y: 120, faces: 3, origin: 'FROM THE SIDE POCKET' },
    note: { name: 'A note to myself', kind: 'Handwritten note', w: 315, h: 423, x: 302, y: 90, faces: 2, origin: 'FROM THE FRONT COMPARTMENT' },
    sheet: { name: 'Puzzle sheet', kind: 'Word search + Sudoku', w: 375, h: 496, x: 735, y: 45, faces: 2, origin: 'FROM THE FRONT COMPARTMENT' },
    blue0: { name: 'Blue Lego 0', kind: 'A number built from Lego', w: 120, h: 160, faces: 1, origin: 'FROM THE FRONT COMPARTMENT' },
    hobbies: { name: 'Bag of Lego parts', kind: 'Labelled “Hobbies”', w: 170, h: 190, faces: 1, origin: 'FROM THE FRONT COMPARTMENT', bag: 'hobbies' },
    grandparents: { name: 'Card from Gran and Pops', kind: 'A thank-you card', w: 360, h: 320, x: 320, y: 555, faces: 2, origin: 'FROM THE FRONT POCKET' },
    newspaper: { name: 'Newspaper clipping', kind: 'An article tucked in the card', w: 195, h: 281, x: 1140, y: 70, faces: 2, origin: 'FROM THE THANK-YOU CARD', hiddenIn: 'grandparents' },
    flat: { name: 'Flat brown Lego puzzle', kind: 'A Lego puzzle with a green tile on top', w: 230, h: 230, faces: 1, origin: 'FROM THE FRONT POCKET' },
    iss: { name: 'A night under the stars', kind: 'A note with an ISS drawing', w: 420, h: 470, x: 1600, y: 70, faces: 1, origin: 'FROM THE MAIN COMPARTMENT' },
    periodic: { name: 'Periodic table', kind: 'Reference sheet', w: 610, h: 343, x: 1040, y: 760, faces: 1, origin: 'FROM THE MAIN COMPARTMENT' },
    calculator: { name: 'Pocket calculator', kind: 'For working things out', w: 260, h: 375, x: 1740, y: 720, faces: 2, origin: 'FROM THE MAIN COMPARTMENT' },
    instructions: { name: 'Satellite instructions', kind: 'A Lego building booklet', w: 330, h: 255, faces: 1, origin: 'FROM THE MAIN COMPARTMENT' },
    equation: { name: 'How high is the ISS?', kind: 'A note with an equation', w: 400, h: 360, faces: 2, origin: 'FROM THE MAIN COMPARTMENT' },
    cube: { name: 'Lego cube pieces', kind: 'Six flat Lego pieces', w: 220, h: 220, faces: 1, origin: 'FROM THE MAIN COMPARTMENT' },
    jobs: { name: 'Bag of Lego parts', kind: 'Labelled “Jobs”', w: 170, h: 190, faces: 1, origin: 'FROM THE MAIN COMPARTMENT', bag: 'jobs' },
    pouch: { name: 'Locked pouch', kind: 'Four zipped pockets, four locks', w: 380, h: 220, faces: 1, origin: 'FROM THE MAIN COMPARTMENT' },
    treasure: { name: 'Treasure bag', kind: 'A velvet bag with its own lock', w: 240, h: 280, faces: 1, origin: 'FROM THE MAIN COMPARTMENT' },
    satellite: { name: 'Lego satellite pieces', built: 'Lego satellite', kind: 'Build it with the instructions', w: 330, h: 240, faces: 1, origin: 'FROM THE TOP POCKET' },
    pets: { name: 'Bag of Lego parts', kind: 'Labelled “Pets”', w: 170, h: 190, faces: 1, origin: 'FROM THE TOP POCKET', bag: 'pets' },
    orange4: { name: 'Orange Lego 4', kind: 'A number built from Lego', w: 120, h: 160, faces: 1, origin: 'FROM THE TOP POCKET' },
    otter: { name: 'Jigsaw puzzle', kind: 'Twelve pieces in a box', w: 300, h: 250, faces: 1, origin: 'FROM THE INSIDE POCKET' },
    cards: { name: 'Hockey cards', kind: 'A stack of ten player cards', w: 210, h: 290, faces: 1, origin: 'FROM THE INSIDE POCKET' },
    faces: { name: 'Bag of Lego parts', kind: 'Labelled “Faces”', w: 170, h: 190, faces: 1, origin: 'FROM THE INSIDE POCKET', bag: 'faces' },
    square: { name: 'Blue square Lego puzzle', kind: 'A Lego puzzle with a red tile on top', w: 230, h: 230, faces: 1, origin: 'FROM THE POUCH FRONT POCKET' },
    hair: { name: 'Bag of Lego parts', kind: 'Labelled “Hair”', w: 170, h: 190, faces: 1, origin: 'FROM THE POUCH FRONT POCKET', bag: 'hair' },
    notepad: { name: 'Notepad', kind: 'Notes about the neighbours', w: 330, h: 440, faces: 2, origin: 'FROM THE POUCH MAIN POCKET' },
    brown1: { name: 'Brown Lego 1', kind: 'A number built from Lego', w: 120, h: 160, faces: 1, origin: 'FROM THE POUCH MAIN POCKET' },
    names: { name: 'Bag of Lego parts', kind: 'Labelled “Names”', w: 170, h: 190, faces: 1, origin: 'FROM THE POUCH MAIN POCKET', bag: 'names' },
    agenda: { name: 'Daily schedule', kind: 'A page from an agenda', w: 310, h: 450, faces: 2, origin: 'FROM THE POUCH BACK POCKET' },
    map: { name: 'Map pieces', kind: 'Nine pieces of a street map', w: 360, h: 220, faces: 1, origin: 'FROM THE POUCH BACK POCKET' },
    red3: { name: 'Red Lego 3', kind: 'A number built from Lego', w: 120, h: 160, faces: 1, origin: 'FROM THE POUCH INSIDE POCKET' }
  };
  // The order of the bottle views does not give away the chronological ordering.
  const stickers = ['assets/sticker-dog.jpg', 'assets/sticker-dinosaur.jpg', 'assets/sticker-mammoth.jpg'];
  const locks = [
    { name: 'Front compartment', answer: '749', releases: ['note', 'sheet', 'blue0', 'hobbies'], selected: 'note', prompt: 'The bottle came out of the side pocket. Take a closer look.', title: 'The front compartment opens.', message: 'Inside are a note, a puzzle sheet, a blue Lego 0 and a bag of Lego parts. They’re on your table now. Read the note, then inspect the sheet to work on it.', hints: [
      'Look closely at the water bottle from the side pocket. Turn it to see all three stickers.',
      'Some numbers are hidden in the animals’ drawings.',
      'Think about the era of each animal. Put them in order from oldest to most recent.',
      'Dinosaur 7, mammoth 4, husky 9. The combination is 749.'
    ] },
    { name: 'Front pocket', answer: '734', releases: ['grandparents', 'newspaper', 'flat'], selected: 'grandparents', prompt: 'A note and a puzzle sheet were tucked inside. See what they tell you.', title: 'A card from Gran and Pops.', message: 'The front pocket opens. Inside are a thank-you card and a flat brown Lego puzzle. Both are on your table.', hints: [
      'Some things you find are for later. The word search and the Sudoku are what you need now. You can mark the grid and fill the empty cells.',
      'Find the underlined words from the note in the word search. Mark each one with a straight line.',
      'Step back from your markings: they form two digits. The blue Sudoku cell gives the last digit.',
      'The word-search markings form 7 and 3. The blue Sudoku cell is 4. The combination is 734.'
    ] },
    { name: 'Main compartment', answer: 'MOON', letters: true, releases: ['iss', 'periodic', 'calculator', 'instructions', 'equation', 'cube', 'jobs', 'pouch', 'treasure'], selected: 'iss', prompt: 'Gran and Pops sent a card. This lock takes four letters.', title: 'Into the main compartment.', message: 'The main compartment holds the most: a note about the night sky, a periodic table, a calculator, Lego instructions, a note with an equation, Lego pieces, a locked pouch and a treasure bag. Most of it is for later.', hints: [
      'Some things you find are for later. The thank-you card from Gran and Pops has all you need.',
      'Open the card. Something was tucked inside it.',
      'Look closely at the photograph in the newspaper clipping. You are looking for a word about the dog.',
      'The dog’s name tag reads MOON. The four-letter combination is MOON.'
    ] },
    { name: 'Top pocket', answer: '326', releases: ['satellite', 'pets', 'orange4'], selected: 'satellite', prompt: 'You have a lot of new things. Only a few of them open this lock.', title: 'The top pocket opens.', message: 'Inside are the pieces for a Lego satellite, another bag of Lego parts and an orange Lego 4.', hints: [
      'You have a lot of items now, but some are missing pieces. A clue and a tool from the main compartment open this lock.',
      'The periodic table might help, and some addition might be needed. The calculator is there to help.',
      'The note with the ISS drawing has a clue to use with the periodic table. The numbers at the top left of some elements come in handy.',
      'KNoWN PHYSiCs splits into K, No, W, N, P, H, Y, Si and Cs. 19 + 102 + 74 + 7 + 15 + 1 + 39 + 14 + 55 = 326.'
    ] },
    { name: 'Inside pocket', answer: '414', releases: ['otter', 'cards', 'faces'], selected: 'otter', prompt: 'The last lock on the backpack itself. Three digits.', title: 'The inside pocket opens.', message: 'Inside are a jigsaw puzzle, a stack of hockey cards and another bag of Lego parts. The next locks are on the pouch.', hints: [
      'With the new items and what you already have, you can open the last lock on the backpack.',
      'Build the Lego satellite with the instructions. With the note about the ISS, the calculator and the model, you can solve the problem.',
      'The note gives the equation. The three values are written on things you already have; check their backs too. The correction comes from the satellite and the scribbles on the back of the note.',
      'GM = 401,926.91 (back of the calculator), v = 7.7 (back of the clipping), Re = 6,371 (instructions, step 4). 401,926.91 ÷ (7.7 × 7.7) − 6,371 = 408. Lined up with the red marks, the satellite’s rings circle + S I X. 408 + 6 = 414.'
    ] },
    { name: 'Pouch · front pocket', answer: '102', releases: ['square', 'hair'], selected: 'square', prompt: 'The pouch has four pockets, each with its own lock. Start with the front one.', title: 'The pouch’s front pocket opens.', message: 'Inside are a blue square Lego puzzle and another bag of Lego parts.', hints: [
      'The new items help you into the first pocket of the pouch.',
      'Finish the jigsaw puzzle. It may tell you how to get the combination.',
      'Turn the finished puzzle over. It tells you what to look for on the hockey cards. The calculator can help again.',
      'The back reads “Card numbers of Canadian-born players”. Bourbonnais #13 + Watts #22 + Larocque #18 + Spooner #49 = 102.'
    ] },
    { name: 'Pouch · main pocket', answer: '518', releases: ['notepad', 'brown1', 'names'], selected: 'notepad', prompt: 'You now have the last piece of something you’ve had for a while.', title: 'The pouch’s main pocket opens.', message: 'Inside are a notepad, a brown Lego 1 and a bag of Lego name tiles.', hints: [
      'You have just received the last item for a puzzle you’ve had for a while.',
      'You have three Lego puzzles. You already have something that tells you the order of their numbers.',
      'The card from Gran and Pops gives the order. On the blue square, use the red tile on top to push and pull the tiles. On the flat brown one, use the green tile to push the orange tiles and free a hidden piece. The cube pieces fit together and show two numbers to add.',
      'The square shows 5. The flat puzzle frees a round tile with a 1. The cube shows 5 + 3 = 8. The combination is 518.'
    ] },
    { name: 'Pouch · back pocket', answer: 'DICK', letters: true, releases: ['agenda', 'map'], selected: 'notepad', prompt: 'This lock takes four letters.', title: 'The pouch’s back pocket opens.', message: 'Inside are a page from an agenda and a street map cut into nine pieces.', hints: [
      'You have collected several bags of Lego parts. Now is the time to use them.',
      'The notepad tells you how to put the Lego parts together.',
      'You are looking for the doctor. Build the five neighbours as you read the notes, then read the doctor’s name.',
      'The doctor has grey hair, a beard, a frog and a guitar. His name is DICK.'
    ] },
    { name: 'Pouch · inside pocket', answer: '632', releases: ['red3'], selected: 'map', prompt: 'The last pocket of the pouch. Three digits.', title: 'The pouch’s inside pocket opens.', message: 'Inside is a red Lego 3. Only the treasure bag is still locked.', hints: [
      'The map and the agenda together give you what you need.',
      'Put the map back together. The agenda tells you where you went that day, and the neighbours you built tell you whose houses those are.',
      'The date gives the first two digits. Draw the errands on the map, in order, to find the last one.',
      'The date is 6 / 3. The errands trace a 2. The combination is 632.'
    ] },
    { name: 'Treasure bag', answer: '4130', releases: [], selected: 'red3', prompt: 'The final lock. Four digits.', title: 'The treasure bag opens!', message: 'Inside are Juno’s plushy and a card: “Congratulations! You completed the game! Feel free to keep the plushy!”', hints: [
      'This is the final lock. You have every piece you need.',
      'You have four numbers made of Lego. Find the clues that put them in order.',
      'Look back at your clues and their backs. Small coloured stickers order the Lego numbers by colour.',
      'Orange I, brown II, red III, blue IV: 4, 1, 3, 0. The combination is 4130.'
    ] }
  ];

  // Lock 5: values written around the backpack (instructions page 3 shows Re at step 4).
  const values = { GM: '401,926.91 km³/s²', v: '7.7 km/s', Re: '6,371 km' };
  // Lock 6: redrawn cards with no league photos or branding. The four Canadian-born players match the physical solution.
  const hockey = [
    { name: 'Hilary Knight', number: 7, position: 'Forward', born: 'Palo Alto, California, USA' },
    { name: 'Jaime Bourbonnais', number: 13, position: 'Defence', born: 'Mississauga, Ontario, Canada' },
    { name: 'Ronja Savolainen', number: 44, position: 'Defence', born: 'Helsinki, Finland' },
    { name: 'Daryl Watts', number: 22, position: 'Forward', born: 'Toronto, Ontario, Canada' },
    { name: 'Kendall Coyne Schofield', number: 26, position: 'Forward', born: 'Palos Heights, Illinois, USA' },
    { name: 'Jocelyne Larocque', number: 18, position: 'Defence', born: 'Ste. Anne, Manitoba, Canada' },
    { name: 'Lee Stecklein', number: 31, position: 'Defence', born: 'Roseville, Minnesota, USA' },
    { name: 'Natalie Spooner', number: 49, position: 'Forward', born: 'Scarborough, Ontario, Canada' },
    { name: 'Taylor Heise', number: 9, position: 'Forward', born: 'Lake City, Minnesota, USA' },
    { name: 'Megan Keller', number: 5, position: 'Defence', born: 'Farmington Hills, Michigan, USA' }
  ];
  // Lock 8: the six bags of parts. Values are what the riddle refers to; labels are what the player sees.
  const parts = {
    hobbies: { label: 'Holding', options: [['guitar', 'Guitar'], ['stick', 'Hockey stick'], ['brush', 'Paintbrush'], ['camera', 'Camera'], ['flippers', 'Flippers']] },
    jobs: { label: 'Outfit', options: [['coat', 'Doctor’s coat'], ['vest', 'Engineer’s safety vest'], ['ranger', 'Park ranger shirt'], ['suit', 'Astronaut suit'], ['chef', 'Chef’s jacket']] },
    pets: { label: 'Pet', options: [['frog', 'Frog'], ['cat', 'Cat'], ['bird', 'Bird'], ['dog', 'Dog'], ['rat', 'Rat']] },
    faces: { label: 'Face', options: [['beard', 'Beard'], ['scar', 'Scar on the left eyebrow'], ['plain', 'Big smile and headband'], ['mark', 'Birth mark'], ['stars', 'Starry face tattoo']] },
    hair: { label: 'Hair', options: [['grey', 'Grey hair'], ['blue', 'Blue hair'], ['black', 'Black hair'], ['blonde', 'Blonde hair'], ['orange', 'Orange hair']] },
    names: { label: 'Name tile', options: [['DICK', 'DICK'], ['BART', 'BART'], ['JUNE', 'JUNE'], ['RICH', 'RICH'], ['MADY', 'MADY']] }
  };
  const partOrder = ['names', 'hair', 'faces', 'jobs', 'hobbies', 'pets'];
  const riddle = [
    'With my ADHD, I forgot some of the details about my neighbours. I remember a few things about their jobs, hobbies, pets and physical features. Hopefully I can piece everything together, as I really need to go see the doctor that lives close by before going on this trip.',
    'Rich is the only one with a visible birth mark on their face.', 'The engineer is the only one who has a scar on their left eyebrow.', 'The person with orange hair keeps a rat as a pet.', 'The park ranger is the only one who enjoys painting.', 'Mady does not have grey, black, or blonde hair.', 'Whoever loves photography has blonde hair.', 'Bart is the one who has the scar.', 'The astronaut is the one who owns the dog.', 'The chef is the one who has a starry face tattoo.', 'The person with the birth mark loves photography.', 'Bart does not have grey, black, or blonde hair.', 'Whoever enjoys music has a beard.', 'June is the one wearing a headband.', 'The doctor is the one who keeps the frog as a pet.', 'The person with grey hair is the one who enjoys music.', 'The astronaut has blonde hair.', 'The engineer’s favourite sport is hockey.', 'The park ranger is the one who keeps the bird.', 'Whoever enjoys painting is the one wearing the headband.', 'Mady is the only one with a face tattoo.', 'The person with the headband has black hair.', 'Whoever plays hockey is the one who owns the cat.', 'Dick has grey hair.'
  ];
  // Lock 7: the square and flat Lego puzzles are 3D (lego-square.js, lego-flat.js; DG-H21, DG-H23). Each save is the
  // list of moves made (lego-sim.js `act`), replayed when the puzzle is shown. The cube is six pieces (lego-cube.js, DG-H31).
  const legoAction = /^(in:(left|right|front|back):-?\d{1,3}:-?\d{1,3}|deeper|out|shift:[+-]1|hand:\d{1,2}:-?[01],-?[01])$/;
  // Cube (DG-H31): six flat pieces, each a 4 × 4 grid of 2 × 2-stud cells one cell thick, from the designer's Stud.io
  // export (assets/lego-cube-flat.ldr). Rows run along the piece's LDraw z, columns along x, seen from the tiled side.
  // They close into a hollow 4 × 4 × 4 cube; each piece covers one face, sharing the edge and corner cells.
  const cubePieces = {
    red: ['#.#.', '###.', '.##.', '##..'],
    blue: ['..#.', '.##.', '####', '#...'],
    green: ['..#.', '####', '###.', '#.#.'],
    pink: ['#.##', '###.', '###.', '#.#.'],
    orange: ['.#..', '.###', '####', '.#..'],
    purple: ['..#.', '###.', '.###', '.#.#']
  };
  const cubeFaces = ['front', 'right', 'back', 'left', 'top', 'bottom'];
  // The solved cube as the designer exported it (assets/lego-cube.ldr; red on top), [face, turn, flip] per piece.
  const cubeSolved = { red: [4, 1, 0], blue: [0, 1, 0], green: [5, 1, 0], pink: [2, 1, 0], orange: [3, 3, 0], purple: [1, 3, 0] };
  // Black marker “5 + 3” round the sides of the solved cube (DG-H33). Each symbol sits on a vertical corner, half on each
  // side face, so it is split over two or three pieces and reads only once the cube is built (game.test.cjs checks the
  // split). corner c lies between side faces c and c + 1 (front, right, back, left), so turning the cube left reads
  // 5, +, 3. Strokes are lines through points in the symbol's box (0–1, y down); width is in faces; pen is 0.12 of a face.
  const arc = (cx, cy, r, from, to, n = 24) => Array.from({ length: n + 1 }, (_, i) => { const a = (from + (to - from) * i / n) * Math.PI / 180; return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; });
  const cubeMarks = [
    { text: '5', corner: 1, width: 1.3, strokes: [[[0.84, 0.12], [0.22, 0.12], [0.19, 0.46]], arc(0.47, 0.64, 0.31, -150, 150)] },
    { text: '+', corner: 2, width: 1, strokes: [[[0.5, 0.1], [0.5, 0.9]], [[0.1, 0.5], [0.9, 0.5]]] },
    { text: '3', corner: 3, width: 1.3, strokes: [[[0.2, 0.15], ...arc(0.47, 0.31, 0.21, -150, 90).slice(1)], arc(0.47, 0.69, 0.23, -90, 150)] }
  ];
  const cubePen = 0.12;
  // Jigsaw: twelve tiles (4 × 3); map: nine tiles (3 × 3). board[position] = tile number.
  const boards = { otter: { cols: 4, rows: 3, start: [7, 2, 10, 4, 0, 9, 5, 11, 1, 6, 3, 8] }, map: { cols: 3, rows: 3, start: [5, 8, 1, 6, 3, 0, 7, 2, 4] } };
  const satellitePages = 10; // Instruction pages 2–11 hold the 15 steps.
  // Props fill about half the table at each stage, so a free space can always be found.
  const sizes = [[1200, 660], [1680, 924], [1920, 1056], [2800, 1540], [2900, 1595], [3040, 1672], [3120, 1716], [3260, 1793], [3400, 1870], [3400, 1870], [3400, 1870]];

  const visible = (id, found = []) => !items[id].hiddenIn || found.includes(id);
  const available = (stage, found = []) => ['bottle', ...locks.slice(0, stage).flatMap(lock => lock.releases)].filter(id => visible(id, found));
  // The table's size: the stage's, or the tight one Tidy made (state.table) until something needs the full table again.
  const tableSize = (stage, state) => { if (state?.table) return state.table; const [w, h] = sizes[Math.min(stage, sizes.length - 1)]; return { w, h }; };
  // Retain the original key/version so earlier opening saves continue.
  const fresh = () => ({ game: 'hiking-opening', version: 1, stage: 0, pieces: {}, lines: [], sudoku: [...givens], hints: locks.map(() => 0), ratings: locks.map(() => 0), table: null, notes: '', calculator: { expression: '', result: '' },
    found: [], satellite: { built: 0, on: false, x: 40, y: 60, rot: 35 }, otter: [...boards.otter.start], map: [...boards.map.start], mapLines: [],
    push: { square: { actions: [] }, flat: { actions: [] } }, cube: {}, figures: Array.from({ length: 5 }, () => ({})) });
  // The letters on each wheel of the four-letter padlock (Master Lock 643DWD): the letters that occur in each position of the
  // manual's list of 358 words and names (every wheel has ten). A code must be made of these.
  const wheelLetters = ['BDJLMNPRST', 'AEHILORTUY', 'ACDELNORST', 'DEHKLNRSTY'];
  const normalizeAnswer = (stage, answer) => String(answer).trim().toUpperCase().replace(locks[stage]?.letters ? /[^A-Z]/g : /[^0-9]/g, '').slice(0, locks[stage]?.answer.length || 0);

  // Footprint on the table, including the caption under each prop.
  function box(id, p) {
    const item = items[id], sideways = p.rot % 180 !== 0, w = sideways ? item.h : item.w, h = sideways ? item.w : item.h;
    return { x: p.x + (item.w - w) / 2, y: p.y + (item.h - h) / 2, w, h: h + 34 };
  }
  const overlaps = (a, b, gap) => a.x < b.x + b.w + gap && b.x < a.x + a.w + gap && a.y < b.y + b.h + gap && b.y < a.y + a.h + gap;
  function freeSpot(state, id, taken) {
    const item = items[id], table = tableSize(state.stage, state);
    for (const gap of [30, 12]) for (let y = 30; y + item.h + 40 <= table.h; y += 15) for (let x = 30; x + item.w + 15 <= table.w; x += 15) {
      const b = { x, y, w: item.w, h: item.h + 34 };
      if (!taken.some(t => overlaps(b, t, gap))) return { x, y };
    }
    return null;
  }
  // Returns false when the table had to be laid out again to make room.
  function place(state, id, tidying = false) {
    const item = items[id], taken = available(state.stage, state.found).filter(other => other !== id && state.pieces[other] && !state.pieces[other].stowed).map(other => box(other, state.pieces[other]));
    const fixed = item.x !== undefined && !taken.some(t => overlaps({ x: item.x, y: item.y, w: item.w, h: item.h + 34 }, t, 10));
    const spot = fixed ? { x: item.x, y: item.y } : freeSpot(state, id, taken);
    if (!spot && !tidying) { state.pieces[id] = { x: 30, y: 30, rot: 0, face: 0, stowed: false }; layout(state); return false; }
    state.pieces[id] = { x: spot ? spot.x : 30, y: spot ? spot.y : 30, rot: 0, face: 0, stowed: false };
    return true;
  }
  // Tidy: pack the props on the smallest table that holds them (shelves of props, a little padding), keeping puzzle work and
  // faces. Put-away items stay put away. The table shrinks to the packing, so the props show as large as they can.
  function layout(state) {
    const PAD = 24, GAP = 24, FRAME = 1.75;           // the frame is about 1.75 times wider than tall
    const ids = available(state.stage, state.found), faces = Object.fromEntries(ids.map(id => [id, state.pieces[id]?.face || 0]));
    const away = new Set(ids.filter(id => state.pieces[id]?.stowed)), live = ids.filter(id => !away.has(id));
    const all = live.map(id => ({ id, w: items[id].w, h: items[id].h + 34 }));
    const orders = [(p, q) => q.h - p.h || q.w - p.w, (p, q) => q.w - p.w || q.h - p.h, (p, q) => q.w * q.h - p.w * p.h];   // tallest, widest, biggest first
    let best = null;
    const widest = Math.max(0, ...all.map(x => x.w)), total = all.reduce((n, x) => n + x.w + GAP, 0);
    for (const order of orders) {
      const boxes = [...all].sort(order);
      for (let W = widest; W <= Math.max(widest, total); W += 10) {
        let x = 0, y = 0, rowH = 0, usedW = 0; const pos = {};
        for (const box of boxes) {
          if (x > 0 && x + box.w > W) { y += rowH + GAP; x = 0; rowH = 0; }
          pos[box.id] = [x, y]; x += box.w + GAP; rowH = Math.max(rowH, box.h); usedW = Math.max(usedW, x - GAP);
        }
        const H = y + rowH, score = Math.max(usedW, FRAME * H);
        if (!best || score < best.score - 1e-6) best = { score, pos, w: usedW, h: H };
      }
    }
    for (const id of ids) delete state.pieces[id];
    for (const id of live) state.pieces[id] = { x: PAD + best.pos[id][0], y: PAD + best.pos[id][1], rot: 0, face: faces[id], stowed: false };
    for (const id of away) state.pieces[id] = { x: PAD, y: PAD, rot: 0, face: faces[id], stowed: true };
    state.table = { w: Math.max(480, Math.ceil(best.w + 2 * PAD)), h: Math.max(300, Math.ceil(best.h + 2 * PAD)) };
  }

  function calculate(expression) {
    const source = String(expression).replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-').replace(/[\s,]/g, '');
    if (!source || source.length > 160) throw new Error('Enter a calculation.');
    const tokens = source.match(/(?:\d+\.?\d*|\.\d+)|[()+*/-]/g) || [];
    if (tokens.join('') !== source) throw new Error('Use numbers and + − × ÷ ( ).');
    let index = 0, depth = 0;
    function atom() {
      if (++depth > 40) throw new Error('Too many brackets.');
      const token = tokens[index++]; let value;
      if (token === '+' || token === '-') value = (token === '-' ? -1 : 1) * atom();
      else if (token === '(') { value = sum(); if (tokens[index++] !== ')') throw new Error('Close the brackets.'); }
      else if (token && /^(?:\d+\.?\d*|\.\d+)$/.test(token)) value = Number(token);
      else throw new Error('Finish the calculation.');
      depth--; return value;
    }
    function product() { let value = atom(); while (tokens[index] === '*' || tokens[index] === '/') { const op = tokens[index++], rhs = atom(); if (op === '/' && rhs === 0) throw new Error('Cannot divide by zero.'); value = op === '*' ? value * rhs : value / rhs; } return value; }
    function sum() { let value = product(); while (tokens[index] === '+' || tokens[index] === '-') { const op = tokens[index++], rhs = product(); value = op === '+' ? value + rhs : value - rhs; } return value; }
    const value = sum(); if (index !== tokens.length || !Number.isFinite(value)) throw new Error('Check the calculation.');
    return Number(value.toPrecision(12));
  }
  const integer = (n, low, high) => Number.isInteger(n) && n >= low && n <= high;
  function validLine(line) {
    if (!Array.isArray(line) || line.length !== 4 || !line.every((n, i) => integer(n, 0, i % 2 ? 15 : 14))) return false;
    const dr = Math.abs(line[2] - line[0]), dc = Math.abs(line[3] - line[1]);
    return (dr || dc) && (dr === 0 || dc === 0 || dr === dc);
  }
  function sameLine(a, b) { return a.every((v, i) => v === b[i]) || a.every((v, i) => v === b[(i + 2) % 4]); }
  function markLine(state, line) {
    if (state.stage < 1 || !validLine(line)) return false;
    const old = state.lines.findIndex(existing => sameLine(existing, line));
    if (old >= 0) state.lines.splice(old, 1);
    else if (state.lines.length < 120) state.lines.push([...line]);
    return true;
  }
  // Cube geometry, in LDraw axes (y points down; the front is -z). A piece lies with its tiles on local -y.
  // cubeTurn(face, turn, flip) is the 3 × 3 rotation (rows) taking the piece's frame to its place: flip turns it over
  // (about local x) so the tiles face in, then a base turn puts the tiles on the face, then `turn` quarter turns about it.
  const faceNormal = [[0, 0, -1], [1, 0, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 1, 0]];
  const faceBase = [[[1, 0, 0], [0, 0, -1], [0, 1, 0]], [[0, -1, 0], [1, 0, 0], [0, 0, 1]], [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, -1, 0], [0, 0, -1]]];
  const mul = (a, b) => a.map(row => [0, 1, 2].map(j => row[0] * b[0][j] + row[1] * b[1][j] + row[2] * b[2][j]));
  function cubeTurn(face, turn, flip) {
    const n = faceNormal[face], quarter = [0, 1, 2].map(i => [0, 1, 2].map(j => n[i] * n[j] + [[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]][i][j]));
    let r = mul(faceBase[face], flip ? [[1, 0, 0], [0, -1, 0], [0, 0, -1]] : [[1, 0, 0], [0, 1, 0], [0, 0, 1]]);
    for (let t = 0; t < turn; t++) r = mul(quarter, r);
    return r;
  }
  // The cube cells ('x,y,z', each 0–3) a piece covers at [face, turn, flip].
  function pieceCells(id, face, turn, flip) {
    const r = cubeTurn(face, turn, flip), n = faceNormal[face], axis = n.findIndex(v => v !== 0), out = [];
    cubePieces[id].forEach((row, i) => [...row].forEach((cell, j) => {
      if (cell !== '#') return;
      const local = [2 * j - 3, 0, 2 * i - 3], v = r.map(rr => (rr[0] * local[0] + rr[1] * local[1] + rr[2] * local[2] + 3) / 2);
      v[axis] = n[axis] > 0 ? 3 : 0; out.push(v.join(','));
    }));
    return out;
  }
  // Put a piece on a face (a piece already there goes back to the table), or take it off with face = null.
  function placeCube(state, id, face, turn = 0, flip = 0) {
    if (!cubePieces[id]) return false;
    if (face === null) { delete state.cube[id]; return true; }
    if (!integer(face, 0, 5) || !integer(turn, 0, 3) || !integer(flip, 0, 1)) return false;
    for (const [other, [f]] of Object.entries(state.cube)) if (other !== id && f === face) delete state.cube[other];
    state.cube[id] = [face, turn, flip]; return true;
  }
  // Which placed pieces overlap another, and whether the cube is whole: all six on, no overlaps, tiles out.
  function cubeStatus(state) {
    const owners = new Map();
    for (const [id, p] of Object.entries(state.cube)) for (const c of pieceCells(id, ...p)) owners.set(c, [...(owners.get(c) || []), id]);
    const clashes = [...new Set([...owners.values()].filter(o => o.length > 1).flat())];
    const placed = Object.keys(state.cube).length, inside = Object.entries(state.cube).filter(([, p]) => p[2]).map(([id]) => id);
    return { placed, clashes, inside, solved: placed === 6 && !clashes.length && !inside.length };
  }
  function unlock(state, answer) {
    if (state.stage >= locks.length || String(answer).trim().toUpperCase() !== locks[state.stage].answer) return false;
    state.stage++; state.table = null;
    if (state.stage === 1) state.pieces.bottle = { ...(state.pieces.bottle || {}), x: 60, y: 122, rot: 0 };
    let roomy = true;
    for (const id of locks[state.stage - 1].releases) if (visible(id, state.found)) roomy = place(state, id) && roomy;
    state.tidied = !roomy;
    return true;
  }
  // Opening the thank-you card for the first time frees the clipping inside it.
  function discover(state, id) {
    if (!items[id]?.hiddenIn || state.found.includes(id) || !available(state.stage, [...state.found, id]).includes(id)) return false;
    state.found.push(id); state.table = null; place(state, id); return true;
  }

  const isPerm = (list, n) => Array.isArray(list) && list.length === n && [...list].sort((a, b) => a - b).every((v, i) => v === i);
  function restore(raw) {
    if (!raw || raw.game !== 'hiking-opening' || raw.version !== 1) throw new Error('This is not a Hiking save.');
    const state = fresh();
    state.stage = integer(raw.stage, 0, locks.length) ? raw.stage : 0;
    // Saves from before the clipping was hidden in the card already had it on the table.
    state.found = Array.isArray(raw.found) ? raw.found.filter(id => items[id]?.hiddenIn) : (raw.pieces?.newspaper ? ['newspaper'] : []);
    const tight = raw.table && integer(raw.table.w, 300, 4000) && integer(raw.table.h, 200, 2500) ? { w: raw.table.w, h: raw.table.h } : null;
    state.table = tight; const table = tableSize(state.stage, state);
    state.notes = typeof raw.notes === 'string' ? raw.notes.slice(0, 6000) : '';
    state.hints = state.hints.map((_, i) => integer(raw.hints?.[i], 0, 4) ? raw.hints[i] : 0);
    state.ratings = state.ratings.map((_, i) => integer(raw.ratings?.[i], 0, 5) ? raw.ratings[i] : 0);
    for (const id of available(state.stage, state.found)) {
      const p = raw.pieces?.[id], item = items[id];
      if (!p || typeof p !== 'object') continue;
      state.pieces[id] = {
        x: Number.isFinite(p.x) ? Math.max(0, Math.min(table.w - item.w, p.x)) : (item.x ?? 30),
        y: Number.isFinite(p.y) ? Math.max(0, Math.min(table.h - item.h, p.y)) : (item.y ?? 30),
        rot: [0, 90, 180, 270].includes(p.rot) ? p.rot : 0,
        face: integer(p.face, 0, item.faces - 1) ? p.face : 0, stowed: p.stowed === true
      };
    }
    if (state.stage > 0) {
      if (Array.isArray(raw.lines)) for (const line of raw.lines.slice(0, 120)) {
        if (validLine(line) && !state.lines.some(old => sameLine(old, line))) state.lines.push([...line]);
      }
      state.sudoku = givens.map((given, i) => given || (integer(raw.sudoku?.[i], 1, 4) ? raw.sudoku[i] : 0));
    }
    if (state.stage >= 3 && typeof raw.calculator?.expression === 'string') {
      state.calculator.expression = raw.calculator.expression.slice(0, 160).replace(/[^\d+\-*/×÷−().,\s]/g, '');
      if (raw.calculator.result !== '' && raw.calculator.result !== undefined) {
        try { state.calculator.result = String(calculate(state.calculator.expression)); } catch (_) { /* Keep the unsolved expression; do not trust a supplied result. */ }
      }
    }
    const sat = raw.satellite;
    if (state.stage >= 4 && sat && typeof sat === 'object') state.satellite = {
      built: integer(sat.built, 0, satellitePages) ? sat.built : 0, on: sat.on === true,
      x: Number.isFinite(sat.x) ? Math.max(-600, Math.min(600, Math.round(sat.x))) : 40, y: Number.isFinite(sat.y) ? Math.max(-600, Math.min(600, Math.round(sat.y))) : 60,
      rot: integer(sat.rot, 0, 355) && sat.rot % 5 === 0 ? sat.rot : 35
    };
    if (state.stage >= 5 && isPerm(raw.otter, 12)) state.otter = [...raw.otter];
    if (state.stage >= 8 && isPerm(raw.map, 9)) state.map = [...raw.map];
    if (state.stage >= 8 && Array.isArray(raw.mapLines)) state.mapLines = raw.mapLines.slice(0, 200).filter(l => Array.isArray(l) && l.length === 4 && l.every(n => integer(n, 0, 1000))).map(l => [...l]);
    // Lego puzzles: the flat one arrives at lock 2, the square at lock 6. Saves from the 2D versions start them afresh.
    for (const [which, min] of [['flat', 2], ['square', 6]]) {
      const list = raw.push?.[which]?.actions;
      if (state.stage >= min && Array.isArray(list)) state.push[which] = { actions: list.slice(0, 200).filter(a => typeof a === 'string' && legoAction.test(a)) };
    }
    // Saves from the four-piece 2D cube use other piece names, so they start afresh.
    if (state.stage >= 3 && raw.cube && typeof raw.cube === 'object') for (const id of Object.keys(cubePieces)) {
      const p = raw.cube[id];
      if (Array.isArray(p) && p.length === 3 && !Object.values(state.cube).some(([f]) => f === p[0])) placeCube(state, id, ...p);
    }
    const have = available(state.stage, state.found);
    if (Array.isArray(raw.figures)) state.figures = state.figures.map((_, i) => {
      const fig = {}, src = raw.figures[i] || {};
      for (const bag of partOrder) if (have.includes(bag) && parts[bag].options.some(([v]) => v === src[bag])) fig[bag] = src[bag];
      return fig;
    });
    return state;
  }
  const api = { grid, givens, items, stickers, locks, values, hockey, parts, partOrder, riddle, cubePieces, cubeFaces, cubeSolved, cubeMarks, cubePen, boards, satellitePages,
    available, tableSize, fresh, restore, validLine, sameLine, markLine, unlock, discover, place, layout, box, overlaps, cubeTurn, pieceCells, placeCube, cubeStatus, normalizeAnswer, wheelLetters, calculate };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.HikingGame = api;
})(typeof window !== 'undefined' ? window : globalThis);
