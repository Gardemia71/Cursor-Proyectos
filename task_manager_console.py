#!/usr/bin/env python3
import json
import os
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
import sys

class Priority(Enum):
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"
    NONE = "Sin prioridad"

class Task:
    def __init__(self, title: str, description: str = "", priority: Priority = Priority.NONE, completed: bool = False):
        self.id = datetime.now().timestamp()
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        task = cls(data['title'], data['description'])
        task.id = data['id']
        task.priority = Priority(data['priority'])
        task.completed = data['completed']
        task.created_at = data['created_at']
        task.updated_at = data['updated_at']
        return task

class TaskManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
    
    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2, ensure_ascii=False)
    
    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()
    
    def update_task(self, task_id: float, **kwargs):
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                task.updated_at = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: float):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
    
    def get_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        if completed is None:
            return self.tasks
        return [task for task in self.tasks if task.completed == completed]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        return [task for task in self.tasks if task.priority == priority]

class TaskManagerGUI:
    """
    Console-based Task Manager GUI
    Provides a command-line interface for managing tasks with priorities
    """
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.running = True
        
    def get_priority_icon(self, priority: Priority) -> str:
        icons = {
            Priority.HIGH: "🔴",
            Priority.MEDIUM: "🟡", 
            Priority.LOW: "🟢",
            Priority.NONE: "⚪"
        }
        return icons.get(priority, "⚪")
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        print("=" * 60)
        print("            🎯 GESTOR DE TAREAS 🎯")
        print("=" * 60)
        print()
    
    def print_statistics(self):
        total = len(self.task_manager.get_tasks())
        completed = len(self.task_manager.get_tasks(completed=True))
        pending = len(self.task_manager.get_tasks(completed=False))
        high_priority = len(self.task_manager.get_tasks_by_priority(Priority.HIGH))
        
        print(f"📊 ESTADÍSTICAS:")
        print(f"   Total: {total} | Completadas: {completed} | Pendientes: {pending} | Alta prioridad: {high_priority}")
        print("-" * 60)
    
    def display_tasks(self, tasks: List[Task] = None):
        if tasks is None:
            tasks = self.task_manager.get_tasks()
        
        if not tasks:
            print("📝 No hay tareas para mostrar.")
            return
        
        # Sort tasks by priority and completion status
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2, Priority.NONE: 3}
        tasks.sort(key=lambda t: (t.completed, priority_order[t.priority]))
        
        print("📋 LISTA DE TAREAS:")
        print()
        
        for i, task in enumerate(tasks, 1):
            status_icon = "✅" if task.completed else "⏳"
            priority_icon = self.get_priority_icon(task.priority)
            
            # Format creation date
            try:
                created_date = datetime.fromisoformat(task.created_at)
                date_str = created_date.strftime("%d/%m/%Y")
            except:
                date_str = "N/A"
            
            print(f"{i:2d}. {status_icon} {priority_icon} {task.title}")
            print(f"    💾 ID: {int(task.id)}")
            print(f"    📅 Creada: {date_str}")
            print(f"    🎯 Prioridad: {task.priority.value}")
            if task.description:
                print(f"    📝 Descripción: {task.description[:50]}{'...' if len(task.description) > 50 else ''}")
            print()
    
    def show_main_menu(self):
        print("\n🎛️  MENÚ PRINCIPAL:")
        print("1. 📝 Ver todas las tareas")
        print("2. ➕ Crear nueva tarea")
        print("3. ✏️  Editar tarea")
        print("4. ❌ Eliminar tarea")
        print("5. ✅ Marcar como completada")
        print("6. 🔍 Filtrar tareas")
        print("7. 📊 Ver estadísticas detalladas")
        print("8. 🚪 Salir")
        print("-" * 60)
    
    def get_priority_choice(self) -> Priority:
        print("\n🎯 Selecciona la prioridad:")
        print("1. 🔴 Alta")
        print("2. 🟡 Media")
        print("3. 🟢 Baja")
        print("4. ⚪ Sin prioridad")
        
        while True:
            choice = input("Opción (1-4): ").strip()
            if choice == "1":
                return Priority.HIGH
            elif choice == "2":
                return Priority.MEDIUM
            elif choice == "3":
                return Priority.LOW
            elif choice == "4":
                return Priority.NONE
            else:
                print("❌ Opción inválida. Por favor selecciona 1-4.")
    
    def create_task(self):
        print("\n➕ CREAR NUEVA TAREA")
        print("-" * 30)
        
        title = input("📝 Título (obligatorio): ").strip()
        if not title:
            print("❌ El título es obligatorio.")
            return
        
        description = input("📄 Descripción (opcional): ").strip()
        priority = self.get_priority_choice()
        
        task = Task(title, description, priority)
        self.task_manager.add_task(task)
        
        print(f"✅ Tarea '{title}' creada exitosamente!")
        input("\nPresiona Enter para continuar...")
    
    def edit_task(self):
        print("\n✏️  EDITAR TAREA")
        print("-" * 20)
        
        tasks = self.task_manager.get_tasks()
        if not tasks:
            print("❌ No hay tareas para editar.")
            input("Presiona Enter para continuar...")
            return
        
        self.display_tasks()
        
        try:
            task_id = float(input("\n💾 Ingresa el ID de la tarea a editar: "))
            
            # Find task
            task = None
            for t in tasks:
                if t.id == task_id:
                    task = t
                    break
            
            if not task:
                print("❌ Tarea no encontrada.")
                input("Presiona Enter para continuar...")
                return
            
            print(f"\n📝 Editando: {task.title}")
            print("(Deja en blanco para mantener el valor actual)")
            
            new_title = input(f"Nuevo título [{task.title}]: ").strip()
            if new_title:
                task.title = new_title
            
            new_description = input(f"Nueva descripción [{task.description}]: ").strip()
            if new_description:
                task.description = new_description
            
            print(f"Prioridad actual: {task.priority.value}")
            change_priority = input("¿Cambiar prioridad? (s/n): ").strip().lower()
            if change_priority == 's':
                task.priority = self.get_priority_choice()
            
            self.task_manager.save_tasks()
            print("✅ Tarea actualizada exitosamente!")
            
        except ValueError:
            print("❌ ID inválido.")
        
        input("Presiona Enter para continuar...")
    
    def delete_task(self):
        print("\n❌ ELIMINAR TAREA")
        print("-" * 20)
        
        tasks = self.task_manager.get_tasks()
        if not tasks:
            print("❌ No hay tareas para eliminar.")
            input("Presiona Enter para continuar...")
            return
        
        self.display_tasks()
        
        try:
            task_id = float(input("\n💾 Ingresa el ID de la tarea a eliminar: "))
            
            # Find task
            task = None
            for t in tasks:
                if t.id == task_id:
                    task = t
                    break
            
            if not task:
                print("❌ Tarea no encontrada.")
                input("Presiona Enter para continuar...")
                return
            
            confirm = input(f"¿Seguro que quieres eliminar '{task.title}'? (s/n): ").strip().lower()
            if confirm == 's':
                self.task_manager.delete_task(task_id)
                print("✅ Tarea eliminada exitosamente!")
            else:
                print("❌ Operación cancelada.")
        
        except ValueError:
            print("❌ ID inválido.")
        
        input("Presiona Enter para continuar...")
    
    def toggle_completion(self):
        print("\n✅ MARCAR COMO COMPLETADA")
        print("-" * 30)
        
        tasks = self.task_manager.get_tasks(completed=False)
        if not tasks:
            print("❌ No hay tareas pendientes.")
            input("Presiona Enter para continuar...")
            return
        
        self.display_tasks(tasks)
        
        try:
            task_id = float(input("\n💾 Ingresa el ID de la tarea: "))
            
            # Find task
            task = None
            for t in tasks:
                if t.id == task_id:
                    task = t
                    break
            
            if not task:
                print("❌ Tarea no encontrada.")
                input("Presiona Enter para continuar...")
                return
            
            self.task_manager.update_task(task_id, completed=True)
            print(f"✅ Tarea '{task.title}' marcada como completada!")
        
        except ValueError:
            print("❌ ID inválido.")
        
        input("Presiona Enter para continuar...")
    
    def filter_tasks(self):
        print("\n🔍 FILTRAR TAREAS")
        print("-" * 20)
        print("1. 📋 Todas las tareas")
        print("2. ⏳ Solo pendientes")
        print("3. ✅ Solo completadas")
        print("4. 🔴 Alta prioridad")
        print("5. 🟡 Media prioridad")
        print("6. 🟢 Baja prioridad")
        
        choice = input("\nOpción (1-6): ").strip()
        
        if choice == "1":
            tasks = self.task_manager.get_tasks()
        elif choice == "2":
            tasks = self.task_manager.get_tasks(completed=False)
        elif choice == "3":
            tasks = self.task_manager.get_tasks(completed=True)
        elif choice == "4":
            tasks = self.task_manager.get_tasks_by_priority(Priority.HIGH)
        elif choice == "5":
            tasks = self.task_manager.get_tasks_by_priority(Priority.MEDIUM)
        elif choice == "6":
            tasks = self.task_manager.get_tasks_by_priority(Priority.LOW)
        else:
            print("❌ Opción inválida.")
            input("Presiona Enter para continuar...")
            return
        
        print()
        self.display_tasks(tasks)
        input("\nPresiona Enter para continuar...")
    
    def show_detailed_statistics(self):
        print("\n📊 ESTADÍSTICAS DETALLADAS")
        print("-" * 40)
        
        all_tasks = self.task_manager.get_tasks()
        completed_tasks = self.task_manager.get_tasks(completed=True)
        pending_tasks = self.task_manager.get_tasks(completed=False)
        
        high_priority = self.task_manager.get_tasks_by_priority(Priority.HIGH)
        medium_priority = self.task_manager.get_tasks_by_priority(Priority.MEDIUM)
        low_priority = self.task_manager.get_tasks_by_priority(Priority.LOW)
        no_priority = self.task_manager.get_tasks_by_priority(Priority.NONE)
        
        print(f"📋 Total de tareas: {len(all_tasks)}")
        print(f"✅ Completadas: {len(completed_tasks)}")
        print(f"⏳ Pendientes: {len(pending_tasks)}")
        print()
        print("🎯 Por prioridad:")
        print(f"   🔴 Alta: {len(high_priority)}")
        print(f"   🟡 Media: {len(medium_priority)}")
        print(f"   🟢 Baja: {len(low_priority)}")
        print(f"   ⚪ Sin prioridad: {len(no_priority)}")
        
        if all_tasks:
            completion_rate = (len(completed_tasks) / len(all_tasks)) * 100
            print(f"\n📈 Tasa de completado: {completion_rate:.1f}%")
        
        input("\nPresiona Enter para continuar...")
    
    def run(self):
        """Método principal para ejecutar la aplicación TaskManagerGUI"""
        while self.running:
            self.clear_screen()
            self.print_header()
            self.print_statistics()
            self.show_main_menu()
            
            choice = input("Selecciona una opción (1-8): ").strip()
            
            if choice == "1":
                self.clear_screen()
                self.print_header()
                self.display_tasks()
                input("\nPresiona Enter para continuar...")
            elif choice == "2":
                self.create_task()
            elif choice == "3":
                self.edit_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.toggle_completion()
            elif choice == "6":
                self.filter_tasks()
            elif choice == "7":
                self.show_detailed_statistics()
            elif choice == "8":
                print("\n👋 ¡Gracias por usar el Gestor de Tareas!")
                print("💾 Todas las tareas han sido guardadas automáticamente.")
                self.running = False
            else:
                print("❌ Opción inválida. Por favor selecciona 1-8.")
                input("Presiona Enter para continuar...")

def main():
    """Función principal para inicializar y ejecutar TaskManagerGUI"""
    try:
        print("🚀 Iniciando TaskManagerGUI...")
        app = TaskManagerGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Aplicación interrumpida por el usuario.")
        print("💾 Las tareas se han guardado automáticamente.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💾 Las tareas se han guardado automáticamente.")

if __name__ == "__main__":
    main()