import requests
import json

# 读取配置文件获取访问凭证
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 从配置中提取token
token = config["mcpServers"]["feishu-remote"]["headers"]["Authorization"].split(" ")[1]

# 正确的MCP服务URL
mcp_url = "https://mcp.feishu.cn/mcp"

# 构建请求头
headers = {
    "X-Lark-MCP-TAT": token,
    "Content-Type": "application/json",
    "X-Lark-MCP-Allowed-Tools": "get-user,create-doc,search-doc"
}

# 1. 初始化连接
def initialize_connection():
    print("=== 1. 初始化连接 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize"
    }
    
    try:
        response = requests.post(mcp_url, json=payload, headers=headers)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        try:
            result = response.json()
            print(f"JSON解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 2. 列出可用工具
def list_tools():
    print("\n=== 2. 列出可用工具 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    
    try:
        response = requests.post(mcp_url, json=payload, headers=headers)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        try:
            result = response.json()
            print(f"JSON解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 3. 调用create-doc工具
def call_create_doc():
    print("\n=== 3. 调用create-doc工具 ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "create-doc",
            "arguments": {
                "title": "测试云文档",
                "content": "这是一个测试云文档，通过MCP服务创建。"
            }
        }
    }
    
    try:
        response = requests.post(mcp_url, json=payload, headers=headers)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        try:
            result = response.json()
            print(f"JSON解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 执行测试
if __name__ == "__main__":
    # 1. 初始化连接
    initialize_result = initialize_connection()
    
    if initialize_result and initialize_result.get("result"):
        # 2. 列出可用工具
        list_tools_result = list_tools()
        
        if list_tools_result and list_tools_result.get("result"):
            # 3. 调用create-doc工具
            call_create_doc_result = call_create_doc()
