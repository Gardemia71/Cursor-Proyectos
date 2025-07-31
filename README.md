# Gestor de Tareas de Escritorio

Una aplicación de escritorio moderna para gestionar tareas con sistema de prioridades opcional. Desarrollada en Python con una interfaz gráfica intuitiva y almacenamiento persistente de datos.

## Características

### ✨ Funcionalidades Principales
- **Crear, editar y eliminar tareas** con facilidad
- **Sistema de prioridades opcional** (Alta, Media, Baja, Sin prioridad)
- **Marcar tareas como completadas** con un clic
- **Filtrado avanzado** por estado y prioridad
- **Interfaz visual intuitiva** con iconos de colores para prioridades
- **Almacenamiento persistente** en formato JSON
- **Estadísticas en tiempo real** de tus tareas

### 🎨 Interfaz de Usuario
- **Tema oscuro moderno** usando ttkbootstrap
- **Panel dividido** con lista de tareas y detalles
- **Iconos visuales** para estados y prioridades:
  - 🔴 Alta prioridad
  - 🟡 Media prioridad  
  - 🟢 Baja prioridad
  - ⚪ Sin prioridad
  - ✓ Tarea completada
  - ○ Tarea pendiente

### 🔍 Sistema de Filtros
- Todas las tareas
- Solo pendientes
- Solo completadas
- Por nivel de prioridad (Alta, Media, Baja)

## Instalación

### Requisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona o descarga este repositorio**
```bash
git clone <url-del-repositorio>
cd gestor-tareas
```

2. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecuta la aplicación**
```bash
python task_manager.py
```

## Uso

### Crear una Nueva Tarea
1. Haz clic en el botón **"Nueva Tarea"**
2. Completa el formulario:
   - **Título**: Nombre de la tarea (obligatorio)
   - **Prioridad**: Selecciona Alta, Media, Baja o Sin prioridad
   - **Descripción**: Detalles adicionales (opcional)
3. Haz clic en **"Guardar"**

### Editar una Tarea
1. Selecciona una tarea de la lista
2. Haz clic en **"Editar"**
3. Modifica los campos necesarios
4. Haz clic en **"Guardar"**

### Completar una Tarea
1. Selecciona una tarea de la lista
2. Haz clic en **"Completar"**
3. La tarea se marcará como completada y aparecerá con ✓

### Eliminar una Tarea
1. Selecciona una tarea de la lista
2. Haz clic en **"Eliminar"**
3. Confirma la eliminación en el diálogo

### Filtrar Tareas
- Usa el menú desplegable **"Filtrar"** para mostrar:
  - Todas las tareas
  - Solo pendientes
  - Solo completadas
  - Por prioridad específica

## Estructura del Proyecto

```
gestor-tareas/
├── task_manager.py      # Aplicación principal
├── requirements.txt     # Dependencias
├── README.md           # Este archivo
└── tasks.json          # Archivo de datos (se crea automáticamente)
```

## Estructura de Datos

Las tareas se almacenan en formato JSON con la siguiente estructura:

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

## Dependencias

- **ttkbootstrap 1.10.1**: Framework de UI moderno para tkinter
- **Pillow 10.0.0**: Procesamiento de imágenes (requerido por ttkbootstrap)

## Características Técnicas

### Arquitectura
- **Modelo-Vista-Controlador (MVC)**: Separación clara de responsabilidades
- **Orientada a objetos**: Clases Task, TaskManager y TaskManagerGUI
- **Persistencia**: Almacenamiento automático en JSON

### Componentes Principales

#### Clase Task
- Modelo de datos para las tareas
- Métodos de serialización (to_dict/from_dict)
- Timestamps automáticos

#### Clase TaskManager  
- Gestión CRUD de tareas
- Carga y guardado automático
- Métodos de filtrado

#### Clase TaskManagerGUI
- Interfaz gráfica principal
- Manejo de eventos
- Actualización en tiempo real

#### Clase TaskDialog
- Diálogo modal para crear/editar tareas
- Validación de formularios
- Interfaz intuitiva

## Mejoras Futuras

- [ ] Fechas de vencimiento
- [ ] Categorías/etiquetas
- [ ] Recordatorios/notificaciones
- [ ] Exportar a diferentes formatos
- [ ] Búsqueda de texto
- [ ] Atajos de teclado
- [ ] Temas personalizables
- [ ] Sincronización en la nube

## Solución de Problemas

### La aplicación no inicia
- Verifica que Python 3.7+ esté instalado: `python --version`
- Instala las dependencias: `pip install -r requirements.txt`

### Error de importación de ttkbootstrap
```bash
pip install --upgrade ttkbootstrap
```

### Archivo tasks.json corrupto
- Elimina el archivo `tasks.json` (se perderán los datos)
- La aplicación creará uno nuevo al iniciarse

## Licencia

Este proyecto está bajo licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Confirma tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Sube la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio del proyecto.