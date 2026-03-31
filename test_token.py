import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 从配置中提取token
token = config["mcpServers"]["feishu-remote"]["headers"]["Authorization"].split(" ")[1]

# 测试token是否有效的API（使用获取当前认证信息的接口）
api_url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"

# 构建请求头
headers = {
    "Content-Type": "application/json"
}

# 构建请求体（使用app_id和app_secret直接获取新的token）
payload = {
    "app_id": "cli_a92fb9e90e799cb5",
    "app_secret": "2PQierezFvaasuwPIBhqxeXDp4ELSO4n"
}

# 发送请求
try:
    response = requests.post(api_url, json=payload, headers=headers)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    try:
        result = response.json()
        print(f"JSON解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("Token验证成功！")
        else:
            print("Token验证失败：")
            print(result.get("msg", "未知错误"))
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
except Exception as e:
    print(f"请求失败: {e}")
