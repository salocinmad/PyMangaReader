import tkinter as tk
from tkinter import filedialog, colorchooser, OptionMenu
import zipfile
import rarfile
import os
from PIL import Image, ImageTk
from pdf2image import convert_from_path

# Diccionario para las traducciones
idiomas = {
    "Español": {
        "Buscar": "Buscar",
        "Redimensionar Imagen": "Redimensionar Imagen",
        "Anterior": "Anterior",
        "Siguiente": "Siguiente",
        "Acercar": "Acercar",
        "Alejar": "Alejar",
        "Cambiar Color": "Cambiar Color",
        "Idioma": "Idioma"
    },
    "Inglés": {
        "Buscar": "Search",
        "Redimensionar Imagen": "Resize Image",
        "Anterior": "Previous",
        "Siguiente": "Next",
        "Acercar": "Zoom In",
        "Alejar": "Zoom Out",
        "Cambiar Color": "Change Color",
        "Idioma": "Language"
    },
    "Japonés": {
        "Buscar": "検索",
        "Redimensionar Imagen": "画像のサイズ変更",
        "Anterior": "前",
        "Siguiente": "次",
        "Acercar": "ズームイン",
        "Alejar": "ズームアウト",
        "Cambiar Color": "色を変える",
        "Idioma": "言語"
    },
    "Chino": {
        "Buscar": "搜索",
        "Redimensionar Imagen": "调整图片大小",
        "Anterior": "上一个",
        "Siguiente": "下一个",
        "Acercar": "放大",
        "Alejar": "缩小",
        "Cambiar Color": "改变颜色",
        "Idioma": "语言"
    },
    "Italiano": {
        "Buscar": "Cerca",
        "Redimensionar Imagen": "Ridimensiona Immagine",
        "Anterior": "Precedente",
        "Siguiente": "Successivo",
        "Acercar": "Ingrandisci",
        "Alejar": "Riduci",
        "Cambiar Color": "Cambia Colore",
        "Idioma": "Lingua"
    }
}

# Clase para el lector de manga
class LectorManga:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lector de Manga")
        self.label = tk.Label(self.root, text="Seleccione un archivo ZIP, CBR o PDF:")
        self.label.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.button_frame = tk.Frame(self.root)
        self.button = tk.Button(self.button_frame, text=idiomas["Español"]["Buscar"], command=self.buscar_archivo, bg='SystemButtonFace')
        self.button.pack(side=tk.LEFT)
        self.resize_button = tk.Button(self.button_frame, text=idiomas["Español"]["Redimensionar Imagen"], command=self.redimensionar_imagen, bg='SystemButtonFace')
        self.resize_button.pack(side=tk.LEFT)
        self.prev_button = tk.Button(self.button_frame, text=idiomas["Español"]["Anterior"], command=self.pagina_anterior, bg='SystemButtonFace')
        self.prev_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.button_frame, text=idiomas["Español"]["Siguiente"], command=self.pagina_siguiente, bg='SystemButtonFace')
        self.next_button.pack(side=tk.LEFT)
        self.zoom_in_button = tk.Button(self.button_frame, text=idiomas["Español"]["Acercar"], command=self.acercar, bg='SystemButtonFace')
        self.zoom_in_button.pack(side=tk.LEFT)
        self.zoom_out_button = tk.Button(self.button_frame, text=idiomas["Español"]["Alejar"], command=self.alejar, bg='SystemButtonFace')
        self.zoom_out_button.pack(side=tk.LEFT)
        self.color_button = tk.Button(self.button_frame, text=idiomas["Español"]["Cambiar Color"], command=self.cambiar_color, bg='SystemButtonFace')
        self.color_button.pack(side=tk.LEFT)
        self.idioma = tk.StringVar(self.root)
        self.idioma.set("Español") # idioma por defecto
        self.idioma_menu = OptionMenu(self.button_frame, self.idioma, *idiomas.keys(), command=self.cambiar_idioma)
        self.idioma_menu.pack(side=tk.LEFT)
        self.button_frame.pack(side=tk.BOTTOM)
        self.image_frame = tk.Canvas(self.root, bd=2, relief=tk.SUNKEN, bg="#282828")
        self.image_frame.pack(fill=tk.BOTH, expand=True)
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.zoom_factor = 1.0
        self.current_image_index = 0
        self.scroll_factor = 0
        

        # Atajos de teclado
        self.root.bind("<Right>", lambda event: self.pagina_siguiente())
        self.root.bind("<Left>", lambda event: self.pagina_anterior())
        self.root.bind("<Up>", lambda event: self.acercar())
        self.root.bind("<Down>", lambda event: self.alejar())
        self.root.bind("<w>", lambda event: self.desplazar_arriba())
        self.root.bind("<s>", lambda event: self.desplazar_abajo())
        self.root.bind("<r>", lambda event: self.redimensionar_imagen())
        # Eventos de la rueda del mouse
        self.root.bind("<MouseWheel>", self.zoom_con_rueda)

    def cambiar_idioma(self, idioma):
        self.button.config(text=idiomas[idioma]["Buscar"])
        self.resize_button.config(text=idiomas[idioma]["Redimensionar Imagen"])
        self.prev_button.config(text=idiomas[idioma]["Anterior"])
        self.next_button.config(text=idiomas[idioma]["Siguiente"])
        self.zoom_in_button.config(text=idiomas[idioma]["Acercar"])
        self.zoom_out_button.config(text=idiomas[idioma]["Alejar"])
        self.color_button.config(text=idiomas[idioma]["Cambiar Color"])
    
    def zoom_con_rueda(self, event):
        # En Windows, event.delta es 120 para scroll hacia arriba, -120 para scroll hacia abajo.
        if event.delta > 0:
            self.acercar()
        else:
            self.alejar()
 
    # Función para buscar archivos
    def buscar_archivo(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Archivos de cómic", "*.zip *.cbr *.pdf")])
        if self.file_path:
            self.entry.insert(0, self.file_path)
            self.extraer_imagenes(self.file_path)

    # Función para extraer imágenes de los archivos
    def extraer_imagenes(self, file_path):
        images_dir = os.path.join(os.path.dirname(self.file_path), "images")
        os.makedirs(images_dir, exist_ok=True)
        self.image_files = []
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                self.extraer_de_archivo(zip_ref, images_dir)
        elif file_path.endswith(".cbr"):
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                self.extraer_de_archivo(rar_ref, images_dir)
        elif file_path.endswith(".pdf"):
            self.extraer_de_pdf(file_path, images_dir)
        self.cargar_imagen()

    # Función para extraer imágenes de archivos comprimidos
    def extraer_de_archivo(self, archive, images_dir):
        for info in archive.infolist():
            if info.filename.endswith((".jpg", ".png")):
                image_data = archive.read(info)
                with open(os.path.join(images_dir, info.filename), 'wb') as f:
                    f.write(image_data)
                self.image_files.append(info.filename)

    # Función para extraer imágenes de archivos PDF
    def extraer_de_pdf(self, file_path, images_dir):
        images = convert_from_path(file_path)
        for i, image in enumerate(images):
            image_file = os.path.join(images_dir, f"pagina_{i}.png")
            image.save(image_file)
            self.image_files.append(image_file)

    # Función para cargar la imagen
    def cargar_imagen(self):
        self.mostrar_imagen(self.image_files[self.current_image_index])

    # Función para mostrar la imagen
    def mostrar_imagen(self, image_file):
        image_path = os.path.join(os.path.dirname(self.file_path), "images", image_file)
        img = Image.open(image_path)
        img.thumbnail((int(self.image_frame.winfo_width() * self.zoom_factor), int(self.image_frame.winfo_height() * self.zoom_factor)), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk, bg=self.image_frame.cget('bg'))
        self.image_label.image = img_tk

    # Función para acercar la imagen
    def acercar(self):
        self.zoom_factor += 0.1
        self.cargar_imagen()

    # Función para alejar la imagen
    def alejar(self):
        if self.zoom_factor > 0.1:
            self.zoom_factor -= 0.1
        self.cargar_imagen()

    # Función para pasar a la siguiente página
    def pagina_siguiente(self):
        self.current_image_index += 1
        if self.current_image_index >= len(self.image_files):
            self.current_image_index = 0
        self.cargar_imagen()

    # Función para pasar a la página anterior
    def pagina_anterior(self):
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.image_files) - 1
        self.cargar_imagen()

    # Función para desplazarse hacia arriba
    def desplazar_arriba(self):
        self.scroll_factor -= 0.1
        self.image_frame.yview_scroll(int(-1*self.scroll_factor), "units")

    # Función para desplazarse hacia abajo
    def desplazar_abajo(self):
        self.scroll_factor += 0.1
        self.image_frame.yview_scroll(int(self.scroll_factor), "units")

    # Función para redimensionar la imagen
    def redimensionar_imagen(self):
        self.zoom_factor = 1.0
        self.cargar_imagen()

    # Función para cambiar el color de fondo
    def cambiar_color(self):
        color_code = colorchooser.askcolor(title ="Elegir color")
        self.root.config(bg=color_code[1])
        self.label.config(bg=color_code[1])
        self.entry.config(bg=color_code[1])
        self.button_frame.config(bg=color_code[1])
        self.image_frame.config(bg=color_code[1])
        self.image_label.config(bg=color_code[1])

if __name__ == "__main__":
    app = LectorManga()
    app.root.mainloop()
