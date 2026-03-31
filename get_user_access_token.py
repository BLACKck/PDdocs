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
redirect_uri = "https://www.feishu.cn"  # 飞书默认回调地址

print("=" * 60)
print("获取 User Access Token 流程")
print("=" * 60)

# 步骤一：构建授权 URL
print("\n步骤一：获取授权码 (code)")
print("\n请在浏览器中打开以下授权 URL：")

# 使用正确的飞书 OAuth 授权 URL
auth_url = "https://open.feishu.cn/open-apis/authen/v1/authorize"
params = {
    "app_id": app_id,
    "redirect_uri": redirect_uri,
    "state": "random_state_string"
}

full_auth_url = f"{auth_url}?{urlencode(params)}"
print(full_auth_url)

print("\n操作步骤：")
print("1. 复制上面的 URL 并在浏览器中打开")
print("2. 使用飞书账号登录并授权")
print("3. 授权成功后会跳转到回调页面")
print("4. 从回调 URL 中复制 code 参数值")

# 询问是否自动打开浏览器
open_browser = input("\n是否自动打开浏览器？(y/n): ")
if open_browser.lower() == 'y':
    webbrowser.open(full_auth_url)
    print("已打开浏览器，请完成授权流程")

# 步骤二：输入授权码
print("\n" + "=" * 60)
print("步骤二：换取 user_access_token")
code = input("请输入授权码 (code): ").strip()

if not code:
    print("错误：授权码不能为空")
    exit(1)

# 使用授权码换取 user_access_token
print("\n正在换取 user_access_token...")

# 尝试不同的 API 端点
token_endpoints = [
    "https://open.feishu.cn/open-apis/authen/v1/oauth/token",
    "https://open.feishu.cn/open-apis/authen/v2/oauth/token",
]

headers = {
    "Content-Type": "application/json"
}

payload = {
    "grant_type": "authorization_code",
    "client_id": app_id,
    "client_secret": app_secret,
    "code": code
}

success = False
for endpoint in token_endpoints:
    print(f"\n尝试端点：{endpoint}")
    response = requests.post(endpoint, headers=headers, json=payload)
    
    print(f"响应状态码：{response.status_code}")
    print(f"响应内容：{response.text}")
    
    try:
        result = response.json()
        if result.get("code") == 0:
            print("\n✓ 获取 user_access_token 成功！")
            print(f"\nuser_access_token: {result.get('data', {}).get('access_token')}")
            print(f"refresh_token: {result.get('data', {}).get('refresh_token')}")
            print(f"expires_in: {result.get('data', {}).get('expires_in')} 秒")
            print(f"token_type: {result.get('data', {}).get('token_type')}")
            
            # 询问是否保存到配置文件
            save_config = input("\n是否将 user_access_token 保存到配置文件？(y/n): ")
            if save_config.lower() == 'y':
                # 更新配置文件
                config["user_access_token"] = result.get('data', {}).get('access_token')
                config["refresh_token"] = result.get('data', {}).get('refresh_token')
                
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                print(f"✓ 配置已保存到 {config_path}")
            
            success = True
            break
        else:
            print(f"\n✗ 获取 user_access_token 失败")
            print(f"错误码：{result.get('code')}")
            print(f"错误信息：{result.get('msg')}")
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}")
    except Exception as e:
        print(f"处理响应失败：{e}")

if not success:
    print("\n所有端点都尝试失败，请检查：")
    print("1. 授权码是否有效")
    print("2. App ID 和 App Secret 是否正确")
    print("3. 应用是否配置了正确的重定向 URI")

print("\n" + "=" * 60)
