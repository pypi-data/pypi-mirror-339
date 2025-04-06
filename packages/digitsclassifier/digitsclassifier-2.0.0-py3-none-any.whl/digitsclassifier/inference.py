import numpy as np
from pathlib import Path
from PIL import Image, ImageOps
import keras

def get_model_path():
    return Path(__file__).parent / 'models' / 'digit_classifier_model.keras'

# Modell laden
model = keras.models.load_model(get_model_path())

def preprocess_image(image_array) -> np.ndarray:
    """
    Lädt ein Graustufenbild mit einem einzelnen Buchstaben und wandelt es so um,
    dass es als Eingabe für ein OCR-Modell geeignet ist:
    - binarisiert,
    - zugeschnitten,
    - proportional auf 24x24 skaliert,
    - mit weißem Rand auf 28x28 erweitert,
    - invertiert (schwarz auf weiß),
    - normalisiert (0–1).
    
    Args:
        image_path (str): Pfad zum Eingabebild
    
    Returns:
        np.ndarray: Vorverarbeitetes Bild als 28x28-Array (float32), Werte zwischen 0 und 1
    """
    # 1. Bild laden und in Graustufen umwandeln
    img = Image.fromarray(image_array).convert("L")

    # 2. In Schwarzweiß (binary) umwandeln – Schwelle bei 128
    bw = img.point(lambda x: 0 if x > 200 else 255, mode='1')

    # 3. Bounding Box (Crop)
    bbox = bw.getbbox()
    if bbox is None:
        raise ValueError("Kein Inhalt im Bild erkannt")
    cropped = bw.crop(bbox)

    # 4. Auf 24x24 skalieren (proportional, auch hochskalierend)
    resized = ImageOps.contain(cropped, (24, 24), method=Image.LANCZOS)
    
    # 5. Neues weißes 28x28-Bild erzeugen und das 24x24-Bild zentriert einfügen
    new_img = Image.new("L", (28, 28), 0)
    left = (28 - resized.width) // 2
    top = (28 - resized.height) // 2
    new_img.paste(resized, (left, top))

    # 7. In NumPy-Array umwandeln und auf Werte zwischen 0 und 1 normalisieren
    arr = np.array(new_img).astype(np.float32) / 255.0
    return arr

# Vorhersagefunktion
def predict_digits(images, probenProStelle=3):
    imgs = np.array([preprocess_image(p) for p in images])
    prediction = model.predict(imgs, verbose=0)
    #predicted_label = np.argmax(prediction, axis=1)  # Klasse mit höchster Wahrscheinlichkeit
    
    sortierteZeichenIndixces = (-prediction).argsort()

    # Nimm nur die n wahrscheinlichsten Zeichen...
    indices_der_ersten_n_zeichen_kandidaten = sortierteZeichenIndixces[...,:probenProStelle]

    wahrscheinlichkeiten = -np.sort(-prediction, axis=1)[...,:probenProStelle]
   
    return indices_der_ersten_n_zeichen_kandidaten, wahrscheinlichkeiten