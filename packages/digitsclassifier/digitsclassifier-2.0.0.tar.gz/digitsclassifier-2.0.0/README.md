# digitsclassifier
Das Projekt dient zur Erkennung von gedrukten Ziffern (0-9).

## Inferenz
Die Library erwaretet ein Bild mit einem einzigen Zeichen. Das Bild muss Schwarz auf Weis sein, es wird ein Graustufenbild erwartet. Die Library übernimmt die Binarisierung und auch das restliche aufbereiten / skalieren des Bildes. 

Für optimale Ergebnisse sollte ein quadratisches Bild übergeben werden, und es sollte idealerweise mindestens 28x28 Pixel haben. 

## Neuronales Netz
Das Neuronale Netz ist nicht Bestandteil dieses Projekts, sondern muss getrennt trainiert werden und dann als [src/models/digit_classifier_model.keras](/src/models/digit_classifier_model.keras) abgelegt sein. 

Das darunterliegende Keras-Netzwerk erwartet die Bilder im Format 28x28 Pixel, wobel das Zeichen selbst nur die inneren 24x24 Pixel belegen darf, der Rest ist Rand. 

Das Netz erwartet die Bilder Weiß auf Schwarz.

## Entwicklungsumgebung einrichten
Zum Erzeugen des Paketes wird [pdm](https://pdm-project.org/en/latest/) verwendet, das muss also installiert sein. 

## Library paketieren

``` bash
pdm build
```