import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import shutil


class VideoToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("VideoToPDF - By Luab")
        self.root.iconbitmap("C:/Users/lucas/PycharmProjects/reservaTeatro/venv/icovideotopdf.ico")  # Establecer ícono
        self.center_window(640, 480)  # Ajuste de tamaño a 640x480
        self.root.configure(bg="#2e2e2e")  # Fondo oscuro

        self.video_path_var = tk.StringVar()
        self.pdf_path_var = tk.StringVar()
        self.keep_images_var = tk.BooleanVar()  # Variable para el checkbox

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Botón para cargar video
        self.load_button = tk.Button(self.root, text="Cargar Video", command=self.browse_file,
                                     font=("Arial", 16, "bold"), bg="#4a4a4a", fg="#ffffff", relief="flat")
        self.load_button.pack(pady=(35, 5), padx=10, fill=tk.X)

        # Marco para la entrada del camino del video
        frame = tk.Frame(self.root, bg="#2e2e2e")
        frame.pack(pady=(5, 35), padx=10, fill=tk.X)

        self.path_entry = tk.Entry(frame, textvariable=self.video_path_var, width=72, state='readonly',
                                   font=("Arial", 16), bg="#ffffff", fg="#000000", borderwidth=0)
        self.path_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        # Botón para seleccionar ubicación del PDF
        self.save_button = tk.Button(self.root, text="Seleccionar Ruta de Guardado", command=self.browse_pdf_location,
                                     font=("Arial", 16, "bold"), bg="#4a4a4a", fg="#ffffff", relief="flat")
        self.save_button.pack(pady=(10, 5), padx=10, fill=tk.X)

        # Marco para la entrada del camino del PDF
        pdf_frame = tk.Frame(self.root, bg="#2e2e2e")
        pdf_frame.pack(pady=5, padx=10, fill=tk.X)

        self.pdf_path_entry = tk.Entry(pdf_frame, textvariable=self.pdf_path_var, width=72, state='readonly',
                                       font=("Arial", 16), bg="#ffffff", fg="#000000", borderwidth=0)
        self.pdf_path_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        # Checkbox para conservar imágenes
        self.keep_images_checkbox = tk.Checkbutton(self.root, text="Conservar imágenes", variable=self.keep_images_var,
                                                   font=("Arial", 14), bg="#2e2e2e", fg="#ffffff",
                                                   selectcolor="#4a4a4a", activebackground="#4a4a4a", relief="flat")
        self.keep_images_checkbox.pack(pady=(40, 15))

        # Botón para convertir
        self.convert_button = tk.Button(self.root, text="Convertir a PDF", command=self.start_conversion, bg="#28a745",
                                        fg="white", font=("Arial", 16, "bold"), height=2, width=20, relief="flat")
        self.convert_button.pack(pady=(5, 35), padx=10, side=tk.BOTTOM)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 Video", "*.mp4")])
        if file_path:
            self.video_path_var.set(file_path)
            # Ajustar automáticamente la ruta del PDF al mismo directorio que el video
            self.pdf_path_var.set(
                os.path.join(os.path.dirname(file_path), f"PDF_{os.path.basename(file_path).replace('.mp4', '')}.pdf"))

    def browse_pdf_location(self):
        directory = filedialog.askdirectory()
        if directory:
            video_name = os.path.basename(self.video_path_var.get()).replace(".mp4", "")
            self.pdf_path_var.set(os.path.join(directory, f"PDF_{video_name}.pdf"))

    def start_conversion(self):
        video_path = self.video_path_var.get()
        pdf_path = self.pdf_path_var.get()
        if not video_path or not pdf_path:
            messagebox.showwarning("Warning", "Please select a video file and PDF save location.")
            return

        # Iniciar la conversión en un hilo separado
        threading.Thread(target=self.convert_video, args=(video_path, pdf_path,), daemon=True).start()

    def convert_video(self, video_path, pdf_path):
        video_dir = os.path.dirname(video_path)
        video_name = os.path.basename(video_path).replace(".mp4", "")
        image_dir = os.path.join(video_dir, f"{video_name}_frames")

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Construir comandos
        get_first_frame_cmd = f'ffmpeg -ss 1 -i "{video_path}" -vf "select=eq(n\\,0)" -vsync vfr "{image_dir}/{video_name}_frames_0000.png"'
        get_other_frames_cmd = f'ffmpeg -i "{video_path}" -vf "select=\'gt(scene,0.05)\',showinfo" -vsync vfr "{image_dir}/{video_name}_frames_%04d.png"'
        resize_frames_cmd = f'magick mogrify -resize 3226x2283 -density 300 -units PixelsPerInch "{image_dir}/{video_name}_frames_*.png"'
        create_pdf_cmd = f'magick convert "{image_dir}/{video_name}_frames_*.png" -density 300 -gravity center -background white -extent 3508x2480 -quality 100 -units PixelsPerInch "{pdf_path}"'

        # Ejecutar comandos
        self.run_command(get_first_frame_cmd)
        self.run_command(get_other_frames_cmd)
        self.run_command(resize_frames_cmd)
        self.run_command(create_pdf_cmd)

        # Notificar al usuario de la finalización
        if not self.keep_images_var.get():
            self.delete_images(image_dir)

        self.show_completion_message(pdf_path)

    def run_command(self, command):
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def delete_images(self, directory):
        if os.path.isdir(directory):
            shutil.rmtree(directory)

    def show_completion_message(self, pdf_path):
        messagebox.showinfo("Conversión Completa", f"PDF guardado como {pdf_path}")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToPDFConverter(root)
    root.mainloop()