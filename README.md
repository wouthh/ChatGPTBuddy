# ChatGPTBuddy

> **Historical experiment:** current provider and API compatibility has not been verified. Never place provider credentials in source code.

ChatGPTBuddy explored terminal-based conversation, a retained message history, configurable system context, token-budget trimming, and optional speech synthesis.

## Historical configuration model

If you inspect this project locally, provide credentials only through the process environment or a local secret manager:

- `OPENAI_API_KEY` for the conversational API;
- `ELEVENLABS_API_KEY` for optional speech synthesis;
- `ELEVENLABS_VOICE_ID` when speech synthesis is enabled.

The script rejects missing values instead of falling back to credentials or key-shaped samples in the repository. Do not commit shell exports, local environment files, generated conversation state, or audio output.

This guidance documents a safer configuration boundary for the historical code. It does not claim that the application remains compatible with current provider APIs, SDKs, authentication requirements, or service terms.
