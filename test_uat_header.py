import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 从配置中提取 token
tat_token = config["mcpServers"]["feishu-remote"]["headers"]["Authorization"].split(" ")[1]
user_access_token = config["user_access_token"]

# MCP 服务 URL
mcp_url = "https://mcp.feishu.cn/mcp"

print("=" * 60)
print("测试不同的 User Access Token 传递方式")
print("=" * 60)

# 测试文档内容
markdown_content = """# 测试云文档

这是一个测试文档。
"""

# 创建文档的请求
create_payload = {
    "method": "tools/call",
    "params": {
        "name": "create-doc",
        "arguments": {
            "title": "测试云文档 - UAT 测试",
            "markdown": markdown_content
        }
    },
    "jsonrpc": "2.0",
    "id": 1
}

# 测试不同的 header 组合
test_cases = [
    {
        "name": "方式 1: 使用 X-Lark-MCP-UAT 头",
        "headers": {
            "X-Lark-MCP-TAT": tat_token,
            "X-Lark-MCP-UAT": user_access_token,
            "Content-Type": "application/json",
            "X-Lark-MCP-Allowed-Tools": "create-doc"
        }
    },
    {
        "name": "方式 2: 使用 X-Access-Token 头",
        "headers": {
            "X-Lark-MCP-TAT": tat_token,
            "X-Access-Token": user_access_token,
            "Content-Type": "application/json",
            "X-Lark-MCP-Allowed-Tools": "create-doc"
        }
    },
    {
        "name": "方式 3: 在参数中传递 user_id",
        "headers": {
            "X-Lark-MCP-TAT": tat_token,
            "Content-Type": "application/json",
            "X-Lark-MCP-Allowed-Tools": "create-doc"
        },
        "payload_modifier": {
            "params": {
                "name": "create-doc",
                "arguments": {
                    "title": "测试云文档 - UAT 测试",
                    "markdown": markdown_content,
                    "user_id": "3gb37268"
                }
            }
        }
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'=' * 60}")
    print(f"测试 {i}: {test_case['name']}")
    print(f"{'=' * 60}")
    
    headers = test_case["headers"]
    payload = test_case.get("payload_modifier", create_payload)
    
    if "payload_modifier" in test_case:
        # 合并 payload
        full_payload = create_payload.copy()
        if "params" in payload:
            full_payload["params"] = payload["params"]
    else:
        full_payload = create_payload
    
    print(f"\n请求头：")
    for key, value in headers.items():
        if "Token" in key:
            print(f"  {key}: {value[:20]}...")
        else:
            print(f"  {key}: {value}")
    
    response = requests.post(mcp_url, headers=headers, json=full_payload)
    
    print(f"\n响应状态码：{response.status_code}")
    print(f"响应内容：{response.text}")
    
    try:
        result = response.json()
        if response.status_code == 200 and "result" in result:
            print("\n✓ 创建成功！")
            if "content" in result.get("result", {}):
                content = result["result"]["content"]
                if "doc_id" in content:
                    print(f"文档 ID: {content['doc_id']}")
                if "url" in content:
                    print(f"文档 URL: {content['url']}")
            break  # 成功后停止测试
        else:
            print("\n✗ 创建失败")
            if "error" in result:
                error = result["error"]
                print(f"错误：{error.get('message')}")
    except Exception as e:
        print(f"处理响应失败：{e}")
    
    print("-" * 60)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
