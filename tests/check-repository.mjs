// Dependency-free link and publication checks. Complements manual review; not a secret scanner.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(process.argv[2] ?? path.join(path.dirname(fileURLToPath(import.meta.url)), '..'));
const errors = [];
const files = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git') continue;
    const file = path.join(dir, entry.name);
    if (entry.isSymbolicLink()) errors.push(`${path.relative(root, file)}: unexpected symlink`);
    else if (entry.isDirectory()) walk(file);
    else files.push(file);
  }
}
walk(root);
const relative = file => path.relative(root, file);
const allowed = new Set(['.md', '.jq', '.sh', '.mjs', '.yaml', '.yml']);
const privacyPatterns = [
  [/\/(?:home|Users)\/[^\s/"'`]+\//, 'personal absolute path'],
  [/[A-Za-z]:\\(?:Users|Documents and Settings)\\/i, 'personal Windows path'],
  [/\bgh[pousr]_[A-Za-z0-9]{20,}\b/, 'GitHub credential pattern'],
  [/\bgithub_pat_[A-Za-z0-9_]{20,}\b/, 'GitHub credential pattern'],
  [/\bAKIA[A-Z0-9]{16}\b/, 'access key pattern'],
  [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, 'private key'],
  [/https?:\/\/[^\s/]+:[^\s/@]+@/, 'URL credentials'],
];
let links = 0;
let skills = 0;
function headings(text) {
  const ids = new Set();
  const counts = new Map();
  let inCode = false;
  for (const line of text.split('\n')) {
    if (/^\s*```/.test(line)) { inCode = !inCode; continue; }
    if (inCode || !/^#{1,6} /.test(line)) continue;
    const base = line.replace(/^#+\s+/, '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .toLowerCase().replace(/[^\p{L}\p{N}_\-\s]/gu, '').replace(/\s/g, '-');
    const n = counts.get(base) ?? 0;
    counts.set(base, n + 1);
    ids.add(n ? `${base}-${n}` : base);
  }
  return ids;
}
for (const file of files) {
  const name = relative(file);
  if (!allowed.has(path.extname(file)) && !['LICENSE', '.gitignore'].includes(path.basename(file)))
    errors.push(`${name}: unexpected publication file type`);
  const bytes = fs.readFileSync(file);
  if (bytes.includes(0) || bytes.length > 256 * 1024) errors.push(`${name}: binary or oversized file`);
  const text = bytes.toString('utf8');
  for (const [pattern, label] of privacyPatterns) if (pattern.test(text)) errors.push(`${name}: ${label}`);
  if (path.basename(file) === 'SKILL.md') {
    skills++;
    const front = text.match(/^---\n([\s\S]*?)\n---\n/);
    const skillName = front?.[1].match(/^name: ([a-z0-9-]+)$/m)?.[1];
    if (skillName !== path.basename(path.dirname(file)) || !/^description: .+/m.test(front?.[1] ?? ''))
      errors.push(`${name}: missing or inconsistent skill metadata`);
  }
  if (!file.endsWith('.md')) continue;
  for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
    const link = match[1];
    if (/^https:\/\//.test(link)) continue;
    if (/^(?:[a-z]+:|\/)/i.test(link)) { errors.push(`${name}: nonportable link ${link}`); continue; }
    const [dest, hash] = link.split('#');
    const target = dest ? path.resolve(path.dirname(file), decodeURIComponent(dest)) : file;
    if (path.relative(root, target).startsWith('..') || !fs.existsSync(target)) {
      errors.push(`${name}: missing/outside link ${link}`); continue;
    }
    if (hash && (!target.endsWith('.md') || !headings(fs.readFileSync(target, 'utf8')).has(decodeURIComponent(hash))))
      errors.push(`${name}: missing heading ${link}`);
    links++;
  }
}
if (skills !== 2) errors.push(`Expected two skill entry points, found ${skills}`);
if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`PASS: ${files.length} text files, ${skills} skills, ${links} local links/anchors; publication-pattern checks clean`);
}
