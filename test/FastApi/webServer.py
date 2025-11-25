from typing import Required
from fastapi import FastAPI, Query, Request, Body
import uvicorn
from pydantic import BaseModel

app = FastAPI()


@app.get("/name")
def get_name():
    return {"name": "张三"}


# 使用Query参数接收查询参数
@app.post("/user")
def get_user(
    # item: IValue,
    name: str = Body(..., description="用户名"),
    age: int = Body(None, description="年龄"),
    is_offer: bool = Body(None, description="是否录用"),
):
    # 打印Body的所有参数
    print("===>", Body(..., description="用户名").__dict__)
    # 返回接收到的所有参数
    result = {"name": name}
    result["age"] = age
    result["is_offer"] = is_offer

    print("接收到的参数:", result)
    return result


# 方式一：通过命令行运行（推荐用于reload模式）
# 在终端中运行: uvicorn 01:app --host 127.0.0.1 --port 3010 --reload

# 方式二：代码中运行（不使用reload，但适合简单测试）
if __name__ == "__main__":
    uvicorn.run(
        "webServer:app",  # 使用导入字符串格式
        host="127.0.0.1",
        port=3010,
        reload=True,  # 现在可以正常启用热重载
    )
