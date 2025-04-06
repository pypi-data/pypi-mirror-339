from functools import wraps

from fastapi import Request

from phi_cloud_server.utils import get_session_token


def broadcast_route(manager):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取请求对象
            request = next(
                (arg for arg in args if isinstance(arg, Request)), kwargs.get("request")
            )
            if not request:
                return await func(*args, **kwargs)

            # 获取路由信息
            route = f"{request.method}:{request.url.path}"
            session_token = get_session_token(request) or ""

            # 执行原始处理函数
            response = await func(*args, **kwargs)

            # 广播事件
            await manager.broadcast_event(route, response, session_token)

            return response

        return wrapper

    return decorator
