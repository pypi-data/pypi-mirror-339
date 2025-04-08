from fastmcp import FastMCP
import httpx
import os

# 创建 MCP 服务
mcp = FastMCP("Bark Message Pusher", dependencies=["httpx"])

# 从环境变量获取设备密钥列表
# 获取并验证设备密钥
DEVICE_KEYS = os.getenv("BARK_DEVICE_KEYS", "").split(",")
BARK_SERVER = os.getenv("BARK_SERVER", "https://api.day.app")


@mcp.tool()
async def send_message(title: str, content: str) -> str:
    """
    向所有配置的 Bark 设备发送消息

    Args:
        title: 消息标题
        content: 消息内容

    Returns:
        str: 发送结果
    """
    if not DEVICE_KEYS or not DEVICE_KEYS[0]:
        return "错误：未配置设备密钥，请设置 BARK_DEVICE_KEYS 环境变量"

    results = []
    async with httpx.AsyncClient() as client:
        for key in DEVICE_KEYS:
            if not key.strip():
                continue

            url = f"{BARK_SERVER}/{key.strip()}/{title}/{content}"
            try:
                response = await client.get(url)
                results.append(
                    f"设备 {key}: {'成功' if response.status_code == 200 else '失败'}"
                )
            except Exception as e:
                results.append(f"设备 {key}: 错误 - {str(e)}")

    return "\n".join(results)


if __name__ == "__main__":
    mcp.run()
