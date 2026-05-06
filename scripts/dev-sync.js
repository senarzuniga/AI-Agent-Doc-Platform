#!/usr/bin/env node
/* eslint-disable no-console */
const chokidar = require('chokidar');
const { execSync } = require('child_process');
const fs = require('fs');

console.log('[INFO] Watching for API key changes in source repositories...');

const sourceRepos = [
  'C:/Users/Inaki Senar/Documents/GitHub/adaptive-sales-engine/.env',
  'C:/Users/Inaki Senar/Documents/GitHub/AI-FACTORY-v2/.env',
];

try {
  execSync('npm run init:keys', { stdio: 'inherit' });
  execSync('npm run sync:keys', { stdio: 'inherit' });
} catch (err) {
  console.warn('[WARN] Initial sync failed:', err.message);
}

for (const repoPath of sourceRepos) {
  if (!fs.existsSync(repoPath)) {
    console.warn(`[WARN] Source env not found: ${repoPath}`);
    continue;
  }

  chokidar.watch(repoPath, { ignoreInitial: true }).on('change', () => {
    console.log(`[INFO] Detected change in ${repoPath}`);
    try {
      execSync('npm run sync:keys', { stdio: 'inherit' });
    } catch (err) {
      console.warn('[WARN] Sync failed:', err.message);
    }
  });
}

console.log('[OK] Watching for changes. Press Ctrl+C to stop.');
