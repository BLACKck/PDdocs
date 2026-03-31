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
    "X-Lark-MCP-Allowed-Tools": "search-doc,create-doc"
}

# 步骤1: 搜索"KAKA知识"知识库
def search_kaka_knowledge():
    print("步骤1: 搜索'KAKA知识'知识库...")
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "search-doc",
            "arguments": {
                "query": "KAKA知识",
                "filters": {
                    "sort_rule": "CREATE_TIME"
                }
            }
        }
    }
    
    response = requests.post(mcp_url, headers=headers, json=payload)
    print(f"响应状态码: {response.status_code}")
    
    try:
        result = response.json()
        print("搜索成功！")
        if result.get("result") and result["result"].get("content"):
            content = result["result"]["content"][0]["text"]
            content_json = json.loads(content)
            print(f"搜索结果: {json.dumps(content_json, indent=2, ensure_ascii=False)}")
            return content_json
        else:
            print("未找到'KAKA知识'知识库")
            return None
    except Exception as e:
        print(f"处理响应失败: {e}")
        return None

# 步骤2: 在知识库下创建"俄罗斯方块"项目
def create_tetris_project(wiki_space_id):
    print(f"\n步骤2: 在知识库下创建'俄罗斯方块'项目 (space_id: {wiki_space_id})...")
    markdown_content = "# 俄罗斯方块项目\n\n本项目包含俄罗斯方块游戏的相关文档和资源。"
    
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "create-doc",
            "arguments": {
                "title": "俄罗斯方块",
                "markdown": markdown_content,
                "wiki_space": str(wiki_space_id)
            }
        }
    }
    
    response = requests.post(mcp_url, headers=headers, json=payload)
    print(f"响应状态码: {response.status_code}")
    
    try:
        result = response.json()
        print("项目创建成功！")
        if result.get("result") and result["result"].get("content"):
            content = result["result"]["content"][0]["text"]
            content_json = json.loads(content)
            print(f"项目信息: {json.dumps(content_json, indent=2, ensure_ascii=False)}")
            return content_json
        else:
            print("项目创建失败")
            return None
    except Exception as e:
        print(f"处理响应失败: {e}")
        return None

# 主函数
def main():
    # 在"KAKA知识"知识库下创建俄罗斯方块项目
    wiki_space_id = 7418508651239784449
    print(f"在'KAKA知识'知识库下创建'俄罗斯方块'项目 (space_id: {wiki_space_id})...")
    
    project_result = create_tetris_project(wiki_space_id)
    
    if project_result:
        print("\n操作完成！")
        print(f"'俄罗斯方块'项目已创建在'KAKA知识'知识库下")
        print(f"项目URL: {project_result.get('doc_url')}")
    else:
        print("创建项目失败")

if __name__ == "__main__":
    main()
