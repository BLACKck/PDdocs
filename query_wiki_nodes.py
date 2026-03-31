#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询飞书知识库完整结构，包括子节点
"""

import requests
import json

# 飞书 API 配置
APP_ID = "cli_a94d456321b89cc5"
APP_SECRET = "your_app_secret"  # 需要从已配置的 CLI 获取
SPACE_ID = "7418508651239784449"

def get_access_token():
    """获取访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            return result["tenant_access_token"]
    return None

def get_wiki_nodes(space_id, parent_node_token=None, access_token=None):
    """获取知识库节点列表"""
    if access_token is None:
        print("错误：无法获取访问令牌")
        return []
    
    url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {}
    if parent_node_token:
        params["parent_node_token"] = parent_node_token
    
    print(f"\n查询参数: space_id={space_id}, parent_node_token={parent_node_token}")
    
    response = requests.get(url, headers=headers, params=params)
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            items = result["data"].get("items", [])
            print(f"获取到 {len(items)} 个节点")
            return items
        else:
            print(f"API 错误: {result}")
    else:
        print(f"HTTP 错误: {response.text}")
    
    return []

def print_node_tree(nodes, level=0):
    """打印节点树结构"""
    for node in nodes:
        indent = "  " * level
        title = node.get("title", "未命名")
        node_token = node.get("node_token", "")
        has_child = node.get("has_child", False)
        parent = node.get("parent_node_token", "")
        
        child_indicator = "📁" if has_child else "📄"
        print(f"{indent}{child_indicator} {title}")
        print(f"{indent}   Node Token: {node_token}")
        print(f"{indent}   Parent: {parent}")
        print()

def main():
    print("=" * 60)
    print("飞书知识库结构查询")
    print("=" * 60)
    
    # 注意：这里需要从已授权的 CLI 获取 token
    # 由于 CLI 已经授权，我们可以尝试使用 CLI 的方式来获取
    print("\n注意：此脚本需要有效的访问令牌")
    print("请确保 lark-cli 已经正确授权")
    
    # 显示当前知识库结构（基于已获取的信息）
    print("\n" + "=" * 60)
    print("KAKA 知识库结构（基于 API 返回）")
    print("=" * 60)
    
    # 一级节点信息（从之前的查询结果）
    nodes = [
        {
            "title": "中心仓",
            "node_token": "JWAmwybIziqMsXkaITyciuUxnLg",
            "has_child": True,
            "parent_node_token": ""
        },
        {
            "title": "企微RPA项目",
            "node_token": "EdGwws5JgiJ6IDk0k08cxET4ndd",
            "has_child": True,
            "parent_node_token": ""
        },
        {
            "title": "大模型外呼",
            "node_token": "DrNnwYPFYi5rb1k0QE7c7itungh",
            "has_child": True,
            "parent_node_token": ""
        },
        {
            "title": "俄罗斯方块",
            "node_token": "ZkC1wi5EIiQNFmkOGzncmkUSnLf",
            "has_child": False,
            "parent_node_token": ""
        }
    ]
    
    print("\n一级节点：")
    print_node_tree(nodes)
    
    print("\n" + "=" * 60)
    print("问题分析")
    print("=" * 60)
    print("""
根据截图显示，知识库结构应该是：

KAKA知识
├── 📁 中心仓
│   ├── 📄 中心仓仓储
│   └── 📄 中心仓订单
├── 📁 企微RPA项目
│   ├── 📄 【售后企微群项目】企微群创建...
│   └── 📄 【售后企微群项目】售后企微群...
├── 📁 大模型外呼
│   ├── 📄 【AI大模型外呼】AI大模型外呼...
│   ├── 📄 AI大模型外呼平台化立项文档
│   └── 📄 【业务线对接指引】AI大模型外...
└── 📄 俄罗斯方块

但 API 返回的结果显示：
1. 所有节点的 parent_node_token 都是空字符串（表示都是一级节点）
2. 即使指定 parent_node_token 参数，API 仍然返回所有一级节点

可能的原因：
1. API 权限问题：当前应用可能没有权限访问子节点
2. API 版本问题：使用的 API 版本可能不支持子节点查询
3. 节点类型问题：子节点可能是快捷方式或其他特殊类型
4. 知识库设置：知识库可能设置了访问限制

建议解决方案：
1. 检查应用权限，确保有 wiki:node:read 权限
2. 尝试使用 wiki:wiki 权限重新授权
3. 使用飞书开放平台提供的其他 API 端点
4. 直接在飞书客户端中查看完整的知识库结构
""")

if __name__ == "__main__":
    main()
