
import tkinter as tk
from pynput import keyboard
import threading
import time

class AutoKeyPresser:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoKeyPresser")
        self.root.config(bg="#EBE8DB")
        self.root.resizable(False, False)

        self.key_to_press = "space"
        self.interval = 1.0
        self.running = False

        self.build_ui()
        threading.Thread(target=self.listen_hotkey, daemon=True).start()

    def build_ui(self):
        tk.Label(self.root, text="🎯 LimKeyPresser", font=("Helvetica", 18, "bold"),
                 bg="#EBE8DB", fg="#B03052").pack(pady=(10, 20))

        frame = tk.Frame(self.root, bg="#EBE8DB")
        frame.pack()

        tk.Label(frame, text="Touche à presser :", bg="#EBE8DB", fg="#3D0301").grid(row=0, column=0, sticky="e")
        self.key_entry = tk.Entry(frame, width=15, bg="#D76C82", fg="white", insertbackground="white", relief="flat")
        self.key_entry.insert(0, "space")
        self.key_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Intervalle (s) :", bg="#EBE8DB", fg="#3D0301").grid(row=1, column=0, sticky="e")
        self.interval_entry = tk.Entry(frame, width=15, bg="#D76C82", fg="white", insertbackground="white", relief="flat")
        self.interval_entry.insert(0, "1.0")
        self.interval_entry.grid(row=1, column=1, padx=10, pady=5)

        self.status_label = tk.Label(self.root, text="AutoKey désactivé (F8)", bg="#EBE8DB", fg="#B03052", font=("Helvetica", 11))
        self.status_label.pack(pady=(15, 10))

    def listen_hotkey(self):
        def on_press(key):
            if key == keyboard.Key.f8:
                self.toggle_autokey()

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def toggle_autokey(self):
        self.running = not self.running
        if self.running:
            self.status_label.config(text="AutoKey ACTIVÉ (F8)", fg="#D76C82")
            self.key_to_press = self.key_entry.get()
            try:
                self.interval = float(self.interval_entry.get())
            except ValueError:
                self.interval = 1.0
            threading.Thread(target=self.press_key_loop, daemon=True).start()
        else:
            self.status_label.config(text="AutoKey désactivé (F8)", fg="#B03052")

    def press_key_loop(self):
        controller = keyboard.Controller()
        while self.running:
            try:
                if len(self.key_to_press) == 1:
                    controller.press(self.key_to_press)
                    controller.release(self.key_to_press)
                else:
                    key = getattr(keyboard.Key, self.key_to_press, None)
                    if key:
                        controller.press(key)
                        controller.release(key)
            except Exception as e:
                print(f"Erreur lors de la frappe : {e}")
            time.sleep(self.interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoKeyPresser(root)
    root.mainloop()
