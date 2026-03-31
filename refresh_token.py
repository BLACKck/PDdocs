import requests
import json

# 读取配置文件获取应用信息
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 应用信息
app_id = "cli_a92fb9e90e799cb5"
app_secret = "2PQierezFvaasuwPIBhqxeXDp4ELSO4n"

# 使用 refresh_token 刷新 access_token
refresh_token = config.get("refresh_token")

if not refresh_token:
    print("错误：配置文件中没有找到 refresh_token")
    print("需要重新进行 OAuth 授权流程")
    exit(1)

print("=" * 60)
print("使用 refresh_token 刷新 user_access_token")
print("=" * 60)

print(f"\nRefresh Token: {refresh_token[:20]}...")

# 使用 refresh_token 获取新的 access_token
token_url = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"
headers = {
    "Content-Type": "application/json"
}

payload = {
    "grant_type": "refresh_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "refresh_token": refresh_token
}

print(f"\n请求 URL: {token_url}")
print(f"请求参数：")
print(f"  grant_type: refresh_token")
print(f"  client_id: {app_id}")
print(f"  refresh_token: {refresh_token[:20]}...")

response = requests.post(token_url, headers=headers, json=payload)

print(f"\n响应状态码：{response.status_code}")
print(f"响应内容：{response.text}")

try:
    result = response.json()
    
    if result.get("code") == 0:
        print("\n✓ 刷新 token 成功！")
        
        access_token = result.get('data', {}).get('access_token')
        new_refresh_token = result.get('data', {}).get('refresh_token')
        expires_in = result.get('data', {}).get('expires_in')
        
        print(f"\n========== 新的 User Access Token 信息 ==========")
        print(f"user_access_token: {access_token}")
        print(f"refresh_token: {new_refresh_token}")
        print(f"expires_in: {expires_in} 秒")
        print(f"==============================================")
        
        # 更新配置文件
        config["user_access_token"] = access_token
        if new_refresh_token:
            config["refresh_token"] = new_refresh_token
        config["token_expires_in"] = expires_in
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ 配置已更新到 {config_path}")
        print("\n提示：新的 token 已保存，现在可以重新测试创建文档")
        
    else:
        print(f"\n✗ 刷新 token 失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        print("\n解决方案：")
        print("1. refresh_token 可能已过期")
        print("2. 需要重新进行 OAuth 授权流程")
        print("3. 运行：python get_user_access_token_v2.py")
        
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")

print("\n" + "=" * 60)
