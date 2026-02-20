---
name: ai-feature
description: Guides implementation of AI-powered features using LLMs in the CV Simulator
---

# AI Integration Standards

## Features
- CV content generation from user input
- Skills analysis and recommendations
- Job description matching score
- CV improvement suggestions

## Architecture
- AI requests go through RabbitMQ (async processing)
- Celery worker handles LLM API calls
- Results cached in Redis (TTL: 1 hour)
- Background task pattern: endpoint → publish to queue → worker processes → store result → notify

## Rules
- Never call LLM APIs synchronously in the request cycle
- Always have a fallback if AI service is unavailable
- Cache identical prompts to reduce API costs
- Use structured output (JSON mode) for all LLM responses
- Rate limit AI endpoints per user
