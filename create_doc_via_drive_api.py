import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 获取 User Access Token
user_access_token = config["user_access_token"]

print("=" * 60)
print("使用飞书 Drive API 直接创建云文档")
print("=" * 60)

print(f"\nUser Access Token: {user_access_token[:20]}...")

# 使用飞书 Drive API 创建文档
url = "https://open.feishu.cn/open-apis/drive/v1/files"
headers = {
    "Authorization": f"Bearer {user_access_token}",
    "Content-Type": "application/json"
}

# 创建文档的请求体
payload = {
    "obj_type": "docx",
    "parent_type": "folder",
    "parent_node": "root",
    "name": "测试云文档 - 直接 API 创建"
}

print(f"\n请求 URL: {url}")
print(f"请求参数：{json.dumps(payload, indent=2, ensure_ascii=False)}")

response = requests.post(url, headers=headers, json=payload)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    
    if result.get("code") == 0:
        print("\n✓ 云文档创建成功！")
        
        file = result.get("data", {}).get("file", {})
        print(f"\n文档信息:")
        print(f"  文件 ID: {file.get('obj_id')}")
        print(f"  文件类型：{file.get('obj_type')}")
        print(f"  文件名：{file.get('name')}")
        print(f"  创建者：{file.get('owner_id')}")
        
        # 尝试获取文档 URL
        obj_id = file.get('obj_id')
        if obj_id:
            doc_url = f"https://ecnhoqsc3a6t.feishu.cn/docx/{obj_id}"
            print(f"  文档 URL: {doc_url}")
    else:
        print("\n✗ 云文档创建失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        
        if result.get("code") == 99991679:
            print("\n权限不足，请检查：")
            print("1. 是否开通了 docx:document:create 权限")
            print("2. 权限类型是否为'用户身份'")
            print("3. 是否需要重新授权")
            
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
