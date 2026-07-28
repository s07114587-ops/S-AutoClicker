# ==============================================================================
# S-AutoClicker Pro
# Copyright (c) 2026 Shubhomoy (sgdev)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# ==============================================================================

import os
import sys
import time
import threading
import webbrowser
import customtkinter as ctk
import pydirectinput
from pynput import keyboard

# pydirectinput Safety Settings
pydirectinput.FAILSAFE = True

class SAutoClicker(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("S-AutoClicker Pro")
        self.geometry("320x460")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # --- Variables ---
        self.is_running = False
        self.hotkey = keyboard.Key.f5  # Default Hotkey: F5
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
            text="Developed by Shubhomoy (sgdev)\nLicensed under GNU AGPLv3", 
            font=("Roboto", 10),
            text_color="#888888"
        )
        self.sub_label.pack(pady=(0, 15))

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
        self.type_option.pack(pady=(2, 15), padx=25, fill="x")

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
        self.status_label.pack(pady=15)

        # Control Buttons
        self.start_btn = ctk.CTkButton(
            master=self.main_frame, 
            text="START (F5)", 
            font=("Roboto", 14, "bold"),
            command=self.start_clicking
        )
        self.start_btn.pack(pady=5, padx=25, fill="x")

        self.stop_btn = ctk.CTkButton(
            master=self.main_frame, 
            text="STOP (F5)", 
            font=("Roboto", 14, "bold"),
            fg_color="#333333",
            state="disabled",
            command=self.stop_clicking
        )
        self.stop_btn.pack(pady=5, padx=25, fill="x")

    # --- Hotkey Handler ---
    def handle_hotkey(self, key):
        if key == self.hotkey:
            if not self.is_running:
                self.start_clicking()
            else:
                self.stop_clicking()

    # --- Click Loop Logic ---
    def click_loop(self):
        try:
            interval = float(self.interval_entry.get())
        except ValueError:
            interval = 0.01

        btn = self.button_option.get().lower()
        click_mode = self.type_option.get()

        pydirectinput.PAUSE = interval

        while self.is_running:
            if click_mode == "Single":
                pydirectinput.click(button=btn)
            elif click_mode == "Double":
                pydirectinput.click(button=btn, clicks=2, interval=0.05)
            elif click_mode == "Hold":
                pydirectinput.mouseDown(button=btn)
                while self.is_running:
                    time.sleep(0.05)
                pydirectinput.mouseUp(button=btn)
                break
            
            time.sleep(interval)

    # --- Start / Stop Commands ---
    def start_clicking(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.configure(text="Status: CLICKING... ⚡", text_color="#53DC50")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal", fg_color="#E53935")
            self.button_option.configure(state="disabled")
            self.type_option.configure(state="disabled")

            self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
            self.click_thread.start()

    def stop_clicking(self):
        if self.is_running:
            self.is_running = False
            
            # If mouse button was held down, release it safety-wise
            btn = self.button_option.get().lower()
            pydirectinput.mouseUp(button=btn)

            self.status_label.configure(text="Status: Stopped 🛑", text_color="#FF4B4B")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled", fg_color="#333333")
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