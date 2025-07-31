# 📋 Gestor de Tareas de Escritorio

Una aplicación de escritorio desarrollada en Python para gestionar tareas con prioridades opcionales. La aplicación cuenta con una interfaz gráfica intuitiva y persistencia de datos.

## ✨ Características

- **Gestión completa de tareas**: Crear, editar, eliminar y marcar como completadas
- **Prioridades opcionales**: Sin prioridad, Baja, Media, Alta, Crítica
- **Filtrado avanzado**: Por prioridad y estado de completado
- **Interfaz visual**: Colores diferenciados según prioridad
- **Persistencia**: Las tareas se guardan automáticamente en un archivo JSON
- **Detalles expandidos**: Vista detallada de cada tarea seleccionada
- **Estadísticas**: Contador de tareas totales, completadas y pendientes

## 🚀 Requisitos

- Python 3.6 o superior
- tkinter (incluido por defecto en la mayoría de instalaciones de Python)

## 📦 Instalación y Uso

1. **Clona o descarga el archivo**:
   ```bash
   # Si tienes el archivo task_manager.py
   cd tu-directorio
   ```

2. **Ejecuta la aplicación**:
   ```bash
   python3 task_manager.py
   ```

3. **¡Listo!** La aplicación se abrirá en una ventana nueva.

## 🎯 Cómo Usar

### Agregar una Nueva Tarea
1. Haz clic en "➕ Agregar Tarea"
2. Completa el formulario:
   - **Título**: Campo obligatorio
   - **Prioridad**: Opcional (Ninguna por defecto)
   - **Descripción**: Opcional
3. Haz clic en "Guardar"

### Gestionar Tareas Existentes
- **Ver detalles**: Selecciona una tarea en la lista
- **Marcar como completada**: Selecciona una tarea y haz clic en "✓ Marcar Completada"
- **Editar**: Selecciona una tarea y haz clic en "✏️ Editar Tarea"
- **Eliminar**: Selecciona una tarea y haz clic en "🗑️ Eliminar Tarea"

### Filtrar Tareas
- **Por prioridad**: Usa el menú desplegable "Filtrar por prioridad"
- **Por estado**: Desmarca "Mostrar completadas" para ocultar tareas terminadas

## 🎨 Código de Colores

- **🔴 Crítica**: Fondo rojo claro
- **🟠 Alta**: Fondo naranja claro
- **🟣 Media**: Fondo púrpura claro
- **🟢 Baja**: Fondo verde claro
- **⚪ Sin prioridad**: Sin color especial
- **🔘 Completadas**: Texto en gris

## 💾 Persistencia de Datos

Las tareas se guardan automáticamente en un archivo `tasks.json` en el mismo directorio que la aplicación. Este archivo se crea automáticamente la primera vez que agregas una tarea.

## 🏗️ Estructura del Proyecto

```
task_manager.py         # Aplicación principal
tasks.json             # Archivo de datos (se crea automáticamente)
README.md              # Este archivo
```

## 🔧 Características Técnicas

- **Interfaz**: tkinter con widgets ttk para un aspecto moderno
- **Almacenamiento**: JSON con codificación UTF-8
- **Arquitectura**: Patrón MVC (Model-View-Controller)
- **Manejo de errores**: Validación de entrada y gestión de excepciones
- **Responsive**: Interfaz redimensionable

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que tienes Python 3.6 o superior instalado
- Asegúrate de que tkinter esté disponible: `python3 -c "import tkinter"`

### No se guardan las tareas
- Verifica que tienes permisos de escritura en el directorio
- Revisa si hay mensajes de error en la consola

### Problemas de visualización
- En algunos sistemas Linux, puede ser necesario instalar: `sudo apt-get install python3-tk`

## 🎯 Funcionalidades Futuras

Posibles mejoras que se podrían implementar:

- [ ] Fechas de vencimiento
- [ ] Categorías personalizadas
- [ ] Búsqueda por texto
- [ ] Exportar a CSV/PDF
- [ ] Notificaciones de recordatorio
- [ ] Tema oscuro/claro
- [ ] Subtareas
- [ ] Sincronización en la nube

## 📄 Licencia

Este proyecto es de código abierto y puede ser usado libremente para fines educativos y personales.

---

¡Disfruta gestionando tus tareas de manera eficiente! 🎉