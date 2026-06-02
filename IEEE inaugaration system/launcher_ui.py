import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class LauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Women In Engineering - Aadya Inauguration")
        self.root.geometry("550x450")
        self.root.configure(bg="#000000")  # Black
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(root, bg="#1C1C1C")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=25)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Women In Engineering Affinity Group KSSEM",
            font=("Times New Roman", 48, "bold"),
            bg="#1C1C1C",
            fg="#FFD700"
        )
        title_label.pack(pady=20)
        
        # Aadya
        aadya_label = tk.Label(
            main_frame,
            text="Aadhya",
            font=("Georgia", 52, "bold"),
            bg="#100F0F",
            fg="#E91FF0"
        )
        aadya_label.pack(pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Inauguration Ceremony",
            font=("Helvetica", 40, "italic"),
            bg="#1C1C1C",
            fg="#E96507"
        )
        subtitle_label.pack(pady=15)
        
        # Launch Button
        launch_button = tk.Button(
            main_frame,
            text="LAUNCH",
            font=("Verdana", 20, "bold"),
            bg="#FFD700",
            fg="#000000",
            padx=50,
            pady=18,
            command=self.launch_camera,
            activebackground="#C9A227",
            activeforeground="#000000",
            relief=tk.RAISED,
            bd=4
        )
        launch_button.pack(pady=35)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready",
            font=("Calibri", 11),
            bg="#1C1C1C",
            fg="#00C853"
        )
        self.status_label.pack(pady=10)
    
    def launch_camera(self):
        try:
            self.status_label.config(text="Opening camera feed...", fg="#FFAB00")
            self.root.update()
            
            # Hide the launcher window immediately
            self.root.withdraw()
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_script = os.path.join(script_dir, "import cv2.py")
            
            if not os.path.exists(main_script):
                self.root.deiconify()
                messagebox.showerror("Error", f"Main script not found: {main_script}")
                self.status_label.config(text="Ready", fg="#00C853")
                return
            
            subprocess.run([sys.executable, main_script], check=True)
            self.root.destroy()  # Close launcher after video playback
            
        except subprocess.CalledProcessError as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Camera feed error: {str(e)}")
            self.status_label.config(text="Ready", fg="#00C853")
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Ready", fg="#00C853")

def main():
    root = tk.Tk()
    app = LauncherUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()