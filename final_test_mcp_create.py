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
print("使用 MCP 创建云文档（最终测试）")
print("=" * 60)

print(f"\nTenant Access Token: {tat_token[:20]}...")
print(f"User Access Token: {user_access_token[:20]}...")

# 测试文档内容
markdown_content = """# 测试云文档

这是一个使用 User Access Token 通过 MCP 创建的测试文档。

## 文档信息

- **创建时间**: 2026-03-26
- **创建方式**: MCP API
- **认证方式**: User Access Token + Tenant Access Token

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
            "title": "测试云文档 - MCP 创建",
            "markdown": markdown_content
        }
    },
    "jsonrpc": "2.0",
    "id": 1
}

print(f"\n请求参数:")
print(f"  标题：测试云文档 - MCP 创建")
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
                error_text = error_detail.get('error', '')
                # 提取关键信息
                if 'errorCode' in error_text:
                    error_code = error_text.split('errorCode=')[1].split('\\')[0] if 'errorCode=' in error_text else '未知'
                    print(f"  错误码：{error_code}")
                if 'api=' in error_text:
                    api = error_text.split('api=')[1].split(',')[0] if 'api=' in error_text else '未知'
                    print(f"  API: {api}")
            except:
                pass
    elif response.status_code == 200 and "result" in result:
        print("\n✓ 云文档创建成功！")
        
        # 提取文档信息
        if "content" in result.get("result", {}):
            content = result["result"]["content"]
            print(f"\n文档信息:")
            # 尝试解析返回的 JSON
            try:
                doc_info = json.loads(content[0]["text"])
                if "doc_id" in doc_info:
                    print(f"  文档 ID: {doc_info['doc_id']}")
                if "url" in doc_info:
                    print(f"  文档 URL: {doc_info['url']}")
                if "title" in doc_info:
                    print(f"  标题：{doc_info['title']}")
            except:
                print(f"  原始内容：{content}")
    else:
        print("\n✗ 创建失败，未知错误")
            
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)

# 提供排查建议
print("\n如果仍然失败，可能的原因：")
print("1. 权限配置问题：检查权限是否是'用户身份'类型")
print("2. 权限未生效：等待 5-10 分钟后重试")
print("3. 应用未发布：需要在飞书开放平台发布应用版本")
print("4. 数据范围限制：检查权限的数据范围配置")

print("\n排查步骤：")
print("1. 访问飞书开放平台 > 应用管理 > 权限管理")
print("2. 确认 docx:document 和 docx:document:create 权限状态为'已开通'")
print("3. 确认权限类型为'用户身份'")
print("4. 确认数据范围为'与用户权限范围一致'")
print("5. 在版本管理中发布应用版本")
print("6. 等待权限生效（5-10 分钟）")
print("7. 重新授权并获取新的 User Access Token")
print("8. 再次测试")

print("\n" + "=" * 60)
