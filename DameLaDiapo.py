import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import shutil
import sys

class DameLaDiapo:
    def __init__(self, root):
        self.root = root
        self.root.title("DameLaDiapo - By Luab")
        self.root.iconbitmap("ico/icovideotopdf.ico")
        self.center_window(720, 480)
        self.root.configure(bg="#2e2e2e")

        self.video_paths = []
        self.pdf_dir = tk.StringVar()
        self.keep_images_var = tk.BooleanVar()
        self.create_pdf_var = tk.BooleanVar(value=True)
        self.conversion_thread = None
        self.cancel_flag = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self.root, text="Cargar Videos", command=self.browse_files,
                                     font=("Arial", 16, "bold"), bg="#4a4a4a", fg="#ffffff", relief="flat")
        self.load_button.pack(pady=(35, 5), padx=10, fill=tk.X)

        frame = tk.Frame(self.root, bg="#2e2e2e")
        frame.pack(pady=(5, 35), padx=10, fill=tk.X)

        self.path_label = tk.Label(frame, text="No se han seleccionado videos", width=72, wraplength=600,
                                   font=("Arial", 16), bg="#ffffff", fg="#000000", borderwidth=0, anchor="w")
        self.path_label.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        self.save_button = tk.Button(self.root, text="Seleccionar Carpeta de Guardado", command=self.browse_pdf_location,
                                     font=("Arial", 16, "bold"), bg="#4a4a4a", fg="#ffffff", relief="flat")
        self.save_button.pack(pady=(10, 5), padx=10, fill=tk.X)

        pdf_frame = tk.Frame(self.root, bg="#2e2e2e")
        pdf_frame.pack(pady=5, padx=10, fill=tk.X)

        self.pdf_path_entry = tk.Entry(pdf_frame, textvariable=self.pdf_dir, width=72, state='readonly',
                                       font=("Arial", 16), bg="#ffffff", fg="#000000", borderwidth=0)
        self.pdf_path_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        self.keep_images_checkbox = tk.Checkbutton(self.root, text="Conservar imágenes", variable=self.keep_images_var,
                                                   font=("Arial", 14), bg="#2e2e2e", fg="#ffffff",
                                                   selectcolor="#4a4a4a", activebackground="#4a4a4a", relief="flat")
        self.keep_images_checkbox.pack(pady=(10, 5))

        self.create_pdf_checkbox = tk.Checkbutton(self.root, text="Crear PDF", variable=self.create_pdf_var,
                                                  font=("Arial", 14), bg="#2e2e2e", fg="#ffffff", selectcolor="#4a4a4a",
                                                  activebackground="#4a4a4a", relief="flat")
        self.create_pdf_checkbox.pack(pady=(5, 10))

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#2e2e2e", fg="#ffffff")
        self.status_label.pack(pady=(5, 20))

        button_frame = tk.Frame(self.root, bg="#2e2e2e")
        button_frame.pack(pady=(5, 35), padx=10, fill=tk.X)

        self.convert_button = tk.Button(button_frame, text="Extraer", command=self.start_conversion, bg="#28a745",
                                        fg="white", font=("Arial", 16, "bold"), height=2, width=20, relief="flat")
        self.convert_button.pack(side=tk.LEFT, padx=(35, 5))

        self.cancel_button = tk.Button(button_frame, text="Cancelar", command=self.cancel_conversion, bg="#dc3545",
                                       fg="white", font=("Arial", 16, "bold"), height=2, width=20, relief="flat")
        self.cancel_button.pack(side=tk.RIGHT, padx=(5, 35))

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP4 Video", "*.mp4")])
        if file_paths:
            if any(';' in os.path.dirname(path) for path in file_paths):
                messagebox.showwarning("Ruta de archivo inválida",
                                       "Una o más rutas de archivo contienen el carácter ';'. Por favor, seleccione archivos con rutas sin ';'.")
                return
            self.video_paths = file_paths
            self.path_label.config(text=f"{len(file_paths)} videos seleccionados")

    def browse_pdf_location(self):
        directory = filedialog.askdirectory()
        if directory:
            if ';' in directory:
                messagebox.showwarning("Ruta de carpeta inválida",
                                       "La ruta de la carpeta seleccionada contiene el carácter ';'. Por favor, seleccione una carpeta con una ruta sin ';'.")
                return
            self.pdf_dir.set(directory)

    def start_conversion(self):
        if not self.video_paths or not self.pdf_dir.get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione archivos de video y una ubicación para guardar el PDF.")
            return

        if not self.keep_images_var.get() and not self.create_pdf_var.get():
            messagebox.showwarning("Advertencia",
                                   "Debe seleccionar al menos una opción: crear PDF o conservar imágenes.")
            return

        self.cancel_flag.clear()
        self.conversion_thread = threading.Thread(target=self.convert_videos, daemon=True)
        self.conversion_thread.start()

    def cancel_conversion(self):
        if self.conversion_thread:
            self.cancel_flag.set()
            self.conversion_thread.join(timeout=5)
            self.conversion_thread = None

        self.update_status("Conversión cancelada.")

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def convert_videos(self):
        for i, video_path in enumerate(self.video_paths):
            if self.cancel_flag.is_set():
                self.update_status("Conversión cancelada.")
                return

            original_video_name = os.path.basename(video_path).replace(".mp4", "")
            video_dir = os.path.dirname(video_path)

            sanitized_video_name = original_video_name.replace(';', '_').replace(' ', '_')[:30]
            output_dir = os.path.join(self.pdf_dir.get(), sanitized_video_name)
            image_dir = os.path.join(output_dir, f"imagenes_{sanitized_video_name}")

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            self.update_status(f"Convirtiendo {original_video_name} ({i + 1}/{len(self.video_paths)})")

            get_first_frame_cmd = f'ffmpeg -ss 1 -i "{video_path}" -vf "select=eq(n\\,0)" -vsync vfr "{os.path.join(image_dir, f"{sanitized_video_name}_frames_0000.png")}"'
            get_other_frames_cmd = f'ffmpeg -i "{video_path}" -vf "select=\'gt(scene,0.025)\',showinfo" -vsync vfr "{os.path.join(image_dir, f"{sanitized_video_name}_frames_%04d.png")}"'
            resize_frames_cmd = f'magick mogrify -resize 3226x2283 -density 300 -units PixelsPerInch "{os.path.join(image_dir, f"{sanitized_video_name}_frames_*.png")}"'
            create_pdf_cmd = f'magick convert "{os.path.join(image_dir, f"{sanitized_video_name}_frames_*.png")}" -density 300 -gravity center -background white -extent 3508x2480 -quality 100 -units PixelsPerInch "{os.path.join(output_dir, f"PDF_{sanitized_video_name}.pdf")}"'

            if not self.run_command(get_first_frame_cmd):
                return
            if not self.run_command(get_other_frames_cmd):
                return
            if not self.run_command(resize_frames_cmd):
                return

            if self.create_pdf_var.get():
                if not self.run_command(create_pdf_cmd):
                    return

            if not self.keep_images_var.get():
                self.delete_images(image_dir)

            if self.cancel_flag.is_set():
                return

        self.update_status("Todos los videos han sido convertidos.")

    def run_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(stdout.decode())
            print(stderr.decode(), file=sys.stderr)
            return process.returncode == 0
        except Exception as e:
            print(f"Error ejecutando el comando: {e}")
            return False

    def delete_images(self, directory):
        if os.path.isdir(directory):
            shutil.rmtree(directory)

    def show_completion_message(self, pdf_path):
        messagebox.showinfo("Conversión Completa", f"PDF guardado en: {pdf_path}")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DameLaDiapo(root)
    root.mainloop()
