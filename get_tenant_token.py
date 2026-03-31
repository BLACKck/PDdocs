import requests
import json

# 飞书应用凭证
app_id = "cli_a92fb9e90e799cb5"
app_secret = "2PQierezFvaasuwPIBhqxeXDp4ELSO4n"

# 获取tenant_access_token的API
token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

# 构建请求体
payload = {
    "app_id": app_id,
    "app_secret": app_secret
}

# 发送请求
response = requests.post(token_url, json=payload)
result = response.json()

if result.get("code") == 0:
    tenant_access_token = result.get("tenant_access_token")
    print(f"获取tenant_access_token成功: {tenant_access_token}")
    
    # 更新mcp-config.json文件
    config_path = "mcp-config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    config["mcpServers"]["feishu-remote"]["headers"]["Authorization"] = f"Bearer {tenant_access_token}"
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("mcp-config.json文件已更新")
else:
    print(f"获取tenant_access_token失败: {result}")
