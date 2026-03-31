import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 从配置中提取token
token = config["mcpServers"]["feishu-remote"]["headers"]["Authorization"].split(" ")[1]

# MCP服务URL
mcp_url = "https://mcp.feishu.cn/mcp"

# 构建请求头
headers = {
    "X-Lark-MCP-TAT": token,
    "Content-Type": "application/json",
    "X-Lark-MCP-Allowed-Tools": "create-doc"
}

# "俄罗斯方块"项目的wiki_node ID
wiki_node = "ZkC1wi5EIiQNFmkOGzncmkUSnLf"

print("在'俄罗斯方块'项目下创建需求文档...")

# 俄罗斯方块需求文档内容
markdown_content = """## 1. 变更记录
| 版本 | 日期 | 变更人 | 变更内容 |
|------|------|--------|----------|
| v1.0 | 2026-03-26 | 系统 | 初始化需求文档 |
| v1.1 | 2026-03-26 | 系统 | 添加灰度模块 |

## 2. 文档概述
本文档描述了俄罗斯方块游戏的功能需求和技术实现方案，包括游戏核心功能、用户界面、游戏规则等内容。

## 3. 项目背景
俄罗斯方块是一款经典的休闲益智游戏，具有广泛的用户基础和市场需求。本项目旨在开发一款现代化的俄罗斯方块游戏，提供良好的用户体验和游戏性。

## 4. 业务场景
- **休闲娱乐**：用户在碎片化时间进行游戏，放松身心
- **挑战自我**：用户通过不断挑战提高自己的游戏水平和分数
- **社交分享**：用户可以分享自己的游戏成绩和成就
- **灰度测试**：通过灰度测试验证游戏功能和用户体验

## 5. 目标用户
- **休闲游戏玩家**：喜欢简单易上手的游戏
- **怀旧游戏爱好者**：对经典俄罗斯方块游戏有情感连接
- **各年龄段用户**：游戏规则简单，适合不同年龄段的用户
- **灰度测试用户**：参与游戏灰度测试的用户

## 6. 产品结构
```mermaid
graph TD
    A[俄罗斯方块游戏] --> B[游戏核心模块]
    A --> C[游戏控制模块]
    A --> D[数据管理模块]
    A --> E[用户界面模块]
    A --> F[灰度模块]
    B --> G[方块生成]
    B --> H[碰撞检测]
    B --> I[行消除]
    B --> J[分数计算]
    C --> K[键盘控制]
    C --> L[游戏状态控制]
    D --> M[分数记录]
    D --> N[最高分存储]
    E --> O[游戏区域]
    E --> P[信息面板]
    E --> Q[控制按钮]
    F --> R[灰度用户管理]
    F --> S[灰度权限控制]
    F --> T[灰度数据收集]
```

## 7. 流程图
```mermaid
flowchart TD
    A[开始游戏] --> B{是否灰度用户?}
    B -->|否| C[显示灰度提示