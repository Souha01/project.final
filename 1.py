from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Teacher Organizer")
root.geometry("600x500")
root.config(background="#E0FFFF") 

data = {}  

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
    if data:
      subjects = list(data.keys())
    else:
     subjects = [""]
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
        if subject in data:
            levels_list = list(data[subject].keys())
        else:
            levels_list = [""]
        
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
    if data:
     subjects_list= list(data.keys()) 
    else:
        subjects_list=[""]
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
        if subject in data:
            levels_list = list(data[subject].keys())
        else:
            levels_list = [""]
        
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
        
        if subject in data and level in data[subject]:
          lessons_titles = []  # إنشاء قائمة فارغة لتخزين عناوين الدروس
          for lesson in data[subject][level]:  #  dont forgنمر على كل درس في هذا المستوى
            lessons_titles.append(lesson["title"])  # نضيف عنوان الدرس للقائمة
        else:
         lessons_titles = [""]

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

root.mainloop()