import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import requests
from io import BytesIO

def remove_white_background(image_path, output_path, tolerance):
    image = Image.open(image_path).convert("RGBA")
    data = np.array(image)
    
    # Creare una maschera per identificare i pixel bianchi con la tolleranza
    white_areas = (data[..., 0:3] > (255 - tolerance)).all(axis=-1)
    
    # Impostare i pixel bianchi come trasparenti
    data[white_areas] = [255, 255, 255, 0]
    
    # Creare una nuova immagine dall'array modificato
    new_image = Image.fromarray(data)
    
    # Salvare l'immagine con sfondo trasparente
    new_image.save(output_path, "PNG")

def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("File immagine", "*.jpg;*.jpeg;*.png")])
    if file_path:
        global img
        img = Image.open(file_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        panel.config(image=img)
        panel.image = img
        global input_path
        input_path = file_path

def save_image():
    if input_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("File PNG", "*.png")])
        if output_path:
            tolerance = tolerance_slider.get()
            remove_white_background(input_path, output_path, tolerance)
            messagebox.showinfo("Successo", "Immagine salvata con successo!")
    else:
        messagebox.showwarning("Nessuna immagine", "Per favore carica prima un'immagine.")

def process_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder = filedialog.askdirectory(title="Seleziona la cartella di destinazione")
        if not output_folder:
            messagebox.showwarning("Nessuna cartella di destinazione", "Per favore seleziona una cartella di destinazione.")
            return
        
        tolerance = tolerance_slider.get()
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.png')
                    remove_white_background(input_file_path, output_file_path, tolerance)
        
        messagebox.showinfo("Successo", "Tutte le immagini sono state elaborate con successo!")

# Creazione della finestra principale
root = tk.Tk()
root.title("Rimozione Sfondo")
root.geometry("500x600")

# Carica il logo e visualizzalo
logo_url = "https://agedis.it/wp-content/uploads/2024/04/cropped-AGEDIS_LOGO_SCRITTA.png"
response = requests.get(logo_url)
logo_image = Image.open(BytesIO(response.content))
logo_image.thumbnail((200, 200))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=logo_photo)
logo_label.image = logo_photo
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Aggiunta dei pulsanti per caricare e salvare l'immagine
load_button = tk.Button(root, text="Carica Immagine", command=load_image, width=20)
load_button.grid(row=1, column=0, padx=20, pady=10)

save_button = tk.Button(root, text="Salva Immagine", command=save_image, width=20)
save_button.grid(row=1, column=1, padx=20, pady=10)

# Aggiunta di un pulsante per elaborare una cartella
process_button = tk.Button(root, text="Elabora Cartella", command=process_folder, width=20)
process_button.grid(row=2, column=0, columnspan=2, pady=10)

# Aggiunta di uno slider per regolare l'intensità
tolerance_label = tk.Label(root, text="Intensità Rimozione Sfondo")
tolerance_label.grid(row=3, column=0, columnspan=2)

tolerance_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, resolution=5)
tolerance_slider.set(10)
tolerance_slider.grid(row=4, column=0, columnspan=2, pady=10)

# Aggiunta di un pannello per visualizzare l'immagine caricata
panel = tk.Label(root)
panel.grid(row=5, column=0, columnspan=2, pady=10)

# Variabile per memorizzare il percorso dell'immagine caricata
input_path = None

# Avvio dell'interfaccia grafica
root.mainloop()
