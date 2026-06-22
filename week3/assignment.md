# Week 3 — Build a Custom MCP Server

Design and implement a Model Context Protocol (MCP) server that wraps a real external API. 
You will be running it **locally** (STDIO transport) and integrating with an MCP client (like Claude Desktop).

## Learning goals
- Understand core MCP capabilities: tools, resources, prompts.
- Implement tool definitions with typed parameters and robust error handling.
- Follow logging and transport best practices (no stdout for STDIO servers).

## Requirements
1. Choose an external API and document which endpoints you’ll use. Examples: weather, GitHub issues, Notion pages, movie/TV databases, calendar, task managers, finance/crypto, travel, sports stats.
2. Expose at least two MCP tools
3. Implement basic resilience:
   - Graceful errors for HTTP failures, timeouts, and empty results.
   - Respect API rate limits (e.g., simple backoff or user-facing warning).
4. Packaging and docs:
   - Provide clear setup instructions, environment variables, and run commands (READMEs).
   - Include an example invocation flow (what to type/click in the client to trigger the tools).
5. Ensure it is runnable from your machine and discoverable by Claude Desktop or an AI IDE like Cursor.

## Deliverables
- Source code under `week3/` (suggested: `week3/server/` with a clear entrypoint like `main.py` or `app.py`).
- `week3/README.md` with:
  - Prerequisites, environment setup, and run instructions (local and/or remote).
  - How to configure the MCP client (Claude Desktop example for local) or agent runtime for remote.
  - Tool reference: names, parameters, example inputs/outputs, and expected behaviors.

## References
As a helpful reference, here is a MCP Server Quickstart: [modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server). 

For additional challenge, here is additional information on remote MCP:
- MCP Authorization (HTTP): [modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- Remote MCP on Cloudflare (Agents): [developers.cloudflare.com/agents/guides/remote-mcp-server/](https://developers.cloudflare.com/agents/guides/remote-mcp-server/). Use the modelcontextprotocol inspector tool to debug your server locally before deploying.
- https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel If you choose to do a remote MCP deployment, Vercel is a good option with a free tier. 