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
    "X-Lark-MCP-Allowed-Tools": "create-doc,fetch-doc,update-doc,get-user,search-doc"
}

# 构建初始化请求体
payload = {
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "test-client",
            "version": "1.0.0"
        }
    },
    "jsonrpc": "2.0",
    "id": 1
}

print("=" * 60)
print("测试飞书 MCP 服务连接")
print("=" * 60)

print(f"\n请求 URL: {mcp_url}")
print(f"请求头：")
for key, value in headers.items():
    print(f"  {key}: {value}")
print(f"\n请求体：{json.dumps(payload, indent=2)}")

print("\n正在发送请求...")

response = requests.post(mcp_url, headers=headers, json=payload)

print(f"\n响应状态码：{response.status_code}")
print(f"响应头：{dict(response.headers)}")
print(f"\n响应内容：{response.text}")

try:
    result = response.json()
    print(f"\n解析后的响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        print("\n✓ MCP 服务连接成功！")
        
        # 检查响应中的关键信息
        if "result" in result:
            print(f"\n服务器信息:")
            if "serverInfo" in result.get("result", {}):
                server_info = result["result"]["serverInfo"]
                print(f"  名称：{server_info.get('name')}")
                print(f"  版本：{server_info.get('version')}")
            
            # 检查可用工具
            if "capabilities" in result.get("result", {}):
                capabilities = result["result"]["capabilities"]
                print(f"\n服务器能力:")
                print(f"  {json.dumps(capabilities, indent=2, ensure_ascii=False)}")
    else:
        print(f"\n✗ MCP 服务连接失败")
        if "error" in result:
            error = result["error"]
            print(f"错误码：{error.get('code')}")
            print(f"错误信息：{error.get('message')}")
            
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
