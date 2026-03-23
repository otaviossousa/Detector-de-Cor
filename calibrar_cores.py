import json
from sensor_cor import SensorCor

ARQUIVO = "cores_calibradas.json"

sensor = SensorCor(integration_time=100, gain=4)

cores = [
    "vermelho",
    "verde",
    "azul",
    "amarelo",
    "branco",
    "preto",
    "laranja"
]

dados = {}

print("=== CALIBRACAO DE CORES ===")
print("Mantenha sempre a mesma distancia entre o objeto e o sensor.")
print("Evite luz ambiente variando durante a calibracao.\n")

for cor in cores:
    input(f"Coloque a cor [{cor}] na frente do sensor e pressione ENTER... ")

    leitura = sensor.ler_media(amostras=20, intervalo=0.05)
    normalizado = sensor.normalizar_rgb(leitura)

    dados[cor] = {
        "raw": leitura,
        "norm": normalizado
    }

    print(f"Cor [{cor}] salva:")
    print(f"  bruto = {leitura}")
    print(f"  norm  = {normalizado}\n")

with open(ARQUIVO, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)

print(f"Calibracao salva em {ARQUIVO}")
