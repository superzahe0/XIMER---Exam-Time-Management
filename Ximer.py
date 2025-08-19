import tkinter as tk
from tkinter import ttk, messagebox

def seconds_to_mmss(sec: int) -> str:
    sign = "-" if sec < 0 else ""
    sec = abs(int(sec))
    m, s = divmod(sec, 60)
    return f"{sign}{m:02d}:{s:02d}"

class QuizTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ZIMER - Exam Time Divider")
        self.geometry("560x380")
        self.resizable(False, False)

        self.running = False
        self.paused = False
        self.total_seconds_initial = 0
        self.total_remaining = 0
        self.total_questions = 0
        self.current_question_idx = 0
        self.current_question_remaining = 0

        frm_top = ttk.Frame(self, padding=12)
        frm_top.pack(fill="x")

        ttk.Label(frm_top, text="Total minutes:").grid(row=0, column=0, sticky="w", padx=(0,8), pady=4)
        self.entry_minutes = ttk.Entry(frm_top, width=10)
        self.entry_minutes.grid(row=0, column=1, sticky="w", pady=4)
        self.entry_minutes.insert(0, "60")

        ttk.Label(frm_top, text="Number of questions:").grid(row=0, column=2, sticky="w", padx=(16,8), pady=4)
        self.entry_questions = ttk.Entry(frm_top, width=10)
        self.entry_questions.grid(row=0, column=3, sticky="w", pady=4)
        self.entry_questions.insert(0, "50")

        frm_buttons = ttk.Frame(self, padding=(12,0,12,12))
        frm_buttons.pack(fill="x")
        self.btn_start = ttk.Button(frm_buttons, text="Start", command=self.start)
        self.btn_start.grid(row=0, column=0, padx=4, pady=8, sticky="w")

        self.btn_pause = ttk.Button(frm_buttons, text="Pause ⏸", command=self.toggle_pause, state="disabled")
        self.btn_pause.grid(row=0, column=1, padx=4, pady=8, sticky="w")

        self.btn_finish = ttk.Button(frm_buttons, text="Finished this question ✓", command=self.finish_question, state="disabled")
        self.btn_finish.grid(row=0, column=2, padx=4, pady=8, sticky="w")

        self.btn_reset = ttk.Button(frm_buttons, text="Reset", command=self.reset_app)
        self.btn_reset.grid(row=0, column=3, padx=4, pady=8, sticky="w")

        frm_disp = ttk.Frame(self, padding=12)
        frm_disp.pack(fill="both", expand=True)

        self.lbl_q = ttk.Label(frm_disp, text="Question: -/-", font=("Arial", 14, "bold"))
        self.lbl_q.pack(anchor="center", pady=(8,8))

        self.lbl_paused = ttk.Label(frm_disp, text="", foreground="#b35c00", font=("Arial", 11, "italic"))
        self.lbl_paused.pack(anchor="center", pady=(0,6))

        frm_timers = ttk.Frame(frm_disp)
        frm_timers.pack(fill="x", pady=6)

        ttk.Label(frm_timers, text="Total remaining time:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.lbl_total = ttk.Label(frm_timers, text="00:00", font=("Consolas", 24, "bold"))
        self.lbl_total.grid(row=1, column=0, sticky="w", padx=4, pady=(0,8))

        ttk.Label(frm_timers, text="Current question time:", font=("Arial", 12)).grid(row=0, column=1, sticky="w", padx=24, pady=4)
        self.lbl_question = ttk.Label(frm_timers, text="00:00", font=("Consolas", 24, "bold"))
        self.lbl_question.grid(row=1, column=1, sticky="w", padx=24, pady=(0,8))

        self.lbl_hint = ttk.Label(
            frm_disp,
            text="This program divides exam time across questions.\nIf a question's time runs out without answering, it will subtract from the rest.",
            foreground="#555"
        )
        self.lbl_hint.pack(anchor="w", pady=6)

        self.progress = ttk.Progressbar(frm_disp, mode="determinate")
        self.progress.pack(fill="x", pady=(6, 12))

        self.after_id = None
        self.bind("<space>", lambda e: self.toggle_pause() if self.btn_pause["state"] == "normal" else None)

    def reset_app(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.running = False
        self.paused = False
        self.total_seconds_initial = 0
        self.total_remaining = 0
        self.total_questions = 0
        self.current_question_idx = 0
        self.current_question_remaining = 0
        self.lbl_q.config(text="Question: -/-")
        self.lbl_total.config(text="00:00")
        self.lbl_question.config(text="00:00")
        self.progress["value"] = 0
        self.lbl_paused.config(text="")
        self.btn_finish.config(state="disabled")
        self.btn_pause.config(state="disabled", text="Pause ⏸")
        self.btn_start.config(state="normal")

    def start(self):
        try:
            minutes = int(self.entry_minutes.get())
            questions = int(self.entry_questions.get())
            if minutes <= 0 or questions <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter positive integers for minutes and questions.")
            return

        self.total_seconds_initial = minutes * 60
        self.total_remaining = self.total_seconds_initial
        self.total_questions = questions
        self.current_question_idx = 1
        self.current_question_remaining = self.allocate_for_remaining_questions()

        self.running = True
        self.paused = False
        self.btn_start.config(state="disabled")
        self.btn_pause.config(state="normal", text="Pause ⏸")
        self.btn_finish.config(state="normal")
        self.tick()
        self.refresh_labels()

    def toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self.lbl_paused.config(text="Paused")
            self.btn_pause.config(text="Resume ▶")
        else:
            self.lbl_paused.config(text="")
            self.btn_pause.config(text="Pause ⏸")

    def allocate_for_remaining_questions(self) -> int:
        remaining_questions = self.total_questions - self.current_question_idx + 1
        if remaining_questions <= 0:
            return 0
        return int(self.total_remaining // remaining_questions)

    def finish_question(self):
        if not self.running:
            return
        if self.current_question_idx >= self.total_questions:
            self.running = False
            self.btn_finish.config(state="disabled")
            self.btn_pause.config(state="disabled")
            self.refresh_labels()
            messagebox.showinfo("Done", "All questions finished. Good luck!")
            return

        self.current_question_idx += 1
        self.current_question_remaining = self.allocate_for_remaining_questions()
        self.refresh_labels()

    def tick(self):
        if self.running and not self.paused:
            self.total_remaining -= 1
            self.current_question_remaining -= 1
            self.refresh_labels()
            if self.total_remaining < -36000:
                self.running = False
        self.after_id = self.after(1000, self.tick)

    def refresh_labels(self):
        self.lbl_q.config(text=f"Question: {self.current_question_idx}/{self.total_questions if self.total_questions else '-'}")
        self.lbl_total.config(text=seconds_to_mmss(self.total_remaining))
        self.lbl_question.config(text=seconds_to_mmss(self.current_question_remaining))
        if self.total_seconds_initial > 0:
            pct = max(0, min(100, int((self.total_remaining / self.total_seconds_initial) * 100)))
            self.progress["value"] = pct
        else:
            self.progress["value"] = 0

if __name__ == "__main__":
    app = QuizTimerApp()
    app.mainloop()
