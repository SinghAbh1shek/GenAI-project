import tkinter as tk
from tkinter import messagebox, StringVar, Listbox, Scrollbar

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List App')
        self.root.geometry('300x400')

        self.task_var = StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Frame for the Entry and Add Task Button
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Entry to add new tasks
        self.task_entry = tk.Entry(frame, textvariable=self.task_var, width=30)
        self.task_entry.pack(side=tk.LEFT)

        # Button to add task
        add_task_btn = tk.Button(frame, text='Add Task', command=self.add_task)
        add_task_btn.pack(side=tk.LEFT)

        # Listbox to display tasks
        self.task_listbox = Listbox(self.root, width=40, height=15)
        self.task_listbox.pack(pady=10)

        # Scrollbar for the Listbox
        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Button to remove selected task
        remove_task_btn = tk.Button(self.root, text='Remove Task', command=self.remove_task)
        remove_task_btn.pack(pady=10)

    def add_task(self):
        task = self.task_var.get()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_var.set('')  # Clear the entry
        else:
            messagebox.showwarning('Warning', 'Please enter a task.')

    def remove_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_task_index)
        except:
            messagebox.showwarning('Warning', 'Please select a task to remove.')

if __name__ == '__main__':
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()