#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在飞书知识库【KAKA知识】根目录下创建【贪吃蛇】文档
并在该文档下创建【贪吃蛇需求文档】子文档
使用tenant_access_token
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

# 知识库配置
SPACE_ID = "7418508651239784449"  # KAKA知识知识库ID

print("\n" + "=" * 60)
print("在飞书知识库【KAKA知识】中创建【贪吃蛇】文档")
print("=" * 60)

headers = {
    "Authorization": f"Bearer {tenant_access_token}",
    "Content-Type": "application/json"
}

# 第二步：获取知识库根目录节点
print("\n【步骤1】获取知识库根目录节点...")
url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{SPACE_ID}/nodes"
params = {
    "parent_node_token": "",  # 空表示获取根目录节点
    "page_size": 50
}

response = requests.get(url, headers=headers, params=params)
result = response.json()

if result.get("code") != 0:
    print(f"✗ 获取知识库节点失败: {result.get('msg')}")
    sys.exit(1)

root_nodes = result.get("data", {}).get("items", [])
print(f"✓ 获取到 {len(root_nodes)} 个根目录节点")

# 查找根目录（origin类型）
root_node_token = None
for node in root_nodes:
    print(f"  节点: {node.get('title')} (类型: {node.get('node_type')}, Token: {node.get('node_token')})")
    if node.get("node_type") == "origin":
        root_node_token = node.get("node_token")

if not root_node_token and root_nodes:
    # 如果没有origin类型，使用第一个节点作为父节点
    root_node_token = root_nodes[0].get("node_token")
    print(f"  使用第一个节点作为父节点: {root_nodes[0].get('title')}")

print(f"  根节点Token: {root_node_token}")

# 第三步：创建【贪吃蛇】文档
print("\n【步骤2】创建【贪吃蛇】文档...")
doc_create_url = "https://open.feishu.cn/open-apis/drive/v1/files"
doc_payload = {
    "obj_type": "docx",
    "name": "贪吃蛇"
}

doc_response = requests.post(doc_create_url, headers=headers, json=doc_payload)
doc_result = doc_response.json()

if doc_result.get("code") != 0:
    print(f"✗ 创建文档失败: {doc_result.get('msg')}")
    print(f"  错误码: {doc_result.get('code')}")
    sys.exit(1)

file_info = doc_result.get("data", {}).get("file", {})
obj_token = file_info.get("obj_id")
print(f"✓ 文档创建成功!")
print(f"  文档ID: {obj_token}")
print(f"  文档名称: {file_info.get('name')}")

# 第四步：将文档添加到知识库根目录
print("\n【步骤3】将文档添加到知识库根目录...")
add_to_wiki_url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{SPACE_ID}/nodes"
add_payload = {
    "obj_type": "docx",
    "obj_token": obj_token,
    "parent_node_token": root_node_token if root_node_token else "",
    "node_type": "origin",
    "title": "贪吃蛇"
}

add_response = requests.post(add_to_wiki_url, headers=headers, json=add_payload)
add_result = add_response.json()

if add_result.get("code") != 0:
    print(f"✗ 添加到知识库失败: {add_result.get('msg')}")
    print(f"  错误码: {add_result.get('code')}")
    # 即使失败也继续，因为文档已经创建
    snake_node_token = None
else:
    snake_node = add_result.get("data", {}).get("node", {})
    snake_node_token = snake_node.get("node_token")
    print(f"✓ 成功添加到知识库!")
    print(f"  节点Token: {snake_node_token}")
    
    # 第五步：在【贪吃蛇】下创建【贪吃蛇需求文档】子文档
    print("\n【步骤4】创建【贪吃蛇需求文档】子文档...")
    
    # 先创建子文档
    child_doc_payload = {
        "obj_type": "docx",
        "name": "贪吃蛇需求文档"
    }
    child_doc_response = requests.post(doc_create_url, headers=headers, json=child_doc_payload)
    child_doc_result = child_doc_response.json()
    
    if child_doc_result.get("code") != 0:
        print(f"✗ 创建子文档失败: {child_doc_result.get('msg')}")
    else:
        child_file_info = child_doc_result.get("data", {}).get("file", {})
        child_obj_token = child_file_info.get("obj_id")
        print(f"✓ 子文档创建成功!")
        print(f"  文档ID: {child_obj_token}")
        
        # 将子文档添加到【贪吃蛇】下
        child_add_payload = {
            "obj_type": "docx",
            "obj_token": child_obj_token,
            "parent_node_token": snake_node_token,
            "node_type": "origin",
            "title": "贪吃蛇需求文档"
        }
        
        child_add_response = requests.post(add_to_wiki_url, headers=headers, json=child_add_payload)
        child_add_result = child_add_response.json()
        
        if child_add_result.get("code") != 0:
            print(f"✗ 添加子文档到知识库失败: {child_add_result.get('msg')}")
        else:
            print(f"✓ 子文档成功添加到【贪吃蛇】下!")
            child_node = child_add_result.get("data", {}).get("node", {})
            print(f"  子文档节点Token: {child_node.get('node_token')}")

print("\n" + "=" * 60)
print("文档创建完成!")
print("=" * 60)
print("\n文档结构:")
print("  📁 KAKA知识 (知识库)")
print("    📄 贪吃蛇 (文档)")
print("      📄 贪吃蛇需求文档 (子文档)")
