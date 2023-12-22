from tkinter import *
from tkinter import ttk
import math
import winsound
import random

# Updated color palette
PRIMARY_COLOR = "#030303"  # Black
SECONDARY_COLOR = "#e74c3c"  # Red
ACCENT_COLOR = "#FF34B3"  # Green
BACKGROUND_COLOR = "#A2CD5A"  #Light green
TEXT_COLOR = "red"

FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
resp = 0
timer = None

# Quotes for motivation
QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "It always seems impossible until it's done. - Nelson Mandela",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
]

def reset_timer():
    reset.config(state=DISABLED)
    start.config(state=NORMAL)
    global timer
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=PRIMARY_COLOR)
    check_maker.config(text="")
    progress_bar['value'] = 0  # Reset progress bar
    global resp
    resp = 0

def start_timer():
    start.config(state=DISABLED)
    reset.config(state=NORMAL)
    global resp
    resp += 1
    work_sec = work_duration.get() * 60
    short_break_sec = short_break_duration.get() * 60
    long_break_sec = long_break_duration.get() * 60

    # Display a motivational quote at the beginning of each session
    if resp % 2 != 0:
        quote_label.config(text=random.choice(QUOTES), font=(FONT_NAME, 12, "bold"))
    else:
        quote_label.config(text="")  # Clear quote for breaks

    if resp % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=SECONDARY_COLOR)
    elif resp % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=SECONDARY_COLOR)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=PRIMARY_COLOR)

def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"
    
    time_text = f"{count_min}:{count_sec}"
    canvas.itemconfig(timer_text, text=time_text)
    
    # Update progress bar
    progress = (count / (work_duration.get() * 60)) * 100
    progress_bar['value'] = progress

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(resp / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_maker.config(text=marks)
        play_sound("end")

def play_sound(sound_type):
    if sound_type == "end":
        winsound.Beep(440, 500)  # Play a sound at the end of each session

def pause_resume_timer():
    global timer
    if timer is not None:
        window.after_cancel(timer)
        pause_resume_button.config(text="Resume", command=resume_timer, style="TButton")
    else:
        current_time = canvas.itemcget(timer_text, "text")
        remaining_seconds = int(current_time[:2]) * 60 + int(current_time[3:])
        count_down(remaining_seconds)
        pause_resume_button.config(text="Pause", command=pause_timer, style="TButtonActive")

def resume_timer():
    global timer
    pause_resume_button.config(text="Pause", command=pause_timer, style="TButtonActive")
    count_down(int(work_duration.get()) * 60)

def pause_timer():
    global timer
    window.after_cancel(timer)
    pause_resume_button.config(text="Resume", command=pause_resume_timer, style="TButton")

def save_task_description():
    task_description_text = task_description.get()
    if task_description_text:
        with open("task_description.txt", "a") as file:
            file.write(task_description_text + "\n")
        task_description.set("")  # Clear the entry after saving

# Main window
window = Tk()
window.title("Pomodoro")
window.geometry("850x1200")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# Style
style = ttk.Style()
style.configure("TButton",
                font=(FONT_NAME, 12),
                foreground=TEXT_COLOR,
                background=ACCENT_COLOR)

timer_label = Label(text="Timer", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=(FONT_NAME, 30, "bold"))
timer_label.grid(column=2, row=1, pady=10)

quote_label = Label(text="", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=(FONT_NAME, 14), wraplength=400, justify='center')
quote_label.grid(column=2, row=2, pady=10)

check_maker = Label(text="", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
check_maker.grid(column=2, row=3, pady=10)

start = ttk.Button(text="Start", command=start_timer, style="TButton")
start.grid(column=0, row=3, pady=10)

reset = ttk.Button(text="Reset", command=reset_timer, style="TButton")
reset.grid(column=3, row=3, pady=10)
reset.config(state=DISABLED)

pause_resume_button = ttk.Button(text="Pause", command=pause_resume_timer, style="TButton")
pause_resume_button.grid(column=1, row=3, pady=10)

canvas = Canvas(width=300, height=300, bg=BACKGROUND_COLOR, highlightthickness=0)
photo = PhotoImage(file="tomato.png")
canvas.create_image(150, 150, image=photo)
canvas.grid(column=2, row=4, pady=10)
timer_text = canvas.create_text(150, 160, text="00:00", fill=TEXT_COLOR, font=(FONT_NAME, 25, "bold"))

# Progress Bar
progress_bar = ttk.Progressbar(window, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(column=2, row=5, pady=10)

# Task Description
task_label = Label(text="Task Description", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=(FONT_NAME, 14))
task_label.grid(column=2, row=6, pady=10)

task_description = StringVar()
task_entry = Entry(window, textvariable=task_description, width=40,
font=(FONT_NAME, 12))
task_entry.grid(column=2, row=7, pady=10)

save_button = ttk.Button(text="Save", command=save_task_description, style="TButton")
save_button.grid(column=2, row=8, pady=20, sticky="s")

# Settings Menu
settings_menu = Menu(window)
window.config(menu=settings_menu)

work_duration = IntVar(value=WORK_MIN)
short_break_duration = IntVar(value=SHORT_BREAK_MIN)
long_break_duration = IntVar(value=LONG_BREAK_MIN)

settings_menu.add_command(label="Settings", command=lambda: settings_window())

def settings_window():
    settings_window = Toplevel(window)
    settings_window.title("Settings")

    Label(settings_window, text="Work Duration (min):").grid(row=0, column=0)
    Entry(settings_window, textvariable=work_duration).grid(row=0, column=1)

    Label(settings_window, text="Short Break Duration (min):").grid(row=1, column=0)
    Entry(settings_window, textvariable=short_break_duration).grid(row=1, column=1)

    Label(settings_window, text="Long Break Duration (min):").grid(row=2, column=0)
    Entry(settings_window, textvariable=long_break_duration).grid(row=2, column=1)

    Button(settings_window, text="Apply", command=settings_window.destroy, style="TButton").grid(row=3, column=0, columnspan=2)

window.mainloop()
