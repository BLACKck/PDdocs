# 飞书 CLI (larksuite/cli) 安装与使用指南

## 文档信息
- **创建日期**: 2026-03-29
- **适用范围**: 飞书知识库查询、文档管理
- **CLI 版本**: 1.0.0

## 重要原则

### ⚠️ 文档协作人管理原则（首要原则）

**所有使用 tenant_access_token 创建的文档，在文档创建完成后均需要将用户 BLACK（User ID: ou_7ef0e95e4659569a31e4c61dc3568630）添加为协作人并给予文档【可管理】权限。**

**原因**：
- tenant_access_token 是应用级别的访问令牌，创建的文档默认属于应用，而不是用户
- 如果不将 BLACK 用户添加为协作人，BLACK 用户将无法管理这些文档
- 给予【可管理】权限确保 BLACK 用户可以完全控制文档的后续操作

**操作步骤**：
1. 使用 tenant_access_token 创建文档
2. 获取文档的 token（doc_id）
3. 将 BLACK 用户添加为协作人，角色设置为 `full_access`（可管理）
4. 验证 BLACK 用户是否成功添加为协作人

**示例**：
```bash
# 步骤 1: 使用 tenant_access_token 创建文档
lark-cli docs +create \
  --title "文档标题" \
  --wiki-node "{parent_node_token}" \
  --markdown "# 文档内容"

# 步骤 2: 将 BLACK 用户添加为协作人
lark-cli api POST "/open-apis/drive/v1/permissions/batch_create" \
  --data '{"type":"docx","token":"{document_token}","members":[{"member_type":"user","member_id":"ou_7ef0e95e4659569a31e4c61dc3568630","role":"full_access"}]}'
```

**注意事项**：
- 此原则适用于所有使用 tenant_access_token 创建的文档
- 必须在文档创建后立即执行，避免权限问题
- 如果文档创建失败，不需要执行此步骤
- 后续所有使用飞书CLI能力的操作，均需要遵循这一首要原则

---

## 修订记录

| 版本 | 修订日期 | 修订内容 | 修订人 |
|------|---------|----------|--------|
| 1.3 | 2026-03-29 | 添加文档协作人管理原则（首要原则） | BLACK |
| 1.2 | 2026-03-29 | 添加账号信息管理章节 | BLACK |
| 1.1 | 2026-03-29 | 添加删除重复文档的问题与解决方案 | BLACK |
| 1.0 | 2026-03-29 | 初始版本，包含安装、配置、查询、创建文档等基础操作 | BLACK |

---

## 一、安装步骤

### 1.1 环境要求
- Node.js (推荐 v18+)
- npm 或 npx

### 1.2 安装 CLI 工具

```bash
# 安装飞书 CLI
npm install -g @larksuite/cli

# 验证安装
lark-cli --version
```

**预期输出**:
```
lark-cli version 1.0.0
```

### 1.3 安装 CLI SKILL（可选）

```bash
# 安装 CLI SKILL（用于 AI Agent 集成）
npx skills add larksuite/cli -y -g
```

> **注意**: 如果遇到克隆超时问题，可以跳过此步骤。核心 CLI 功能已经可以正常使用。

---

## 二、配置与授权

### 2.1 初始化应用配置

```bash
# 初始化应用配置（首次使用）
lark-cli config init
```

**执行过程**:
1. CLI 会输出一个授权链接
2. 在浏览器中打开链接完成配置
3. 等待配置完成

**预期输出**:
```
打开以下链接配置应用:

  https://open.feishu.cn/page/cli?user_code=XXXX-XXXX&lpv=1.0.0&ocv=1.0.0&from=cli

等待配置应用...

OK: 应用配置成功! App ID: cli_xxxxxxxxxxxxxxxx
```

### 2.2 登录授权

```bash
# 推荐方式：使用常用权限自动授权
lark-cli auth login --recommend
```

**执行过程**:
1. CLI 会输出一个授权链接和用户码
2. 在浏览器中打开链接
3. 输入用户码并完成授权
4. 等待授权完成

**预期输出**:
```
在浏览器中打开以下链接进行认证:

  https://accounts.feishu.cn/oauth/v1/device/verify?flow_id=xxxxx&user_code=XXXX-XXXX

等待用户授权...
[lark-cli] device-flow: token obtained successfully
授权成功，正在获取用户信息...

OK: 登录成功! 用户: BLACK (ou_xxxxxxxxxxxxxxxx)
  已授权 scopes: auth:user.id:read base:app:copy ... (大量权限)
```

### 2.3 添加特定权限

如果某些功能提示缺少权限，可以单独添加：

```bash
# 添加搜索权限
lark-cli auth login --scope "search:docs:read"

# 添加多个权限
lark-cli auth login --scope "search:docs:read wiki:wiki:readonly"
```

### 2.4 验证授权状态

```bash
# 查看当前授权状态
lark-cli auth status

# 查看所有已授权的权限
lark-cli auth scopes
```

### 2.5 账号信息管理

根据不同的操作需求，可能需要使用不同的应用或用户身份来执行。以下是当前可用的账号信息：

#### 应用账号信息

| 应用名称 | APP ID | APP Secret | 用途 |
|---------|---------|------------|------|
| 应用 1 | cli_a94d456321b89cc5 | VqIdqBeLyM2sw6MT2Rh1xeH17EcQR2KV | 通用操作、文档查询、创建文档 |
| 应用 2 | cli_a92fb9e90e799cb5 | 2PQierezFvaasuwPIBhqxeXDp4ELSO4n | 特殊权限操作、API 调用 |

#### 用户信息

| 用户名称 | User ID | 说明 |
|---------|----------|------|
| BLACK | ou_7ef0e95e4659569a31e4c61dc3568630 | 主要操作用户 |

#### 使用场景说明

1. **应用 1（cli_a94d456321b89cc5）**：
   - 适用于常规的文档查询、创建、更新操作
   - 使用 `lark-cli auth login --recommend` 授权时默认使用此应用
   - 适用于用户级别的操作

2. **应用 2（cli_a92fb9e90e799cb5）**：
   - 适用于需要特殊权限的操作
   - 使用 `lark-cli api` 命令时可能需要此应用的 tenant_access_token
   - 适用于应用级别的操作

3. **用户身份（BLACK）**：
   - 适用于需要用户权限的操作
   - 使用 `lark-cli api` 命令时默认使用用户身份
   - 适用于文档创建、更新、删除等操作

#### 切换应用账号

```bash
# 切换到应用 1
lark-cli config set app_id cli_a94d456321b89cc5
lark-cli config set app_secret VqIdqBeLyM2sw6MT2Rh1xeH17EcQR2KV

# 切换到应用 2
lark-cli config set app_id cli_a92fb9e90e799cb5
lark-cli config set app_secret 2PQierezFvaasuwPIBhqxeXDp4ELSO4n

# 查看当前配置
lark-cli config show
```

#### 获取 tenant_access_token

```bash
# 使用应用 1 获取 tenant_access_token
lark-cli api POST /open-apis/auth/v3/tenant_access_token/internal --data '{"app_id":"cli_a94d456321b89cc5","app_secret":"VqIdqBeLyM2sw6MT2Rh1xeH17EcQR2KV"}'

# 使用应用 2 获取 tenant_access_token
lark-cli api POST /open-apis/auth/v3/tenant_access_token/internal --data '{"app_id":"cli_a92fb9e90e799cb5","app_secret":"2PQierezFvaasuwPIBhqxeXDp4ELSO4n"}'
```

#### 使用不同的身份执行 API 调用

```bash
# 使用用户身份
lark-cli api GET /open-apis/wiki/v2/spaces

# 使用应用身份
lark-cli api GET /open-apis/wiki/v2/spaces --as app

# 使用特定应用的身份
lark-cli api GET /open-apis/wiki/v2/spaces --app-id cli_a92fb9e90e799cb5
```

---

## 三、知识库查询操作

### 3.1 查询知识库空间列表

```bash
# 获取所有知识库空间
lark-cli api GET /open-apis/wiki/v2/spaces
```

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "has_more": false,
    "items": [
      {
        "name": "KAKA知识",
        "space_id": "7418508651239784449",
        "space_type": "team",
        "visibility": "public"
      }
    ]
  }
}
```

### 3.2 查询知识库节点

```bash
# 获取知识库的一级节点
lark-cli api GET "/open-apis/wiki/v2/spaces/{space_id}/nodes"

# 示例
lark-cli api GET "/open-apis/wiki/v2/spaces/7418508651239784449/nodes"
```

### 3.3 使用搜索功能查询文档（推荐）

由于 Wiki API 的 `parent_node_token` 参数可能无法正确过滤子节点，**推荐使用搜索功能**来查找所有文档：

```bash
# 搜索特定关键词的文档
lark-cli docs +search --query "关键词" --page-size 20

# 示例：搜索"中心仓"相关文档
lark-cli docs +search --query "中心仓" --page-size 20

# 示例：搜索"企微RPA"相关文档
lark-cli docs +search --query "企微RPA" --page-size 20
```

**返回示例**:
```json
{
  "ok": true,
  "data": {
    "has_more": false,
    "results": [
      {
        "entity_type": "WIKI",
        "result_meta": {
          "token": "YSIEwzlV9iNTHHkzOeFcf0jWnIh",
          "title_highlighted": "【售后企微群项目】企微群创建、分配及消息发送",
          "url": "https://xxx.feishu.cn/wiki/YSIEwzlV9iNTHHkzOeFcf0jWnIh"
        }
      }
    ],
    "total": 3
  }
}
```

### 3.4 获取文档内容

```bash
# 获取文档的 Markdown 内容
lark-cli docs +fetch --doc {document_token}

# 示例
lark-cli docs +fetch --doc YSIEwzlV9iNTHHkzOeFcf0jWnIh
```

**返回示例**:
```json
{
  "ok": true,
  "data": {
    "doc_id": "YSIEwzlV9iNTHHkzOeFcf0jWnIh",
    "markdown": "# 文档标题\n\n文档内容...",
    "title": "文档标题",
    "total_length": 33473
  }
}
```

---

## 四、常见问题与解决方案

### 4.1 问题：缺少权限

**错误信息**:
```json
{
  "error": {
    "type": "missing_scope",
    "message": "missing required scope(s): search:docs:read"
  }
}
```

**解决方案**:
```bash
# 重新授权添加缺失的权限
lark-cli auth login --scope "search:docs:read"
```

### 4.2 问题：无法获取子节点

**现象**: 
- API 返回 `has_child: true`，但无法获取子节点内容
- 使用 `parent_node_token` 参数仍返回所有一级节点

**解决方案**:
使用搜索功能代替 Wiki API：
```bash
# 使用搜索功能查找子文档
lark-cli docs +search --query "父文档关键词" --page-size 20
```

### 4.3 问题：Token 过期

**错误信息**:
```json
{
  "error": {
    "type": "auth_error",
    "message": "token expired"
  }
}
```

**解决方案**:
```bash
# 重新登录授权
lark-cli auth login --recommend
```

### 4.4 问题：权限缓存不同步

**现象**:
- `lark-cli auth scopes` 显示有权限
- 实际调用时提示缺少权限

**解决方案**:
```bash
# 清除缓存并重新授权
lark-cli auth logout
lark-cli auth login --recommend
```

### 4.5 问题：删除重复文档失败

**现象**:
- 尝试使用 API 删除重复文档时遇到权限错误
- 命令执行没有输出，但文档仍然存在
- 出现 403 禁止访问或 400 无效访问令牌错误

**原因分析**:
1. **权限问题**：应用可能没有删除文档的权限
2. **认证问题**：用户访问令牌可能无效或过期
3. **API 路径问题**：删除 API 的路径或参数可能不正确
4. **飞书 CLI 限制**：飞书 CLI 可能不支持直接删除知识库节点

**解决方案**:

#### 方案 1：手动删除（推荐）
1. 登录飞书客户端
2. 进入【KAKA知识】知识库
3. 导航到文档所在目录
4. 找到重复的文档并手动删除

#### 方案 2：使用正确的 API 路径
```bash
# 使用云文档删除 API（需要正确的权限）
lark-cli api DELETE /open-apis/drive/v1/files/{obj_token}?type=docx

# 或者使用完整的 URL 格式
lark-cli api DELETE "https://open.feishu.cn/open-apis/drive/v1/files/{obj_token}?type=docx"
```

#### 方案 3：检查并获取有效的访问凭证
```bash
# 检查当前认证状态
lark-cli auth status

# 重新授权以获取新的令牌
lark-cli auth login --recommend

# 验证令牌有效性
lark-cli api GET /open-apis/authen/v1/access_token/check_user
```

#### 方案 4：使用 tenant_access_token
```bash
# 获取 tenant_access_token
lark-cli api POST /open-apis/auth/v3/tenant_access_token/internal --data '{"app_id":"您的app_id","app_secret":"您的app_secret"}'

# 使用 tenant_access_token 删除文档
lark-cli api DELETE /open-apis/drive/v1/files/{obj_token}?type=docx --as app
```

**注意事项**:
- 删除操作需要相应的权限：`docs:document:delete`
- 确保使用正确的文档 token（obj_token）
- 某些删除操作可能是异步的，需要检查任务状态
- 删除操作不可逆，请谨慎操作

---

## 五、权限说明

### 5.1 常用权限列表

| 权限 | 说明 | 用途 |
|------|------|------|
| `wiki:wiki:readonly` | 知识库只读 | 查询知识库结构 |
| `wiki:node:read` | 节点读取 | 读取知识库节点 |
| `wiki:space:read` | 空间读取 | 读取知识库空间 |
| `search:docs:read` | 文档搜索 | 搜索文档内容 |
| `docx:document:readonly` | 文档只读 | 读取文档内容 |
| `drive:file:download` | 文件下载 | 下载文档附件 |

### 5.2 推荐授权方式

```bash
# 方式一：使用推荐权限（最简单）
lark-cli auth login --recommend

# 方式二：手动指定权限（最精确）
lark-cli auth login --scope "wiki:wiki:readonly wiki:node:read wiki:space:read search:docs:read docx:document:readonly"
```

---

## 六、完整操作流程示例

### 6.1 查询知识库完整内容的流程

```bash
# 步骤 1: 安装 CLI
npm install -g @larksuite/cli

# 步骤 2: 初始化配置
lark-cli config init

# 步骤 3: 登录授权（包含搜索权限）
lark-cli auth login --recommend
lark-cli auth login --scope "search:docs:read"

# 步骤 4: 验证授权
lark-cli auth status

# 步骤 5: 查询知识库空间
lark-cli api GET /open-apis/wiki/v2/spaces

# 步骤 6: 查询知识库节点
lark-cli api GET "/open-apis/wiki/v2/spaces/{space_id}/nodes"

# 步骤 7: 搜索文档（推荐方式）
lark-cli docs +search --query "关键词" --page-size 20

# 步骤 8: 获取文档内容
lark-cli docs +fetch --doc {document_token}
```

### 6.2 在知识库中创建子文档并添加协作人

#### 6.2.1 获取知识库空间和节点信息

```bash
# 步骤 1: 获取知识库空间列表
lark-cli api GET /open-apis/wiki/v2/spaces

# 步骤 2: 获取知识库节点列表
lark-cli api GET "/open-apis/wiki/v2/spaces/{space_id}/nodes"
```

#### 6.2.2 使用 tenant_access_token 创建文档

```bash
# 步骤 3: 使用 tenant_access_token 创建文档
lark-cli docs +create \
  --title "文档标题" \
  --wiki-node "{parent_node_token}" \
  --markdown "# 文档内容\n\n## 章节 1\n\n内容..."
```

**示例**:
```bash
# 在俄罗斯方块目录下创建需求文档
lark-cli docs +create \
  --title "俄罗斯方块需求文档" \
  --wiki-node "ZkC1wi5EIiQNFmkOGzncmkUSnLf" \
  --markdown "# 俄罗斯方块需求文档\n\n## 功能需求\n\n- 基本的俄罗斯方块游戏玩法\n- 分数系统\n- 难度递增\n- 游戏控制\n\n## 技术需求\n\n- 前端实现\n- 游戏逻辑\n- 数据存储\n"
```

**预期输出**:
```json
{
  "ok": true,
  "data": {
    "doc_id": "NO8kwXrz0iO747klC7zcodnJnsf",
    "doc_url": "https://www.feishu.cn/wiki/NO8kwXrz0iO747klC7zcodnJnsf",
    "message": "文档创建成功"
  }
}
```

#### 6.2.3 添加 BLACK 用户为协作人（重要！）

**⚠️ 重要**：根据文档协作人管理原则，必须将 BLACK 用户添加为协作人并给予【可管理】权限。

```bash
# 步骤 4: 将 BLACK 用户添加为协作人
lark-cli api POST "/open-apis/drive/v1/permissions/batch_create" \
  --data '{"type":"docx","token":"{document_token}","members":[{"member_type":"user","member_id":"ou_7ef0e95e4659569a31e4c61dc3568630","role":"full_access"}]}'
```

**示例**:
```bash
# 为刚刚创建的俄罗斯方块需求文档添加 BLACK 用户为协作人
lark-cli api POST "/open-apis/drive/v1/permissions/batch_create" \
  --data '{"type":"docx","token":"NO8kwXrz0iO747klC7zcodnJnsf","members":[{"member_type":"user","member_id":"ou_7ef0e95e4659569a31e4c61dc3568630","role":"full_access"}]}'
```

**预期输出**:
```json
{
  "code": 0,
  "data": {
    "permissions": [
      {
        "member_id": "ou_7ef0e95e4659569a31e4c61dc3568630",
        "member_type": "user",
        "role": "full_access"
      }
    ]
  }
}
```

#### 6.2.4 验证操作结果

```bash
# 验证文档创建成功
lark-cli docs +fetch --doc {document_token}

# 验证 BLACK 用户是否成功添加为协作人
lark-cli api GET "/open-apis/drive/v1/permissions/{document_token}?type=docx"

# 搜索验证文档存在
lark-cli docs +search --query "文档标题" --page-size 20
```

### 6.3 快速查询脚本

创建脚本 `query_wiki.sh`:

```bash
#!/bin/bash

# 配置
SPACE_ID="7418508651239784449"
OUTPUT_DIR="./wiki_export"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 查询知识库节点
echo "正在查询知识库节点..."
lark-cli api GET "/open-apis/wiki/v2/spaces/$SPACE_ID/nodes" > "$OUTPUT_DIR/nodes.json"

# 搜索所有文档
echo "正在搜索所有文档..."
lark-cli docs +search --query "" --page-size 20 > "$OUTPUT_DIR/search_results.json"

# 提取文档 token 并获取内容
echo "正在获取文档内容..."
cat "$OUTPUT_DIR/search_results.json" | jq -r '.data.results[].result_meta.token' | while read token; do
  echo "获取文档: $token"
  lark-cli docs +fetch --doc "$token" > "$OUTPUT_DIR/doc_$token.json"
done

echo "完成！结果保存在 $OUTPUT_DIR 目录"
```

---

## 七、API 参考

### 7.1 Wiki API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/open-apis/wiki/v2/spaces` | GET | 获取知识库空间列表 |
| `/open-apis/wiki/v2/spaces/{space_id}/nodes` | GET | 获取知识库节点 |
| `/open-apis/wiki/v2/nodes/{node_token}` | GET | 获取节点详情 |

### 7.2 Docs API

| 命令 | 说明 |
|------|------|
| `lark-cli docs +search` | 搜索文档 |
| `lark-cli docs +fetch` | 获取文档内容 |
| `lark-cli docs +create` | 创建文档 |
| `lark-cli docs +update` | 更新文档 |

### 7.3 Auth API

| 命令 | 说明 |
|------|------|
| `lark-cli auth login` | 登录授权 |
| `lark-cli auth logout` | 登出 |
| `lark-cli auth status` | 查看授权状态 |
| `lark-cli auth scopes` | 查看已授权权限 |

---

## 八、最佳实践

### 8.1 权限管理
- 首次使用时使用 `--recommend` 参数获取常用权限
- 遇到权限问题时，使用 `--scope` 参数单独添加
- 定期检查授权状态，及时更新过期 token

### 8.2 查询效率
- 使用搜索功能代替 Wiki API 查询子节点
- 使用 `--page-size` 参数控制每次查询的数量
- 使用 `--page-all` 参数自动分页获取所有结果

### 8.3 数据导出
- 使用 `--format` 参数指定输出格式（json/table/csv）
- 使用 `-o` 参数将结果保存到文件
- 批量操作时使用脚本自动化

---

## 九、故障排查

### 9.1 日志查看

```bash
# 查看 CLI 日志
cat ~/.lark-cli/logs/cli.log

# 查看 API 请求日志
lark-cli api GET "/open-apis/wiki/v2/spaces" --dry-run
```

### 9.2 调试模式

```bash
# 使用 dry-run 模式查看请求详情
lark-cli docs +search --query "test" --dry-run

# 查看完整的 API schema
lark-cli schema wiki.spaces.get_node
```

### 9.3 重置配置

```bash
# 登出
lark-cli auth logout

# 重新初始化
lark-cli config init

# 重新授权
lark-cli auth login --recommend
```

---

## 十、参考资源

- **官方文档**: https://github.com/larksuite/cli
- **飞书开放平台**: https://open.feishu.cn/
- **API 文档**: https://open.feishu.cn/document/

---

## 附录：本次操作记录

### A.1 安装过程
```bash
npm install -g @larksuite/cli
# 安装成功，版本 1.0.0
```

### A.2 配置过程
```bash
lark-cli config init
# 应用配置成功，App ID: cli_a94d456321b89cc5
```

### A.3 授权过程
```bash
# 第一次授权（常用权限）
lark-cli auth login --recommend
# 成功授权 113 个权限

# 第二次授权（添加搜索权限）
lark-cli auth login --scope "search:docs:read"
# 成功添加 search:docs:read 权限
```

### A.4 查询过程
```bash
# 查询知识库空间
lark-cli api GET /open-apis/wiki/v2/spaces
# 返回 2 个知识库空间

# 查询 KAKA 知识库节点
lark-cli api GET "/open-apis/wiki/v2/spaces/7418508651239784449/nodes"
# 返回 4 个一级节点

# 搜索文档（解决问题）
lark-cli docs +search --query "中心仓" --page-size 20
# 返回 18 个文档

lark-cli docs +search --query "企微RPA" --page-size 20
# 返回 3 个文档

lark-cli docs +search --query "大模型外呼" --page-size 20
# 返回 4 个文档
```

### A.5 最终结果
- **知识库空间**: 2 个
- **KAKA 知识库文档总数**: 26 个
  - 中心仓: 18 个文档
  - 企微RPA项目: 3 个文档
  - 大模型外呼: 4 个文档
  - 俄罗斯方块: 1 个文档

---

**文档版本**: 1.3  
**最后更新**: 2026-03-29
