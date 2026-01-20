#!/usr/bin/env python3
"""
Estrategia: Abrir Chrome con debugging, hacer cambios vía DevTools Protocol
"""

import subprocess
import time
import requests

print("🚀 Iniciando Chrome con remote debugging...")

# Cerrar Chrome si está abierto
subprocess.run(["pkill", "-9", "chrome"], stderr=subprocess.DEVNULL)
time.sleep(2)

# Abrir Chrome con remote debugging habilitado
chrome_process = subprocess.Popen(
    [
        "google-chrome",
        "--remote-debugging-port=9222",
        "--user-data-dir=/home/medalcode/.config/google-chrome",
    ]
)

print("⏳ Esperando que Chrome inicie...")
time.sleep(5)

try:
    # Conectar a Chrome DevTools
    response = requests.get("http://localhost:9222/json")
    tabs = response.json()

    if not tabs:
        print("❌ No se pudo conectar a Chrome")
        exit(1)

    print("✅ Conectado a Chrome via DevTools Protocol")

    # Aquí usaríamos websocket para comunicarnos con Chrome
    # Pero esto requiere más setup. Por ahora, hagamos algo más simple...

except Exception as e:
    print(f"❌ Error: {e}")
    chrome_process.terminate()

print("\n💡 Chrome está corriendo con debugging...")
print("Mantén esta ventana abierta")
