from tkinter import *
from tkinter import messagebox
import json, os

root = Tk()
root.title("Teacher Organizer")
root.geometry("600x500")
root.config(background="#E0FFFF") 

# ملف التخزين
DATA_FILE = "save_data.json"

# تحميل البيانات من الملف عند التشغيل
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

# حفظ البيانات في الملف
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# إضافة المادة والمستوى
def add_subject():
    window_subject = Toplevel(root)
    window_subject.title("Add New Subject")
    window_subject.config(background="#E0FFFF")

    Label(window_subject, text="ADD NEW SUBJECT", font=("Noto Sans", 20, "bold"),
          bg="#E0FFFF", fg="#1E90FF").pack(pady=10)

    Label(window_subject, text="SUBJECT NAME:", font=("Noto Sans", 15, "bold"),
          bg="#E0FFFF").pack(pady=5)
    entry_subject_name = Entry(window_subject, font=("Libre Baskerville", 12))
    entry_subject_name.pack(pady=5)

    Label(window_subject, text="LEVEL:", font=("Noto Sans", 15, "bold"),
          bg="#E0FFFF").pack(pady=5)
    entry_level_name = Entry(window_subject, font=("Libre Baskerville", 12))
    entry_level_name.pack(pady=5)

    def save_subject():
        subject_name = entry_subject_name.get().strip()
        level_name = entry_level_name.get().strip()

        if subject_name != "" and level_name != "":
            if subject_name not in data:
                data[subject_name] = {}
            
            if level_name not in data[subject_name]:
                data[subject_name][level_name] = []
            
            save_data()
            messagebox.showinfo("Saved", f"Subject '{subject_name}' with level '{level_name}' was added successfully.")
            window_subject.destroy()  
        else:
            messagebox.showwarning("Warning", "Please enter all required data.")

    Button(window_subject, text="Save", fg="#FFFFFF", bg="#00BFFF",
           font=("Noto Sans", 14, "bold"), command=save_subject).pack(pady=10)

# إضافة درس
def add_lesson():
    window_lesson = Toplevel(root)
    window_lesson.title("Add Lesson")
    window_lesson.config(background="#E0FFFF")

    Label(window_lesson, text="SUBJECT", font=("Noto Sans", 15, "bold"), bg="#E0FFFF").pack(pady=5)
    
    selected_subject = StringVar(window_lesson)
    subjects = list(data.keys()) if data else [""]
    selected_subject.set("Select Subject")

    subject_menu = OptionMenu(window_lesson, selected_subject, *subjects)
    subject_menu.pack(pady=5)

    Label(window_lesson, text="LEVEL", font=("Noto Sans", 15, "bold"), bg="#E0FFFF").pack(pady=5)
    selected_level = StringVar(window_lesson)
    selected_level.set("Select Level")
    level_menu = OptionMenu(window_lesson, selected_level, "")
    level_menu.pack(pady=5)

    def update_levels(*args):
        subject = selected_subject.get()
        levels_list = list(data[subject].keys()) if subject in data else [""]
        
        menu = level_menu["menu"]
        menu.delete(0, "end")
        
        for level_name in levels_list:
            menu.add_command(label=level_name, command=lambda lvl=level_name: selected_level.set(lvl))
        
        if levels_list:
            selected_level.set("Select Level")

    selected_subject.trace_add("write", update_levels)
    update_levels()

    Label(window_lesson, text="LESSON TITLE:", font=("Noto Sans", 15, "bold"), bg="#E0FFFF").pack(pady=5)
    entry_lesson_title = Entry(window_lesson, font=("Libre Baskerville", 12))
    entry_lesson_title.pack(pady=5)

    Label(window_lesson, text="LESSON DESCRIPTION:", font=("Noto Sans", 15, "bold"), bg="#E0FFFF").pack(pady=5)
    text_lesson_description = Text(window_lesson, height=5, width=40, font=("Libre Baskerville", 12), bg="#FFFACD")
    text_lesson_description.pack(pady=5)

    def save_lesson():
        subject = selected_subject.get()
        level = selected_level.get()
        title = entry_lesson_title.get().strip()
        description = text_lesson_description.get("1.0", "end").strip()

        if subject in data and level in data[subject]:
            if title != "" and description != "":
                data[subject][level].append({"title": title, "description": description})
                save_data()
                messagebox.showinfo("Saved", "Lesson saved successfully!")
                window_lesson.destroy()
            else:
                messagebox.showwarning("Warning", "Please fill all fields correctly.")
        else:
            messagebox.showwarning("Warning", "Please select a valid subject and level.")

    Button(window_lesson, text="Save Lesson", fg="#FFFFFF", bg="#00BFFF",
           font=("Noto Sans", 14, "bold"), padx=10, pady=5, command=save_lesson).pack(pady=10)

# عرض الدروس
def view_lessons():
    window_view = Toplevel(root)
    window_view.title("View Lessons")
    window_view.config(background="#E0FFFF")

    Label(window_view, text="SUBJECT", font=("Noto Sans", 15, "bold"), bg="#E0FFFF").pack(pady=5)
    selected_subject = StringVar(window_view)
    subjects_list = list(data.keys()) if data else [""]
    selected_subject.set("Select Subject")
    subject_menu = OptionMenu(window_view, selected_subject, *subjects_list)
    subject_menu.pack(pady=5)

    Label(window_view, text="LEVEL", font=("Noto Sans", 15, "bold"), bg="#E0FFFF").pack(pady=5)
    selected_level = StringVar(window_view)
    selected_level.set("Select Level")
    level_menu = OptionMenu(window_view, selected_level, "")
    level_menu.pack(pady=5)

    def update_levels_view(*args):
        subject = selected_subject.get()
        levels_list = list(data[subject].keys()) if subject in data else [""]
        
        menu = level_menu["menu"]
        menu.delete(0, "end")
        
        for level_name in levels_list:
            menu.add_command(label=level_name, command=lambda lvl=level_name: selected_level.set(lvl))
        if levels_list:
            selected_level.set("Select Level")

    selected_subject.trace_add("write", update_levels_view)

    Label(window_view, text="LESSONS", font=("Noto Sans", 15, "bold"), bg="#E0FFFF").pack(pady=5)
    selected_lesson = StringVar(window_view)
    selected_lesson.set("Select Lesson")
    lesson_menu = OptionMenu(window_view, selected_lesson, "")
    lesson_menu.pack(pady=5)

    def update_lessons_list(*args):
        subject = selected_subject.get()
        level = selected_level.get()
        
        lessons_titles = [lesson["title"] for lesson in data[subject][level]] if subject in data and level in data[subject] else [""]
        
        menu = lesson_menu["menu"]
        menu.delete(0, "end")
        for lesson_title in lessons_titles:
            menu.add_command(label=lesson_title, command=lambda value=lesson_title: selected_lesson.set(value))
        if lessons_titles:
            selected_lesson.set("Select Lesson")

    selected_level.trace_add("write", update_lessons_list)

    text_display = Text(window_view, height=10, width=50, font=("Libre Baskerville", 12),
                        state="disabled", bg="#FFFACD")
    text_display.pack(pady=10)

    def show_lesson():
        subject = selected_subject.get()
        level = selected_level.get()
        lesson_title = selected_lesson.get()

        if subject == "Select Subject" or level == "Select Level" or lesson_title == "Select Lesson":
            messagebox.showwarning("Warning", "Please select subject, level, and lesson before displaying.")
            return

        if subject in data and level in data[subject]:
            for lesson in data[subject][level]:
                if lesson["title"] == lesson_title:
                    text_display.config(state="normal")
                    text_display.delete("1.0", "end")
                    text_display.insert("end", f"Title: {lesson['title']}\n\nDescription:\n{lesson['description']}")
                    text_display.config(state="disabled")
                    return

    Button(window_view, text="Show Lesson", fg="#FFFFFF", bg="#00BFFF",
           font=("Noto Sans", 14, "bold"), command=show_lesson).pack(pady=5)
    
    # تحديث
    update_levels_view()
    if subjects_list and selected_subject.get() != "Select Subject":
        update_lessons_list()

# نافذة الحذف
def delete_item():
    window_delete = Toplevel(root)
    window_delete.title("Delete Item")
    window_delete.config(background="#E0FFFF")

    Label(window_delete, text="Select Subject:", font=("Noto Sans", 12, "bold"), bg="#E0FFFF").pack(pady=5)
    selected_subject = StringVar(window_delete)
    subjects = list(data.keys()) if data else [""]
    selected_subject.set("Select Subject")
    OptionMenu(window_delete, selected_subject, *subjects).pack(pady=5)

    Label(window_delete, text="Select Level:", font=("Noto Sans", 12, "bold"), bg="#E0FFFF").pack(pady=5)
    selected_level = StringVar(window_delete)
    selected_level.set("Select Level")
    level_menu = OptionMenu(window_delete, selected_level, "")
    level_menu.pack(pady=5)

    Label(window_delete, text="Select Lesson:", font=("Noto Sans", 12, "bold"), bg="#E0FFFF").pack(pady=5)
    selected_lesson = StringVar(window_delete)
    selected_lesson.set("Select Lesson")
    lesson_menu = OptionMenu(window_delete, selected_lesson, "")
    lesson_menu.pack(pady=5)

    # تحديث المستويات عند اختيار المادة
    def update_levels(*args):
        subject = selected_subject.get()
        levels = list(data[subject].keys()) if subject in data else [""]
        menu = level_menu["menu"]
        menu.delete(0, "end")
        for lvl in levels:
            menu.add_command(label=lvl, command=lambda v=lvl: selected_level.set(v))
        if levels:
            selected_level.set("Select Level")

    selected_subject.trace_add("write", update_levels)

    # تحديث الدروس عند اختيار المستوى
    def update_lessons(*args):
        subject = selected_subject.get()
        level = selected_level.get()
        lessons = [l["title"] for l in data[subject][level]] if subject in data and level in data[subject] else [""]
        menu = lesson_menu["menu"]
        menu.delete(0, "end")
        for ls in lessons:
            menu.add_command(label=ls, command=lambda v=ls: selected_lesson.set(v))
        if lessons:
            selected_lesson.set("Select Lesson")

    selected_level.trace_add("write", update_lessons)

    # زر الحذف
    def delete_selected():
        subject, level, lesson = selected_subject.get(), selected_level.get(), selected_lesson.get()
        if subject in data:
            if level == "Select Level" and lesson == "Select Lesson":
                del data[subject]
                save_data()
                messagebox.showinfo("Deleted", f"Subject '{subject}' deleted.")
            elif level in data[subject] and lesson == "Select Lesson":
                del data[subject][level]
                if not data[subject]:
                    del data[subject]
                save_data()
                messagebox.showinfo("Deleted", f"Level '{level}' deleted from subject '{subject}'.")
            elif level in data[subject]:
                data[subject][level] = [l for l in data[subject][level] if l["title"] != lesson]
                if not data[subject][level]:
                    del data[subject][level]
                if not data[subject]:
                    del data[subject]
                save_data()
                messagebox.showinfo("Deleted", f"Lesson '{lesson}' deleted.")
            window_delete.destroy()
        else:
            messagebox.showwarning("Error", "Invalid selection!")

    Button(window_delete, text="Delete", fg="#FFFFFF", bg="#FF4500",
           font=("Noto Sans", 14, "bold"), command=delete_selected).pack(pady=10)

# القائمة
Label_menu = Label(root, text="Teacher Organizer Menu", fg="#FFFFFF", bg="#00BFFF",
                   font=("Noto Sans", 20, "bold"), padx=10, pady=10)
Label_menu.pack()

Button(root, text="Add Subject", fg="#FFFFFF", bg="#00BFFF",
       font=("Noto Sans", 14, "bold"), padx=18, pady=10, command=add_subject).pack(pady=5)

Button(root, text="Add Lesson", fg="#FFFFFF", bg="#00BFFF",
       font=("Noto Sans", 14, "bold"), padx=18, pady=10, command=add_lesson).pack(pady=5)

Button(root, text="View Lessons", fg="#FFFFFF", bg="#00BFFF",
       font=("Noto Sans", 14, "bold"), padx=10, pady=10, command=view_lessons).pack(pady=5)

Button(root, text="Delete", fg="#FFFFFF", bg="#FF4500",
       font=("Noto Sans", 14, "bold"), padx=10, pady=10, command=delete_item).pack(pady=5)

root.mainloop()
