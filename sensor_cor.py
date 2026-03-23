import time
import math
import board
import busio
import adafruit_tcs34725


class SensorCor:
    def __init__(self, integration_time=100, gain=4):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_tcs34725.TCS34725(self.i2c)

        # Ajustes do sensor
        # integration_time: tempo de integração em ms
        # gain: ganho do sensor
        self.sensor.integration_time = integration_time
        self.sensor.gain = gain

    def ler_bruto(self):
        r, g, b, c = self.sensor.color_raw
        return {
            "r": r,
            "g": g,
            "b": b,
            "c": c
        }

    def ler_media(self, amostras=10, intervalo=0.05):
        soma_r = soma_g = soma_b = soma_c = 0

        for _ in range(amostras):
            leitura = self.ler_bruto()
            soma_r += leitura["r"]
            soma_g += leitura["g"]
            soma_b += leitura["b"]
            soma_c += leitura["c"]
            time.sleep(intervalo)

        return {
            "r": soma_r / amostras,
            "g": soma_g / amostras,
            "b": soma_b / amostras,
            "c": soma_c / amostras
        }

    def normalizar_rgb(self, leitura):
        r = leitura["r"]
        g = leitura["g"]
        b = leitura["b"]

        total = r + g + b
        if total == 0:
            return {
                "rn": 0,
                "gn": 0,
                "bn": 0
            }

        return {
            "rn": r / total,
            "gn": g / total,
            "bn": b / total
        }

    def brilho_relativo(self, leitura):
        c = leitura["c"]
        rgb_total = leitura["r"] + leitura["g"] + leitura["b"]

        if c <= 0:
            return 0

        return rgb_total / c

    def distancia(self, a, b):
        return math.sqrt(
            (a["rn"] - b["rn"]) ** 2 +
            (a["gn"] - b["gn"]) ** 2 +
            (a["bn"] - b["bn"]) ** 2
        )
