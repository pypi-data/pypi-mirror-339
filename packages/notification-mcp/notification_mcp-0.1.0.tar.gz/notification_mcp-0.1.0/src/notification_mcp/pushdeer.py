from fastmcp import FastMCP
import httpx
import os
from typing import Optional
from enum import Enum

# 创建 MCP 服务
mcp = FastMCP("PushDeer Message Pusher", dependencies=["httpx"])

# 从环境变量获取配置
PUSHDEER_KEYS = os.getenv("PUSHDEER_KEYS", "").split(",")
if not PUSHDEER_KEYS or not PUSHDEER_KEYS[0]:
    raise ValueError("PUSHDEER_KEYS 不能为空")

PUSHDEER_SERVER = os.getenv("PUSHDEER_SERVER", "https://api2.pushdeer.com")


class MessageType(str, Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    IMAGE = "image"


@mcp.tool()
async def send_message(
    text: str,
    desp: Optional[str] = None,
    type: MessageType = MessageType.TEXT,
    pushkey: Optional[str] = None,
) -> str:
    """
    向 PushDeer 设备发送消息

    Args:
        text: 消息内容（对于图片类型，这是图片URL）
        desp: 消息描述（可选）
        type: 消息类型，可选值：text/markdown/image
        pushkey: 指定推送密钥（可选，不指定则使用环境变量中的密钥）

    Returns:
        str: 发送结果
    """
    # 如果指定了 pushkey，则只使用该密钥
    keys = [pushkey] if pushkey else PUSHDEER_KEYS

    results = []
    async with httpx.AsyncClient() as client:
        for key in keys:
            if not key.strip():
                continue

            url = f"{PUSHDEER_SERVER}/message/push"
            data = {"pushkey": key.strip(), "text": text, "type": type.value}
            if desp:
                data["desp"] = desp

            try:
                response = await client.post(url, data=data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("code") == 0:
                        results.append(f"设备 {key}: 发送成功")
                    else:
                        results.append(f"设备 {key}: 发送失败 - {result.get('error')}")
                else:
                    results.append(
                        f"设备 {key}: 请求失败 - HTTP {response.status_code}"
                    )
            except Exception as e:
                results.append(f"设备 {key}: 错误 - {str(e)}")

    return "\n".join(results)


@mcp.tool()
async def send_markdown(
    markdown: str,
    desp: Optional[str] = None,
    pushkey: Optional[str] = None,
) -> str:
    """
    发送 Markdown 格式消息

    Args:
        markdown: Markdown 格式的消息内容
        desp: 消息描述（可选）
        pushkey: 指定推送密钥（可选）

    Returns:
        str: 发送结果
    """
    return await send_message(
        text=markdown, desp=desp, type=MessageType.MARKDOWN, pushkey=pushkey
    )


@mcp.tool()
async def send_image(
    image_url: str,
    desp: Optional[str] = None,
    pushkey: Optional[str] = None,
) -> str:
    """
    发送图片消息

    Args:
        image_url: 图片的 URL 地址
        desp: 消息描述（可选）
        pushkey: 指定推送密钥（可选）

    Returns:
        str: 发送结果
    """
    return await send_message(
        text=image_url, desp=desp, type=MessageType.IMAGE, pushkey=pushkey
    )


if __name__ == "__main__":
    mcp.run()
