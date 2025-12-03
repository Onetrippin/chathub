from fastapi import HTTPException

def downstream_error(status_code: int, detail: str, service: str):
    raise HTTPException(status_code=status_code, detail={"service": service, "error": detail})
