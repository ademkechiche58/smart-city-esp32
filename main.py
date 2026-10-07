import machine
import time
import dht
import max7219
import ds1307
import ssd1306
from machine import Pin, ADC, SoftI2C

# --- 1. CONFIGURATION ---
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Écrans
oled = ssd1306.SSD1306(128, 64, i2c)  # Reverted: correct for Wokwi
spi = machine.SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
matrix = max7219.Matrix8x8(spi, Pin(5, Pin.OUT), 4)
matrix.brightness(2)

# Capteurs & Actionneurs
dht_sensor = dht.DHT22(Pin(4))
ldr = ADC(Pin(34))
pot_eau = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)
pot_eau.atten(ADC.ATTN_11DB)

led_public = Pin(2, Pin.OUT)
rtc = ds1307.DS1307(i2c)

# --- 2. FONCTIONS D'AFFICHAGE ---

def maj_oled(heure, temp, hum, lux, statut):
    oled.fill(0)
    oled.text("SMART CITY HUB", 10, 0)
    oled.hline(0, 12, 128, 1)
    oled.text("Heure: {}".format(heure), 0, 22)
    oled.text("Temp : {}C".format(temp), 0, 34)
    oled.text("Hum  : {}%".format(hum), 0, 46)
    oled.text("Mode : {}".format(statut), 0, 58)
    oled.show()

def alerte_matrice(message):
    longueur = len(message)
    for x in range(32, -((longueur * 8) + 32), -1):
        matrix.fill(0)
        matrix.text(message, x, 0, 1)
        matrix.show()
        time.sleep(0.02)

# --- 3. BOUCLE PRINCIPALE ---
print("Système optimisé lancé...")

# Debug: afficher le tuple RTC une seule fois au démarrage
t_debug = rtc.datetime()
print("RTC tuple:", t_debug)

while True:
    try:
        # Lecture de l'heure
        t = rtc.datetime()

        # FIX: indices corrigés selon le tuple DS1307 standard
        # DS1307 retourne: (annee, mois, jour, jour_semaine, heure, minute, seconde, ?)
        heure_str = "{:02d}:{:02d}".format(t[4], t[5])

        # Lecture Capteurs
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
        except Exception:  # FIX: ne pas attraper BaseException silencieusement
            temp, hum = "--", "--"

        lux = ldr.read()    # Valeur brute ADC 0-4095 (plus haut = plus de lumière)
        eau = pot_eau.read()

        # Debug série (à commenter une fois le projet stable)
        print("RTC={} | lux={} | eau={} | temp={} | hum={}".format(t, lux, eau, temp, hum))

        # FIX: logique d'éclairage corrigée (était inversée)
        if lux < 2500:      # Environnement sombre → allumer l'éclairage public
            led_public.value(1)
            statut = "NUIT"
        else:               # Environnement lumineux → éteindre
            led_public.value(0)
            statut = "JOUR"

        # Mise à jour OLED
        maj_oled(heure_str, temp, hum, lux, statut)

        # Gestion de la Matrice LED
        if eau > 3000:
            alerte_matrice("!!! INONDATION !!!")
        elif temp != "--" and temp > 45:
            alerte_matrice("!!! CANICULE !!!")
        else:
            matrix.fill(0)
            matrix.text(heure_str, 2, 0, 1)
            matrix.show()

    except Exception as e:
        print("Erreur:", e)

    time.sleep(0.5)
