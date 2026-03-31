# 安装飞书 CLI 工具指南

## 方法一：使用 pip 安装（推荐）

### 步骤 1：确保 pip 已安装
```bash
pip --version
```

### 步骤 2：升级 pip（可选）
```bash
python -m pip install --upgrade pip
```

### 步骤 3：安装飞书 CLI
```bash
pip install lark-cli
```

如果找不到包，尝试：
```bash
pip install git+https://github.com/larksuite/cli.git
```

### 步骤 4：验证安装
```bash
lark --version
```

## 方法二：从源码安装

### 步骤 1：克隆仓库
```bash
git clone https://github.com/larksuite/cli.git
cd cli
```

### 步骤 2：安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 3：安装 CLI
```bash
pip install .
```

### 步骤 4：验证安装
```bash
lark --version
```

## 方法三：下载预编译版本

### 步骤 1：访问 Release 页面
访问：https://github.com/larksuite/cli/releases

### 步骤 2：下载适合您系统的版本
- Windows: 下载 `.exe` 或 `.zip` 文件
- macOS: 下载 `.dmg` 或 `.tar.gz` 文件
- Linux: 下载 `.tar.gz` 或对应发行版的包

### 步骤 3：解压并添加到 PATH
以 Windows 为例：
1. 解压下载的 zip 文件
2. 将解压后的文件夹移动到合适位置（如 `C:\Program Files\lark-cli`）
3. 将该文件夹添加到系统环境变量 PATH 中

### 步骤 4：验证安装
```bash
lark --version
```

## 配置飞书 CLI

### 步骤 1：初始化配置
```bash
lark init
```

### 步骤 2：输入配置信息
- App ID: `cli_a92fb9e90e799cb5`
- App Secret: `2PQierezFvaasuwPIBhqxeXDp4ELSO4n`

### 步骤 3：获取 Access Token
```bash
lark auth login
```

### 步骤 4：测试命令
```bash
lark doc list
```

## 常用命令

### 文档操作
```bash
# 列出文档
lark doc list

# 创建文档
lark doc create --title "文档标题" --content "文档内容"

# 查看文档
lark doc get --doc_id "文档 ID"

# 更新文档
lark doc update --doc_id "文档 ID" --content "新内容"

# 删除文档
lark doc delete --doc_id "文档 ID"
```

### 用户操作
```bash
# 获取当前用户信息
lark auth whoami

# 退出登录
lark auth logout
```

### 帮助
```bash
# 查看所有命令
lark --help

# 查看特定命令的帮助
lark doc --help
lark doc create --help
```

## 常见问题

### Q1: 安装时提示找不到 lark-cli 包
**解决方案**：
- 飞书 CLI 可能未发布到 PyPI
- 使用方法二（源码安装）或方法三（下载预编译版本）

### Q2: git clone 失败
**解决方案**：
- 检查网络连接
- 使用镜像：`git clone https://gitee.com/mirror/github/larksuite/cli.git`
- 下载 ZIP 文件手动解压

### Q3: 安装后无法运行 lark 命令
**解决方案**：
- 确保已添加到 PATH 环境变量
- 重启终端或命令行
- 使用完整路径运行：`python -m lark`

### Q4: 权限问题
**解决方案**：
- 以管理员身份运行命令行
- 检查 pip 安装路径的权限

## 替代方案

如果飞书 CLI 安装失败，可以使用以下方式：

### 方案 1：使用 Python 脚本
我们已经有多个 Python 脚本可以调用飞书 API：
- `create_docx_api.py` - 创建云文档
- `check_user_permissions.py` - 检查用户权限
- `test_create_doc.py` - 测试创建文档

### 方案 2：使用 Postman
1. 下载并安装 Postman
2. 导入飞书 API Collection
3. 配置 Access Token
4. 直接调用 API

### 方案 3：使用 curl 命令
```bash
curl -X POST https://open.feishu.cn/open-apis/docx/v1/documents \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"测试文档"}'
```

## 当前项目使用的 Token

### Tenant Access Token
```
t-g1043qlD6CKSJB4PAPIW3OHN3WUKVDBLA3EBZ7IQ
```

### User Access Token
```
u-7zwRfYte17vVvRg.4jUbNy5ljHx4g5ihNo2aYMi00DAs
```

### App ID
```
cli_a92fb9e90e799cb5
```

### App Secret
```
2PQierezFvaasuwPIBhqxeXDp4ELSO4n
```

## 下一步

安装完成后，运行以下命令测试：
```bash
lark auth whoami
```

如果显示当前用户信息，说明安装成功！

---
**创建时间**: 2026-03-26  
**最后更新**: 2026-03-26
