const sharp = require('sharp');
const path = require('path');

const input = process.argv[2] || path.join(__dirname, 'Raven_Profile_Icon_v2.png');
const output = process.argv[3] || path.join(__dirname, 'Raven_Profile_Icon_v3.png');

function isNeutralChecker(data, i) {
  const r = data[i];
  const g = data[i + 1];
  const b = data[i + 2];
  const low = Math.min(r, g, b);
  const high = Math.max(r, g, b);
  return (low >= 242 && high - low <= 12) ||
    (low >= 195 && high <= 240 && high - low <= 10);
}

(async () => {
  const { data, info } = await sharp(input).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const { width, height } = info;
  const count = width * height;
  const outside = new Uint8Array(count);
  const queue = new Int32Array(count);
  let head = 0;
  let tail = 0;

  function enqueue(pixel) {
    if (outside[pixel] || !isNeutralChecker(data, pixel * 3)) return;
    outside[pixel] = 1;
    queue[tail++] = pixel;
  }

  for (let x = 0; x < width; x++) {
    enqueue(x);
    enqueue((height - 1) * width + x);
  }
  for (let y = 0; y < height; y++) {
    enqueue(y * width);
    enqueue(y * width + width - 1);
  }

  while (head < tail) {
    const pixel = queue[head++];
    const x = pixel % width;
    const y = Math.floor(pixel / width);
    if (x > 0) enqueue(pixel - 1);
    if (x + 1 < width) enqueue(pixel + 1);
    if (y > 0) enqueue(pixel - width);
    if (y + 1 < height) enqueue(pixel + width);
  }

  const rgba = Buffer.alloc(count * 4);
  for (let pixel = 0; pixel < count; pixel++) {
    const source = pixel * 3;
    const target = pixel * 4;
    rgba[target] = data[source];
    rgba[target + 1] = data[source + 1];
    rgba[target + 2] = data[source + 2];
    rgba[target + 3] = outside[pixel] || isNeutralChecker(data, source) ? 0 : 255;
  }

  await sharp(rgba, { raw: { width, height, channels: 4 } }).png().toFile(output);
  console.log(`Removed ${tail} edge-connected checker pixels; wrote ${output}`);
})().catch(error => {
  console.error(error);
  process.exit(1);
});
