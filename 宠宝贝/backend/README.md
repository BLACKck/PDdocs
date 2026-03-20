# 宠宝贝后端管理系统

## 项目结构

```
backend/
├── manage.py
├── settings.py
├── urls.py
├── wsgi.py
└── apps/
    ├── accounts/  # 账号权限管理模块
    ├── pets/      # 宠物信息管理模块
    ├── products/  # 商品库存管理模块
    └── orders/    # 订单系统管理模块
```

## 技术栈

- Python 3.8+
- Django 5.0+
- Django REST Framework
- SQLite (开发环境)

## 安装步骤

1. **创建虚拟环境**
   ```bash
   python -m venv venv
   ```

2. **激活虚拟环境**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **安装依赖**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **运行数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

6. **启动开发服务器**
   ```bash
   python manage.py runserver
   ```

## API接口

### 账号权限管理
- `GET /api/accounts/users/` - 获取用户列表
- `POST /api/accounts/users/` - 创建用户
- `GET /api/accounts/users/{id}/` - 获取用户详情
- `PUT /api/accounts/users/{id}/` - 更新用户信息
- `DELETE /api/accounts/users/{id}/` - 删除用户
- `POST /api/accounts/users/{id}/reset_password/` - 重置用户密码
- `POST /api/accounts/users/{id}/toggle_status/` - 切换用户状态

### 宠物信息管理
- `GET /api/pets/pets/` - 获取宠物列表
- `POST /api/pets/pets/` - 创建宠物信息
- `GET /api/pets/pets/{id}/` - 获取宠物详情
- `PUT /api/pets/pets/{id}/` - 更新宠物信息
- `DELETE /api/pets/pets/{id}/` - 删除宠物信息
- `POST /api/pets/pets/{id}/approve/` - 审核通过宠物信息
- `POST /api/pets/pets/{id}/reject/` - 审核拒绝宠物信息
- `POST /api/pets/pets/batch_approve/` - 批量审核通过宠物信息
- `POST /api/pets/pets/batch_reject/` - 批量审核拒绝宠物信息
- `GET /api/pets/pets/statistics/` - 宠物信息统计

### 商品库存管理
- `GET /api/products/products/` - 获取商品列表
- `POST /api/products/products/` - 创建商品
- `GET /api/products/products/{id}/` - 获取商品详情
- `PUT /api/products/products/{id}/` - 更新商品信息
- `DELETE /api/products/products/{id}/` - 删除商品
- `POST /api/products/products/{id}/toggle_status/` - 上架/下架商品
- `POST /api/products/products/batch_operation/` - 批量操作商品

- `GET /api/products/inventories/` - 获取库存列表
- `POST /api/products/inventories/{id}/stock_in/` - 商品入库
- `POST /api/products/inventories/{id}/stock_out/` - 商品出库
- `POST /api/products/inventories/{id}/set_alert/` - 设置库存预警

- `GET /api/products/prices/` - 获取价格列表
- `POST /api/products/prices/{id}/update_price/` - 修改商品价格
- `POST /api/products/prices/{id}/set_promotion/` - 设置促销价
- `POST /api/products/prices/{id}/cancel_promotion/` - 取消促销
- `POST /api/products/prices/batch_update_price/` - 批量修改价格

### 订单系统管理
- `GET /api/orders/orders/` - 获取订单列表
- `GET /api/orders/orders/{id}/` - 获取订单详情
- `POST /api/orders/orders/{id}/ship/` - 发货
- `POST /api/orders/orders/{id}/cancel/` - 取消订单
- `POST /api/orders/orders/{id}/confirm_receipt/` - 确认收货
- `POST /api/orders/orders/{id}/handle_refund/` - 处理退款
- `POST /api/orders/orders/batch_operation/` - 批量操作订单
- `GET /api/orders/orders/statistics/` - 订单统计

- `GET /api/orders/logistics/` - 获取物流信息列表
- `POST /api/orders/logistics/{id}/update_logistics/` - 更新物流信息
- `POST /api/orders/logistics/batch_update/` - 批量更新物流信息

## 注意事项

1. 开发环境使用SQLite数据库，生产环境建议使用MySQL或PostgreSQL
2. 所有API接口都需要认证，使用Django的Session认证或Basic认证
3. 超级管理员可以管理所有功能，普通管理员只能管理部分功能
4. 商品图片和宠物照片存储在项目的media目录中

## 部署

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   - 设置SECRET_KEY
   - 设置数据库连接信息
   - 设置DEBUG=False

3. **运行数据库迁移**
   ```bash
   python manage.py migrate
   ```

4. **收集静态文件**
   ```bash
   python manage.py collectstatic
   ```

5. **使用WSGI服务器部署**
   - 使用Gunicorn或uWSGI
   - 配置Nginx作为反向代理