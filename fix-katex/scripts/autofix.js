import fs from 'fs';
import path from 'path';

function processFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // Fix globally: `<InlineMath math="...\\text..." />` to `<InlineMath math={String.raw`...`} />`
  content = content.replace(/math="([^"]*\\\\[^"]*)"/g, (match, p1) => {
    let unescaped = p1.replace(/\\\\/g, '\\');
    return `math={String.raw\`${unescaped}\`}`;
  });

  // Fix globally: `math: '...'` to `math: String.raw`...``
  content = content.replace(/math:\s*'([^']*\\\\[^']*)'/g, (match, p1) => {
    let unescaped = p1.replace(/\\\\/g, '\\');
    return `math: String.raw\`${unescaped}\``;
  });

  // Fix globally: `latex: '...'` to `latex: String.raw`...``
  content = content.replace(/latex:\s*'([^']*\\\\[^']*)'/g, (match, p1) => {
    let unescaped = p1.replace(/\\\\/g, '\\');
    return `latex: String.raw\`${unescaped}\``;
  });

  // Fix globally: `formulas: ['...', '...']` to `formulas: [String.raw`...`, ...]`
  content = content.replace(/formulas:\s*\[([^\]]+)\]/g, (match, p1) => {
    let newInner = p1.replace(/'([^']*)'/g, (m, str) => {
      if (str.includes('\\\\')) {
        return `String.raw\`${str.replace(/\\\\/g, '\\')}\``;
      }
      return m;
    });
    return `formulas: [${newInner}]`;
  });

  // Specifically fix any lingering \\text{ directly inside strings if they're assigned to inline expressions
  // e.g. `const myMath = "\\text{hello}"` -> `const myMath = String.raw`\text{hello}`` (Best effort)
  content = content.replace(/=\s*"([^"]*\\\\text[^"]*)"/g, (match, p1) => {
    let unescaped = p1.replace(/\\\\/g, '\\');
    return `= String.raw\`${unescaped}\``;
  });

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`[fix-katex] Fixed KaTeX formatting in: ${filePath}`);
  }
}

function walkDir(dir) {
  if (!fs.existsSync(dir)) {
    console.error(`[fix-katex] Error: Directory or file not found at ${dir}`);
    return;
  }
  
  const stat = fs.statSync(dir);
  if (stat.isFile()) {
    if (dir.endsWith('.tsx') || dir.endsWith('.ts') || dir.endsWith('.jsx') || dir.endsWith('.js')) {
      processFile(dir);
    }
    return;
  }

  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      walkDir(fullPath);
    } else if (fullPath.endsWith('.tsx') || fullPath.endsWith('.ts') || fullPath.endsWith('.jsx') || fullPath.endsWith('.js')) {
      processFile(fullPath);
    }
  }
}

// Get target path from args, or default to 'web/src/components' relative to project root
const args = process.argv.slice(2);
let targetPath = args.length > 0 ? args[0] : 'web/src/components';

console.log(`[fix-katex] Scanning for KaTeX formatting anti-patterns in: ${targetPath}...`);
walkDir(path.resolve(process.cwd(), targetPath));
console.log(`[fix-katex] Done.`);
