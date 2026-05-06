#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function parseArgs(argv) {
  const args = { source: null, output: null, password: process.env.KEYS_ENCRYPTION_PASSWORD || '' };
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--source') {
      args.source = argv[i + 1];
      i += 1;
    } else if (token === '--output') {
      args.output = argv[i + 1];
      i += 1;
    } else if (token === '--password') {
      args.password = argv[i + 1];
      i += 1;
    }
  }
  return args;
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function encryptBuffer(buffer, password) {
  const iv = crypto.randomBytes(12);
  const salt = crypto.randomBytes(16);
  const key = crypto.scryptSync(password, salt, 32);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(buffer), cipher.final()]);
  const tag = cipher.getAuthTag();
  return {
    algorithm: 'aes-256-gcm',
    iv: iv.toString('base64'),
    salt: salt.toString('base64'),
    tag: tag.toString('base64'),
    data: encrypted.toString('base64'),
  };
}

function run() {
  const args = parseArgs(process.argv);
  if (!args.source || !args.output) {
    console.error('Usage: node scripts/encrypt-keys.js --source <file> --output <file.enc> [--password <passphrase>]');
    process.exit(1);
  }
  if (!args.password) {
    console.error('[ERROR] Missing passphrase. Set KEYS_ENCRYPTION_PASSWORD or pass --password.');
    process.exit(1);
  }

  const sourcePath = path.resolve(args.source);
  const outputPath = path.resolve(args.output);
  if (!fs.existsSync(sourcePath)) {
    console.error(`[ERROR] Source file not found: ${sourcePath}`);
    process.exit(1);
  }

  const input = fs.readFileSync(sourcePath);
  const payload = encryptBuffer(input, args.password);

  ensureDir(path.dirname(outputPath));
  fs.writeFileSync(outputPath, JSON.stringify(payload, null, 2), 'utf8');
  console.log(`[OK] Encrypted ${sourcePath} -> ${outputPath}`);
}

if (require.main === module) {
  run();
}

module.exports = { parseArgs, encryptBuffer };
