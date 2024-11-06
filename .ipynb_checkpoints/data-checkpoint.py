import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Load existing data or create new DataFrame if no CSV is available
try:
    students_df = pd.read_csv("students.csv")
except FileNotFoundError:
    columns = ['Name', "Father's Name", 'Roll Number', 'Class', 'City']
    students_df = pd.DataFrame(columns=columns)

# Function to add a student
def add_student():
    global students_df
    name = entry_name.get()
    father_name = entry_father_name.get()
    roll_number = int(entry_roll_number.get())
    student_class = entry_class.get()
    city = entry_city.get()

    if roll_number in students_df['Roll Number'].values:
        messagebox.showerror("Error", "Student with this roll number already exists.")
    else:
        new_student = pd.DataFrame([[name, father_name, roll_number, student_class, city]], 
                                   columns=students_df.columns)
        students_df = pd.concat([students_df, new_student], ignore_index=True)
        students_df.to_csv("students.csv", index=False)
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
        update_treeview()
        update_summary()

# Function to view students by roll number or city
def view_student():
    roll_number = entry_roll_number.get()
    city_filter = entry_city_filter.get()
    
    if roll_number:  # View by roll number
        roll_number = int(roll_number)
        student_data = students_df[students_df['Roll Number'] == roll_number]
    elif city_filter:  # View by city
        student_data = students_df[students_df['City'].str.lower() == city_filter.lower()]
    else:
        messagebox.showerror("Error", "Please enter a roll number or a city to filter.")
        return
    
    clear_treeview()
    
    if not student_data.empty:
        for _, row in student_data.iterrows():
            tree.insert("", tk.END, values=list(row))
    else:
        messagebox.showerror("Error", "No students found.")

# Function to update student data
def update_student():
    global students_df
    roll_number = int(entry_roll_number.get())
    
    if roll_number in students_df['Roll Number'].values:
        students_df.loc[students_df['Roll Number'] == roll_number, 'Name'] = entry_name.get()
        students_df.loc[students_df['Roll Number'] == roll_number, "Father's Name"] = entry_father_name.get()
        students_df.loc[students_df['Roll Number'] == roll_number, 'Class'] = entry_class.get()
        students_df.loc[students_df['Roll Number'] == roll_number, 'City'] = entry_city.get()
        students_df.to_csv("students.csv", index=False)
        messagebox.showinfo("Success", "Student updated successfully!")
        clear_entries()
        update_treeview()
        update_summary()
    else:
        messagebox.showerror("Error", "Student with this roll number not found.")

# Function to delete a student
def delete_student():
    global students_df
    roll_number = int(entry_roll_number.get())
    
    if roll_number in students_df['Roll Number'].values:
        students_df = students_df[students_df['Roll Number'] != roll_number]
        students_df.to_csv("students.csv", index=False)
        messagebox.showinfo("Success", "Student deleted successfully!")
        clear_entries()
        update_treeview()
        update_summary()
    else:
        messagebox.showerror("Error", "Student with this roll number not found.")

# Function to clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_father_name.delete(0, tk.END)
    entry_roll_number.delete(0, tk.END)
    entry_class.delete(0, tk.END)
    entry_city.delete(0, tk.END)

# Function to clear the Treeview
def clear_treeview():
    for i in tree.get_children():
        tree.delete(i)

# Function to update the Treeview with all student data
def update_treeview():
    clear_treeview()
    for _, row in students_df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Function to update the summary with student count and last roll number
def update_summary():
    total_students = len(students_df)
    last_roll_number = students_df['Roll Number'].max() if total_students > 0 else 0
    summary_label.config(text=f"Total Students: {total_students}, Last Roll Number: {last_roll_number}")

# GUI Setup
root = tk.Tk()
root.title("School Management System")

# Centering the window on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width // 2) - (window_width // 2)
y_coordinate = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Add a label at the top of the GUI
tk.Label(root, text="This software is created by NAK Developers", font=("Arial", 14)).pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Labels and Entry Fields
tk.Label(root, text="Name").pack(padx=10, pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.pack(padx=10, pady=5)

tk.Label(root, text="Father's Name").pack(padx=10, pady=5)
entry_father_name = tk.Entry(root, width=30)
entry_father_name.pack(padx=10, pady=5)

tk.Label(root, text="Roll Number").pack(padx=10, pady=5)
entry_roll_number = tk.Entry(root, width=30)
entry_roll_number.pack(padx=10, pady=5)

tk.Label(root, text="Class").pack(padx=10, pady=5)
entry_class = tk.Entry(root, width=30)
entry_class.pack(padx=10, pady=5)

tk.Label(root, text="City").pack(padx=10, pady=5)
entry_city = tk.Entry(root, width=30)
entry_city.pack(padx=10, pady=5)

# City Filter
tk.Label(root, text="Filter by City").pack(padx=10, pady=5)
entry_city_filter = tk.Entry(root, width=30)
entry_city_filter.pack(padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Student", command=add_student).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(root, text="View Student", command=view_student).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(root, text="Update Student", command=update_student).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(side=tk.LEFT, padx=10, pady=5)

# Summary Label
summary_label = tk.Label(root, text="Total Students: 0, Last Roll Number: 0", font=("Arial", 12))
summary_label.pack(padx=10, pady=10)

# Treeview for displaying student data
tree = ttk.Treeview(root, columns=list(students_df.columns), show='headings')
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Define style for the Treeview to add borders
style = ttk.Style()
style.configure("Treeview", bordercolor="black", borderwidth=1)
style.configure("Treeview.Heading", font=("Arial", 12, 'bold'))

for col in students_df.columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)  # Set width for better visibility


# Make the grid expand with window resizing
root.grid_rowconfigure(10, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Initialize the Treeview with existing data and summary
update_treeview()
update_summary()

# Run the GUI
root.mainloop()
