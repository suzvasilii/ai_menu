from functools import wraps
from fastapi import HTTPException

def service_handle_errors(status_code = 500):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=status_code, detail=f"Service error: {str(e)}")
        return wrapper
    return decorator

def saver_handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unable to save image. Details: {str(e)}")
    return wrapper

def tg_handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unable to send message. Details: {str(e)}")
    return wrapper
