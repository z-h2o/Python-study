# URL缩短服务

基于 FastAPI 和 MySQL 的 URL 缩短服务，支持短链接生成、重定向和访问统计功能。

## 功能特性

- ✅ 短链接生成（5字符唯一标识）
- ✅ URL重定向功能
- ✅ 点击次数统计
- ✅ URL格式验证
- ✅ 数据库自动初始化
- ✅ 健康检查端点
- ✅ 完整的错误处理

## 技术栈

- **后端框架**: FastAPI
- **数据库**: MySQL
- **ORM**: PyMySQL
- **验证**: Pydantic

## 快速开始

### 1. 环境准备

确保您已安装以下软件：
- Python 3.8+
- MySQL 5.7+

### 2. 数据库设置

1. 创建MySQL数据库和用户（可跳过如果使用现有root用户）：

```sql
CREATE DATABASE url_shortener CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'url_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON url_shortener.* TO 'url_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 安装依赖

```bash
cd URL缩短服务
pip install -r requirements.txt
```

### 4. 配置修改

编辑 `main.py` 文件中的数据库配置：

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",      # 替换为您的MySQL用户名
    "password": "",      # 替换为您的MySQL密码
    "database": "url_shortener",
    # 其他配置保持不变
}
```

### 5. 启动服务

```bash
# 方式一：通过Python代码启动（开发模式）
python main.py

# 方式二：通过uvicorn命令启动（推荐）
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

## API使用说明

### 1. 健康检查

```bash
GET /
```

**响应示例：**
```json
{
  "status": "healthy",
  "service": "URL缩短服务",
  "version": "1.0.0",
  "message": "服务运行正常"
}
```

### 2. 创建短链接

```bash
POST /shorten
Content-Type: application/json

{
  "target_url": "https://www.example.com"
}
```

**响应示例：**
```json
{
  "short_url": "http://localhost:3000/aBc12",
  "target_url": "https://www.example.com",
  "message": "短链接创建成功"
}
```

### 3. 访问短链接（重定向）

```bash
GET /{short_id}
```

例如：`GET /aBc12` 会重定向到原始URL

## 项目结构

```
URL缩短服务/
├── main.py          # 主程序代码
├── requirements.txt # 项目依赖
└── README.md        # 使用说明
```

## 注意事项

1. 确保MySQL服务已启动且数据库配置正确
2. 生产环境中建议使用环境变量存储敏感信息
3. 可考虑添加HTTPS支持和访问限流功能
4. 定期清理不活跃的链接以优化数据库性能

## 故障排除

- **数据库连接失败**: 检查MySQL服务是否运行，连接参数是否正确
- **表不存在**: 服务启动时会自动创建表，确保用户有权限创建表
- **端口被占用**: 修改`main.py`中的端口号或停止占用该端口的服务

## License

MIT