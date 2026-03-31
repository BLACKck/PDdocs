import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 从配置中提取 token
token = config["mcpServers"]["feishu-remote"]["headers"]["Authorization"].split(" ")[1]

# MCP 服务 URL
mcp_url = "https://mcp.feishu.cn/mcp"

# 构建请求头
headers = {
    "X-Lark-MCP-TAT": token,
    "Content-Type": "application/json",
    "X-Lark-MCP-Allowed-Tools": "fetch-doc"
}

# 需求文档 ID
doc_id = "EIWcd8E86oX8xDxWLBqcDzmZnQd"

print("获取需求文档当前内容...")
print(f"文档 ID: {doc_id}")

# 获取文档内容（使用 doc_id 参数）
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "fetch-doc",
        "arguments": {
            "doc_id": doc_id
        }
    }
}

response = requests.post(mcp_url, headers=headers, json=payload)
print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    if result.get("result") and result["result"].get("content"):
        content = result["result"]["content"][0]["text"]
        print(f"\n文档内容：\n{content}")
    else:
        print("\n获取文档内容失败")
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")
