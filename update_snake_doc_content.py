#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用飞书API更新【贪吃蛇需求文档】的内容
"""

import requests
import json
import sys

# 飞书应用凭证
app_id = "cli_a92fb9e90e799cb5"
app_secret = "2PQierezFvaasuwPIBhqxeXDp4ELSO4n"

# 第一步：获取tenant_access_token
print("=" * 60)
print("获取 tenant_access_token")
print("=" * 60)

token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
payload = {
    "app_id": app_id,
    "app_secret": app_secret
}

response = requests.post(token_url, json=payload)
result = response.json()

if result.get("code") != 0:
    print(f"✗ 获取tenant_access_token失败: {result}")
    sys.exit(1)

tenant_access_token = result.get("tenant_access_token")
print(f"✓ 获取tenant_access_token成功: {tenant_access_token[:20]}...")

# 读取需求文档内容
doc_path = "d:\\PDM\\PDdocs\\贪吃蛇\\需求管理\\需求文档主文档\\需求文档.md"
try:
    with open(doc_path, "r", encoding="utf-8") as f:
        doc_content = f.read()
    print(f"✓ 成功读取需求文档，共 {len(doc_content)} 字符")
except Exception as e:
    print(f"✗ 读取需求文档失败: {e}")
    sys.exit(1)

# 子文档的document_id
# 从之前的创建脚本中获取的文档ID
child_document_id = "doxcnM5GGwGPLAimzP2kncJncp4SYnVg"

print("\n" + "=" * 60)
print("更新飞书文档内容")
print("=" * 60)

# 使用文档API更新内容
headers = {
    "Authorization": f"Bearer {tenant_access_token}",
    "Content-Type": "application/json"
}

# 构建更新内容的请求体
# 注意：飞书文档API需要使用特定的