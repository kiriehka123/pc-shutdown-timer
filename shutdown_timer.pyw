import subprocess
import time
import tkinter as tk
from tkinter import messagebox


BG = "#0b1220"
PANEL = "#111b30"
CARD = "#182640"
TEXT = "#f3f6fc"
MUTED = "#94a3b8"
ACCENT = "#6595ff"
ACCENT_HOVER = "#7da5ff"
GREEN = "#28c995"
RED = "#ed7180"


class ShutdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер выключения")
        self.root.geometry("440x560")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.deadline = None
        self.active = False

        panel = tk.Frame(root, bg=PANEL, padx=25, pady=24)
        panel.pack(fill="both", expand=True, padx=14, pady=14)

        header = tk.Frame(panel, bg=PANEL)
        header.pack(fill="x")
        icon = tk.Label(header, text="◷", bg="#20375f", fg=ACCENT, font=("Segoe UI Symbol", 23, "bold"), width=2, height=1)
        icon.pack(side="left", padx=(0, 12))
        title_box = tk.Frame(header, bg=PANEL)
        title_box.pack(side="left", fill="y")
        tk.Label(title_box, text="Таймер выключения", bg=PANEL, fg=TEXT, font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(title_box, text="Запланируйте выключение компьютера", bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 0))

        tk.Label(panel, text="ВЫКЛЮЧИТЬ ЧЕРЕЗ", bg=PANEL, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(28, 10))

        time_row = tk.Frame(panel, bg=PANEL)
        time_row.pack(fill="x")
        self.hours = tk.StringVar(value="1")
        self.minutes = tk.StringVar(value="0")
        self.hour_box = self.make_time_box(time_row, self.hours, "ЧАСЫ", 999)
        self.hour_box.pack(side="left", fill="x", expand=True)
        tk.Label(time_row, text=":", bg=PANEL, fg=MUTED, font=("Segoe UI", 24, "bold")).pack(side="left", padx=10)
        self.minute_box = self.make_time_box(time_row, self.minutes, "МИНУТЫ", 59)
        self.minute_box.pack(side="left", fill="x", expand=True)

        preset_row = tk.Frame(panel, bg=PANEL)
        preset_row.pack(fill="x", pady=(12, 0))
        for label, h, m in (("30 минут", 0, 30), ("1 час", 1, 0), ("2 часа", 2, 0)):
            tk.Button(
                preset_row, text=label, command=lambda hours=h, minutes=m: self.set_time(hours, minutes),
                bg=CARD, fg="#c6d4eb", activebackground="#243857", activeforeground=TEXT,
                relief="flat", bd=0, padx=12, pady=7, font=("Segoe UI", 9), cursor="hand2",
            ).pack(side="left", padx=(0, 8))

        countdown_card = tk.Frame(panel, bg=CARD, padx=16, pady=13)
        countdown_card.pack(fill="x", pady=(22, 0))
        tk.Label(countdown_card, text="ОСТАЛОСЬ ДО ВЫКЛЮЧЕНИЯ", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.countdown = tk.Label(countdown_card, text="--:--:--", bg=CARD, fg=TEXT, font=("Segoe UI", 25, "bold"))
        self.countdown.pack(anchor="w", pady=(3, 0))

        self.status = tk.Label(panel, text="Таймер не запущен", bg=PANEL, fg=MUTED, font=("Segoe UI", 9))
        self.status.pack(anchor="w", pady=(12, 12))

        buttons = tk.Frame(panel, bg=PANEL)
        buttons.pack(fill="x")
        self.start_button = tk.Button(
            buttons, text="Запустить таймер", command=self.start, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white", relief="flat", bd=0,
            padx=12, pady=11, font=("Segoe UI", 10, "bold"), cursor="hand2",
        )
        self.start_button.pack(side="left", fill="x", expand=True)
        self.cancel_button = tk.Button(
            buttons, text="Отменить", command=self.cancel, bg=CARD, fg="#d5deec",
            activebackground="#243857", activeforeground=TEXT, relief="flat", bd=0,
            padx=12, pady=11, font=("Segoe UI", 10), cursor="hand2",
        )
        self.cancel_button.pack(side="left", fill="x", expand=True, padx=(9, 0))

        tk.Label(panel, text="Таймер работает, даже если закрыть это окно.", bg=PANEL, fg="#71819a", font=("Segoe UI", 8)).pack(anchor="w", pady=(16, 0))

    def make_time_box(self, parent, variable, caption, maximum):
        box = tk.Frame(parent, bg=CARD, padx=12, pady=9)
        tk.Label(box, text=caption, bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        spin = tk.Spinbox(
            box, from_=0, to=maximum, textvariable=variable, width=4, justify="left",
            bg=CARD, fg=TEXT, insertbackground=TEXT, buttonbackground=CARD,
            selectbackground=ACCENT, selectforeground="white", relief="flat", bd=0,
            highlightthickness=0, font=("Segoe UI", 22, "bold"), wrap=True,
        )
        spin.pack(anchor="w", fill="x", pady=(4, 0))
        return box

    def set_time(self, hours, minutes):
        if self.active:
            return
        self.hours.set(str(hours))
        self.minutes.set(str(minutes))

    def set_inputs_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        for box in (self.hour_box, self.minute_box):
            for child in box.winfo_children():
                if isinstance(child, tk.Spinbox):
                    child.configure(state=state)

    def start(self):
        try:
            hours = int(self.hours.get())
            minutes = int(self.minutes.get())
            if hours < 0 or not 0 <= minutes <= 59:
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showerror("Проверьте время", "Введите целое количество часов и минут от 0 до 59.", parent=self.root)
            return

        seconds = hours * 3600 + minutes * 60
        if seconds < 60:
            messagebox.showerror("Укажите время", "Выберите время не меньше одной минуты.", parent=self.root)
            return

        try:
            result = subprocess.run(
                ["shutdown.exe", "/s", "/t", str(seconds)], capture_output=True, text=True, check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except OSError as exc:
            messagebox.showerror("Не удалось запустить таймер", str(exc), parent=self.root)
            return

        if result.returncode != 0:
            details = (result.stderr or result.stdout or "Windows не приняла команду.").strip()
            messagebox.showerror("Не удалось запустить таймер", details, parent=self.root)
            return

        self.deadline = time.monotonic() + seconds
        self.active = True
        self.start_button.configure(state="disabled", bg="#314766", fg="#a9b7ca", cursor="arrow")
        self.set_inputs_enabled(False)
        self.status.configure(text="Выключение запланировано", fg=GREEN)
        self.update_countdown()

    def update_countdown(self):
        if not self.active or self.deadline is None:
            return
        remaining = max(0, int(self.deadline - time.monotonic() + 0.999))
        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.countdown.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(250, self.update_countdown)

    def cancel(self):
        try:
            result = subprocess.run(
                ["shutdown.exe", "/a"], capture_output=True, text=True, check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except OSError as exc:
            messagebox.showerror("Не удалось отменить выключение", str(exc), parent=self.root)
            return

        self.active = False
        self.deadline = None
        self.start_button.configure(state="normal", bg=ACCENT, fg="white", cursor="hand2")
        self.set_inputs_enabled(True)
        self.countdown.configure(text="--:--:--")
        if result.returncode == 0:
            self.status.configure(text="Выключение отменено", fg=GREEN)
        else:
            self.status.configure(text="Активный таймер выключения не найден", fg=MUTED)


if __name__ == "__main__":
    window = tk.Tk()
    app = ShutdownTimer(window)
    window.mainloop()

