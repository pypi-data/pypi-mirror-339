# How to run
## sse
```bash
zmp-alert-mcp-server -e https://api.ags.cloudzcp.net -p 8888 -s zmp-f9aed626-c0d6-4293-8a66-c36755e8e948 --transport sse
```

## stdio
first install the zmp-alert-mcp-server
```bash
pip install zmp-alert-mcp-server
```

then configure the mcp server into the mcp host like claude desktop or cursor
```json
{
  "mcpServers": {
    "zmp-alert-mcp-server": {
      "command": "python3",
      "args": [
        "-m",
        "zmp_alert_mcp_server",
        "--transport",
        "stdio",
        "--endpoint",
        "https://api.ags.cloudzcp.net",
        "--access-key",
        "xxxxxxx"
      ]
    }
  }
}

```
