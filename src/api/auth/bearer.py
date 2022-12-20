from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(jwtBearer, self.__init__(auto_error=auto_error))

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid or Expired token"
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid or Expired token"
            )

    def verify_jwt(self, jwtToken: str):
        isToken: bool = False
        payload = decodeJWT(jwtToken)
        if payload:
            isToken = True
        return isToken
