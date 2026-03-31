import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

auth_header = config["mcpServers"]["feishu-remote"]["headers"]["Authorization"]
mcp_url = config["mcpServers"]["feishu-remote"]["url"]

# 测试搜索用户工具
payload = {
    "toolcalls": [
        {
            "thought": "测试MCP服务",
            "name": "search-user",
            "params": {
                "query": "test"
            }
        }
    ]
}

# 发送请求
try:
    response = requests.post(mcp_url, json=payload, headers={"Authorization": auth_header})
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    try:
        result = response.json()
        print(f"JSON解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
except Exception as e:
    print(f"请求失败: {e}")
