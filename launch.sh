#!/bin/bash

# Script para ejecutar el Gestor de Tareas

echo "🚀 Iniciando Gestor de Tareas..."

# Verificar si Python 3 está disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar si tkinter está disponible
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Error: tkinter no está disponible"
    echo "En Ubuntu/Debian, instálalo con: sudo apt-get install python3-tk"
    exit 1
fi

# Ejecutar la aplicación
echo "✅ Ejecutando la aplicación..."
python3 task_manager.py