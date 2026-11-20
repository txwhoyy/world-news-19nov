// The World Today — news-image-20261119
// Entrypoint: validates the committed entry.png (1024x1024 PNG, at most
// 1 MiB) and copies it to the output directory. Node 22, stdlib only.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;
const MAX_DIMENSION = 1024;
const ENTRY = new URL("./entry.png", import.meta.url);

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

/** Read the PNG IHDR chunk and return [width, height]. */
function pngDimensions(buf: Buffer): [number, number] {
  if (buf.length < 33) fail("entry.png is too small to be a PNG");
  if (!buf.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail("entry.png does not start with the PNG signature");
  }
  const ihdrLength = buf.readUInt32BE(8);
  const ihdrType = buf.toString("ascii", 12, 16);
  if (ihdrType !== "IHDR" || ihdrLength !== 13) {
    fail("entry.png has no valid IHDR chunk");
  }
  return [buf.readUInt32BE(16), buf.readUInt32BE(20)];
}

function main(): void {
  let buf: Buffer;
  try {
    buf = readFileSync(ENTRY);
  } catch {
    fail("entry.png is missing next to main.ts");
  }

  const size = statSync(ENTRY).size;
  if (size > MAX_BYTES) {
    fail(`entry.png is ${size} bytes, over the 1 MiB limit`);
  }

  const [width, height] = pngDimensions(buf);
  if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
    fail(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
  }
  if (width !== 1024 || height !== 1024) {
    fail(`entry.png is ${width}x${height}, expected exactly 1024x1024`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, "entry.png");
  copyFileSync(ENTRY, outPath);
  console.log(`wrote ${outPath} (${width}x${height}, ${size} bytes)`);
}

main();
