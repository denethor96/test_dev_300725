# Instrucciones

1. Crear `.env` a partir de `.env.example`

2. Ejecutar proyecto
    ```
    docker compose up --build
    ```
    - MongoDB usará la carpeta local `mongo_data/` para persistencia
    - La documentación interactiva estará disponible en: `http://localhost:8000/docs`
    - El endpoint de registro de usuario es: `http://localhost:8000/register` para el método `POST`