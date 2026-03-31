import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 从配置中提取 token
tenant_access_token = config["mcpServers"]["feishu-remote"]["headers"]["Authorization"].split(" ")[1]

# 飞书开放平台 API URL
drive_api_url = "https://open.feishu.cn/open-apis/drive/v1/files"

# 需求文档 ID
doc_id = "EIWcd8E86oX8xDxWLBqcDzmZnQd"

# "俄罗斯方块"项目的 folder token（需要从项目 URL 中获取）
# 项目 URL: https://www.feishu.cn/wiki/ZkC1wi5EIiQNFmkOGzncmkUSnLf
# wiki space ID: 7418508651239784449
folder_token = "ZkC1wi5EIiQNFmkOGzncmkUSnLf"

print("尝试使用飞书 Drive API 移动文档...")
print(f"文档 ID: {doc_id}")
print(f"目标文件夹 token: {folder_token}")

# 构建请求头
headers = {
    "Authorization": f"Bearer {tenant_access_token}",
    "Content-Type": "application/json"
}

# 构建移动文档的请求体
payload = {
    "folder_token": folder_token
}

# 发送移动文档请求
move_url = f"{drive_api_url}/{doc_id}/move"
response = requests.post(move_url, headers=headers, json=payload)

print(f"\n移动文档响应状态码：{response.status_code}")
print(f"移动文档响应内容：{response.text}")

try:
    result = response.json()
    if result.get("code") == 0:
        print(f"\n文档移动成功！")
        print(f"文档 ID: {doc_id}")
        print(f"文档已移动到'俄罗斯方块'项目下")
        print(f"文档 URL: https://www.feishu.cn/docx/{doc_id}")
    else:
        print(f"\n文档移动失败")
        print(f"错误码：{result.get('code')}")
        print(f"错误信息：{result.get('msg')}")
        print(f"\n请尝试手动移动文档：")
        print(f"1. 打开文档：https://www.feishu.cn/docx/{doc_id}")
        print(f"2. 点击文档右上角的'...'按钮")
        print(f"3. 选择'移动'选项")
        print(f"4. 选择'KAKA 知识'知识库 > '俄罗斯方块'项目")
        print(f"5. 点击'确定'完成移动")
except json.JSONDecodeError as e:
    print(f"JSON 解析失败：{e}")
except Exception as e:
    print(f"处理响应失败：{e}")
