# ==============================================================================
# S-AutoClicker Pro (Strong Edition)
# Copyright (c) 2026 Shubhomoy (sgdev)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# ==============================================================================

import time
import threading
import customtkinter as ctk
import pydirectinput
from pynput import keyboard

# pydirectinput Safety & Speed Settings
pydirectinput.FAILSAFE = True
pydirectinput.PAUSE = 0  # 0 করে দিলাম যাতে একদম ম্যাক্সিমাম স্পিড পাস ভাই!

class SAutoClicker(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("S-AutoClicker Pro")
        self.geometry("320x520") # হট-কী বাটনের জন্য একটু বড় করলাম
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # --- Variables ---
        self.is_running = False
        self.hotkey = keyboard.Key.f5  # Default Hotkey
        self.hotkey_name = "F5"
        self.listening_for_key = False
        self.click_thread = None

        # --- UI Layout ---
        self.setup_ui()

        # --- Global Key Listener ---
        self.listener = keyboard.Listener(on_press=self.handle_hotkey)
        self.listener.start()

    def setup_ui(self):
        # Main Frame
        self.main_frame = ctk.CTkFrame(master=self, corner_radius=12)
        self.main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        # App Title
        self.title_label = ctk.CTkLabel(
            master=self.main_frame, 
            text="⚡ S-AutoClicker", 
            font=("Roboto", 20, "bold"),
            text_color="#53DC50"
        )
        self.title_label.pack(pady=(15, 2))

        # Subtitle / License
        self.sub_label = ctk.CTkLabel(
            master=self.main_frame, 
            text="Developed by Shubhomoy (sgdev)\nStrong & OP Edition", 
            font=("Roboto", 10),
            text_color="#888888"
        )
        self.sub_label.pack(pady=(0, 15))

        # --- Hotkey Binder UI ---
        self.hotkey_btn = ctk.CTkButton(
            master=self.main_frame,
            text=f"Current Hotkey: {self.hotkey_name}\n(Click to Change)",
            font=("Roboto", 12, "bold"),
            fg_color="#1F6AA5",
            command=self.start_bind_hotkey
        )
        self.hotkey_btn.pack(pady=(0, 15), padx=25, fill="x")

        # Mouse Button Selection
        self.btn_label = ctk.CTkLabel(master=self.main_frame, text="Mouse Button:", font=("Roboto", 13, "bold"))
        self.btn_label.pack(anchor="w", padx=25)
        
        self.button_option = ctk.CTkOptionMenu(
            master=self.main_frame,
            values=["Left", "Right", "Middle"]
        )
        self.button_option.pack(pady=(2, 10), padx=25, fill="x")

        # Click Type Selection
        self.type_label = ctk.CTkLabel(master=self.main_frame, text="Click Type:", font=("Roboto", 13, "bold"))
        self.type_label.pack(anchor="w", padx=25)
        
        self.type_option = ctk.CTkOptionMenu(
            master=self.main_frame,
            values=["Single", "Double", "Hold"]
        )
        self.type_option.pack(pady=(2, 10), padx=25, fill="x")

        # Click Interval Input
        self.interval_frame = ctk.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.interval_frame.pack(pady=5, padx=25, fill="x")

        self.interval_label = ctk.CTkLabel(master=self.interval_frame, text="Interval (sec):", font=("Roboto", 13))
        self.interval_label.pack(side="left")

        self.interval_entry = ctk.CTkEntry(master=self.interval_frame, width=80)
        self.interval_entry.insert(0, "0.01")
        self.interval_entry.pack(side="right")

        # Status Label
        self.status_label = ctk.CTkLabel(
            master=self.main_frame, 
            text="Status: Stopped 🛑", 
            font=("Roboto", 14, "bold"),
            text_color="#FF4B4B"
        )
        self.status_label.pack(pady=10)

        # Control Buttons
        self.start_btn = ctk.CTkButton(
            master=self.main_frame, 
            text=f"START ({self.hotkey_name})", 
            font=("Roboto", 14, "bold"),
            command=lambda: self.after(0, self.start_clicking)
        )
        self.start_btn.pack(pady=5, padx=25, fill="x")

        self.stop_btn = ctk.CTkButton(
            master=self.main_frame, 
            text=f"STOP ({self.hotkey_name})", 
            font=("Roboto", 14, "bold"),
            fg_color="#333333",
            state="disabled",
            command=lambda: self.after(0, self.stop_clicking)
        )
        self.stop_btn.pack(pady=5, padx=25, fill="x")

    # --- Hotkey Binder Logic ---
    def start_bind_hotkey(self):
        self.listening_for_key = True
        self.hotkey_btn.configure(text="Press ANY KEY now...", fg_color="#E53935")

    def handle_hotkey(self, key):
        # যদি নতুন কি সেট করার জন্য বাটনে ক্লিক করা থাকে
        if getattr(self, 'listening_for_key', False):
            self.hotkey = key
            try:
                # ক্যারেক্টার কি (যেমন a, b, c)
                key_name = key.char.upper()
            except AttributeError:
                # স্পেশাল কি (যেমন Shift, F5, Ctrl)
                key_name = str(key).replace('Key.', '').upper()
            
            self.listening_for_key = False
            self.after(0, self.update_hotkey_ui, key_name)
            return

        # যদি সেট করা কি চাপা হয়
        if key == self.hotkey:
            if not self.is_running:
                self.after(0, self.start_clicking) # থ্রেড সেফটির জন্য after(0)
            else:
                self.after(0, self.stop_clicking)

    def update_hotkey_ui(self, key_name):
        self.hotkey_name = key_name
        self.hotkey_btn.configure(text=f"Current Hotkey: {key_name}\n(Click to Change)", fg_color="#1F6AA5")
        self.start_btn.configure(text=f"START ({key_name})")
        self.stop_btn.configure(text=f"STOP ({key_name})")

    # --- Click Loop Logic (Made Strong) ---
    def click_loop(self):
        try:
            interval = float(self.interval_entry.get())
        except ValueError:
            interval = 0.01

        btn = self.button_option.get().lower()
        click_mode = self.type_option.get()

        while self.is_running:
            start_time = time.time()
            
            if click_mode == "Single":
                pydirectinput.mouseDown(button=btn)
                pydirectinput.mouseUp(button=btn)
            elif click_mode == "Double":
                pydirectinput.mouseDown(button=btn)
                pydirectinput.mouseUp(button=btn)
                pydirectinput.mouseDown(button=btn)
                pydirectinput.mouseUp(button=btn)
            elif click_mode == "Hold":
                pydirectinput.mouseDown(button=btn)
                while self.is_running:
                    time.sleep(0.01)
                pydirectinput.mouseUp(button=btn)
                break
            
            # ল্যাগ কমানোর জন্য পারফেক্ট স্লিপ টাইমিং
            elapsed = time.time() - start_time
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    # --- Start / Stop Commands ---
    def start_clicking(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.configure(text="Status: CLICKING... ⚡", text_color="#53DC50")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal", fg_color="#E53935")
            self.hotkey_btn.configure(state="disabled")
            self.button_option.configure(state="disabled")
            self.type_option.configure(state="disabled")

            self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
            self.click_thread.start()

    def stop_clicking(self):
        if self.is_running:
            self.is_running = False
            
            # Safety release
            btn = self.button_option.get().lower()
            pydirectinput.mouseUp(button=btn)

            self.status_label.configure(text="Status: Stopped 🛑", text_color="#FF4B4B")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled", fg_color="#333333")
            self.hotkey_btn.configure(state="normal")
            self.button_option.configure(state="normal")
            self.type_option.configure(state="normal")

    def on_closing(self):
        self.is_running = False
        self.listener.stop()
        self.destroy()

if __name__ == "__main__":
    app = SAutoClicker()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()