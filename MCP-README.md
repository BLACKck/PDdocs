# 飞书 MCP 远程服务配置指南

## 配置说明

根据飞书开放平台文档，本项目已配置为使用远程 MCP 服务。以下是配置和使用步骤：

### 1. 准备工作

1. **创建自建应用**：在 [飞书开放平台](https://open.feishu.cn/) 创建一个自建应用
2. **申请权限**：根据需要使用的工具，为应用申请对应的 API 权限
3. **获取访问凭证**：
   - User Access Token (UAT)：代表用户身份的凭证
   - Tenant Access Token (TAT)：代表应用身份的凭证

### 2. 配置文件

配置文件路径：`mcp-config.json`

当前配置：
```json
{
  "mcpServers": {
    "feishu-remote": {
      "url": "https://open.feishu.cn/open-apis/mcp/v1/tools",
      "headers": {
        "Authorization": "Bearer YOUR_TENANT_ACCESS_TOKEN"
      }
    }
  }
}
```

### 3. 替换访问凭证

将 `YOUR_TENANT_ACCESS_TOKEN` 替换为实际的 Tenant Access Token 或 User Access Token。

### 4. 所需权限

根据使用的工具，需要申请以下权限：

#### 通用工具
- `search-user`：需要 `contact:user:search` 权限（仅支持 UAT）
- `get-user`：需要 `contact:contact.base:readonly` 和 `contact:user.base:readonly` 权限
- `fetch-file`：需要 `docs:document.media:download` 和 `board:whiteboard:node:read` 权限

#### 云文档工具
- `search-doc`：需要 `search:docs:read` 和 `wiki:wiki:readonly` 权限
- `create-doc`：需要 `docx:document:create`、`wiki:node:read`、`wiki:node:create`、`docs:document.media:upload`、`board:whiteboard:node:create`、`docx:document:write_only`、`docx:document:readonly` 权限
- `fetch-doc`：需要相应的文档访问权限

### 5. 使用方法

根据飞书 MCP 文档，通过以下步骤调用远程 MCP 服务：

1. 构建请求体，包含工具名称和参数
2. 发送 POST 请求到配置的 URL
3. 处理响应结果

### 6. 注意事项

- MCP 工具入参、出参格式可能灵活调整，调用时请勿依赖入参和出参的结构定义
- 如涉及多个权限，请全部申请
- 根据调用身份（UAT 或 TAT），参考申请 API 权限完成开通

## 参考文档

- [开发者调用远程 MCP 服务](https://open.feishu.cn/document/mcp_open_tools/developers-call-remote-mcp-server)
- [申请 API 权限](https://open.feishu.cn/document/server-docs/authentication-management/permission/permission-application-process)
- [获取 user_access_token](https://open.feishu.cn/document/server-docs/authentication-management/access-token/obtain-user-token)
- [获取 tenant_access_token](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant-access-token)
