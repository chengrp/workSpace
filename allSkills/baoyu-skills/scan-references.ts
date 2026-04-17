#!/usr/bin/env bun
import { globSync } from 'glob';
import { readFileSync } from 'fs';
import { resolve, dirname, relative } from 'path';

const TARGET_DIR = 'skills/baoyu-article-illustrator';

const REFERENCE_PATTERNS = [
  /\[([^\]]+)\]\(([^)]+\.md)\)/g,
  /^\s*\[([^\]]+)\]:\s*(.+\.md)$/gm,
  /!\[([^\]]*)\]\(([^)]+\.md)\)/g,
  /<(?:a|link|img)\s+(?:href|src)\s*=\s*["']([^"']+\.md)["']/gi,
  /(?:src|href|path|file)=["']([^"']+\.md)["']/gi,
  /(?:from|import|include|require)\s*["']([^"']+\.md)["']/gi,
];

function cleanPath(raw: string): string | null {
  if (!raw) return null;
  
  let cleaned = raw.split('#')[0];
  cleaned = cleaned.split('?')[0];
  cleaned = cleaned.replace(/\/g, '/').replace(/^\.?\//, '').replace(/^\.\.\//, '');
  
  if (!cleaned.endsWith('.md')) return null;
  return cleaned;
}

function scanFile(filePath: string, allFiles: Set<string>): string[] {
  const content = readFileSync(filePath, 'utf-8');
  const refs = new Set<string>();
  
  for (const pattern of REFERENCE_PATTERNS) {
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      const rawPath = match[2] || match[1];
      const cleaned = cleanPath(rawPath);
      if (cleaned) {
        let resolved = cleaned;
        for (const targetFile of allFiles) {
          const targetName = targetFile.split('/').pop()!;
          if (cleaned === targetName || targetFile.endsWith(cleaned)) {
            resolved = targetFile;
            break;
          }
        }
        refs.add(resolved);
      }
    }
  }
  
  return Array.from(refs);
}

async function main() {
  const files = globSync('**/*.md', { cwd: TARGET_DIR });
  const fileSet = new Set(files);
  
  console.error(`Scanning ${files.length} files...`);
  
  const nodes = files.map((f, i) => ({
    id: `f_${i}`,
    label: f.split('/').pop()!,
    type: 'file',
    path: `${TARGET_DIR}/${f}`,
  }));
  
  const edges: Array<{from: string; to: string; label: string; type: string}> = [];
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const refs = scanFile(`${TARGET_DIR}/${file}`, fileSet);
    
    for (const ref of refs) {
      const targetIdx = files.findIndex(f => f === ref || f.endsWith(ref) || ref.endsWith(f));
      if (targetIdx >= 0 && targetIdx !== i) {
        edges.push({ from: `f_${i}`, to: `f_${targetIdx}`, label: 'references', type: 'EXTRACTED' });
      }
    }
  }
  
  const graph = { nodes, edges, stats: { nodes: nodes.length, edges: edges.length } };
  console.log(JSON.stringify(graph, null, 2));
}

main().catch(console.error);
