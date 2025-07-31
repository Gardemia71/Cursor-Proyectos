# Gestor de Tareas de Escritorio - TaskManagerGUI

Una aplicación de escritorio moderna para gestionar tareas con sistema de prioridades opcional. Desarrollada en Python con múltiples interfaces: gráfica (tkinter) y consola, con almacenamiento persistente de datos.

## 🎯 Aplicación TaskManagerGUI

La aplicación principal se llama **TaskManagerGUI** y está disponible en diferentes versiones:

### 📁 Archivos Disponibles

1. **`task_manager_console.py`** - **Versión de consola (RECOMENDADA)**
   - Funciona sin dependencias externas
   - Interfaz de texto interactiva
   - Todas las funcionalidades completas

2. **`task_manager_simple.py`** - Versión GUI con tkinter nativo
   - Interfaz gráfica básica
   - Requiere tkinter (incluido en Python)

3. **`task_manager.py`** - Versión GUI moderna con ttkbootstrap
   - Interfaz gráfica avanzada
   - Requiere dependencias externas

4. **`demo_taskmanager.py`** - Script de demostración
   - Muestra uso programático
   - Ejemplos de todas las funcionalidades

## 🚀 Ejecución

### Opción 1: Versión de Consola (Funciona en cualquier entorno)
```bash
python3 task_manager_console.py
```

### Opción 2: Uso Programático
```python
from task_manager_console import TaskManagerGUI

# Crear instancia de la aplicación
app = TaskManagerGUI()

# Ejecutar aplicación interactiva
app.run()

# O usar programáticamente
task_manager = app.task_manager
app.display_tasks()
```

### Opción 3: Ver Demostración
```bash
python3 demo_taskmanager.py
```

## ✨ Características

### 🎯 Funcionalidades Principales
- **Crear, editar y eliminar tareas** con facilidad
- **Sistema de prioridades opcional** (Alta, Media, Baja, Sin prioridad)
- **Marcar tareas como completadas** con un clic
- **Filtrado avanzado** por estado y prioridad
- **Interfaz visual intuitiva** con iconos de colores para prioridades
- **Almacenamiento persistente** en formato JSON
- **Estadísticas en tiempo real** de tus tareas

### 🎨 Iconos Visuales
- 🔴 **Alta prioridad**
- 🟡 **Media prioridad**  
- 🟢 **Baja prioridad**
- ⚪ **Sin prioridad**
- ✅ **Tarea completada**
- ⏳ **Tarea pendiente**

### 🔍 Sistema de Filtros
- Todas las tareas
- Solo pendientes
- Solo completadas
- Por nivel de prioridad (Alta, Media, Baja)

## 💻 Interfaz de Consola

```
============================================================
            🎯 GESTOR DE TAREAS 🎯
============================================================

📊 ESTADÍSTICAS:
   Total: 4 | Completadas: 1 | Pendientes: 3 | Alta prioridad: 1
------------------------------------------------------------

🎛️  MENÚ PRINCIPAL:
1. 📝 Ver todas las tareas
2. ➕ Crear nueva tarea
3. ✏️  Editar tarea
4. ❌ Eliminar tarea
5. ✅ Marcar como completada
6. 🔍 Filtrar tareas
7. 📊 Ver estadísticas detalladas
8. 🚪 Salir
------------------------------------------------------------
```

## 📚 Uso de la Aplicación

### Crear una Nueva Tarea
1. Selecciona opción **2** en el menú principal
2. Ingresa el título (obligatorio)
3. Agrega descripción (opcional)
4. Selecciona prioridad (Alta/Media/Baja/Sin prioridad)
5. La tarea se guarda automáticamente

### Editar una Tarea
1. Selecciona opción **3** en el menú principal
2. Ve la lista de tareas con sus IDs
3. Ingresa el ID de la tarea a editar
4. Modifica los campos necesarios
5. Los cambios se guardan automáticamente

### Completar una Tarea
1. Selecciona opción **5** en el menú principal
2. Ve la lista de tareas pendientes
3. Ingresa el ID de la tarea
4. La tarea se marca como completada ✅

### Filtrar Tareas
1. Selecciona opción **6** en el menú principal
2. Elige el tipo de filtro:
   - Todas las tareas
   - Solo pendientes
   - Solo completadas
   - Por prioridad específica

## 🔧 Uso Programático

### Crear Instancia
```python
from task_manager_console import TaskManagerGUI, Task, Priority

# Crear aplicación
app = TaskManagerGUI()
```

### Gestionar Tareas
```python
# Acceder al gestor de tareas
manager = app.task_manager

# Crear nueva tarea
task = Task("Mi tarea", "Descripción", Priority.HIGH)
manager.add_task(task)

# Obtener tareas
todas = manager.get_tasks()
pendientes = manager.get_tasks(completed=False)
alta_prioridad = manager.get_tasks_by_priority(Priority.HIGH)

# Marcar como completada
manager.update_task(task.id, completed=True)

# Eliminar tarea
manager.delete_task(task.id)
```

### Mostrar Información
```python
# Mostrar tareas
app.display_tasks()

# Mostrar estadísticas
app.print_statistics()

# Ejecutar aplicación interactiva
app.run()
```

## 📊 Estructura de Datos

Las tareas se almacenan en `tasks.json` con la siguiente estructura:

```json
{
  "id": 1735047892.123456,
  "title": "Completar proyecto",
  "description": "Finalizar la documentación y pruebas",
  "priority": "Alta",
  "completed": false,
  "created_at": "2024-12-24T10:30:00",
  "updated_at": "2024-12-24T10:30:00"
}
```

## 🏗️ Arquitectura

### Clases Principales

#### `TaskManagerGUI`
- **Interfaz principal** de la aplicación
- **Método `run()`** para ejecución interactiva
- **Métodos de visualización** y navegación
- **Gestión de menús** y opciones

#### `TaskManager`
- **Gestión CRUD** de tareas
- **Carga y guardado** automático
- **Métodos de filtrado** y búsqueda

#### `Task`
- **Modelo de datos** para las tareas
- **Serialización** JSON automática
- **Timestamps** de creación y actualización

#### `Priority`
- **Enum** para niveles de prioridad
- **Valores**: Alta, Media, Baja, Sin prioridad

## 🔄 Persistencia

- **Guardado automático** en cada operación
- **Archivo JSON** con codificación UTF-8
- **Recuperación automática** al iniciar
- **Manejo de errores** robusto

## 📈 Estadísticas

La aplicación proporciona estadísticas en tiempo real:
- Total de tareas
- Tareas completadas y pendientes
- Distribución por prioridades
- Tasa de completado

## 🛠️ Instalación y Dependencias

### Requisitos Mínimos
- Python 3.6 o superior
- Solo librerías estándar (para versión de consola)

### Sin Instalación Adicional
La versión de consola funciona inmediatamente:
```bash
python3 task_manager_console.py
```

### Para Versión GUI (Opcional)
```bash
pip install -r requirements.txt
python3 task_manager.py  # Versión moderna
# O
python3 task_manager_simple.py  # Versión básica
```

## 🔍 Solución de Problemas

### No se puede ejecutar la aplicación
```bash
# Verificar Python
python3 --version

# Usar versión de consola
python3 task_manager_console.py
```

### Archivo de tareas corrupto
```bash
# Respaldar datos (si es posible)
cp tasks.json tasks_backup.json

# Eliminar archivo corrupto
rm tasks.json

# La aplicación creará uno nuevo
python3 task_manager_console.py
```

## 🚀 Ejemplos Rápidos

### Crear y usar TaskManagerGUI
```python
# Importar
from task_manager_console import TaskManagerGUI

# Crear aplicación
app = TaskManagerGUI()

# Ejecutar (modo interactivo)
app.run()
```

### Crear tareas programáticamente
```python
from task_manager_console import Task, Priority

# Crear tarea
task = Task("Estudiar Python", "Completar tutorial", Priority.HIGH)

# Agregar a la aplicación
app.task_manager.add_task(task)

# Mostrar todas las tareas
app.display_tasks()
```

## 📝 Licencia

Este proyecto está bajo licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. El código está bien documentado y modularizado para facilitar el desarrollo colaborativo.

---

**TaskManagerGUI** - Tu solución completa para gestión de tareas con prioridades 🎯