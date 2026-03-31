import requests
import json

# 读取配置文件获取应用信息
config_path = "mcp-config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

# 应用信息
app_id = "cli_a92fb9e90e799cb5"
app_secret = "2PQierezFvaasuwPIBhqxeXDp4ELSO4n"

print("=" * 60)
print("获取 User Access Token 的替代方案")
print("=" * 60)

print("\n由于重定向 URL 配置问题，我们采用以下步骤：")
print("\n方法一：通过飞书开放平台控制台获取（推荐）")
print("1. 访问飞书开放平台：https://open.feishu.cn/")
print("2. 登录开发者账号")
print("3. 进入应用管理 > 选择您的应用（俄罗斯方块）")
print("4. 点击'凭证管理'或'开发配置'")
print("5. 在'网页应用'部分找到'User Access Token'")
print("6. 点击'获取 User Access Token'按钮")
print("7. 扫码授权后获取 token")

print("\n" + "-" * 60)

print("\n方法二：配置重定向 URI 后使用 OAuth 流程")
print("1. 访问飞书开放平台：https://open.feishu.cn/")
print("2. 进入应用管理 > 选择您的应用")
print("3. 点击'开发配置'或'应用首页'")
print("4. 找到'重定向 URI'配置")
print("5. 添加重定向 URI: https://open.feishu.cn/tool/redirect")
print("6. 保存配置")
print("7. 然后运行方法一的脚本获取授权码")

print("\n" + "-" * 60)

print("\n方法三：使用 OAuth 授权码方式（需先配置重定向 URI）")
print("请先在飞书开放平台配置重定向 URI 为：https://open.feishu.cn/tool/redirect")
print("配置完成后，运行以下命令：")
print("python get_user_access_token_v2.py")

print("\n" + "=" * 60)

# 询问用户选择哪种方式
print("\n请选择获取方式：")
print("1. 查看方法一的详细说明")
print("2. 查看方法二的详细说明")
print("3. 已配置重定向 URI，继续 OAuth 流程")

choice = input("\n请输入选择 (1/2/3): ").strip()

if choice == "1":
    print("\n" + "=" * 60)
    print("方法一详细说明：")
    print("=" * 60)
    print("\n1. 访问飞书开放平台控制台")
    print("   URL: https://open.feishu.cn/developer/console")
    print("\n2. 登录开发者账号")
    print("   使用您的飞书账号扫码或密码登录")
    print("\n3. 找到您的应用")
    print("   在应用列表中找到'俄罗斯方块'或对应的应用")
    print("\n4. 获取 User Access Token")
    print("   - 点击应用进入详情页")
    print("   - 点击左侧菜单'开发配置'")
    print("   - 找到'User Access Token'部分")
    print("   - 点击'获取 User Access Token'")
    print("   - 使用飞书 App 扫码授权")
    print("   - 授权成功后会显示 User Access Token")
    print("\n5. 复制并保存 User Access Token")
    print("   将获取到的 User Access Token 保存到配置文件")
    
elif choice == "2":
    print("\n" + "=" * 60)
    print("方法二详细说明：")
    print("=" * 60)
    print("\n步骤一：配置重定向 URI")
    print("1. 访问飞书开放平台：https://open.feishu.cn/")
    print("2. 登录并进入应用管理")
    print("3. 选择您的应用（俄罗斯方块）")
    print("4. 点击'开发配置'")
    print("5. 找到'重定向 URI'配置项")
    print("6. 添加以下 URI：")
    print("   https://open.feishu.cn/tool/redirect")
    print("7. 点击'保存'按钮")
    print("\n步骤二：获取授权码")
    print("1. 保存配置后等待 1-2 分钟生效")
    print("2. 运行脚本：python get_user_access_token_v2.py")
    print("3. 复制显示的授权 URL 并在浏览器打开")
    print("4. 扫码授权后会跳转到重定向页面")
    print("5. 从页面中复制授权码 (code)")
    print("\n步骤三：换取 User Access Token")
    print("1. 回到终端粘贴授权码")
    print("2. 脚本会自动换取 User Access Token")
    print("3. 获取成功后会询问是否保存到配置文件")
    
elif choice == "3":
    print("\n好的，将继续 OAuth 流程...")
    print("请确保已配置重定向 URI 为：https://open.feishu.cn/tool/redirect")
    print("\n运行命令：python get_user_access_token_v2.py")
    print("然后按照提示操作即可")
    
else:
    print("\n无效选择，请重新运行脚本并选择 1/2/3")

print("\n" + "=" * 60)
