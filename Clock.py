import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading
import pytz
import calendar

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("    ****Clock****    ")
        self.root.config(bg='turquoise2')
        self.root.geometry('500x550')
        self.timezones = ['Asia/Kolkata', 'UTC', 'US/Eastern', 'US/Pacific', 'Europe/London']
        self.current_timezone = tk.StringVar(value=self.timezones[0])
        self.alarm_time = None
        self.alarm_title = None
        self.alarm_description = None
        
        time_label = tk.Label(self.root,text="Digital Clock", font=('@Microsoft JhengHei UI', 36,"bold"), borderwidth=4, relief="sunken")
        time_label.pack(pady=20)
        time_label.place(x=110,y=5)
        time_label.config(bg='turquoise4')
        self.time_label = tk.Label(self.root, font=('@Microsoft JhengHei UI', 36,"bold"))
        self.time_label.pack(pady=20)
        self.time_label.place(x=145,y=80)
        self.time_label.config(bg='turquoise2')

        self.date_label = tk.Label(self.root, font=('@Microsoft JhengHei UI', 24,"bold"))
        self.date_label.pack(pady=10)
        self.date_label.place(x=160,y=160)
        self.date_label.config(bg='turquoise2')

        timezone_frame = tk.Frame(self.root)
        timezone_frame.pack(pady=10)
        timezone_frame.place(x=15,y=225)
        timezone_frame.config(bg='turquoise2')

        timezone_label = tk.Label(timezone_frame, text="Select Timezone:", font=('@Microsoft JhengHei UI', 19,"bold"))
        timezone_label.pack(side=tk.LEFT, padx=10)
        timezone_label.config(bg='turquoise2')
      

        timezone_dropdown = ttk.Combobox(timezone_frame, textvariable=self.current_timezone, values=self.timezones, font=('@Microsoft JhengHei UI', 14))
        timezone_dropdown.pack(side=tk.LEFT, padx=10)
       

        calendar_button = tk.Button(self.root, text="Show Calendar", command=self.show_calendar, font=('@Microsoft JhengHei UI', 14,"bold"))
        calendar_button.pack(pady=10)
        calendar_button.place(x=170,y=300)
        calendar_button.config(bg='paleturquoise3')

        alarm_button = tk.Button(self.root, text="Set Alarm", command=self.set_alarm, font=('@Microsoft JhengHei UI', 14,"bold"))
        alarm_button.pack(pady=10)
        alarm_button.place(x=197,y=360)
        alarm_button.config(bg='paleturquoise3')
        
        reminder_button = tk.Button(self.root, text="Set Reminder", command=self.set_reminder, font=('@Microsoft JhengHei UI', 14,"bold"))
        reminder_button.pack(pady=10)
        reminder_button.place(x=174,y=420)
        reminder_button.config(bg='paleturquoise3')
        
        exit_button = tk.Button(self.root, text="Exit",font=('@Microsoft JhengHei UI', 14,"bold") ,command=self.root.destroy)
        exit_button.pack(pady=20)
        exit_button.place(x=218,y=480)
        exit_button.config(bg='paleturquoise3')

        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        timezone = pytz.timezone(self.current_timezone.get())
        now = datetime.now(timezone)
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        self.time_label.configure(text=time_str)
        self.date_label.configure(text=date_str)

        if self.alarm_time:
            if now >= self.alarm_time:
                messagebox.showinfo(title=self.alarm_title, message=self.alarm_description)
                self.play_alarm_sound()
                self.alarm_time = None

        self.root.after(1000, self.update_clock)

    def play_alarm_sound(self):
        import platform
        if platform.system() == 'Windows':
            import winsound
            for i in range(10):
                winsound.PlaySound('alarm.wav', winsound.SND_FILENAME)

    def show_calendar(self):
        timezone = pytz.timezone(self.current_timezone.get())
        now = datetime.now(timezone)
        year = now.year
        month = now.month
        cal_str = calendar.month(year, month)
        messagebox.showinfo(title="Calendar", message=cal_str)

    def set_alarm(self):
        alarm_window = tk.Toplevel(self.root)
        alarm_window.title("Set Alarm")
        alarm_window.config(bg='paleturquoise3')
        hour_label = tk.Label(alarm_window, text="Hour:", font=('@Microsoft JhengHei UI', 16))
        hour_label.grid(row=0, column=0)
        hour_label.config(bg='paleturquoise3')
        hour_entry = tk.Entry(alarm_window, font=('@Microsoft JhengHei UI', 16))
        hour_entry.grid(row=0, column=1)

        minute_label = tk.Label(alarm_window, text="Minute:", font=('@Microsoft JhengHei UI', 16))
        minute_label.grid(row=1, column=0)
        minute_label.config(bg='paleturquoise3')
        minute_entry = tk.Entry(alarm_window, font=('@Microsoft JhengHei UI', 16))
        minute_entry.grid(row=1, column=1)

        title_label = tk.Label(alarm_window, text="Title:", font=('@Microsoft JhengHei UI', 16))
        title_label.grid(row=2, column=0)
        title_label.config(bg='paleturquoise3')
        title_entry = tk.Entry(alarm_window, font=('@Microsoft JhengHei UI', 16))
        title_entry.grid(row=2, column=1)

        description_label = tk.Label(alarm_window, text="Description:", font=('@Microsoft JhengHei UI', 16))
        description_label.grid(row=3, column=0)
        description_label.config(bg='paleturquoise3')
        description_entry = tk.Entry(alarm_window, font=('@Microsoft JhengHei UI', 16))
        description_entry.grid(row=3, column=1)

        set_button = tk.Button(
            alarm_window, 
            text="Set", 
            font=('@Microsoft JhengHei UI', 16), 
            command=lambda: (self.set_alarm_time(hour_entry.get(), minute_entry.get(), title_entry.get(), description_entry.get()),alarm_window.destroy())
        )
        set_button.grid(row=4, column=0, columnspan=2, pady=10)


    def set_alarm_time(self, hour, minute, title, description):
        timezone = pytz.timezone(self.current_timezone.get())
        now = datetime.now(timezone)
        alarm_time = now.replace(hour=int(hour), minute=int(minute), second=0)
        if alarm_time < now:
            alarm_time += timedelta(days=1)
        self.alarm_time = alarm_time
        self.alarm_title = title
        self.alarm_description = description
        messagebox.showinfo(title="Alarm Set", message=f"Alarm set for {hour}:{minute} with title '{title}' and description '{description}'")


    def set_reminder(self):
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("Set Reminder")
        reminder_window.config(bg='paleturquoise3')
        
        time_label = tk.Label(reminder_window, text="Time (in minutes):", font=('@Microsoft JhengHei UI', 16))
        time_label.grid(row=0, column=0)
        time_label.config(bg='paleturquoise3')
        
        time_entry = tk.Entry(reminder_window, font=('@Microsoft JhengHei UI', 16))
        time_entry.grid(row=0, column=1)

        title_label = tk.Label(reminder_window, text="Title:", font=('@Microsoft JhengHei UI', 16))
        title_label.grid(row=1, column=0)
        title_label.config(bg='paleturquoise3')

        title_entry = tk.Entry(reminder_window, font=('@Microsoft JhengHei UI', 16))
        title_entry.grid(row=1, column=1)

        description_label = tk.Label(reminder_window, text="Description:", font=('@Microsoft JhengHei UI', 16))
        description_label.grid(row=2, column=0)
        description_label.config(bg='paleturquoise3')

        description_entry = tk.Entry(reminder_window, font=('@Microsoft JhengHei UI', 16))
        description_entry.grid(row=2, column=1)

        set_button = tk.Button(
            reminder_window, 
            text="Set", 
            font=('@Microsoft JhengHei UI', 16), 
            command=lambda: (self.set_reminder_thread(time_entry.get(), title_entry.get(), description_entry.get()), reminder_window.destroy())
        )

        set_button.grid(row=3, column=0, columnspan=2, pady=10)

    def set_reminder_thread(self, time_str, title, description):
        time_int = int(time_str) * 60
        thread = threading.Thread(target=self.reminder_thread_func, args=(time_int,title,description))
        thread.start()
        messagebox.showinfo(title="Reminder Set", message="Reminder has been set successfully.")

    def reminder_thread_func(self, time_int, title, description):
        timezone = pytz.timezone(self.current_timezone.get())
        now = datetime.now(timezone)
        reminder_time = now + timedelta(seconds=time_int)
        reminder_str =reminder_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("Set Reminder")

        time_label = tk.Label(reminder_window, text="Time (in minutes):", font=('@Microsoft JhengHei UI', 14))
        time_label.grid(row=0, column=0, pady=5, padx=5)

        time_entry = tk.Entry(reminder_window, font=('@Microsoft JhengHei UI', 14))
        time_entry.grid(row=0, column=1, pady=5, padx=5)

        title_label = tk.Label(reminder_window, text="Title:", font=('@Microsoft JhengHei UI', 14))
        title_label.grid(row=1, column=0, pady=5, padx=5)

        title_entry = tk.Entry(reminder_window, font=('@Microsoft JhengHei UI', 14))
        title_entry.grid(row=1, column=1, pady=5, padx=5)

        description_label = tk.Label(reminder_window, text="Description:", font=('@Microsoft JhengHei UI', 14))
        description_label.grid(row=2, column=0, pady=5, padx=5)

        description_entry = tk.Entry(reminder_window, font=('@Microsoft JhengHei UI', 14))
        description_entry.grid(row=2, column=1, pady=5, padx=5)

        set_button = tk.Button(reminder_window, text="Set", font=('@Microsoft JhengHei UI', 14), command=lambda: (self.set_reminder_thread(time_entry.get(), title_entry.get(), description_entry.get()),reminder_window.destroy()))
        set_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

    def set_reminder_thread(self, time_str, title, description):
        time_int = int(time_str) * 60
        thread = threading.Thread(target=self.reminder_thread_func, args=(time_int,title,description))
        thread.start()
        messagebox.showinfo(title="Reminder Set", message=f"A reminder for '{title}' has been set for {time_str} minutes from now.")

    def reminder_thread_func(self, time_int, title, description):
        timezone = pytz.timezone(self.current_timezone.get())
        now = datetime.now(timezone)
        reminder_time = now + timedelta(seconds=time_int)
        while now < reminder_time:
            timezone = pytz.timezone(self.current_timezone.get())
            now = datetime.now(timezone)
        messagebox.showinfo(title=title, message=description)
        self.play_alarm_sound()
clock = Clock()
