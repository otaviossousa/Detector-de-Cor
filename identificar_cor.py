import json
import math
import time
from sensor_cor import SensorCor

ARQUIVO = "cores_calibradas.json"

try:
    sensor = SensorCor(integration_time=100, gain=4)
except Exception as e:
    print("="*50)
    print(f"ERRO FATAL: Não foi possível inicializar o sensor de cor.")
    print(f"Verifique a conexão do hardware (pinos SCL, SDA, VCC, GND).")
    print(f"Detalhes do erro: {e}")
    print("="*50)
    exit()

try:
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        referencias = json.load(f)
except Exception:
    referencias = {}


def classificar_cor(leitura_norm):
    melhor_cor = None
    menor_distancia = None

    if isinstance(referencias, dict):
        for cor, dados in referencias.items():
            if not isinstance(dados, dict):
                continue

            ref = dados.get("norm")
            if not isinstance(ref, dict):
                continue

            try:
                ref_seguro = {
                    "rn": float(ref["rn"]),
                    "gn": float(ref["gn"]),
                    "bn": float(ref["bn"])
                }
                if math.isnan(ref_seguro["rn"]) or math.isnan(ref_seguro["gn"]) or math.isnan(ref_seguro["bn"]):
                    continue
            except (KeyError, ValueError, TypeError):
                continue

            distancia = sensor.distancia(leitura_norm, ref_seguro)

            if menor_distancia is None or distancia < menor_distancia:
                menor_distancia = distancia
                melhor_cor = cor

    # confiança simples
    if menor_distancia is None:
        confianca = 0
    else:
        confianca = max(0, 100 - (menor_distancia * 300))

    return melhor_cor, menor_distancia, confianca


print("=== IDENTIFICADOR DE CORES ===")
print("Pressione Ctrl+C para sair.\n")

while True:
    try:
        leitura = sensor.ler_media(amostras=10, intervalo=0.05)
        leitura_norm = sensor.normalizar_rgb(leitura)

        cor, distancia, confianca = classificar_cor(leitura_norm)

        print("Leitura bruta:", leitura)
        print("Leitura norm.:", leitura_norm)
        if cor:
            print(f"Cor detectada: {cor}")
            print(f"Distancia: {distancia:.4f}")
        else:
            print("Cor detectada: Nenhuma cor calibrada encontrada.")
            print("Distancia: N/A")
        print(f"Confianca: {confianca:.2f}%")
    except Exception as e:
        print(f"!!! ERRO AO LER O SENSOR: {e}")
        print("Verifique a conexão do hardware. Nova tentativa em 5 segundos...")
        time.sleep(5)
    print("-" * 40)
