# DameLaDiapo

DameLaDiapo es una aplicación diseñada para extraer diapositivas de videos, grabaciones de clases, tutoriales o conferencias. La herramienta captura automáticamente imágenes de cada diapositiva y, opcionalmente, las convierte en un archivo PDF. Ideal para cuando no tenemos acceso al archivo de la presentación original pero necesitamos tener las imágenes para estudiar, hacer resúmenes o lo sea. 

Utiliza FFmpeg para la extracción de fotogramas y ImageMagick para la manipulación y conversión de imágenes. Desarrollada en Python, la aplicación integra eficientemente estas herramientas y proporciona un entorno robusto para el procesamiento de datos. La interfaz gráfica, creada con Tkinter, ofrece una experiencia de usuario intuitiva y accesible.

## Características

- **Extracción de Diapositivas:** Captura automáticamente imágenes de cada diapositiva de videos y opcionalmente las convierte en un archivo PDF.
- **Carga de Múltiples Videos:** Permite la conversión masiva de videos, procesándolos de manera secuencial.
- **Selección de Rutas:** Permite elegir graficamente las de entrada y salida de los archivos.
- **Opción de Conservación de Imágenes:** Decide si deseas mantener las imágenes extraídas del video en una carpeta.
- **Opción de Creación de PDF:** Decide si deseas crear un PDF en formato horizontal A4 con las imágenes extraídas.




## Requisitos

Para ejecutar esta aplicación, necesitarás tener instalados los siguientes programas:

- [Python](https://www.python.org/downloads/): Lenguaje de programación necesario para ejecutar el script.
- [FFmpeg](https://ffmpeg.org/download.html): Herramienta para procesamiento de video y audio.
- [ImageMagick](https://imagemagick.org/script/download.php): Herramienta para manipulación de imágenes.


## Instalación y uso

**Instala ffmpeg y ImageMagick**:

- **ffmpeg**: [Instrucciones de instalación](https://ffmpeg.org/download.html)
- **ImageMagick**: [Instrucciones de instalación](https://imagemagick.org/script/download.php)
     
  Asegúrate de agregar FFmpeg e ImageMagick a tu variable de entorno `PATH` para que el script pueda encontrarlos y ejecutarlos correctamente.


**Opción 1: Uso del Ejecutable (Solo Windows)**
1. **Descarga el ejecutable:**
- Ve al directorio dist del repositorio y descarga el archivo DameLaDiapo.exe.


**Opción 2**
1. **Clona el repositorio"**:

    ```bash
    git clone https://github.com/LucasAbrego/DameLaDiapo.git
    ```

2. **Navega al directorio del proyecto**:

    ```bash
    cd "La ruta donde tengas DameLaDiapo"
    ```

3. **Ejecuta el script** `DameLaDiapo.py`:

    ```bash
    python DameLaDiapo.py
    ```



## Interfaz de Usuario
1. **Cargar Videos:** Usa el botón "Cargar Videos" para seleccionar el archivo de video que deseas convertir.
2. **Seleccionar Carpeta de Guardado:** Usa el botón "Seleccionar Carpeta de Guardado" para definir dónde se guardará el archivo PDF.
3. **Conservar Imágenes:** Marca la casilla "Conservar imágenes" si deseas mantener las imágenes extraídas.
4. **Crear PDF:** Marca la casilla "Crear PDF" si deseas generar un PDF con las imágenes extraídas.
5. **Extraer:** Haz clic en el botón "Extraer" para iniciar el proceso de conversión.
6. **Cancelar:** Haz clic en el botón "Cancelar" para detener el proceso de conversión.

### Créditos
- **FFmpeg:** Utilizado para la extracción de imágenes de videos.
- **ImageMagick:** Utilizado para la manipulación de imágenes y creación de PDFs.


### Licencia
Este proyecto está licenciado bajo la **Licencia Pública General GNU v3.0**. Consulta el archivo LICENSE para más detalles.
