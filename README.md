# Smart City Hub (ESP32, MicroPython)

Station Smart City basée sur un ESP32, programmée en MicroPython et simulée sur Wokwi. Elle mesure l'environnement, gère l'éclairage public automatiquement et affiche des alertes.

## Fonctionnalités
- Lecture de l'heure (RTC DS1307)
- Mesure de la température et de l'humidité (DHT22)
- Mesure de la luminosité (LDR) : éclairage public automatique (LED allumée si lux < 2500, mode NUIT / JOUR)
- Mesure du niveau d'eau (simulé par un potentiomètre)
- Affichage sur écran OLED : heure, température, humidité, mode
- Matrice LED 4x MAX7219 : heure normale, ou alerte défilante
  - "INONDATION" si niveau d'eau > 3000
  - "CANICULE" si température > 45 °C
- Gestion des erreurs de lecture capteur (affichage "--")

## Matériel simulé
| Composant | Broche ESP32 |
|---|---|
| Écran OLED SSD1306 (I2C) | SCL 22, SDA 21 |
| RTC DS1307 (I2C) | SCL 22, SDA 21 |
| Matrice LED MAX7219 (SPI) | SCK 18, MOSI 23, CS 5 |
| Capteur DHT22 | GPIO 4 |
| LDR (luminosité) | GPIO 34 (ADC) |
| Potentiomètre (niveau d'eau) | GPIO 35 (ADC) |
| LED éclairage public | GPIO 2 |

## Protocoles
I2C (OLED, RTC) et SPI (matrice LED)

## Fichiers
- `main.py` : programme principal
- `ssd1306.py`, `max7219.py`, `ds1307.py` : bibliothèques
- `diagram.json` : schéma de câblage Wokwi

## Simulation
Lien Wokwi : https://wokwi.com/projects/462125410040804353

## Auteur
Adem Kechiche, Électronique, Électrotechnique et Automatique (Systèmes Embarqués), ESSTHS
