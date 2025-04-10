# Arcanna Input MCP Server

The Arcanna Input MCP server allows user to interact with Arcanna's AI use cases that use external api integration through the Model Context Protocol (MCP).

## Usage with Claude Desktop or other MCP Clients

#### Configuration
Add the following entry to the `mcpServers` section in your MCP client config file (`claude_desktop_config.json` for Claude
Desktop).

### Use docker image (https://hub.docker.com/r/arcanna/arcanna-input-mcp-server) or PyPi package (https://pypi.org/project/arcanna-mcp-input-server)

### Building local image from this repository
#### Prerequisites
- Docker - https://docs.docker.com/engine/install/

#### Configuration
1. Change directory to the directory where the Dockerfile is.
2. Run ```docker build -t arcanna/arcanna-input-mcp-server . --progress=plain --no-cache```
3. Add the configuration bellow to your claude desktop/mcp client config.


```json
{
  "mcpServers": {
    "arcanna-input-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "ARCANNA_INPUT_API_KEY",
        "-e",
        "ARCANNA_HOST",
        "-e",
        "ARCANNA_USER",
        "arcanna/arcanna-input-mcp-server"
      ],
      "env": {
        "ARCANNA_INPUT_API_KEY": "<YOUR_ARCANNA_API_KEY_HERE>",
        "ARCANNA_HOST": "<YOUR_ARCANNA_HOST_HERE>",
        "ARCANNA_USER": "<YOUR_USERNAME_HERE>"
      }
    }
  }
}
```

## Features

- **Job Management**: Create, retrieve, start, stop, and train jobs
- **Event Processing**: Send events for AI-powered decision making
- **Feedback System**: Provide feedback on decisions to improve model accuracy
- **Health Monitoring**: Check server and API key status

## Tools

### Job Management
- **get_external_input_jobs**
  - Retrieve all jobs associated with your API key
  - Returns a list of job details including status, labels, and processing metrics

- **get_external_input_job_by_id**
  - Retrieve specific job details by ID

- **get_external_input_job_by_name**
  - Retrieve specific job details by name

- **get_external_input_job_labels**
  - Retrieve decision labels for a specific job

### Event Management
- **send_event_to_external_input_job**
  - Submit an event to Arcanna for AI decision-making

- **send_event_with_id_to_external_input_job**
  - Submit an event with a custom identifier

### System Health
- **health_check_input_server**
  - Verify server status and API key validity
  - Returns API key authorization status
