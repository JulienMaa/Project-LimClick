import tkinter as tk
from pynput import mouse, keyboard
import threading
import time

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.config(bg="#EBE8DB")
        self.root.resizable(False, False)

        self.clicking = False
        self.button = "left"  # "left" ou "right"
        self.interval = 0.1
        self.topmost = False

        self.build_ui()
        threading.Thread(target=self.listen_hotkey, daemon=True).start()

    def build_ui(self):
        tk.Label(self.root, text="🖱️ LimAutoClicker", font=("Helvetica", 18, "bold"),
                 bg="#EBE8DB", fg="#B03052").pack(pady=(10, 20))

        frame = tk.Frame(self.root, bg="#EBE8DB")
        frame.pack()

        tk.Label(frame, text="Bouton à cliquer :", bg="#EBE8DB", fg="#3D0301").grid(row=0, column=0, sticky="e")
        self.button_toggle = tk.Button(frame, text="🖱️ Clic gauche", command=self.toggle_button,
                                       bg="#D76C82", fg="white", relief="flat", width=15)
        self.button_toggle.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Intervalle (s) :", bg="#EBE8DB", fg="#3D0301").grid(row=1, column=0, sticky="e")
        self.interval_entry = tk.Entry(frame, width=15, bg="#D76C82", fg="white", insertbackground="white", relief="flat")
        self.interval_entry.insert(0, "0.1")
        self.interval_entry.grid(row=1, column=1, padx=10, pady=5)

        self.status_label = tk.Label(self.root, text="AutoClicker désactivé (F8)", bg="#EBE8DB", fg="#B03052", font=("Helvetica", 11))
        self.status_label.pack(pady=(15, 10))

        # Bouton Topmost
        self.topmost_button = tk.Button(self.root, text="🔓 Rester au-dessus: OFF", command=self.toggle_topmost,
                                        bg="#D76C82", fg="white", relief="flat")
        self.topmost_button.pack(pady=(5, 10))

    def toggle_button(self):
        if self.button == "left":
            self.button = "right"
            self.button_toggle.config(text="🖱️ Clic droit")
        else:
            self.button = "left"
            self.button_toggle.config(text="🖱️ Clic gauche")

    def toggle_topmost(self):
        self.topmost = not self.topmost
        self.root.attributes('-topmost', self.topmost)
        if self.topmost:
            self.topmost_button.config(text="🔒 Rester au-dessus: ON")
        else:
            self.topmost_button.config(text="🔓 Rester au-dessus: OFF")

    def listen_hotkey(self):
        def on_press(key):
            if key == keyboard.Key.f8:
                self.toggle_clicking()

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            self.status_label.config(text="AutoClicker ACTIVÉ (F8)", fg="#D76C82")
            try:
                self.interval = float(self.interval_entry.get())
            except ValueError:
                self.interval = 0.1
            threading.Thread(target=self.click_loop, daemon=True).start()
        else:
            self.status_label.config(text="AutoClicker désactivé (F8)", fg="#B03052")

    def click_loop(self):
        m = mouse.Controller()
        while self.clicking:
            try:
                if self.button == "left":
                    m.click(mouse.Button.left)
                elif self.button == "right":
                    m.click(mouse.Button.right)
            except Exception as e:
                print(f"Erreur lors du click : {e}")
            time.sleep(self.interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
