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
print("使用 User Access Token 创建测试云文档")
print("=" * 60)

print(f"\nTenant Access Token: {tat_token[:20]}...")
print(f"User Access Token: {user_access_token[:20]}...")

# 步骤一：初始化 MCP 连接
print("\n步骤一：初始化 MCP 连接...")

headers = {
    "X-Lark-MCP-TAT": tat_token,
    "Content-Type": "application/json",
    "X-Lark-MCP-Allowed-Tools": "create-doc"
}

init_payload = {
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

response = requests.post(mcp_url, headers=headers, json=init_payload)
init_result = response.json()

if response.status_code == 200 and init_result.get("result"):
    print("✓ MCP 连接成功")
else:
    print("✗ MCP 连接失败")
    print(f"错误：{init_result}")
    exit(1)

# 步骤二：使用 User Access Token 创建文档
print("\n步骤二：创建测试云文档...")

# 测试文档内容
markdown_content = """# 测试云文档

这是一个使用 User Access Token 通过 MCP 创建的测试文档。

## 文档信息

- **创建时间**: 2026-03-26
- **创建方式**: MCP API
- **认证方式**: User Access Token

## 测试目的

验证 User Access Token 在 MCP 服务中的使用情况。

## 内容测试

这是一些测试内容：

1. 列表项 1
2. 列表项 2
3. 列表项 3

### 代码示例

```python
def hello_world():
    print("Hello from Feishu MCP!")
```

---
*此文档由自动化脚本创建*
"""

create_payload = {
    "method": "tools/call",
    "params": {
        "name": "create-doc",
        "arguments": {
            "title": "测试云文档 - User Access Token",
            "markdown": markdown_content
        }
    },
    "jsonrpc": "2.0",
    "id": 2
}

# 使用 User Access Token 创建文档
# 注意：MCP 服务可能需要特殊的头来传递用户 token
uat_headers = {
    "X-Lark-MCP-TAT": tat_token,
    "Content-Type": "application/json",
    "X-Lark-MCP-Allowed-Tools": "create-doc",
    "Authorization": f"Bearer {user_access_token}"
}

print(f"\n请求参数:")
print(f"  标题：测试云文档 - User Access Token")
print(f"  内容长度：{len(markdown_content)} 字符")

response = requests.post(mcp_url, headers=uat_headers, json=create_payload)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    print(f"\n解析后的响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200 and "result" in result:
        print("\n✓ 云文档创建成功！")
        
        # 提取文档信息
        if "content" in result.get("result", {}):
            content = result["result"]["content"]
            print(f"\n文档信息:")
            if "doc_id" in content:
                print(f"  文档 ID: {content['doc_id']}")
            if "url" in content:
                print(f"  文档 URL: {content['url']}")
            if "title" in content:
                print(f"  标题：{content['title']}")
    else:
        print("\n✗ 云文档创建失败")
        if "error" in result:
            error = result["error"]
            print(f"错误码：{error.get('code')}")
            print(f"错误信息：{error.get('message')}")
            
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
