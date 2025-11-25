# Python (FastAPI + MySQL)
import secrets
import pymysql
from pymysql.cursors import DictCursor
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, field_validator, ConfigDict
from starlette.responses import RedirectResponse
import uvicorn
import os

# -- MySQL数据库配置 --
# 注意：请根据您的MySQL服务器配置修改以下参数
DB_CONFIG = {
    "host": "localhost",  # MySQL主机地址
    "user": "root",  # MySQL用户名
    "password": "12345678",  # MySQL密码，请替换为您的实际密码
    "database": "url_shortener",  # 数据库名称，确保已创建
    "charset": "utf8mb4",  # 支持全UTF-8字符集
    "cursorclass": DictCursor,  # 使用字典游标
    "autocommit": False,  # 手动控制事务
}


# -- 数据库表初始化函数 --
def init_db():
    """
    初始化数据库表结构
    在应用启动时调用此函数创建必要的表
    """
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # 创建urls表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS urls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                short_id VARCHAR(20) NOT NULL UNIQUE,
                target_url TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                clicks INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_sql)
        conn.commit()
        print("数据库表初始化成功")
    except Exception as e:
        print(f"数据库初始化错误: {e}")
    finally:
        conn.close()


# -- 数据库连接依赖 --
def get_db():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()


# -- Pydantic 模型 --
class URLBase(BaseModel):
    """
    URL请求模型，包含URL验证规则
    """

    target_url: str

    # Pydantic V2 配置
    model_config = ConfigDict(
        # 启用示例值
        json_schema_extra={"example": {"target_url": "https://www.example.com"}}
    )

    @field_validator("target_url")
    def validate_url(cls, v):
        """
        验证URL格式
        - 必须包含http://或https://
        - URL长度不能超过1000个字符
        - 检查基本URL格式
        """
        # 验证URL长度
        if len(v) > 1000:
            raise ValueError("URL长度不能超过1000个字符")

        # 验证是否包含协议
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL必须包含http://或https://")

        # 基本URL格式检查（可选，这里只做简单检查）
        try:
            from urllib.parse import urlparse

            parsed = urlparse(v)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("URL格式无效")
        except Exception:
            raise ValueError("URL格式无效")

        return v


class URLInfo(URLBase):
    is_active: bool
    clicks: int


# -- 应用初始化 --
app = FastAPI(
    title="URL缩短服务", description="基于FastAPI和MySQL的URL缩短工具", version="1.0.0"
)


# -- 根路径健康检查 --
@app.get("/")
def health_check():
    """
    健康检查端点
    用于监控服务状态
    """
    return {
        "status": "healthy",
        "service": "URL缩短服务",
        "version": "1.0.0",
        "message": "服务运行正常",
    }


@app.post("/shorten")
def create_url(url: URLBase, db: pymysql.connections.Connection = Depends(get_db)):
    """
    创建短链接
    1. 生成唯一的短ID
    2. 验证URL格式
    3. 存储到数据库
    4. 返回短链接
    """
    # 验证URL是否包含协议（http://或https://）
    if not url.target_url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL必须包含http://或https://")

    # 生成唯一的短ID（最多尝试5次）
    max_attempts = 5
    short_id = None

    for _ in range(max_attempts):
        # 生成5个字符的URL安全令牌
        candidate_id = secrets.token_urlsafe(5)[:5]  # 限制长度为5

        # 检查短ID是否已存在
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM urls WHERE short_id = %s", (candidate_id,)
                )
                if not cursor.fetchone():
                    short_id = candidate_id
                    break
        except Exception as e:
            print(f"检查短ID时出错: {e}")

    if not short_id:
        raise HTTPException(status_code=500, detail="无法生成唯一的短链接，请稍后重试")

    # 存储到数据库
    try:
        with db.cursor() as cursor:
            sql = """
            INSERT INTO urls (short_id, target_url, is_active, clicks)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (short_id, url.target_url, True, 0))
        db.commit()

        # 返回短链接
        short_url = f"http://localhost:3000/{short_id}"
        return {
            "short_url": short_url,
            "target_url": url.target_url,
            "message": "短链接创建成功",
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建短链接失败: {str(e)}")


@app.get("/{short_id}")
def redirect_to_url(
    short_id: str, db: pymysql.connections.Connection = Depends(get_db)
):
    """
    根据短ID重定向到原始URL
    1. 查询数据库获取原始URL
    2. 检查链接是否有效
    3. 增加点击次数
    4. 执行重定向
    """
    try:
        with db.cursor() as cursor:
            # 查询短链接信息
            sql = """
            SELECT target_url, is_active 
            FROM urls 
            WHERE short_id = %s
            """
            cursor.execute(sql, (short_id,))
            result = cursor.fetchone()
            print("result===>", result)
            if not result:
                raise HTTPException(status_code=404, detail="短链接不存在")

            target_url = result["target_url"]
            is_active = result["is_active"]
            print("is_active===>", is_active, target_url)
            if not is_active:
                raise HTTPException(status_code=404, detail="短链接已被禁用")

            # 更新点击次数
            update_clicks_sql = """
            UPDATE urls 
            SET clicks = clicks + 1 
            WHERE short_id = %s
            """
            cursor.execute(update_clicks_sql, (short_id,))
            db.commit()

            # 执行重定向
            return RedirectResponse(url=target_url)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"重定向时出错: {e}")
        raise HTTPException(status_code=500, detail="重定向服务临时不可用")


if __name__ == "__main__":
    # 初始化数据库表
    # init_db()
    # 启动应用
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
