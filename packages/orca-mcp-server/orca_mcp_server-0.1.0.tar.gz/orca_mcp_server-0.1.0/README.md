# Orca Security MCP Integration

This integration connects Orca Security's AI Sonar and data serving capabilities to MCP (Model Control Protocol), allowing you to ask natural language questions about your cloud infrastructure security posture directly in Cursor, Claude or other AI tools.

## Features

- Natural language processing of security questions via Orca's AI Sonar
- Direct querying of Orca Security's data
- Pretty-formatted JSON responses
- Environment variable configuration for flexible deployment

## Setup

1. Install `uv` if you don't have it already:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone this repository
3. Install using `uv` (which will handle dependencies automatically)
4. Set environment variables (optional, see below)
5. Run the MCP server

## Environment Variables

| Variable               | Description                        | Default                       |
| ---------------------- | ---------------------------------- | ----------------------------- |
| `ORCA_API_HOST`        | Orca Security API host             | <https://api.orcasecurity.io> |
| `ORCA_AUTH_TOKEN`      | Your Orca API authentication token | TOKEN                         |
| `ORCA_REQUEST_TIMEOUT` | API request timeout in seconds     | 30.0                          |

## Running the Integration

```bash
# Set your Orca authentication token
export ORCA_AUTH_TOKEN="your-token-here"

# First time setup
uv sync

# Run the MCP server
uv run orcamcp
```

## Configure Claude Desktop

To integrate with Claude Desktop, you need to update the Claude Desktop configuration file:

1. Create or edit the file at `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the following configuration (replacing `<TOKEN>` with your actual Orca token):

   ```json
   {
     "mcpServers": {
       "OrcaSecurity": {
         "command": "uv",
         "args": ["--directory", "/path/to/your/orcamcp", "run", "orcamcp"],
         "env": {
           "ORCA_AUTH_TOKEN": "<TOKEN>"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop for the changes to take effect

## Using the Integration

Once running, you can query the Orca Security data using natural language:

Example queries:

- "Show me all critical vulnerabilities in my AWS environment"
- "What EC2 instances are missing security patches?"
- "Which S3 buckets are publicly accessible?"

## Troubleshooting

If you encounter issues:

1. Check the log output for error messages
2. Verify your Orca authentication token is valid
3. Ensure your network allows connections to the Orca API endpoint
