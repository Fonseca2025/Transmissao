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
    # O parse_mode='Markdown' permite usar negrito com asteriscos
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown" 
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("✅ SUCESSO: Mensagem entregue no Telegram!")
    else:
        print(f"❌ ERRO GRAVE: O Telegram rejeitou a mensagem.")
        print(f"Código do erro: {response.status_code}")
        print(f"Explicação: {response.text}")
        exit(1)

def main():
    # Define o fuso horário para garantir a data certa no Brasil
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    
    # Data para buscar no JSON (formato americano: 2026-02-24)
    data_americana = datetime.now(fuso_brasil).strftime('%Y-%m-%d')
    
    # Data para mostrar na mensagem (formato brasileiro: 24/02/2026)
    data_br = datetime.now(fuso_brasil).strftime('%d/%m/%Y')
    
    print(f"📅 Data de hoje buscada: {data_americana}")

    try:
        with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        exit(1)
    
    # Busca o agente do dia no arquivo
    agente = dados.get(data_americana)
    
    if agente:
        # Cria a mensagem formatada
        msg = (
            f"🌞 *Bom dia! Paz e Bem.*\n\n"
            f"Passando para lembrar da escala de transmissão de hoje ({data_br}):\n\n"
            f"{agente}\n\n"
            f"Deus abençoe sua missão! 🙏"
        )
        enviar_telegram(msg)
    else:
        print(f"Nenhuma escala encontrada para {data_americana}.")

if __name__ == "__main__":
    main()
