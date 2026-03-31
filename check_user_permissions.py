import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 获取 User Access Token
user_access_token = config["user_access_token"]

print("=" * 60)
print("检查当前用户权限")
print("=" * 60)

print(f"\nUser Access Token: {user_access_token[:20]}...")

# 使用飞书 API 检查当前用户信息
url = "https://open.feishu.cn/open-apis/authen/v1/user_info"
headers = {
    "Authorization": f"Bearer {user_access_token}",
    "Content-Type": "application/json"
}

print(f"\n请求 URL: {url}")

response = requests.get(url, headers=headers)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    
    if result.get("code") == 0:
        print("\n✓ 用户信息获取成功！")
        
        user_data = result.get("data", {})
        print(f"\n用户信息:")
        print(f"  姓名：{user_data.get('name')}")
        print(f"  英文名：{user_data.get('en_name')}")
        print(f"  用户 ID: {user_data.get('user_id')}")
        print(f"  Open ID: {user_data.get('open_id')}")
        print(f"  Union ID: {user_data.get('union_id')}")
        print(f"  手机号：{user_data.get('mobile')}")
        print(f"  Token 过期时间：{user_data.get('expires_in')} 秒")
        
        print("\n✓ User Access Token 有效")
        print("\n权限问题排查：")
        print("1. 确认在飞书开放平台开通的权限是'用户身份'类型")
        print("2. 确认权限名称是'docx:document'和'docx:document:create'")
        print("3. 确认权限已经审核通过（不是审核中状态）")
        print("4. 尝试在飞书开放平台重新授权应用")
    else:
        print("\n✗ 用户信息获取失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
