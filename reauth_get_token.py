import requests
import json
import webbrowser
from urllib.parse import urlencode

# 读取配置文件获取应用信息
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 应用信息
app_id = "cli_a92fb9e90e799cb5"
app_secret = "2PQierezFvaasuwPIBhqxeXDp4ELSO4n"
redirect_uri = "https://open.feishu.cn/tool/redirect"

print("=" * 60)
print("重新获取 User Access Token（权限已更新）")
print("=" * 60)

print("\n说明：由于权限已更新，需要重新授权获取新的 User Access Token")

# 步骤一：构建授权 URL
print("\n步骤一：获取授权码 (code)")
print("\n请在浏览器中打开以下授权 URL：")

auth_url = "https://open.feishu.cn/open-apis/authen/v1/authorize"
params = {
    "app_id": app_id,
    "redirect_uri": redirect_uri,
    "state": "reauth_12345"
}

full_auth_url = f"{auth_url}?{urlencode(params)}"
print("\n" + full_auth_url + "\n")

print("操作步骤：")
print("1. 复制上面的 URL 并在浏览器中打开")
print("2. 使用飞书 App 扫码授权")
print("3. 授权成功后会跳转到重定向页面")
print("4. 页面会显示授权码 (code)")
print("5. 复制授权码")

# 询问是否自动打开浏览器
open_browser = input("\n是否自动打开浏览器？(y/n): ")
if open_browser.lower() == 'y':
    webbrowser.open(full_auth_url)
    print("已打开浏览器，请完成授权流程并复制授权码")

# 步骤二：输入授权码
print("\n" + "=" * 60)
print("步骤二：换取 user_access_token")
code = input("请输入授权码 (code): ").strip()

while not code:
    print("错误：授权码不能为空")
    code = input("请重新输入授权码 (code): ").strip()

# 使用授权码换取 user_access_token
print("\n正在换取 user_access_token...")

token_url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
headers = {
    "Content-Type": "application/json"
}

payload = {
    "grant_type": "authorization_code",
    "app_id": app_id,
    "app_secret": app_secret,
    "code": code
}

response = requests.post(token_url, headers=headers, json=payload)

print(f"\n响应状态码：{response.status_code}")

try:
    result = response.json()
    
    if result.get("code") == 0:
        print("\n✓ 获取 user_access_token 成功！")
        
        access_token = result.get('data', {}).get('access_token')
        refresh_token = result.get('data', {}).get('refresh_token')
        expires_in = result.get('data', {}).get('expires_in')
        
        print(f"\n========== User Access Token 信息 ==========")
        print(f"user_access_token: {access_token}")
        print(f"refresh_token: {refresh_token}")
        print(f"expires_in: {expires_in} 秒")
        print(f"==========================================")
        
        # 更新配置文件
        config["user_access_token"] = access_token
        config["refresh_token"] = refresh_token
        config["token_expires_in"] = expires_in
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ 配置已保存到 {config_path}")
        print("\n提示：新的 token 已保存，包含最新的权限")
        print("现在可以运行：python create_test_doc_final.py")
        
    else:
        print(f"\n✗ 获取 user_access_token 失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
