import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 获取 User Access Token
user_access_token = config["user_access_token"]

print("=" * 60)
print("测试创建云文档（权限已开通）")
print("=" * 60)

print(f"\nUser Access Token: {user_access_token[:20]}...")

# 使用飞书云文档 API v2 创建文档
url = "https://open.feishu.cn/open-apis/docx/v1/documents"
headers = {
    "Authorization": f"Bearer {user_access_token}",
    "Content-Type": "application/json"
}

# 创建文档的请求体
payload = {
    "title": "测试云文档 - 权限验证成功",
    "folder_token": ""
}

print(f"\n请求 URL: {url}")
print(f"请求参数：{json.dumps(payload, indent=2, ensure_ascii=False)}")

response = requests.post(url, headers=headers, json=payload)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    
    if result.get("code") == 0:
        print("\n" + "=" * 60)
        print("✓ 云文档创建成功！")
        print("=" * 60)
        
        document = result.get("data", {})
        print(f"\n文档信息:")
        print(f"  文档 ID: {document.get('document_id')}")
        print(f"  标题：{document.get('title')}")
        print(f"  创建者：{document.get('owner_id')}")
        
        # 获取文档 URL
        doc_id = document.get('document_id')
        if doc_id:
            doc_url = f"https://ecnhoqsc3a6t.feishu.cn/docx/{doc_id}"
            print(f"  文档 URL: {doc_url}")
            print(f"\n请在浏览器中打开以上 URL 查看文档")
        
        print("\n" + "=" * 60)
        print("权限配置成功！")
        print("=" * 60)
        
    else:
        print("\n✗ 云文档创建失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        
        if result.get("code") == 99991679:
            print("\n权限不足，可能需要重新授权")
            print("请运行：python reauth_get_token.py")
            
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
