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

function decryptPayload(payload, password) {
  const iv = Buffer.from(payload.iv, 'base64');
  const salt = Buffer.from(payload.salt, 'base64');
  const tag = Buffer.from(payload.tag, 'base64');
  const data = Buffer.from(payload.data, 'base64');
  const key = crypto.scryptSync(password, salt, 32);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);
  return Buffer.concat([decipher.update(data), decipher.final()]);
}

function run() {
  const args = parseArgs(process.argv);
  if (!args.source || !args.output) {
    console.error('Usage: node scripts/decrypt-keys.js --source <file.enc> --output <file> [--password <passphrase>]');
    process.exit(1);
  }
  if (!args.password) {
    console.error('[ERROR] Missing passphrase. Set KEYS_ENCRYPTION_PASSWORD or pass --password.');
    process.exit(1);
  }

  const sourcePath = path.resolve(args.source);
  const outputPath = path.resolve(args.output);
  if (!fs.existsSync(sourcePath)) {
    console.error(`[ERROR] Encrypted file not found: ${sourcePath}`);
    process.exit(1);
  }

  const payload = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
  const plaintext = decryptPayload(payload, args.password);
  fs.writeFileSync(outputPath, plaintext);
  console.log(`[OK] Decrypted ${sourcePath} -> ${outputPath}`);
}

if (require.main === module) {
  run();
}

module.exports = { parseArgs, decryptPayload };
