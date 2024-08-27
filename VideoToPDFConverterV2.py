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

        self.video_paths = []  # Lista para almacenar múltiples rutas de videos
        self.pdf_dir = tk.StringVar()
        self.keep_images_var = tk.BooleanVar()  # Variable para el checkbox

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Botón para cargar videos
        self.load_button = tk.Button(self.root, text="Cargar Videos", command=self.browse_files,
                                     font=("Arial", 16, "bold"), bg="#4a4a4a", fg="#ffffff", relief="flat")
        self.load_button.pack(pady=(35, 5), padx=10, fill=tk.X)

        # Marco para la entrada del camino de los videos
        frame = tk.Frame(self.root, bg="#2e2e2e")
        frame.pack(pady=(5, 35), padx=10, fill=tk.X)

        self.path_entry = tk.Entry(frame, textvariable=tk.StringVar(value="No se han seleccionado videos"), width=72, state='readonly',
                                   font=("Arial", 16), bg="#ffffff", fg="#000000", borderwidth=0)
        self.path_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        # Botón para seleccionar ubicación del PDF
        self.save_button = tk.Button(self.root, text="Seleccionar Carpeta de Guardado", command=self.browse_pdf_location,
                                     font=("Arial", 16, "bold"), bg="#4a4a4a", fg="#ffffff", relief="flat")
        self.save_button.pack(pady=(10, 5), padx=10, fill=tk.X)

        # Marco para la entrada del camino de la carpeta de PDFs
        pdf_frame = tk.Frame(self.root, bg="#2e2e2e")
        pdf_frame.pack(pady=5, padx=10, fill=tk.X)

        self.pdf_path_entry = tk.Entry(pdf_frame, textvariable=self.pdf_dir, width=72, state='readonly',
                                       font=("Arial", 16), bg="#ffffff", fg="#000000", borderwidth=0)
        self.pdf_path_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        # Checkbox para conservar imágenes
        self.keep_images_checkbox = tk.Checkbutton(self.root, text="Conservar imágenes", variable=self.keep_images_var,
                                                   font=("Arial", 14), bg="#2e2e2e", fg="#ffffff",
                                                   selectcolor="#4a4a4a", activebackground="#4a4a4a", relief="flat")
        self.keep_images_checkbox.pack(pady=(40, 15))

        # Etiqueta para mostrar el estado de la conversión
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#2e2e2e", fg="#ffffff")
        self.status_label.pack(pady=(5, 10))

        # Botón para convertir
        self.convert_button = tk.Button(self.root, text="Convertir a PDF", command=self.start_conversion, bg="#28a745",
                                        fg="white", font=("Arial", 16, "bold"), height=2, width=20, relief="flat")
        self.convert_button.pack(pady=(5, 35), padx=10, side=tk.BOTTOM)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP4 Video", "*.mp4")])
        if file_paths:
            self.video_paths = file_paths
            self.path_entry.config(state='normal')
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, f"{len(file_paths)} videos seleccionados")
            self.path_entry.config(state='readonly')

    def browse_pdf_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.pdf_dir.set(directory)

    def start_conversion(self):
        if not self.video_paths or not self.pdf_dir.get():
            messagebox.showwarning("Warning", "Please select video files and PDF save location.")
            return

        # Iniciar la conversión en un hilo separado
        threading.Thread(target=self.convert_videos, daemon=True).start()

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def convert_videos(self):
        for i, video_path in enumerate(self.video_paths):
            video_name = os.path.basename(video_path).replace(".mp4", "")
            video_dir = os.path.dirname(video_path)
            output_dir = os.path.join(self.pdf_dir.get(), video_name)
            image_dir = os.path.join(output_dir, f"imagenes_{video_name}")

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Actualizar el estado de la interfaz gráfica
            self.update_status(f"Convirtiendo {video_name} ({i + 1}/{len(self.video_paths)})")

            # Construir comandos
            get_first_frame_cmd = f'ffmpeg -ss 1 -i "{video_path}" -vf "select=eq(n\\,0)" -vsync vfr "{image_dir}/{video_name}_frames_0000.png"'
            get_other_frames_cmd = f'ffmpeg -i "{video_path}" -vf "select=\'gt(scene,0.05)\',showinfo" -vsync vfr "{image_dir}/{video_name}_frames_%04d.png"'
            resize_frames_cmd = f'magick mogrify -resize 3226x2283 -density 300 -units PixelsPerInch "{image_dir}/{video_name}_frames_*.png"'
            create_pdf_cmd = f'magick convert "{image_dir}/{video_name}_frames_*.png" -density 300 -gravity center -background white -extent 3508x2480 -quality 100 -units PixelsPerInch "{os.path.join(output_dir, f"PDF_{video_name}.pdf")}"'

            # Ejecutar comandos
            self.run_command(get_first_frame_cmd)
            self.run_command(get_other_frames_cmd)
            self.run_command(resize_frames_cmd)
            self.run_command(create_pdf_cmd)

            # Notificar al usuario de la finalización para cada video
            if not self.keep_images_var.get():
                self.delete_images(image_dir)

        # Actualizar estado al finalizar todos los procesos
        self.update_status("Todos los videos han sido convertidos.")

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
