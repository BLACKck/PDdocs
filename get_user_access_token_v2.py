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
# 使用飞书官方工具的重定向 URI
redirect_uri = "https://open.feishu.cn/tool/redirect"

print("=" * 60)
print("获取 User Access Token - OAuth 流程")
print("=" * 60)

print("\n重要提示：")
print("请先在飞书开放平台配置重定向 URI：")
print(f"  {redirect_uri}")
print("\n配置步骤：")
print("1. 访问 https://open.feishu.cn/")
print("2. 登录并进入应用管理")
print("3. 选择应用（俄罗斯方块）")
print("4. 点击'开发配置'")
print("5. 找到'重定向 URI'并添加上述 URI")
print("6. 保存配置并等待 1-2 分钟生效")

print("\n" + "=" * 60)
input("\n确认已配置重定向 URI 后，按回车继续...")

# 步骤一：构建授权 URL
print("\n步骤一：获取授权码 (code)")
print("\n请在浏览器中打开以下授权 URL：")

auth_url = "https://open.feishu.cn/open-apis/authen/v1/authorize"
params = {
    "app_id": app_id,
    "redirect_uri": redirect_uri,
    "state": "random_state_12345"
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

token_url = "https://open.feishu.cn/open-apis/authen/v1/oauth/token"
headers = {
    "Content-Type": "application/json"
}

payload = {
    "grant_type": "authorization_code",
    "client_id": app_id,
    "client_secret": app_secret,
    "code": code
}

response = requests.post(token_url, headers=headers, json=payload)

print(f"\n响应状态码：{response.status_code}")

try:
    result = response.json()
    print(f"响应内容：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if result.get("code") == 0:
        print("\n✓ 获取 user_access_token 成功！")
        
        access_token = result.get('data', {}).get('access_token')
        refresh_token = result.get('data', {}).get('refresh_token')
        expires_in = result.get('data', {}).get('expires_in')
        token_type = result.get('data', {}).get('token_type')
        
        print(f"\nuser_access_token: {access_token}")
        print(f"refresh_token: {refresh_token}")
        print(f"expires_in: {expires_in} 秒")
        print(f"token_type: {token_type}")
        
        # 询问是否保存到配置文件
        save_config = input("\n是否将 user_access_token 保存到配置文件？(y/n): ")
        if save_config.lower() == 'y':
            # 更新配置文件
            config["user_access_token"] = access_token
            config["refresh_token"] = refresh_token
            config["token_expires_in"] = expires_in
            
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ 配置已保存到 {config_path}")
            print("\n提示：user_access_token 有有效期限制，过期后需要使用 refresh_token 刷新")
        else:
            print("\n请自行保存 user_access_token，后续使用时需要用到")
            
    elif result.get("code") == 20029:
        print(f"\n✗ 错误：重定向 URI 配置不正确")
        print("错误码：20029")
        print("错误信息：redirect_uri 校验失败")
        print("\n解决方案：")
        print("1. 访问飞书开放平台：https://open.feishu.cn/")
        print("2. 进入应用管理 > 选择您的应用")
        print("3. 点击'开发配置'")
        print("4. 找到'重定向 URI'配置")
        print(f"5. 添加重定向 URI: {redirect_uri}")
        print("6. 保存配置并等待 1-2 分钟生效")
        print("7. 重新运行本脚本")
        
    elif result.get("code") == 20002:
        print(f"\n✗ 错误：授权码无效或已过期")
        print("错误码：20002")
        print("错误信息：invalid authorization code")
        print("\n解决方案：")
        print("1. 授权码只能使用一次，且在 5 分钟内有效")
        print("2. 请重新运行脚本获取新的授权码")
        
    else:
        print(f"\n✗ 获取 user_access_token 失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
    print(f"原始响应：{response.text}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
