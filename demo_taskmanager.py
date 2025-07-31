#!/usr/bin/env python3
"""
Demo script para TaskManagerGUI
Muestra cómo usar la aplicación TaskManagerGUI programáticamente
"""

from task_manager_console import TaskManagerGUI, Task, Priority
import time

def demo_taskmanager_gui():
    """
    Demostración de las capacidades de TaskManagerGUI
    """
    print("🎯 DEMO: TaskManagerGUI")
    print("=" * 50)
    
    # Crear instancia de la aplicación
    print("🚀 Creando instancia de TaskManagerGUI...")
    app = TaskManagerGUI()
    
    # Acceder al gestor de tareas
    task_manager = app.task_manager
    
    print("✅ TaskManagerGUI inicializada correctamente!")
    print()
    
    # Crear algunas tareas de demostración
    print("📝 Creando tareas de demostración...")
    
    # Tarea de alta prioridad
    task1 = Task(
        title="Completar presentación del proyecto",
        description="Preparar slides y ensayar la presentación para la reunión de mañana",
        priority=Priority.HIGH
    )
    task_manager.add_task(task1)
    
    # Tarea de media prioridad
    task2 = Task(
        title="Revisar documentación",
        description="Leer y actualizar la documentación técnica del sistema",
        priority=Priority.MEDIUM
    )
    task_manager.add_task(task2)
    
    # Tarea de baja prioridad
    task3 = Task(
        title="Organizar escritorio",
        description="Limpiar y organizar el área de trabajo",
        priority=Priority.LOW
    )
    task_manager.add_task(task3)
    
    # Tarea sin prioridad
    task4 = Task(
        title="Llamar al dentista",
        description="Programar cita para limpieza dental",
        priority=Priority.NONE
    )
    task_manager.add_task(task4)
    
    print(f"✅ {len(task_manager.get_tasks())} tareas creadas exitosamente!")
    print()
    
    # Mostrar estadísticas
    print("📊 ESTADÍSTICAS ACTUALES:")
    total = len(task_manager.get_tasks())
    completed = len(task_manager.get_tasks(completed=True))
    pending = len(task_manager.get_tasks(completed=False))
    high_priority = len(task_manager.get_tasks_by_priority(Priority.HIGH))
    
    print(f"   📋 Total: {total}")
    print(f"   ✅ Completadas: {completed}")
    print(f"   ⏳ Pendientes: {pending}")
    print(f"   🔴 Alta prioridad: {high_priority}")
    print()
    
    # Mostrar todas las tareas usando el método de la aplicación
    print("📋 TAREAS ACTUALES:")
    app.display_tasks()
    
    # Completar una tarea
    print("✅ Marcando una tarea como completada...")
    task_manager.update_task(task3.id, completed=True)
    
    # Mostrar estadísticas actualizadas
    print("📊 ESTADÍSTICAS DESPUÉS DEL CAMBIO:")
    completed = len(task_manager.get_tasks(completed=True))
    pending = len(task_manager.get_tasks(completed=False))
    print(f"   ✅ Completadas: {completed}")
    print(f"   ⏳ Pendientes: {pending}")
    print()
    
    # Demostrar filtros
    print("🔍 DEMO DE FILTROS:")
    print()
    
    print("🔴 Tareas de alta prioridad:")
    high_priority_tasks = task_manager.get_tasks_by_priority(Priority.HIGH)
    app.display_tasks(high_priority_tasks)
    
    print("⏳ Tareas pendientes:")
    pending_tasks = task_manager.get_tasks(completed=False)
    app.display_tasks(pending_tasks)
    
    # Mostrar información sobre la clase TaskManagerGUI
    print("ℹ️  INFORMACIÓN SOBRE TaskManagerGUI:")
    print(f"   📁 Archivo de datos: {task_manager.filename}")
    print(f"   🏗️  Tipo de aplicación: {type(app).__name__}")
    print(f"   📋 Métodos principales: run(), display_tasks(), create_task(), edit_task()")
    print()
    
    print("🎉 Demo completado exitosamente!")
    print("💡 Para usar la aplicación interactivamente, ejecuta:")
    print("   python3 task_manager_console.py")
    print()
    print("   O crea una instancia programáticamente:")
    print("   from task_manager_console import TaskManagerGUI")
    print("   app = TaskManagerGUI()")
    print("   app.run()  # Para modo interactivo")

def show_usage_examples():
    """
    Muestra ejemplos de uso programático
    """
    print("\n💡 EJEMPLOS DE USO PROGRAMÁTICO:")
    print("=" * 40)
    
    examples = [
        ("Crear aplicación", "app = TaskManagerGUI()"),
        ("Ejecutar aplicación", "app.run()"),
        ("Acceder al gestor", "manager = app.task_manager"),
        ("Crear tarea", "task = Task('Título', 'Descripción', Priority.HIGH)"),
        ("Agregar tarea", "manager.add_task(task)"),
        ("Obtener tareas", "todas = manager.get_tasks()"),
        ("Filtrar por prioridad", "altas = manager.get_tasks_by_priority(Priority.HIGH)"),
        ("Marcar completada", "manager.update_task(task_id, completed=True)"),
        ("Eliminar tarea", "manager.delete_task(task_id)"),
        ("Mostrar tareas", "app.display_tasks()"),
        ("Estadísticas", "app.print_statistics()"),
    ]
    
    for description, code in examples:
        print(f"📝 {description:20} → {code}")
    
    print()

if __name__ == "__main__":
    try:
        demo_taskmanager_gui()
        show_usage_examples()
    except Exception as e:
        print(f"❌ Error en la demo: {e}")
        print("💾 Los datos se mantienen seguros en tasks.json")