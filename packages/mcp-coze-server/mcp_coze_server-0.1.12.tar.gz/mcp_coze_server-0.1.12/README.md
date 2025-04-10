# MCP Coze Server

A MCP server implementation for Coze API

## Installation

1. Install the package from PyPI:
```bash
pip install mcp-coze-server
```

2. Install additional dependencies:
```bash
pip install cozepy @ git+https://github.com/shizeying/coze-py.git@v0.13.1.post1
```

Or install from source:
```bash
git clone https://github.com/shizeying/coze-mcp-server.git
cd coze-mcp-server
pip install -r requirements.txt
pip install -e .
```

## Usage

1. 设置环境变量：

```bash
export COZE_API_TOKEN="your_api_token"
export COZE_API_BASE="https://api.coze.cn"  # 或其他API地址
```

2. 运行服务器：

```bash
python -m mcp_coze_server
```

## Configuration

Support the following configuration methods:

1. Environment variables:
   - COZE_API_TOKEN
   - COZE_API_BASE

2. Command line arguments:
   - --coze-api-token
   - --coze-api-base

## Development

1. Clone the repository:

```bash
git clone https://github.com/shizeying/coze-mcp-server.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 