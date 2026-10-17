// Check the same pinned renderer used by the browser, without a network request.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import katex from '../../learning/site/vendor/katex/katex.mjs';

const root = new URL('../../', import.meta.url);
const vendor = new URL('learning/site/vendor/katex/', root);
const provenance = JSON.parse(readFileSync(new URL('PROVENANCE.json', vendor), 'utf8'));
if (provenance.version !== katex.version) throw new Error('KaTeX version differs from its provenance.');
for (const [path, expected] of Object.entries(provenance.files)) {
  const actual = createHash('sha256').update(readFileSync(new URL(path, vendor))).digest('hex');
  if (actual !== expected) throw new Error(`Vendored asset changed: ${path}`);
}
const content = JSON.parse(readFileSync(new URL('learning/content.json', root), 'utf8'));
const app = readFileSync(new URL('learning/site/app.js', root), 'utf8');
let count = 0;
function check(text) {
  const delimiters = /\\([()[\]])/g;
  let opening = null, match;
  while ((match = delimiters.exec(text))) {
    if (match[1] === '(' || match[1] === '[') {
      if (opening) throw new Error(`Nested math delimiter: ${text}`);
      opening = {end:delimiters.lastIndex, close:match[1] === '(' ? ')' : ']'};
    } else {
      if (!opening || match[1] !== opening.close) throw new Error(`Unmatched math delimiter: ${text}`);
      katex.renderToString(text.slice(opening.end, match.index), {
        throwOnError:true, strict:'error', trust:false, output:'htmlAndMathml',
        displayMode:opening.close === ']'
      });
      count++;
      opening = null;
    }
  }
  if (opening) throw new Error(`Unclosed math delimiter: ${text}`);
}
function walk(value) {
  if (typeof value === 'string') check(value);
  else if (Array.isArray(value)) value.forEach(walk);
  else if (value && typeof value === 'object') Object.values(value).forEach(walk);
}
walk(content);
for (const match of app.matchAll(/return String\.raw`([^`]+)`/g)) check(match[1]);
if (!count) throw new Error('No typeset expressions found.');
if (/I can explain this in my own words|mark-complete|type=["']checkbox["']|<progress|localStorage/i.test(app)) {
  throw new Error('Self-assessment or progress controls must not return.');
}
console.log(`${count} mathematical expressions render with KaTeX ${katex.version}; no self-assessment controls.`);
