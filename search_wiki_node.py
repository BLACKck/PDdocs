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
    "X-Lark-MCP-Allowed-Tools": "search-doc"
}

print("搜索'俄罗斯方块'项目，获取正确的 wiki_node...")

# 搜索"俄罗斯方块"项目
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "search-doc",
        "arguments": {
            "query": "俄罗斯方块",
            "filters": {
                "sort_rule": "CREATE_TIME"
            }
        }
    }
}

response = requests.post(mcp_url, headers=headers, json=payload)
print(f"响应状态码：{response.status_code}")

try:
    result = response.json()
    if result.get("result") and result["result"].get("content"):
        content = result["result"]["content"][0]["text"]
        content_json = json.loads(content)
        print(f"搜索结果：{json.dumps(content_json, indent=2, ensure_ascii=False)}")
        
        # 提取 wiki_space 或 wiki_node 信息
        wiki_space = content_json.get("wiki_space")
        wiki_node = content_json.get("wiki_node")
        
        if wiki_space:
            print(f"\n找到 wiki_space: {wiki_space}")
        if wiki_node:
            print(f"找到 wiki_node: {wiki_node}")
    else:
        print("未找到搜索结果")
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")
