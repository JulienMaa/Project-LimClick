import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
import pyautogui
import keyboard
import threading
import time
import json
from PIL import ImageGrab
from pynput.mouse import Listener
import os

SETTINGS_FILE = "settings.json"

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker Couleur")
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        self.root.config(bg="#f0f4f8")
        self.root.attributes("-topmost", True)

        self.color_to_match = None
        self.check_position = None
        self.click_position = None
        self.interval = 1.0
        self.running = False
        self.listener = None

        self.build_ui()
        threading.Thread(target=self.listen_toggle_key, daemon=True).start()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=("Helvetica", 12), anchor="center", width=20)
        style.configure("TCheckbutton", font=("Helvetica", 12))

        ttk.Label(main_frame, text="AutoClicker Couleur", font=("Helvetica", 18, "bold"),
                  foreground="#2980b9", background="#f0f4f8").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(main_frame, text="💾 Sauvegarder", command=self.save_settings).grid(row=1, column=0, pady=5)
        ttk.Button(main_frame, text="📂 Charger", command=self.load_settings).grid(row=1, column=1, pady=5)
        ttk.Button(main_frame, text="🎨 Choisir couleur", command=self.pick_color).grid(row=2, column=0, pady=5, padx=10)
        ttk.Button(main_frame, text="🖱 Pipette", command=lambda: self.wait_for_click_position("color")).grid(row=2, column=1, pady=5, padx=10)
        ttk.Button(main_frame, text="📌 Point à vérifier", command=lambda: self.wait_for_click_position("check")).grid(row=3, column=0, pady=5, padx=10)
        ttk.Button(main_frame, text="🎯 Point de clic", command=lambda: self.wait_for_click_position("click")).grid(row=3, column=1, pady=5, padx=10)

        ttk.Label(main_frame, text="⏱️ Intervalle (s)", foreground="#34495e", background="#f0f4f8").grid(row=4, column=0, pady=5)
        self.interval_entry = ttk.Entry(main_frame, font=("Helvetica", 12), width=10)
        self.interval_entry.insert(0, "1.0")
        self.interval_entry.grid(row=4, column=1, pady=5, padx=10)

        self.keep_on_top = tk.IntVar(value=1)
        ttk.Checkbutton(main_frame, text="🪟 Garder fenêtre au premier plan", variable=self.keep_on_top,
                        command=self.toggle_topmost).grid(row=5, column=0, columnspan=2, pady=5)

        ttk.Label(main_frame, text="🎨 Couleur sélectionnée", foreground="#34495e", background="#f0f4f8").grid(row=6, column=0, columnspan=2, pady=5)
        self.color_display = tk.Label(main_frame, relief="solid", width=20, height=2, bg="#ffffff", anchor="center", font=("Helvetica", 12))
        self.color_display.grid(row=7, column=0, columnspan=2, pady=10)

        self.status_label = ttk.Label(main_frame, text="AutoClicker désactivé (F7)", font=("Helvetica", 12),
                                      foreground="#e74c3c", background="#f0f4f8")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10)

    def toggle_topmost(self):
        self.root.attributes("-topmost", bool(self.keep_on_top.get()))

    def update_color_display(self):
        if self.color_to_match:
            hex_color = '#%02x%02x%02x' % self.color_to_match
            self.color_display.config(background=hex_color)

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choisir une couleur")
        if color_code[0]:
            self.color_to_match = tuple(map(int, color_code[0]))
            print("Couleur choisie :", self.color_to_match)
            self.update_color_display()
            self.status_label.config(text=f"Couleur choisie : {self.color_to_match}", foreground="#2ecc71")

    def wait_for_click_position(self, mode):
        self.status_label.config(text="Cliquez n'importe où pour capturer...", foreground="#f39c12")
        threading.Thread(target=self._start_listener, args=(mode,), daemon=True).start()

    def _start_listener(self, mode):
        with Listener(on_click=lambda x, y, button, pressed: self.on_click(x, y, button, pressed, mode)) as listener:
            self.listener = listener
            listener.join()

    def on_click(self, x, y, button, pressed, mode):
        if pressed:
            if mode == "check":
                self.check_position = (x, y)
                self.status_label.config(text=f"Point à vérifier défini : {self.check_position}", foreground="#3498db")
            elif mode == "click":
                self.click_position = (x, y)
                self.status_label.config(text=f"Point de clic défini : {self.click_position}", foreground="#3498db")
            elif mode == "color":
                screenshot = ImageGrab.grab()
                picked_color = screenshot.getpixel((x, y))
                self.color_to_match = picked_color
                self.update_color_display()
                self.status_label.config(text=f"Couleur capturée : {picked_color}", foreground="#2ecc71")
            self.listener.stop()

    def listen_toggle_key(self):
        keyboard.add_hotkey("f7", self.toggle_autoclicker)
        while True:
            time.sleep(0.1)

    def toggle_autoclicker(self):
        self.running = not self.running
        self.status_label.config(
            text="✅ AutoClicker activé (F7)" if self.running else "⛔ AutoClicker désactivé (F7)",
            foreground="#2ecc71" if self.running else "#e74c3c"
        )
        if self.running:
            try:
                self.interval = float(self.interval_entry.get())
            except ValueError:
                self.interval = 1.0
            threading.Thread(target=self.autoclick_loop, daemon=True).start()

    def autoclick_loop(self):
        while self.running:
            if self.color_to_match and self.check_position and self.click_position:
                # Capture the screen to check the color
                screenshot = ImageGrab.grab()
                current_color = screenshot.getpixel(self.check_position)

                if not self.color_similar(current_color, self.color_to_match):
                    # 🛡️ Double-check right before clicking
                    screenshot_verify = ImageGrab.grab()
                    color_before_click = screenshot_verify.getpixel(self.check_position)

                    if not self.color_similar(color_before_click, self.color_to_match):
                        self.status_label.config(text="🎯 Couleur différente — clic effectué", foreground="#27ae60")
                        pyautogui.click(self.click_position)
                    else:
                        self.status_label.config(text="🔄 Changement annulé — couleur redevenue identique", foreground="#f1c40f")
                else:
                    self.status_label.config(text="✅ Couleur identique — pas de clic", foreground="#2980b9")
            else:
                self.status_label.config(text="⚠️ Paramètres incomplets", foreground="#f39c12")

            time.sleep(self.interval)

    def color_similar(self, c1, c2, tolerance=30):
        return all(abs(a - b) < tolerance for a, b in zip(c1, c2))

    def save_settings(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        data = {
            "color": self.color_to_match,
            "check_position": self.check_position,
            "click_position": self.click_position,
            "interval": self.interval_entry.get(),
            "keep_on_top": self.keep_on_top.get()
        }
        with open(file_path, "w") as f:
            json.dump(data, f)
        self.status_label.config(text=f"✅ Paramètres sauvegardés dans {os.path.basename(file_path)}", foreground="#2ecc71")

    def load_settings(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            self.color_to_match = tuple(data.get("color")) if data.get("color") else None
            self.check_position = tuple(data.get("check_position")) if data.get("check_position") else None
            self.click_position = tuple(data.get("click_position")) if data.get("click_position") else None
            self.interval_entry.delete(0, tk.END)
            self.interval_entry.insert(0, data.get("interval", "1.0"))
            self.keep_on_top.set(data.get("keep_on_top", 1))
            self.toggle_topmost()
            self.update_color_display()
            self.status_label.config(text=f"📂 Paramètres chargés depuis {os.path.basename(file_path)}", foreground="#2980b9")
        except Exception as e:
            messagebox.showerror("Erreur de chargement", f"Impossible de charger les paramètres : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
