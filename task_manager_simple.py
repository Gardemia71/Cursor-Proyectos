import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
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
        self.root = tk.Tk()
        self.root.title("Gestor de Tareas")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure styles
        self.root.configure(bg='#2b2b2b')
        
        self.task_manager = TaskManager()
        self.selected_task_id = None
        
        self.setup_ui()
        self.refresh_task_list()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="Gestor de Tareas", 
                              font=("Helvetica", 20, "bold"), 
                              fg='white', bg='#2b2b2b')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Task list
        left_panel = tk.LabelFrame(main_frame, text="Lista de Tareas", 
                                  font=("Helvetica", 10, "bold"),
                                  fg='white', bg='#2b2b2b', 
                                  relief='raised', bd=2)
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(1, weight=1)
        
        # Filter frame
        filter_frame = tk.Frame(left_panel, bg='#2b2b2b')
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(10, 10), padx=10)
        filter_frame.columnconfigure(1, weight=1)
        
        tk.Label(filter_frame, text="Filtrar:", fg='white', bg='#2b2b2b').grid(row=0, column=0, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="Todas")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["Todas", "Pendientes", "Completadas", "Alta Prioridad", "Media Prioridad", "Baja Prioridad"],
                                   state="readonly")
        filter_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        filter_combo.bind("<<ComboboxSelected>>", self.on_filter_change)
        
        # Task listbox with scrollbar
        listbox_frame = tk.Frame(left_panel, bg='#2b2b2b')
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.task_listbox = tk.Listbox(listbox_frame, font=("Consolas", 10),
                                      bg='#3c3c3c', fg='white',
                                      selectbackground='#5c5c5c',
                                      selectforeground='white')
        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)
        
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        button_frame = tk.Frame(left_panel, bg='#2b2b2b')
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10), padx=10)
        
        # Custom button style
        button_config = {
            'font': ('Helvetica', 9, 'bold'),
            'relief': 'raised',
            'bd': 2,
            'pady': 5,
            'padx': 10
        }
        
        tk.Button(button_frame, text="Nueva Tarea", command=self.add_task, 
                 bg='#28a745', fg='white', **button_config).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(button_frame, text="Editar", command=self.edit_task, 
                 bg='#007bff', fg='white', **button_config).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(button_frame, text="Eliminar", command=self.delete_task, 
                 bg='#dc3545', fg='white', **button_config).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(button_frame, text="Completar", command=self.toggle_task_completion, 
                 bg='#17a2b8', fg='white', **button_config).pack(side=tk.LEFT)
        
        # Right panel - Task details
        right_panel = tk.LabelFrame(main_frame, text="Detalles de la Tarea", 
                                   font=("Helvetica", 10, "bold"),
                                   fg='white', bg='#2b2b2b',
                                   relief='raised', bd=2)
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.columnconfigure(0, weight=1)
        
        # Task details
        self.details_frame = tk.Frame(right_panel, bg='#2b2b2b')
        self.details_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), pady=(10, 10), padx=10)
        self.details_frame.columnconfigure(1, weight=1)
        
        tk.Label(self.details_frame, text="Título:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_label = tk.Label(self.details_frame, text="", wraplength=300, 
                                   fg='white', bg='#2b2b2b', justify=tk.LEFT)
        self.title_label.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        tk.Label(self.details_frame, text="Prioridad:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').grid(row=1, column=0, sticky=tk.W, pady=2)
        self.priority_label = tk.Label(self.details_frame, text="", fg='white', bg='#2b2b2b')
        self.priority_label.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        tk.Label(self.details_frame, text="Estado:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').grid(row=2, column=0, sticky=tk.W, pady=2)
        self.status_label = tk.Label(self.details_frame, text="", fg='white', bg='#2b2b2b')
        self.status_label.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        tk.Label(self.details_frame, text="Creada:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').grid(row=3, column=0, sticky=tk.W, pady=2)
        self.created_label = tk.Label(self.details_frame, text="", fg='white', bg='#2b2b2b')
        self.created_label.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        tk.Label(self.details_frame, text="Descripción:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').grid(row=4, column=0, sticky=(tk.W, tk.N), pady=(10, 2))
        
        # Description text area
        desc_frame = tk.Frame(right_panel, bg='#2b2b2b')
        desc_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=10)
        desc_frame.columnconfigure(0, weight=1)
        desc_frame.rowconfigure(0, weight=1)
        
        self.description_text = tk.Text(desc_frame, wrap=tk.WORD, height=10, state=tk.DISABLED, 
                                       font=("Helvetica", 10), bg='#3c3c3c', fg='white',
                                       insertbackground='white')
        self.description_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        desc_scrollbar = tk.Scrollbar(desc_frame, orient="vertical", command=self.description_text.yview)
        desc_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.description_text.configure(yscrollcommand=desc_scrollbar.set)
        
        # Statistics frame
        stats_frame = tk.LabelFrame(right_panel, text="Estadísticas", 
                                   font=("Helvetica", 9, "bold"),
                                   fg='white', bg='#2b2b2b',
                                   relief='raised', bd=1)
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 10), padx=10)
        stats_frame.columnconfigure(0, weight=1)
        
        self.stats_label = tk.Label(stats_frame, text="", font=("Helvetica", 9), 
                                   fg='white', bg='#2b2b2b')
        self.stats_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    
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
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x450")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg='#2b2b2b')
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_dialog(task)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog(self, task):
        main_frame = tk.Frame(self.dialog, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text="Título:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').pack(anchor=tk.W, pady=(0, 5))
        self.title_entry = tk.Entry(main_frame, font=("Helvetica", 10), bg='#3c3c3c', 
                                   fg='white', insertbackground='white')
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Priority
        tk.Label(main_frame, text="Prioridad:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').pack(anchor=tk.W, pady=(0, 5))
        self.priority_var = tk.StringVar()
        priority_frame = tk.Frame(main_frame, bg='#2b2b2b')
        priority_frame.pack(fill=tk.X, pady=(0, 15))
        
        priorities = [(Priority.HIGH, "🔴 Alta"), (Priority.MEDIUM, "🟡 Media"), 
                     (Priority.LOW, "🟢 Baja"), (Priority.NONE, "⚪ Sin prioridad")]
        
        for i, (priority, text) in enumerate(priorities):
            tk.Radiobutton(priority_frame, text=text, variable=self.priority_var, 
                          value=priority.value, fg='white', bg='#2b2b2b',
                          selectcolor='#3c3c3c', activebackground='#3c3c3c',
                          activeforeground='white').pack(side=tk.LEFT, padx=(0, 15))
        
        # Description
        tk.Label(main_frame, text="Descripción:", font=("Helvetica", 10, "bold"), 
                fg='white', bg='#2b2b2b').pack(anchor=tk.W, pady=(0, 5))
        desc_frame = tk.Frame(main_frame, bg='#2b2b2b')
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.description_text = tk.Text(desc_frame, wrap=tk.WORD, height=8, 
                                       font=("Helvetica", 10), bg='#3c3c3c', 
                                       fg='white', insertbackground='white')
        self.description_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        desc_scrollbar = tk.Scrollbar(desc_frame, orient="vertical", command=self.description_text.yview)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.description_text.configure(yscrollcommand=desc_scrollbar.set)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        button_config = {
            'font': ('Helvetica', 10, 'bold'),
            'relief': 'raised',
            'bd': 2,
            'pady': 8,
            'padx': 15
        }
        
        tk.Button(button_frame, text="Cancelar", command=self.cancel, 
                 bg='#6c757d', fg='white', **button_config).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(button_frame, text="Guardar", command=self.save, 
                 bg='#28a745', fg='white', **button_config).pack(side=tk.RIGHT)
        
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