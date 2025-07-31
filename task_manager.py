import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

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
    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("Gestor de Tareas")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.task_manager = TaskManager()
        self.selected_task_id = None
        
        self.setup_ui()
        self.refresh_task_list()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Gestor de Tareas", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Task list
        left_panel = ttk.LabelFrame(main_frame, text="Lista de Tareas", padding="10")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(1, weight=1)
        
        # Filter frame
        filter_frame = ttk.Frame(left_panel)
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        
        ttk.Label(filter_frame, text="Filtrar:").grid(row=0, column=0, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="Todas")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["Todas", "Pendientes", "Completadas", "Alta Prioridad", "Media Prioridad", "Baja Prioridad"],
                                   state="readonly")
        filter_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        filter_combo.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # Task listbox with scrollbar
        listbox_frame = ttk.Frame(left_panel)
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.task_listbox = tk.Listbox(listbox_frame, font=("Consolas", 10))
        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        button_frame = ttk.Frame(left_panel)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Nueva Tarea", command=self.add_task, bootstyle=SUCCESS).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Editar", command=self.edit_task, bootstyle=PRIMARY).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Eliminar", command=self.delete_task, bootstyle=DANGER).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Completar", command=self.toggle_task_completion, bootstyle=INFO).pack(side=tk.LEFT)
        
        # Right panel - Task details
        right_panel = ttk.LabelFrame(main_frame, text="Detalles de la Tarea", padding="10")
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.columnconfigure(0, weight=1)
        
        # Task details
        self.details_frame = ttk.Frame(right_panel)
        self.details_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))
        self.details_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.details_frame, text="Título:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_label = ttk.Label(self.details_frame, text="", wraplength=300)
        self.title_label.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        ttk.Label(self.details_frame, text="Prioridad:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.priority_label = ttk.Label(self.details_frame, text="")
        self.priority_label.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        ttk.Label(self.details_frame, text="Estado:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.status_label = ttk.Label(self.details_frame, text="")
        self.status_label.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        ttk.Label(self.details_frame, text="Creada:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.created_label = ttk.Label(self.details_frame, text="")
        self.created_label.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        ttk.Label(self.details_frame, text="Descripción:", font=("Helvetica", 10, "bold")).grid(row=4, column=0, sticky=(tk.W, tk.N), pady=(10, 2))
        
        # Description text area
        desc_frame = ttk.Frame(right_panel)
        desc_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        desc_frame.columnconfigure(0, weight=1)
        desc_frame.rowconfigure(0, weight=1)
        
        self.description_text = tk.Text(desc_frame, wrap=tk.WORD, height=10, state=tk.DISABLED, font=("Helvetica", 10))
        self.description_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        desc_scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", command=self.description_text.yview)
        desc_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.description_text.configure(yscrollcommand=desc_scrollbar.set)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(right_panel, text="Estadísticas", padding="10")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        stats_frame.columnconfigure(0, weight=1)
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Helvetica", 9))
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
    
    def get_priority_color(self, priority: Priority) -> str:
        colors = {
            Priority.HIGH: "🔴",
            Priority.MEDIUM: "🟡",
            Priority.LOW: "🟢",
            Priority.NONE: "⚪"
        }
        return colors.get(priority, "⚪")
    
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        
        # Get filtered tasks
        filter_value = self.filter_var.get()
        if filter_value == "Todas":
            tasks = self.task_manager.get_tasks()
        elif filter_value == "Pendientes":
            tasks = self.task_manager.get_tasks(completed=False)
        elif filter_value == "Completadas":
            tasks = self.task_manager.get_tasks(completed=True)
        elif filter_value == "Alta Prioridad":
            tasks = self.task_manager.get_tasks_by_priority(Priority.HIGH)
        elif filter_value == "Media Prioridad":
            tasks = self.task_manager.get_tasks_by_priority(Priority.MEDIUM)
        elif filter_value == "Baja Prioridad":
            tasks = self.task_manager.get_tasks_by_priority(Priority.LOW)
        else:
            tasks = self.task_manager.get_tasks()
        
        # Sort tasks by priority and completion status
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2, Priority.NONE: 3}
        tasks.sort(key=lambda t: (t.completed, priority_order[t.priority]))
        
        for task in tasks:
            status_icon = "✓" if task.completed else "○"
            priority_icon = self.get_priority_color(task.priority)
            
            display_text = f"{status_icon} {priority_icon} {task.title}"
            if task.completed:
                display_text = f"[COMPLETADA] {display_text}"
            
            self.task_listbox.insert(tk.END, display_text)
            self.task_listbox.insert(tk.END, "")  # Add space between tasks
        
        self.update_statistics()
    
    def update_statistics(self):
        total_tasks = len(self.task_manager.get_tasks())
        completed_tasks = len(self.task_manager.get_tasks(completed=True))
        pending_tasks = len(self.task_manager.get_tasks(completed=False))
        high_priority = len(self.task_manager.get_tasks_by_priority(Priority.HIGH))
        
        stats_text = f"Total: {total_tasks} | Completadas: {completed_tasks} | Pendientes: {pending_tasks} | Alta prioridad: {high_priority}"
        self.stats_label.config(text=stats_text)
    
    def on_filter_change(self, event):
        self.refresh_task_list()
    
    def on_task_select(self, event):
        selection = self.task_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        # Skip empty lines
        if index % 2 == 1:
            return
        
        task_index = index // 2
        
        # Get filtered tasks to match the display
        filter_value = self.filter_var.get()
        if filter_value == "Todas":
            tasks = self.task_manager.get_tasks()
        elif filter_value == "Pendientes":
            tasks = self.task_manager.get_tasks(completed=False)
        elif filter_value == "Completadas":
            tasks = self.task_manager.get_tasks(completed=True)
        elif filter_value == "Alta Prioridad":
            tasks = self.task_manager.get_tasks_by_priority(Priority.HIGH)
        elif filter_value == "Media Prioridad":
            tasks = self.task_manager.get_tasks_by_priority(Priority.MEDIUM)
        elif filter_value == "Baja Prioridad":
            tasks = self.task_manager.get_tasks_by_priority(Priority.LOW)
        else:
            tasks = self.task_manager.get_tasks()
        
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2, Priority.NONE: 3}
        tasks.sort(key=lambda t: (t.completed, priority_order[t.priority]))
        
        if task_index < len(tasks):
            task = tasks[task_index]
            self.selected_task_id = task.id
            self.show_task_details(task)
    
    def show_task_details(self, task: Task):
        self.title_label.config(text=task.title)
        self.priority_label.config(text=f"{self.get_priority_color(task.priority)} {task.priority.value}")
        self.status_label.config(text="Completada" if task.completed else "Pendiente")
        
        # Format creation date
        try:
            created_date = datetime.fromisoformat(task.created_at)
            formatted_date = created_date.strftime("%d/%m/%Y %H:%M")
        except:
            formatted_date = "Fecha no disponible"
        
        self.created_label.config(text=formatted_date)
        
        # Show description
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(1.0, task.description or "Sin descripción")
        self.description_text.config(state=tk.DISABLED)
    
    def add_task(self):
        dialog = TaskDialog(self.root, "Nueva Tarea")
        if dialog.result:
            task = Task(
                title=dialog.result['title'],
                description=dialog.result['description'],
                priority=dialog.result['priority']
            )
            self.task_manager.add_task(task)
            self.refresh_task_list()
    
    def edit_task(self):
        if not self.selected_task_id:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para editar.")
            return
        
        # Find the selected task
        task = None
        for t in self.task_manager.get_tasks():
            if t.id == self.selected_task_id:
                task = t
                break
        
        if not task:
            messagebox.showerror("Error", "No se pudo encontrar la tarea seleccionada.")
            return
        
        dialog = TaskDialog(self.root, "Editar Tarea", task)
        if dialog.result:
            self.task_manager.update_task(
                task.id,
                title=dialog.result['title'],
                description=dialog.result['description'],
                priority=dialog.result['priority']
            )
            self.refresh_task_list()
            self.show_task_details(task)
    
    def delete_task(self):
        if not self.selected_task_id:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta tarea?"):
            self.task_manager.delete_task(self.selected_task_id)
            self.selected_task_id = None
            self.refresh_task_list()
            
            # Clear details
            self.title_label.config(text="")
            self.priority_label.config(text="")
            self.status_label.config(text="")
            self.created_label.config(text="")
            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            self.description_text.config(state=tk.DISABLED)
    
    def toggle_task_completion(self):
        if not self.selected_task_id:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea.")
            return
        
        # Find the selected task
        task = None
        for t in self.task_manager.get_tasks():
            if t.id == self.selected_task_id:
                task = t
                break
        
        if task:
            self.task_manager.update_task(task.id, completed=not task.completed)
            self.refresh_task_list()
            self.show_task_details(task)
    
    def on_closing(self):
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

class TaskDialog:
    def __init__(self, parent, title, task=None):
        self.result = None
        
        self.dialog = ttk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_dialog(task)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog(self, task):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Título:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, font=("Helvetica", 10))
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Priority
        ttk.Label(main_frame, text="Prioridad:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.priority_var = tk.StringVar()
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=(0, 15))
        
        priorities = [(Priority.HIGH, "🔴 Alta"), (Priority.MEDIUM, "🟡 Media"), 
                     (Priority.LOW, "🟢 Baja"), (Priority.NONE, "⚪ Sin prioridad")]
        
        for i, (priority, text) in enumerate(priorities):
            ttk.Radiobutton(priority_frame, text=text, variable=self.priority_var, 
                           value=priority.value).pack(side=tk.LEFT, padx=(0, 15))
        
        # Description
        ttk.Label(main_frame, text="Descripción:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.description_text = tk.Text(desc_frame, wrap=tk.WORD, height=8, font=("Helvetica", 10))
        self.description_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        desc_scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", command=self.description_text.yview)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.description_text.configure(yscrollcommand=desc_scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(button_frame, text="Cancelar", command=self.cancel, bootstyle=SECONDARY).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Guardar", command=self.save, bootstyle=SUCCESS).pack(side=tk.RIGHT)
        
        # Fill form if editing
        if task:
            self.title_entry.insert(0, task.title)
            self.priority_var.set(task.priority.value)
            self.description_text.insert(1.0, task.description)
        else:
            self.priority_var.set(Priority.NONE.value)
        
        # Focus on title entry
        self.title_entry.focus()
    
    def save(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "El título es obligatorio.")
            return
        
        description = self.description_text.get(1.0, tk.END).strip()
        priority_value = self.priority_var.get()
        priority = Priority(priority_value)
        
        self.result = {
            'title': title,
            'description': description,
            'priority': priority
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

if __name__ == "__main__":
    app = TaskManagerGUI()
    app.run()