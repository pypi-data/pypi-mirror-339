# OpenAPI Tools Overview

OpenAPI Tools provides a unified toolkit for creating, managing, and using AI tools across different LLM platforms like OpenAI, Anthropic, and LangChain.

> The most critical aspect to understand is that tool execution happens
> on your server where you're using the SDK. This means:
>
> - You bear the infrastructure costs
> - We manage and provide a streamlined, automated way of creating agents and executing tools
> - Your data remains in your environment during execution

## Key Features

- **Centralized tool management** through Swagger/OpenAPI specs conversion
- **Multi-platform compatibility** with various AI providers
- **Local execution** for your security and control
- **Simple integration** via easy-to-use adapters

## Getting Started

Installation is simple:

```bash
pip install reacter-openapitools
```