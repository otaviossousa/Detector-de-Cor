import json
from sensor_cor import SensorCor

ARQUIVO = "cores_calibradas.json"

sensor = SensorCor(integration_time=100, gain=4)

with open(ARQUIVO, "r", encoding="utf-8") as f:
    referencias = json.load(f)


def classificar_cor(leitura_norm):
    melhor_cor = None
    menor_distancia = None

    for cor, dados in referencias.items():
        ref = dados["norm"]

        distancia = sensor.distancia(leitura_norm, ref)

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
    leitura = sensor.ler_media(amostras=10, intervalo=0.05)
    leitura_norm = sensor.normalizar_rgb(leitura)

    cor, distancia, confianca = classificar_cor(leitura_norm)

    print("Leitura bruta:", leitura)
    print("Leitura norm.:", leitura_norm)
    print(f"Cor detectada: {cor}")
    print(f"Distancia: {distancia:.4f}")
    print(f"Confianca: {confianca:.2f}%")
    print("-" * 40)
