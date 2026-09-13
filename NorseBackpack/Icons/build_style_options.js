const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const OUT = path.join(ROOT, 'Options');
const INK = '#283B34';
const ACCENT = '#B56A2A';

const subjects = {
  longship: {
    label: 'Longship',
    title: 'Norse longship',
    body: `<path class="ink" d="M7 40h50c-4 9-13 13-25 13S11 49 7 40Z"/><path class="line" d="M9 40c-3-4-2-8 2-11-1 5 1 8 6 11m40 0c4-2 6-7 5-11 4 3 4 8 0 12M31 12v28"/><path class="accent" d="M31 15h19v21H31Z"/><path class="line" d="M31 15H15l6 10-6 11h16M11 57c7-3 14-3 21 0s14 3 21 0"/><g class="detail"><circle cx="20" cy="43" r="2.7"/><circle cx="28" cy="43" r="2.7"/><circle cx="36" cy="43" r="2.7"/><circle cx="44" cy="43" r="2.7"/></g>`
  },
  settlement: {
    label: 'Settlement',
    title: 'Norse settlement',
    body: `<path class="line" d="M7 52V35l10-10 10 10v17M22 52V29l12-13 13 13v23M42 52V37l8-9 8 9v15M5 53h55"/><path class="accent" d="m5 35 12-13 12 13H5Zm15-6 14-16 16 16H20Zm20 8 10-12 11 12H40Z"/><path class="detail" d="M13 52V40h8v12m8 0V35h10v17m8 0V42h6v10"/>`
  },
  longhouse: {
    label: 'Longhouse',
    title: 'Norse longhouse',
    body: `<path class="line" d="M10 33v19h43V33M20 35v17m27-17v17M28 52V39h10v13M7 53h49"/><path class="accent" d="M7 32 22 17h27l8 15-9 4H21Z"/><path class="detail" d="M15 40v7m29-7v7M13 27c11-5 25-7 39-5"/>`
  },
  runestone: {
    label: 'Runestone',
    title: 'Runestone',
    body: `<path class="ink" d="m18 54-2-30 8-13 18 2 7 12-3 29Z"/><path class="accentline" d="M25 45V22m0 11 13-10M25 34l13 10M21 49h24"/><path class="line" d="M13 55h38"/>`
  },
  burial_mound: {
    label: 'Burial mound',
    title: 'Burial mound',
    body: `<path class="ink" d="M6 50c5-13 14-20 26-20s21 7 26 20Z"/><path class="line" d="M4 51h56"/><path class="accentline" d="m16 45 4-6m5 6 3-8m19 8-4-7m10 7-3-5"/><path class="accent" d="M28 30V20l4-5 4 5v10Z"/>`
  },
  round_shield: {
    label: 'Round shield',
    title: 'Round shield',
    body: `<circle class="accent" cx="32" cy="32" r="23"/><path class="ink" d="M32 9a23 23 0 0 1 23 23H32Zm0 46A23 23 0 0 1 9 32h23Z"/><path class="line" d="M32 9v46M9 32h46"/><circle class="boss" cx="32" cy="32" r="7"/>`
  },
  dane_axe: {
    label: 'Dane axe',
    title: 'Dane axe',
    body: `<path class="haft" d="m17 56 25-43"/><path class="ink" d="M39 11c8-1 15 1 21 6-7 3-10 9-11 17-5-7-10-10-17-11Z"/><path class="accentline" d="M41 15c5 0 10 1 14 3-4 3-6 7-7 11"/><path class="accentline" d="m14 57 6-2"/>`
  },
  raven: {
    label: 'Raven',
    title: 'Raven',
    body: `<path class="ink" d="M9 47c9-2 14-9 15-19 1-10 8-16 18-15 7 0 12 4 14 10l8 4-11 4c0 7-3 12-9 16l10 8-17-5c-9 3-19 2-28-3Z"/><path class="beak" d="m53 22 11 5-12 4 4-4Z"/><path class="accentline" d="M19 43c9-1 17 1 25 7m-18-16c8 1 14 5 18 11"/><circle class="eye" cx="47" cy="20" r="1.7"/><path class="line" d="M29 50v6m8-7v7m-11 1h7m1 0h7"/>`
  }
};

const styles = [
  {
    id: '01_clean_map', label: 'Clean map',
    css: `.ink,.beak{fill:${INK};stroke:${INK};stroke-width:2.4}.accent{fill:${ACCENT};stroke:${INK};stroke-width:2.5}.line,.detail,.accentline,.haft{fill:none;stroke:${INK};stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}.accentline{stroke:${ACCENT}}.haft{stroke-width:4.2}.detail{fill:${ACCENT};stroke-width:1.5}.boss{fill:#F0E6CF;stroke:${INK};stroke-width:3}.eye{fill:${ACCENT}}`
  },
  {
    id: '02_carved_woodcut', label: 'Carved woodcut',
    css: `.ink,.beak{fill:${INK};stroke:${INK};stroke-width:3.2}.accent{fill:${ACCENT};stroke:${INK};stroke-width:3}.line,.detail,.accentline,.haft{fill:none;stroke:${INK};stroke-width:3.2;stroke-linecap:square;stroke-linejoin:miter}.accentline{stroke:${ACCENT};stroke-dasharray:7 2}.haft{stroke-width:5}.detail{fill:${ACCENT};stroke-width:2}.boss{fill:${ACCENT};stroke:${INK};stroke-width:4}.eye{fill:${ACCENT}}`
  },
  {
    id: '03_historic_manuscript', label: 'Historic manuscript',
    ornament: `<path d="M8 9c5-5 10-5 14 0s9 5 14 0" fill="none" stroke="${ACCENT}" stroke-width="1.3" opacity=".8"/>`,
    css: `.ink,.beak{fill:none;stroke:${INK};stroke-width:2}.accent{fill:none;stroke:${ACCENT};stroke-width:2}.line,.detail,.accentline,.haft{fill:none;stroke:${INK};stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.accentline{stroke:${ACCENT}}.haft{stroke-width:3}.detail{stroke:${ACCENT};stroke-width:1.5}.boss{fill:none;stroke:${ACCENT};stroke-width:2}.eye{fill:${ACCENT}}`
  },
  {
    id: '04_antique_cartography', label: 'Antique cartography',
    defs: `<pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="5" stroke="${INK}" stroke-width="1"/></pattern>`,
    css: `.ink{fill:url(#hatch);stroke:${INK};stroke-width:1.7}.beak{fill:none;stroke:${INK};stroke-width:1.7}.accent{fill:none;stroke:${ACCENT};stroke-width:1.7}.line,.detail,.accentline,.haft{fill:none;stroke:${INK};stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}.accentline{stroke:${ACCENT};stroke-width:1.4}.haft{stroke-width:2.7}.detail{stroke-width:1.2}.boss{fill:url(#hatch);stroke:${INK};stroke-width:1.8}.eye{fill:${INK}}`
  },
  {
    id: '05_hand_drawn', label: 'Hand drawn',
    defs: `<filter id="wobble" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency="0.025" numOctaves="2" seed="8" result="noise"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="1.3"/></filter>`,
    group: 'filter="url(#wobble)"', double: true,
    css: `.ink,.beak{fill:none;stroke:${INK};stroke-width:2.5}.accent{fill:none;stroke:${ACCENT};stroke-width:2.4}.line,.detail,.accentline,.haft{fill:none;stroke:${INK};stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}.accentline{stroke:${ACCENT}}.haft{stroke-width:3.5}.detail{stroke:${ACCENT};stroke-width:1.6}.boss{fill:none;stroke:${INK};stroke-width:2.6}.eye{fill:${ACCENT}}`
  }
];

function svgFor(subject, style) {
  const art = style.double
    ? `<g opacity=".24" transform="translate(.8 .5)">${subject.body}</g><g ${style.group || ''}>${subject.body}</g>`
    : `<g ${style.group || ''}>${subject.body}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title desc"><title id="title">${subject.title} — ${style.label}</title><desc id="desc">${style.label} version of ${subject.title.toLowerCase()}.</desc><defs>${style.defs || ''}<style>${style.css}</style></defs>${style.ornament || ''}${art}</svg>\n`;
}

fs.mkdirSync(OUT, { recursive: true });
for (const style of styles) {
  const dir = path.join(OUT, style.id);
  fs.mkdirSync(dir, { recursive: true });
  for (const [name, subject] of Object.entries(subjects)) {
    fs.writeFileSync(path.join(dir, `${name}.svg`), svgFor(subject, style));
  }
}

const previewWidth = 1180;
const previewHeight = 720;
const startX = 176;
const cardW = 116;
const gap = 8;
const rowH = 116;
let preview = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${previewWidth} ${previewHeight}" role="img" aria-labelledby="title desc"><title id="title">Five Norse icon style options</title><desc id="desc">Five complete style options for eight Norse map and text icons.</desc><rect width="100%" height="100%" rx="18" fill="#F3EFE5"/><text x="34" y="45" fill="#25372F" font-family="Georgia,serif" font-size="27">Norse icon style options</text><text x="35" y="69" fill="#657065" font-family="Arial,sans-serif" font-size="12">Five complete sets · 40 transparent SVG files · identical subjects and scale</text>`;

Object.values(subjects).forEach((subject, i) => {
  preview += `<text x="${startX + i * (cardW + gap) + cardW / 2}" y="100" text-anchor="middle" fill="#59635D" font-family="Arial,sans-serif" font-size="11">${subject.label}</text>`;
});

styles.forEach((style, row) => {
  const y = 116 + row * rowH;
  preview += `<text x="34" y="${y + 49}" fill="#25372F" font-family="Arial,sans-serif" font-size="13" font-weight="700">${style.label}</text><text x="34" y="${y + 68}" fill="#8A7D63" font-family="Arial,sans-serif" font-size="10">Option ${row + 1}</text>`;
  Object.entries(subjects).forEach(([name], col) => {
    const x = startX + col * (cardW + gap);
    preview += `<rect x="${x}" y="${y}" width="${cardW}" height="100" rx="8" fill="#FFFDF7" stroke="#D7D1BF"/><image x="${x + 26}" y="${y + 10}" width="64" height="64" xlink:href="Options/${style.id}/${name}.svg"/><image x="${x + 88}" y="${y + 70}" width="20" height="20" xlink:href="Options/${style.id}/${name}.svg"/>`;
  });
});

preview += `<g transform="translate(35 688)" font-family="Arial,sans-serif" font-size="11" fill="#657065"><circle cx="5" cy="-4" r="5" fill="${INK}"/><text x="18" y="0">forest green #283B34</text><circle cx="170" cy="-4" r="5" fill="${ACCENT}"/><text x="183" y="0">muted rust #B56A2A</text><text x="955" y="0">Large: map · small: text</text></g></svg>\n`;
fs.writeFileSync(path.join(ROOT, 'Norse_Icon_Style_Options.svg'), preview);

console.log(`Built ${styles.length * Object.keys(subjects).length} icons and comparison sheet.`);

const subjects2 = {
  bone_comb: {
    label: 'Bone comb',
    title: 'Bone or antler comb',
    body: `<path class="accent" d="M10 20h44v13H10Z"/><path class="detail" d="M14 25h36M17 20v13m8-13v13m14-13v13m8-13v13"/><path class="line" d="M12 33v20m5-20v20m5-20v20m5-20v20m5-20v20m5-20v20m5-20v20m5-20v20m5-20v20"/>`
  },
  hnefatafl_piece: {
    label: 'Game piece',
    title: 'Hnefatafl game piece',
    body: `<path class="ink" d="M25 13h14l3 9-5 8 10 19H17l10-19-5-8Z"/><path class="accent" d="M23 19h18l-2 7H25Z"/><path class="accentline" d="M22 43h20M27 35h10"/><path class="line" d="M14 51h36"/>`
  },
  silver_coin: {
    label: 'Silver coin',
    title: 'Hammered silver coin',
    body: `<circle class="ink" cx="32" cy="32" r="23"/><circle class="accent" cx="32" cy="32" r="17"/><path class="accentline" d="M32 20v24M20 32h24"/><g class="detail"><circle cx="32" cy="13" r="1.5"/><circle cx="51" cy="32" r="1.5"/><circle cx="32" cy="51" r="1.5"/><circle cx="13" cy="32" r="1.5"/></g>`
  },
  rune_stick: {
    label: 'Rune stick',
    title: 'Carved rune stick',
    body: `<path class="accent" d="m12 43 5-24 35 3-4 24Z"/><path class="line" d="m19 22 30 3M16 41l30 3"/><path class="detail" d="m21 26 5 4m-6 2 5 4m8-9 5 4m-6 2 5 4m8-9 3 3m-4 3 3 3"/>`
  },
  drinking_horn: {
    label: 'Drinking horn',
    title: 'Norse drinking horn',
    body: `<path class="ink" d="M14 16c12 5 24 8 37 8-5 16-15 27-31 31 7-8 8-18 2-28Z"/><path class="accent" d="M12 14c13 5 27 8 41 8l-2 7c-14-1-27-4-40-9Z"/><path class="accentline" d="M22 48c8-3 14-9 18-17"/><path class="line" d="M18 55h10"/>`
  },
  palisade_fort: {
    label: 'Palisade fort',
    title: 'Timber palisade fort',
    body: `<path class="line" d="M8 53V28l5-6 5 6 5-6 5 6 5-6 5 6 5-6 5 6 5-6 4 6v25M6 54h52"/><path class="ink" d="M24 53V38l8-7 8 7v15Z"/><path class="accent" d="m21 38 11-10 11 10Z"/><path class="detail" d="M29 53V42h6v11M13 30v18m10-18v18m20-18v18m10-18v18"/>`
  },
  trading_port: {
    label: 'Trading port',
    title: 'Norse trading port',
    body: `<path class="line" d="M7 48h50M11 55c7-3 14-3 21 0s14 3 21 0M12 48V27h16v21m7 0V21h17v27M37 21l7-8 8 8"/><path class="accent" d="M10 27h20L20 17Z"/><path class="ink" d="M17 39h15c-2 5-5 7-8 7s-6-2-7-7Z"/><path class="accentline" d="M24 30v9m0-8 7 6h-7"/>`
  },
  wooden_church: {
    label: 'Wooden church',
    title: 'Early wooden church',
    body: `<path class="line" d="M15 53V29h34v24M25 53V39h14v14M8 54h48"/><path class="accent" d="M11 29 25 16h20l8 13Z"/><path class="ink" d="M27 16V9h10v7Z"/><path class="accentline" d="M32 4v10M27 8h10"/><path class="detail" d="M20 35v8m24-8v8"/>`
  }
};

const OUT2 = path.join(ROOT, 'Options_02');
fs.mkdirSync(OUT2, { recursive: true });
for (const style of styles) {
  const dir = path.join(OUT2, style.id);
  fs.mkdirSync(dir, { recursive: true });
  for (const [name, subject] of Object.entries(subjects2)) {
    fs.writeFileSync(path.join(dir, `${name}.svg`), svgFor(subject, style));
  }
}

let preview2 = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${previewWidth} ${previewHeight}" role="img" aria-labelledby="title desc"><title id="title">Five Norse icon style options — second batch</title><desc id="desc">Five complete style options for eight additional Norse map, prop and text icons.</desc><rect width="100%" height="100%" rx="18" fill="#F3EFE5"/><text x="34" y="45" fill="#25372F" font-family="Georgia,serif" font-size="27">Norse icon style options · batch 2</text><text x="35" y="69" fill="#657065" font-family="Arial,sans-serif" font-size="12">Five complete sets · 40 transparent SVG files · puzzle props and map locations</text>`;

Object.values(subjects2).forEach((subject, i) => {
  preview2 += `<text x="${startX + i * (cardW + gap) + cardW / 2}" y="100" text-anchor="middle" fill="#59635D" font-family="Arial,sans-serif" font-size="11">${subject.label}</text>`;
});

styles.forEach((style, row) => {
  const y = 116 + row * rowH;
  preview2 += `<text x="34" y="${y + 49}" fill="#25372F" font-family="Arial,sans-serif" font-size="13" font-weight="700">${style.label}</text><text x="34" y="${y + 68}" fill="#8A7D63" font-family="Arial,sans-serif" font-size="10">Option ${row + 1}</text>`;
  Object.entries(subjects2).forEach(([name], col) => {
    const x = startX + col * (cardW + gap);
    preview2 += `<rect x="${x}" y="${y}" width="${cardW}" height="100" rx="8" fill="#FFFDF7" stroke="#D7D1BF"/><image x="${x + 26}" y="${y + 10}" width="64" height="64" xlink:href="Options_02/${style.id}/${name}.svg"/><image x="${x + 88}" y="${y + 70}" width="20" height="20" xlink:href="Options_02/${style.id}/${name}.svg"/>`;
  });
});

preview2 += `<g transform="translate(35 688)" font-family="Arial,sans-serif" font-size="11" fill="#657065"><circle cx="5" cy="-4" r="5" fill="${INK}"/><text x="18" y="0">forest green #283B34</text><circle cx="170" cy="-4" r="5" fill="${ACCENT}"/><text x="183" y="0">muted rust #B56A2A</text><text x="955" y="0">Large: map · small: text</text></g></svg>\n`;
fs.writeFileSync(path.join(ROOT, 'Norse_Icon_Style_Options_Batch_2.svg'), preview2);

console.log(`Built ${styles.length * Object.keys(subjects2).length} additional icons and second comparison sheet.`);
