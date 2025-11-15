#****************************************************************************************************
#
#       Name:         Kyle McColgan
#       File name:    passwordGen.py
#       Date:         11 November 2025
#       Description: This program provides a GUI-based client to generate URL-friendly passwords.
#
#****************************************************************************************************

import tkinter as tk
from tkinter import messagebox, scrolledtext
import secrets
import base64

#****************************************************************************************************

class PasswordGenApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('passwordGen - Simple Password Generator')
        self.root.geometry("540x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#0d1117")

        # Style configuration.
        self.font_title = ("Segoe UI", 15, "bold")
        self.font_text = ("Segoe UI", 10)
        self.font_button = ("Segoe UI", 10, "bold")
        self.accent_color = "#58a6ff"
        self.secondary_color = "#2ea043"
        self.text_color = "#c9d1d9"
        self.bg_color = "#0d1117"
        self.panel_color = "#161b22"
        self.muted_text = "#8b949e"

        # Header
        tk.Label(
            self.root,
            text="🔐 passwordGen",
            bg=self.bg_color,
            fg=self.accent_color,
            font=self.font_title
        ).pack(pady=(18, 3))

        tk.Label(
            self.root,
            text="Generate cryptographically secure passwords instantly.",
            bg=self.bg_color,
            fg=self.muted_text,
            font=("Segoe UI", 9)
        ).pack(pady=(0, 12))

        #Output Panel.
        output_frame = tk.Frame(self.root, bg=self.panel_color, bd=1, relief="flat")
        output_frame.pack(pady=10, padx=25, fill="x")

        tk.Label(
            output_frame,
            text="Generated Password:",
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", padx=10, pady=(8, 0))

        self.output_box = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=60,
            height=3,
            state="disabled",
            bg="#0d1117",
            fg="#00ff9f",
            insertbackground="white",
            font=("Consolas", 10),
            relief="flat",
            padx=10,
            pady=8
        )
        self.output_box.pack(padx=10, pady=(4, 8))

        # Frame for length input and generate buttons.
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=8)

        tk.Label(
            input_frame,
            text="Password Length:",
            bg=self.bg_color,
            fg=self.text_color
        ).grid(row=0, column=0, padx=6)

        self.length_entry = tk.Entry(
            input_frame,
            width=6,
            font=self.font_text,
            justify="center",
            bg=self.panel_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat"
        )
        self.length_entry.insert(0, "64")
        self.length_entry.grid(row=0, column=1, padx=6)

        tk.Button(
            input_frame,
            text="Generate",
            font=self.font_button,
            bg=self.accent_color,
            fg="#0d1117",
            activebackground=self.accent_color,
            activeforeground="#0d1117",
            relief="flat",
            width=14,
            cursor="hand2",
            command=self.generate_password
        ).grid(row=0, column=2, padx=10)

        #Bottom buttons.
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=22)

        self._create_button(button_frame, "Copy", self.copy_password, self.accent_color)
        self._create_button(button_frame, "Save", self.save_password, self.secondary_color)
        self._create_button(button_frame, "Quit", self.root.quit, "#ff5555")

        #Footer.
        tk.Label(
            self.root,
            text="© 2025 Kyle McColgan - Built with Python 🐍",
            bg=self.bg_color,
            fg=self.muted_text,
            font=("Segoe UI", 8)
        ).pack(side="bottom", pady=6)

        self.root.mainloop()

    def _create_button(self, parent, text, command, color):
        """Helper function to create modern, flat-style buttons."""
        return tk.Button(
            parent,
            text=text,
            font=self.font_button,
            bg=color,
            fg="#0d1117",
            activebackground=color,
            activeforeground="#0d1117",
            relief="flat",
            width=10,
            cursor="hand2",
            command=command
        ).pack(side="left", padx=10)

    def generate_password(self):
        # Retrieve the desired password length
        try:
            length = int(self.length_entry.get())
            if not 8 <= length <= 512:
                messagebox.showwarning("Invalid Length", "Password length must be between 8 and 512 characters.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        # Generate password
        # Generate enough random bytes for the desired length
        bytes_needed = (length * 6 + 7) // 8  # Calculating required bytes for Base64 output
        random_bytes = secrets.token_bytes(bytes_needed)
        password = base64.b64encode(random_bytes).decode('utf-8')[:length]

        # Display password in text widget
        self.output_box.config(state="normal")
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, password)
        self.output_box.config(state='disabled')

    def copy_password(self):
        password = self.output_box.get(1.0, tk.END).strip()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "Please generate a password first.")

    def save_password(self):
        password = self.output_box.get(1.0, tk.END).strip()
        if password:
            with open("generated_password.txt", "w") as file:
                file.write(password)
            messagebox.showinfo("Saved", "Password saved to generated_password.txt")
        else:
            messagebox.showwarning("No Password", "Please generate a password first.")

#****************************************************************************************************

if __name__ == "__main__":
    PasswordGenApp()

#****************************************************************************************************