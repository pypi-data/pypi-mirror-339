# AWS CDK MCP Server

MCP server for AWS Cloud Development Kit (CDK) best practices, infrastructure as code patterns, and security compliance with CDK Nag.

## Features

### CDK General Guidance

- Prescriptive patterns with AWS Solutions Constructs and GenAI CDK libraries
- Structured decision flow for choosing appropriate implementation approaches
- Security automation through CDK Nag integration and Lambda Powertools

### CDK Nag Integration

- Work with CDK Nag rules for security and compliance
- Explain specific CDK Nag rules with AWS Well-Architected guidance
- Check if CDK code contains Nag suppressions that require human review

### AWS Solutions Constructs

- Search and discover AWS Solutions Constructs patterns
- Find recommended patterns for common architecture needs
- Get detailed documentation on Solutions Constructs

### Generative AI CDK Constructs

- Search for GenAI CDK constructs by name or type
- Discover specialized constructs for AI/ML workloads
- Get implementation guidance for generative AI applications

### Amazon Bedrock Agent Schema Generation

- Generate OpenAPI schema for Bedrock Agent Action Groups
- Streamline the creation of Bedrock Agent schemas
- Convert code files to compatible OpenAPI specifications

## Tools and Resources

- **CDK Nag Rules**: Access rule packs via `cdk-nag://rules/{rule_pack}`
- **Lambda Powertools**: Get guidance on Lambda Powertools via `lambda-powertools://{topic}`
- **AWS Solutions Constructs**: Access patterns via `aws-solutions-constructs://{pattern_name}`
- **GenAI CDK Constructs**: Access documentation via `genai-cdk-constructs://{construct_type}/{construct_name}`

## Prerequisites

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python using `uv python install 3.10`

## Installation

Here are some ways you can work with MCP across AWS, and we'll be adding support to more products including Amazon Q Developer CLI soon: (e.g. for Amazon Q Developer CLI MCP, `~/.aws/amazonq/mcp.json`):

```json
{
  "mcpServers": {
    "awslabs.cdk-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.cdk-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Security Considerations

When using this MCP server, you should consider:

- Reviewing all CDK Nag warnings and errors manually
- Fixing security issues rather than suppressing them whenever possible
- Documenting clear justifications for any necessary suppressions
- Using the CheckCDKNagSuppressions tool to verify no unauthorized suppressions exist

Before applying CDK NAG Suppressions, you should consider conducting your own independent assessment to ensure that your use would comply with your own specific security and quality control practices and standards, as well as the local laws, rules, and regulations that govern you and your content.
