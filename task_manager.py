#!/usr/bin/env python3
"""
Gestor de Tareas de Escritorio
Una aplicación GUI para gestionar tareas con prioridades opcionales
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from enum import Enum

class Priority(Enum):
    NINGUNA = "Ninguna"
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Crítica"

class Task:
    def __init__(self, title, description="", priority=Priority.NINGUNA, completed=False, created_at=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=Priority(data.get('priority', Priority.NINGUNA.value)),
            completed=data.get('completed', False),
            created_at=data.get('created_at')
        )

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.data_file = "tasks.json"
        self.load_tasks()
    
    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()
    
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
    
    def toggle_task_completion(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = not self.tasks[index].completed
            self.save_tasks()
    
    def get_tasks(self, filter_priority=None, show_completed=True):
        filtered_tasks = []
        for task in self.tasks:
            if not show_completed and task.completed:
                continue
            if filter_priority and task.priority != filter_priority:
                continue
            filtered_tasks.append(task)
        return filtered_tasks
    
    def save_tasks(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando tareas: {e}")
    
    def load_tasks(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
        except Exception as e:
            print(f"Error cargando tareas: {e}")
            self.tasks = []

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("800x600")
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        self.task_manager = TaskManager()
        self.setup_ui()
        self.refresh_task_list()
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestor de Tareas", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame para controles
        controls_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Botón agregar tarea
        ttk.Button(controls_frame, text="➕ Agregar Tarea", 
                  command=self.add_task_dialog).grid(row=0, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Filtro por prioridad
        ttk.Label(controls_frame, text="Filtrar por prioridad:").grid(row=1, column=0, pady=5, sticky=tk.W)
        
        self.priority_filter = ttk.Combobox(controls_frame, state="readonly")
        self.priority_filter['values'] = ["Todas"] + [p.value for p in Priority]
        self.priority_filter.set("Todas")
        self.priority_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        self.priority_filter.grid(row=2, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Checkbox para mostrar completadas
        self.show_completed = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls_frame, text="Mostrar completadas", 
                       variable=self.show_completed,
                       command=self.refresh_task_list).grid(row=3, column=0, pady=5, sticky=tk.W)
        
        # Botones de acción
        ttk.Button(controls_frame, text="✓ Marcar Completada", 
                  command=self.toggle_completion).grid(row=4, column=0, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(controls_frame, text="✏️ Editar Tarea", 
                  command=self.edit_task).grid(row=5, column=0, pady=5, sticky=tk.W+tk.E)
        
        ttk.Button(controls_frame, text="🗑️ Eliminar Tarea", 
                  command=self.delete_task).grid(row=6, column=0, pady=5, sticky=tk.W+tk.E)
        
        # Configurar el ancho del frame de controles
        controls_frame.columnconfigure(0, weight=1)
        
        # Frame para lista de tareas
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Tareas", padding="10")
        list_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview para mostrar tareas
        columns = ("Estado", "Título", "Prioridad", "Fecha")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.task_tree.heading("Estado", text="Estado")
        self.task_tree.heading("Título", text="Título")
        self.task_tree.heading("Prioridad", text="Prioridad")
        self.task_tree.heading("Fecha", text="Fecha Creación")
        
        self.task_tree.column("Estado", width=80, minwidth=80)
        self.task_tree.column("Título", width=300, minwidth=200)
        self.task_tree.column("Prioridad", width=100, minwidth=80)
        self.task_tree.column("Fecha", width=150, minwidth=100)
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Frame para detalles de tarea
        details_frame = ttk.LabelFrame(main_frame, text="Detalles de la Tarea", padding="10")
        details_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        details_frame.columnconfigure(0, weight=1)
        
        self.details_text = tk.Text(details_frame, height=4, wrap=tk.WORD)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind para selección de tarea
        self.task_tree.bind('<<TreeviewSelect>>', self.on_task_select)
        
        # Estadísticas
        self.stats_label = ttk.Label(main_frame, text="")
        self.stats_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))
    
    def add_task_dialog(self):
        dialog = TaskDialog(self.root, "Agregar Nueva Tarea")
        if dialog.result:
            task = Task(
                title=dialog.result['title'],
                description=dialog.result['description'],
                priority=dialog.result['priority']
            )
            self.task_manager.add_task(task)
            self.refresh_task_list()
    
    def edit_task(self):
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para editar.")
            return
        
        item = selection[0]
        task_index = self.task_tree.index(item)
        
        # Obtener tareas filtradas para encontrar el índice correcto
        filtered_tasks = self.get_filtered_tasks()
        if task_index >= len(filtered_tasks):
            return
        
        task = filtered_tasks[task_index]
        original_index = self.task_manager.tasks.index(task)
        
        dialog = TaskDialog(self.root, "Editar Tarea", task)
        if dialog.result:
            self.task_manager.tasks[original_index].title = dialog.result['title']
            self.task_manager.tasks[original_index].description = dialog.result['description']
            self.task_manager.tasks[original_index].priority = dialog.result['priority']
            self.task_manager.save_tasks()
            self.refresh_task_list()
    
    def delete_task(self):
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta tarea?"):
            item = selection[0]
            task_index = self.task_tree.index(item)
            
            # Obtener tareas filtradas para encontrar el índice correcto
            filtered_tasks = self.get_filtered_tasks()
            if task_index >= len(filtered_tasks):
                return
            
            task = filtered_tasks[task_index]
            original_index = self.task_manager.tasks.index(task)
            
            self.task_manager.remove_task(original_index)
            self.refresh_task_list()
    
    def toggle_completion(self):
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea.")
            return
        
        item = selection[0]
        task_index = self.task_tree.index(item)
        
        # Obtener tareas filtradas para encontrar el índice correcto
        filtered_tasks = self.get_filtered_tasks()
        if task_index >= len(filtered_tasks):
            return
        
        task = filtered_tasks[task_index]
        original_index = self.task_manager.tasks.index(task)
        
        self.task_manager.toggle_task_completion(original_index)
        self.refresh_task_list()
    
    def get_filtered_tasks(self):
        filter_priority = None
        if self.priority_filter.get() != "Todas":
            filter_priority = Priority(self.priority_filter.get())
        
        return self.task_manager.get_tasks(
            filter_priority=filter_priority,
            show_completed=self.show_completed.get()
        )
    
    def refresh_task_list(self):
        # Limpiar lista actual
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Obtener tareas filtradas
        filtered_tasks = self.get_filtered_tasks()
        
        # Agregar tareas al treeview
        for task in filtered_tasks:
            status = "✓ Completada" if task.completed else "⏳ Pendiente"
            date_str = datetime.fromisoformat(task.created_at).strftime("%d/%m/%Y %H:%M")
            
            # Configurar colores según prioridad
            tags = []
            if task.priority == Priority.CRITICA:
                tags = ["critical"]
            elif task.priority == Priority.ALTA:
                tags = ["high"]
            elif task.priority == Priority.MEDIA:
                tags = ["medium"]
            elif task.priority == Priority.BAJA:
                tags = ["low"]
            
            if task.completed:
                tags.append("completed")
            
            self.task_tree.insert("", tk.END, values=(
                status, task.title, task.priority.value, date_str
            ), tags=tags)
        
        # Configurar colores de las etiquetas
        self.task_tree.tag_configure("critical", background="#ffebee")
        self.task_tree.tag_configure("high", background="#fff3e0")
        self.task_tree.tag_configure("medium", background="#f3e5f5")
        self.task_tree.tag_configure("low", background="#e8f5e8")
        self.task_tree.tag_configure("completed", foreground="#666666")
        
        # Actualizar estadísticas
        self.update_stats()
    
    def update_stats(self):
        total_tasks = len(self.task_manager.tasks)
        completed_tasks = len([t for t in self.task_manager.tasks if t.completed])
        pending_tasks = total_tasks - completed_tasks
        
        stats_text = f"Total: {total_tasks} | Completadas: {completed_tasks} | Pendientes: {pending_tasks}"
        self.stats_label.config(text=stats_text)
    
    def on_task_select(self, event):
        selection = self.task_tree.selection()
        if not selection:
            self.details_text.delete(1.0, tk.END)
            return
        
        item = selection[0]
        task_index = self.task_tree.index(item)
        
        # Obtener tareas filtradas para encontrar el índice correcto
        filtered_tasks = self.get_filtered_tasks()
        if task_index >= len(filtered_tasks):
            return
        
        task = filtered_tasks[task_index]
        
        # Mostrar detalles en el área de texto
        self.details_text.delete(1.0, tk.END)
        details = f"Título: {task.title}\n"
        details += f"Prioridad: {task.priority.value}\n"
        details += f"Estado: {'Completada' if task.completed else 'Pendiente'}\n"
        details += f"Fecha de creación: {datetime.fromisoformat(task.created_at).strftime('%d/%m/%Y %H:%M')}\n"
        details += f"\nDescripción:\n{task.description}"
        
        self.details_text.insert(1.0, details)
    
    def on_closing(self):
        self.task_manager.save_tasks()
        self.root.destroy()

class TaskDialog:
    def __init__(self, parent, title, task=None):
        self.result = None
        
        # Crear ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Centrar la ventana
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo título
        ttk.Label(main_frame, text="Título de la tarea:").pack(anchor=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, width=50)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Campo prioridad
        ttk.Label(main_frame, text="Prioridad:").pack(anchor=tk.W, pady=(0, 5))
        self.priority_combo = ttk.Combobox(main_frame, state="readonly")
        self.priority_combo['values'] = [p.value for p in Priority]
        self.priority_combo.set(Priority.NINGUNA.value)
        self.priority_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Campo descripción
        ttk.Label(main_frame, text="Descripción:").pack(anchor=tk.W, pady=(0, 5))
        self.description_text = tk.Text(main_frame, height=6, wrap=tk.WORD)
        self.description_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Guardar", 
                  command=self.save).pack(side=tk.RIGHT)
        
        # Si se está editando una tarea, llenar los campos
        if task:
            self.title_entry.insert(0, task.title)
            self.priority_combo.set(task.priority.value)
            self.description_text.insert(1.0, task.description)
        
        # Hacer focus en el título
        self.title_entry.focus()
        
        # Esperar hasta que se cierre la ventana
        self.dialog.wait_window()
    
    def save(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "El título es obligatorio.")
            return
        
        self.result = {
            'title': title,
            'description': self.description_text.get(1.0, tk.END).strip(),
            'priority': Priority(self.priority_combo.get())
        }
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

def main():
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()