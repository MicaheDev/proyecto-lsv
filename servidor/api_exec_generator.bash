#!/bin/bash

# Salir inmediatamente si ocurre un error
set -e

echo "🚀 Limpiando procesos antiguos en el puerto 5000..."
killall -9 python python3 2>/dev/null || true

echo "📦 Compilando API Flask para Linux..."
pyinstaller --onefile \
    --hidden-import=bcrypt \
    --hidden-import=_bcrypt \
    --hidden-import=unicodedata \
    app.py

echo "✅ ¡Compilación completada con éxito!"
echo "📂 Tu binario portable está en: servidor/dist/app"