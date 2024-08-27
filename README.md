# VideoToPDFConverter

VideoToPDFConverter es una aplicación de Python diseñada para extraer diapositivas de videos, como grabaciones de clases o presentaciones, y convertirlas en un archivo PDF de alta calidad. Esta herramienta es útil para convertir tutoriales, conferencias, y otros contenidos en formato PDF para facilitar su revisión, impresión o almacenamiento.


## Características

- **Extracción de Diapositivas:** Convierte videos en presentaciones PDF extrayendo imágenes de los mismos.
- **Selección de Rutas:** Permite seleccionar la ubicación del archivo de entrada (video) y la ruta de salida (PDF).
- **Opción de Conservación de Imágenes:** Decide si quieres mantener las imágenes extraídas del video.
- **Carga de múltiples videos (Solo VideoToPDFConverterV2):** Permite la conversión masiva de videos, procesándolos de manera secuencial generando un PDF y carpeta de imágenes para cada video.


## Requisitos

Para ejecutar esta aplicación, necesitarás tener instalados los siguientes programas:

- [Python](https://www.python.org/downloads/): Lenguaje de programación necesario para ejecutar el script.
- [FFmpeg](https://ffmpeg.org/download.html): Herramienta para procesamiento de video y audio.
- [ImageMagick](https://imagemagick.org/script/download.php): Herramienta para manipulación de imágenes.


## Instalación y uso

1. **Instala ffmpeg y ImageMagick**:

    - **ffmpeg**: [Instrucciones de instalación](https://ffmpeg.org/download.html)
    - **ImageMagick**: [Instrucciones de instalación](https://imagemagick.org/script/download.php)
     
    Asegúrate de agregar FFmpeg e ImageMagick a tu variable de entorno `PATH` para que el script pueda encontrarlos y ejecutarlos correctamente.
   
2. **Clona el repositorio**:

    ```bash
    git clone https://github.com/LucasAbrego/VideoToPDFConverter.git
    ```

3. **Navega al directorio del proyecto**:

    ```bash
    cd "La ruta donde tengas VideoToPDFConverter"
    ```

. **Ejecuta el script** `VideoToPDFConverter.py` **para convertir videos individuales en PDF**:

    ```bash
    python VideoToPDFConverter.py
    ```

   **O ejecuta el script** `VideoToPDFConverterV2.py` **para convertir múltiples videos de manera secuencial**:

    ```bash
    python VideoToPDFConverterV2.py
    ```
    
Ambos scripts utilizan FFmpeg e ImageMagick para extraer imágenes y crear el archivo PDF, pero `VideoToPDFConverterV2.py` añade la funcionalidad de procesar múltiples videos.

## Interfaz de Usuario
1. Cargar Video: Usa el botón "Cargar Video" para seleccionar el archivo de video que deseas convertir.
2. Seleccionar Ruta de Guardado: Usa el botón "Seleccionar Ruta de Guardado" para definir dónde se guardará el archivo PDF.
3. Convertir a PDF: Haz clic en el botón "Convertir a PDF" para iniciar el proceso de conversión.


### Créditos
- FFmpeg: Utilizado para la extracción de imágenes de videos.
- ImageMagick: Utilizado para la manipulación de imágenes y creación de PDFs.


### Licencia
Este proyecto está licenciado bajo la **Licencia Pública General GNU v3.0**. Consulta el archivo LICENSE para más detalles.
