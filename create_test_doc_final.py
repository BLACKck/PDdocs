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

# 测试文档内容
markdown_content = """# 测试云文档

这是一个使用 User Access Token 通过 MCP 创建的测试文档。

## 文档信息

- **创建时间**: 2026-03-26
- **创建方式**: MCP API
- **认证方式**: User Access Token

## 测试目的

验证 User Access Token 在 MCP 服务中的使用情况。

---
*此文档由自动化脚本创建*
"""

# 构建请求
headers = {
    "X-Lark-MCP-TAT": tat_token,
    "X-Lark-MCP-UAT": user_access_token,
    "Content-Type": "application/json",
    "X-Lark-MCP-Allowed-Tools": "create-doc"
}

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
    "id": 1
}

print(f"\n请求参数:")
print(f"  标题：测试云文档 - User Access Token")
print(f"  内容长度：{len(markdown_content)} 字符")

print("\n正在创建文档...")

response = requests.post(mcp_url, headers=headers, json=create_payload)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    print(f"\n解析后的响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 检查是否有错误
    if "error" in result:
        error = result["error"]
        print(f"\n✗ 创建失败")
        print(f"错误信息：{error.get('message', '')}")
        
        # 解析错误详情
        if "content" in result.get("result", {}):
            try:
                error_detail = json.loads(result["result"]["content"][0]["text"])
                print(f"\n详细错误：")
                print(f"  错误码：{error_detail.get('error', '').split(':')[0] if ':' in error_detail.get('error', '') else error_detail.get('error')}")
                print(f"  描述：{error_detail.get('error', '').split('💡')[0]}")
            except:
                pass
    elif response.status_code == 200 and "result" in result:
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
        print("\n✗ 创建失败，未知错误")
            
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)

# 提供权限说明
print("\n权限说明：")
print("  创建文档需要以下权限：")
print("  - docx:document:create (创建云文档)")
print("  - docx:document:read (读取云文档)")
print("\n当前已开通权限：")
print("  - docx:document:readonly (只读权限)")
print("\n如果创建失败，请检查是否开通了 docx:document:create 权限")
print("开通方式：飞书开放平台 > 应用管理 > 权限管理 > 开通权限")

print("\n" + "=" * 60)
