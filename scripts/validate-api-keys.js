#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require('fs');
const path = require('path');

function parseEnv(content) {
  const out = {};
  const lines = content.split(/\r?\n/);
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const idx = line.indexOf('=');
    if (idx <= 0) continue;
    const key = line.slice(0, idx).trim();
    const value = line.slice(idx + 1).trim();
    out[key] = value;
  }
  return out;
}

function maskKey(key) {
  if (!key) return '***';
  if (key.length <= 8) return `${key.slice(0, 2)}...${key.slice(-2)}`;
  return `${key.slice(0, 4)}...${key.slice(-4)}`;
}

async function testHttpAuth(url, headers) {
  try {
    const response = await fetch(url, { method: 'GET', headers });
    return response.status === 200 || response.status === 401 || response.status === 403;
  } catch (_err) {
    return false;
  }
}

async function testOpenAIKey(key) {
  return testHttpAuth('https://api.openai.com/v1/models', {
    Authorization: `Bearer ${key}`,
  });
}

async function testAnthropicKey(key) {
  return testHttpAuth('https://api.anthropic.com/v1/models', {
    'x-api-key': key,
    'anthropic-version': '2023-06-01',
  });
}

async function testGroqKey(key) {
  return testHttpAuth('https://api.groq.com/openai/v1/models', {
    Authorization: `Bearer ${key}`,
  });
}

async function testCohereKey(key) {
  return testHttpAuth('https://api.cohere.ai/v1/models', {
    Authorization: `Bearer ${key}`,
  });
}

async function validateApiKey(service, key) {
  switch (service) {
    case 'openai':
      return testOpenAIKey(key);
    case 'anthropic':
      return testAnthropicKey(key);
    case 'groq':
      return testGroqKey(key);
    case 'cohere':
      return testCohereKey(key);
    default:
      return Boolean(key);
  }
}

function serviceMapFromEnv(envObj) {
  return {
    openai: envObj.OPENAI_API_KEY,
    anthropic: envObj.ANTHROPIC_API_KEY,
    groq: envObj.GROQ_API_KEY,
    cohere: envObj.COHERE_API_KEY,
    pinecone: envObj.PINECONE_API_KEY,
    qdrant: envObj.QDRANT_API_KEY,
    supabase: envObj.SUPABASE_KEY,
    azure_openai: envObj.AZURE_OPENAI_KEY,
  };
}

async function validateKeyMap(keyMap) {
  const results = [];
  const entries = Object.entries(keyMap);
  for (const [service, key] of entries) {
    if (!key) {
      results.push({ service, present: false, valid: false, masked: '***' });
      continue;
    }
    const valid = await validateApiKey(service, key);
    results.push({ service, present: true, valid, masked: maskKey(key) });
  }
  return results;
}

function parseArgs(argv) {
  const args = { file: '.env' };
  for (let i = 2; i < argv.length; i += 1) {
    if (argv[i] === '--file') {
      args.file = argv[i + 1];
      i += 1;
    }
  }
  return args;
}

async function run() {
  const args = parseArgs(process.argv);
  const envPath = path.resolve(args.file);
  if (!fs.existsSync(envPath)) {
    console.error(`[ERROR] Env file not found: ${envPath}`);
    process.exit(1);
  }

  const envObj = parseEnv(fs.readFileSync(envPath, 'utf8'));
  const keyMap = serviceMapFromEnv(envObj);
  const results = await validateKeyMap(keyMap);

  let validCount = 0;
  for (const row of results) {
    if (!row.present) {
      console.log(`[WARN] ${row.service}: missing`);
      continue;
    }
    const status = row.valid ? 'VALID' : 'UNVERIFIED';
    if (row.valid) validCount += 1;
    console.log(`[INFO] ${row.service}: ${status} (${row.masked})`);
  }

  console.log(`[OK] Validation complete: ${validCount}/${results.length} keys reported as reachable or present.`);
}

if (require.main === module) {
  run();
}

module.exports = {
  parseEnv,
  validateApiKey,
  validateKeyMap,
  maskKey,
};
