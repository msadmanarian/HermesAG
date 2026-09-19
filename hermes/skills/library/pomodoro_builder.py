from typing import Any, Dict
from hermes.skills.base import BaseSkill, SkillDefinition

class PomodoroBuilderSkill(BaseSkill):
    """
    Synthesizes a cross-platform floating Pomodoro Application (as featured in Tina Huang's live demo).
    Includes timer countdown, always-on-top windowing, and Obsidian session logging.
    """
    def __init__(self):
        self.definition = SkillDefinition(
            skill_id="pomodoro_builder",
            name="Floating Pomodoro App Builder",
            description="Generates complete, executable code for an Obsidian-integrated floating Pomodoro timer.",
            tags=["demo", "pomodoro", "gui", "obsidian"]
        )

    async def execute(self, inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        target_os = inputs.get("os", "macos_windows")
        code = """import tkinter as tk
from datetime import datetime
from pathlib import Path

class FloatingPomodoroApp:
    def __init__(self, root, vault_path="data/obsidian_vault"):
        self.root = root
        self.root.title("Hermes Pomodoro")
        self.root.attributes("-topmost", True)
        self.root.geometry("220x110+100+100")
        self.root.configure(bg="#1e1e2e")
        self.vault_path = Path(vault_path)

        self.remaining_seconds = 25 * 60
        self.is_running = False

        self.label = tk.Label(root, text="25:00", font=("Helvetica", 28, "bold"), fg="#a6e3a1", bg="#1e1e2e")
        self.label.pack(pady=5)

        self.btn_frame = tk.Frame(root, bg="#1e1e2e")
        self.btn_frame.pack()

        self.start_btn = tk.Button(self.btn_frame, text="Start", command=self.toggle_timer, bg="#89b4fa", fg="#11111b")
        self.start_btn.pack(side=tk.LEFT, padx=4)

        self.reset_btn = tk.Button(self.btn_frame, text="Reset", command=self.reset_timer, bg="#f38ba8", fg="#11111b")
        self.reset_btn.pack(side=tk.LEFT, padx=4)

    def toggle_timer(self):
        self.is_running = not self.is_running
        self.start_btn.config(text="Pause" if self.is_running else "Resume")
        if self.is_running:
            self.tick()

    def reset_timer(self):
        self.is_running = False
        self.remaining_seconds = 25 * 60
        self.label.config(text="25:00")
        self.start_btn.config(text="Start")

    def tick(self):
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            mins, secs = divmod(self.remaining_seconds, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.root.after(1000, self.tick)
        elif self.remaining_seconds == 0:
            self.log_to_obsidian()
            self.label.config(text="Done! 🎉")

    def log_to_obsidian(self):
        self.vault_path.mkdir(parents=True, exist_ok=True)
        log_file = self.vault_path / "Pomodoro_Sessions.md"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"- [x] **Pomodoro Completed:** {now_str} (25 min focus)\n"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingPomodoroApp(root)
    root.mainloop()
"""
        return {"code": code, "language": "python", "gui_framework": "tkinter"}
