## Content Moderation System

Implements automated moderation using:
- llama-guard-3-8b for safety checks
- llama-3.1-70b for content analysis

### Features
- Platform-specific examples (Twitter/Facebook/Reddit/Instagram)
- JSON report generation
- Safety improvement suggestions

### Usage
```bash
pip install groq
export GROQ_API_KEY="your-key"
jupyter notebook content_moderation.ipynb