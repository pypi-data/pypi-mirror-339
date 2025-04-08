# Tencent Cloud TAT MCP Server

An MCP server implementation for executing commands on Tencent Cloud instances using the TencentCloud Automation Tools (TAT) API.

## Features

- **RunCommand**: Asynchronously execute Shell/PowerShell commands on Tencent Cloud instances
- **QueryTask**: Retrieve command execution results and outputs
- **Supports both Linux and Windows**: Automatically handles command encoding based on OS type

## Tools

### RunCommand
Sync Execute commands on Tencent Cloud instances.

**Inputs**:
- `Region` (string): Tencent Cloud region (e.g. ap-beijing, ap-guangzhou)
- `InstanceId` (string): Target cloud server instance ID (format: ins-xxxxxxxx or lhins-xxxxxxxx)
- `Command` (string): Command to execute (will be automatically Base64 encoded)
- `SystemType` (string, optional): OS type (Linux/Windows, default: Linux)

### RunCommand
Async Execute commands on Tencent Cloud instances.

**Inputs**:
- `Region` (string): Tencent Cloud region (e.g. ap-beijing, ap-guangzhou)
- `InstanceId` (string): Target cloud server instance ID (format: ins-xxxxxxxx or lhins-xxxxxxxx)
- `Command` (string): Command to execute (will be automatically Base64 encoded)
- `SystemType` (string, optional): OS type (Linux/Windows, default: Linux)

### QueryTask
Retrieve asynchronous command execution results.

**Inputs**:
- `Region` (string): Tencent Cloud region
- `TaskId` (string): Task ID returned by RunCommand (format: invt-xxxxxx)

## Configuration

### Setting up Tencent Cloud Credentials

1. Obtain SecretId and SecretKey from Tencent Cloud Console
2. Set your default region (optional)

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tencent-tat": {
     "command": "uv",
    "args": [
      "run",
      "mcp-server-tat"]
      "env": {
        "TENCENTCLOUD_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "TENCENTCLOUD_SECRET_KEY": "YOUR_SECRET_KEY_HERE",
        "TENCENTCLOUD_REGION": "YOUR_REGION_HERE"
      }
    }
  }
}
```

## Installation

```sh
pip install mcp-server-tat
```


## License

MIT License. See LICENSE for details.
