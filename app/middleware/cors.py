from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción, especifica los dominios permitidos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )