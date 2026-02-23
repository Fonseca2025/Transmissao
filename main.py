import json
import requests
import os
from datetime import datetime
import pytz

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
    response = requests.post(url, json=payload)
    
    # AQUI ESTÁ A MUDANÇA: Verifica se deu certo
    if response.status_code == 200:
        print("✅ SUCESSO: Mensagem entregue no Telegram!")
    else:
        print(f"❌ ERRO GRAVE: O Telegram rejeitou a mensagem.")
        print(f"Código do erro: {response.status_code}")
        print(f"Explicação do Telegram: {response.text}")
        # Força o GitHub a mostrar erro vermelho
        exit(1)

def main():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    hoje = datetime.now(fuso_brasil).strftime('%Y-%m-%d')
    
    print(f"📅 Data de hoje buscada: {hoje}")

    try:
        with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        exit(1)
    
    agente = dados.get(hoje)
    
    if agente:
        print(f"Escala encontrada: {agente}")
        msg = f"🔔 *Escala da Missa - Hoje ({hoje})*\n\n{agente}"
        enviar_telegram(msg)
    else:
        print(f"Nenhuma escala encontrada para {hoje}.")

if __name__ == "__main__":
    main()
