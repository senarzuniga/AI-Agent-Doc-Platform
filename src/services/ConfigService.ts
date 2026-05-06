export class ConfigService {
  private static instance: ConfigService;

  private readonly config: Map<string, string> = new Map();

  private readonly knownKeys = [
    'OPENAI_API_KEY',
    'ANTHROPIC_API_KEY',
    'GROQ_API_KEY',
    'COHERE_API_KEY',
    'PINECONE_API_KEY',
    'QDRANT_API_KEY',
    'SUPABASE_URL',
    'SUPABASE_KEY',
    'AZURE_OPENAI_KEY',
    'AZURE_OPENAI_ENDPOINT',
  ];

  private constructor() {
    // Singleton: use ConfigService.getInstance()
  }

  static getInstance(): ConfigService {
    if (!ConfigService.instance) {
      ConfigService.instance = new ConfigService();
    }
    return ConfigService.instance;
  }

  async loadFromEnvironment(): Promise<void> {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    require('dotenv').config();

    for (const key of this.knownKeys) {
      const value = process.env[key];
      if (value) {
        this.config.set(key, value);
        console.log(`[OK] Loaded ${key}`);
      } else {
        console.warn(`[WARN] Missing ${key}`);
      }
    }
  }

  getApiKey(service: string): string {
    const keyMap: Record<string, string> = {
      openai: 'OPENAI_API_KEY',
      anthropic: 'ANTHROPIC_API_KEY',
      groq: 'GROQ_API_KEY',
      cohere: 'COHERE_API_KEY',
      pinecone: 'PINECONE_API_KEY',
      qdrant: 'QDRANT_API_KEY',
      supabase: 'SUPABASE_KEY',
    };

    const envKey = keyMap[service.toLowerCase()];
    if (!envKey) {
      throw new Error(`Unsupported service: ${service}`);
    }

    const apiKey = this.config.get(envKey);
    if (!apiKey) {
      throw new Error(`API key not found for service: ${service}`);
    }

    return apiKey;
  }

  get(key: string): string | undefined {
    return this.config.get(key);
  }

  maskKey(key: string): string {
    if (!key) return '***';
    if (key.length <= 8) {
      return `${key.slice(0, 2)}...${key.slice(-2)}`;
    }
    return `${key.slice(0, 4)}...${key.slice(-4)}`;
  }
}
