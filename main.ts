import { copyFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const SOURCE = 'entry.png';
const DEST = join(OUT_DIR, 'entry.png');

function run() {
    if (!existsSync(OUT_DIR)) {
        mkdirSync(OUT_DIR, { recursive: true });
    }
    
    copyFileSync(SOURCE, DEST);
    process.stdout.write(`Copied ${SOURCE} to ${DEST}\n`);
}

run();
