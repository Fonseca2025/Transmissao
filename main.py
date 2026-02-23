import json
import requests
import os
from datetime import datetime
import pytz # Para garantir o fuso horário do Brasil

# Configurações
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
ARQUIVO_ESCALA = 'escala.json'

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    requests.post(url, json=payload)

def main():
    # Define o fuso horário de Brasília
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    hoje = datetime.now(fuso_brasil).strftime('%Y-%m-%d')
    
    # Carrega a escala
    with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Verifica se tem escala hoje
    agente = dados.get(hoje)
    
    if agente:
        msg = f"🔔 *Escala da Missa - Hoje ({hoje})*\n\n{agente}"
        enviar_telegram(msg)
        print("Mensagem enviada!")
    else:
        print(f"Nenhuma escala encontrada para {hoje}.")

if __name__ == "__main__":
    main()
