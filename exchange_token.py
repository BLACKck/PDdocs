import requests
import json

# 读取配置文件获取应用信息
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 应用信息
app_id = "cli_a92fb9e90e799cb5"
app_secret = "2PQierezFvaasuwPIBhqxeXDp4ELSO4n"

# 从 URL 中获取的授权码
code = "cDKrLcbDxLdf4x2EaB73dz8FJ40aDG6a"

print("=" * 60)
print("正在换取 user_access_token...")
print("=" * 60)

print(f"\n授权码：{code}")
print(f"App ID: {app_id}")

# 使用正确的 API 端点和参数
token_url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
headers = {
    "Content-Type": "application/json"
}

# 使用正确的参数名称
payload = {
    "grant_type": "authorization_code",
    "app_id": app_id,
    "app_secret": app_secret,
    "code": code
}

print(f"\n请求 URL: {token_url}")
print(f"请求参数：{json.dumps(payload, indent=2, ensure_ascii=False)}")

response = requests.post(token_url, headers=headers, json=payload)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    
    if result.get("code") == 0:
        print("\n✓ 获取 user_access_token 成功！")
        
        access_token = result.get('data', {}).get('access_token')
        refresh_token = result.get('data', {}).get('refresh_token')
        expires_in = result.get('data', {}).get('expires_in')
        token_type = result.get('data', {}).get('token_type')
        
        print(f"\n========== User Access Token 信息 ==========")
        print(f"user_access_token: {access_token}")
        print(f"refresh_token: {refresh_token}")
        print(f"expires_in: {expires_in} 秒")
        print(f"token_type: {token_type}")
        print(f"==========================================")
        
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
            
    else:
        print(f"\n✗ 获取 user_access_token 失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        
        if result.get("code") == 20025:
            print("\n解决方案：")
            print("请检查 App ID 和 App Secret 是否正确")
            print("确认应用已开通网页应用类型")
            
        elif result.get("code") == 20002:
            print("\n解决方案：")
            print("授权码已失效，请重新获取授权码")
            
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
