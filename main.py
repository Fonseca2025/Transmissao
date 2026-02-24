import json
import requests
import os
import urllib.parse  # Biblioteca para criar o link do WhatsApp
from datetime import datetime
import pytz

# Configurações
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
ARQUIVO_ESCALA = 'escala.json'

def enviar_telegram(mensagem, link_whatsapp):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Montamos o texto com um botão embutido (Markdown)
    texto_final = (
        f"{mensagem}\n\n"
        f"👇 *Clique abaixo para enviar no WhatsApp:*\n"
        f"[📲 ENVIAR AGORA NO ZAP]({link_whatsapp})"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": texto_final,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True # Para não ficar mostrando prévia do link
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("✅ SUCESSO: Mensagem entregue no Telegram!")
    else:
        print(f"❌ ERRO GRAVE: {response.text}")
        exit(1)

def main():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    data_americana = datetime.now(fuso_brasil).strftime('%Y-%m-%d')
    data_br = datetime.now(fuso_brasil).strftime('%d/%m/%Y')
    
    print(f"📅 Data de hoje buscada: {data_americana}")

    try:
        with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        exit(1)
    
    agente = dados.get(data_americana)
    
    if agente:
        # 1. Cria a mensagem de texto bonita
        texto_base = (
            f"🌞 *Bom dia! Paz e Bem.*\n\n"
            f"Passando para lembrar da escala de transmissão de hoje ({data_br}):\n\n"
            f"{agente}\n\n"
            f"Deus abençoe sua missão! 🙏"
        )
        
        # 2. Cria o link mágico do WhatsApp
        # O urllib.parse.quote transforma espaços em %20, etc.
        texto_codificado = urllib.parse.quote(texto_base.replace('*', '')) # Remove asteriscos pro Zap não bugar
        link_zap = f"https://wa.me/?text={texto_codificado}"

        # 3. Envia para o seu Telegram
        enviar_telegram(texto_base, link_zap)
    else:
        print(f"Nenhuma escala encontrada para {data_americana}.")

if __name__ == "__main__":
    main()
