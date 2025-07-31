from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError

from src.schemas import UserIn, UserOut, ErrorMessage
from src.crud import get_user_by_email, create_user
from src.exceptions import validation_exception_handler, http_exception_handler

app = FastAPI()

# Registrar los exception handlers personalizados
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.post("/register", response_model=UserOut, responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorMessage}})
async def register(user: UserIn):
    existing = await get_user_by_email(user.email)
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    user_data = await create_user(user)
    
    return user_data
