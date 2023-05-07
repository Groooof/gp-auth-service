from fastapi.responses import JSONResponse


async def validation_error_handler(*args):
    return JSONResponse({'detail': 'invalid_request'}, status_code=400)
