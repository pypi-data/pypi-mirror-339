# 消息推送服务 (MCP)

这是一个使用 [FastMCP](https://github.com/your-fastmcp-repo) 框架构建的消息推送服务集合。它允许您通过简单的 API 调用将消息发送到 PushDeer 和 Bark 服务。

## 功能

- **PushDeer 推送** (`pushdeer.py`):
    - 发送文本消息 (`send_message`)
    - 发送 Markdown 格式消息 (`send_markdown`)
    - 发送图片消息 (`send_image`)
- **Bark 推送** (`barkme.py`):
    - 发送带有标题和内容的消息 (`send_message`)

## 依赖

- Python 3.x
- `httpx`
- `fastmcp` (请确保已安装)

具体依赖请参考 `pyproject.toml`。

## 安装与配置

1.  **克隆仓库** (如果尚未完成):
    ```bash
    git clone <your-repo-url>
    cd mcp/fmt
    ```

2.  **安装依赖**:
    建议使用虚拟环境。
    ```bash
    # 使用 uv (推荐)
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt # 如果有 requirements.txt
    # 或者根据 pyproject.toml 安装
    uv pip install .

    # 或者使用 pip
    # python -m venv .venv
    # source .venv/bin/activate
    # pip install httpx fastmcp # 根据 pyproject.toml 调整
    ```

3.  **配置环境变量**:

    在运行脚本前，请设置以下环境变量：

    - **PushDeer (`pushdeer.py`)**:
        - `PUSHDEER_KEYS`: 必需。您的 PushDeer 推送密钥，多个密钥用英文逗号 `,` 分隔。
        - `PUSHDEER_SERVER`: 可选。您的自建 PushDeer 服务器地址，默认为 `https://api2.pushdeer.com`。
    - **Bark (`barkme.py`)**:
        - `BARK_DEVICE_KEYS`: 必需。您的 Bark 设备密钥，多个密钥用英文逗号 `,` 分隔。
        - `BARK_SERVER`: 可选。您的自建 Bark 服务器地址，默认为 `https://api.day.app`。

    您可以将这些变量设置在 `.env` 文件中 (如果您的环境支持)，或者直接在运行环境中导出。

## 运行服务

您可以使用 `FastMCP` 提供的命令行工具来运行这些服务，或者直接运行 Python 脚本：

```bash
# 运行 PushDeer 服务
# 方法一: 使用 FastMCP CLI
fastmcp run pushdeer.py
# 方法二: 直接运行脚本
python pushdeer.py

# 运行 Bark 服务
# 方法一: 使用 FastMCP CLI
fastmcp run barkme.py
# 方法二: 直接运行脚本
python barkme.py
```


## 贡献

欢迎提交 Pull Request 或提出 Issue。