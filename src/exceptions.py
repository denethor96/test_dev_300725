from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException, Request


def format_field_path(loc):
    path = []
    result = ""

    if len(loc) == 1 and loc[0] == "body":
        return None

    for part in loc[1:]:
        if isinstance(part, int):
            path.append(f"[{part}]")
        else:
            path.append(str(part))

    for p in path:
        if p.startswith("["):
            result += p
        elif result:
            result += "." + p
        else:
            result = p

    return result


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    mensajes = []

    for err in errors:
        loc = err.get("loc", [])
        err_type = err.get("type", "")
        orig_msg = err.get("msg", "")
        
        if err_type == "value_error.missing" or orig_msg == "Field required" or err_type == "missing":
            field_path = format_field_path(loc)

            if field_path is None:
                msg = "Debe enviar los datos del usuario en el cuerpo de la solicitud."
            else:
                msg = f"El campo '{field_path}' es obligatorio."

        elif err_type == "type_error.email":
            msg = "El correo electrónico no es válido."
        elif "email" in str(loc).lower() and "valid" in orig_msg.lower():
            msg = "El correo electrónico no es válido."
        elif err_type.startswith("value_error"):
            msg = orig_msg.replace("Value error, ", "")
        else:
            msg = orig_msg or "Error de validación."

        mensajes.append(msg)
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"mensajes": mensajes}
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"mensaje": exc.detail if isinstance(exc.detail, str) else str(exc.detail)}
    )
