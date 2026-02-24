import json
import requests
import os
import urllib.parse
from datetime import datetime
import pytz

# --- CONFIGURAÇÕES ---
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
ARQUIVO_ESCALA = 'escala.json'

# Agenda: Nome (minúsculo) -> Telefone
AGENDA = {
    "albert": "5538998557578",
    "enzo": "5538984032914",
    "marcia": "5538988243015", "márcia": "5538988243015",
    "lucas": "5538992556263",
    "paulo": "5538998857945", 
    "duda": "5538988047091",
    "wellington": "5538991289962",
    "júlia": "5538992627352", "julia": "5538992627352",
    "ávilo": "5538991126733", "avilo": "5538991126733",
    "josé": "5538998920057", "jose": "5538998920057",
    "julimar": "5538999493437", "júlimar": "5538999493437",
    "evelyn": "5538991183066",
    "alice": "5538988294593",
    "gabi": "5538988228118"
}

def enviar_telegram(mensagem_resumo, botoes_links):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Monta o texto que chega NO SEU TELEGRAM
    texto_final = (
        f"📅 *Resumo da Escala de Hoje:*\n"
        f"{mensagem_resumo}\n\n"
        f"👇 *Links Personalizados para Envio:*\n"
        f"{botoes_links}"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": texto_final,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ Erro ao enviar: {response.text}")
        exit(1)
    else:
        print("✅ Mensagem enviada com sucesso!")

def main():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    data_americana = datetime.now(fuso_brasil).strftime('%Y-%m-%d')
    data_br = datetime.now(fuso_brasil).strftime('%d/%m/%Y')
    
    print(f"📅 Processando dia: {data_americana}")

    try:
        with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro no arquivo JSON: {e}")
        exit(1)
    
    texto_escala = dados.get(data_americana)
    
    if texto_escala:
        # Prepara busca
        texto_escala_lower = texto_escala.lower()
        links_gerados = ""
        telefones_processados = []

        # 1. Procura cada pessoa da agenda na escala de hoje
        for nome_chave, telefone in AGENDA.items():
            if nome_chave in texto_escala_lower:
                if telefone not in telefones_processados:
                    telefones_processados.append(telefone)
                    
                    # Formata o nome (ex: de 'júlia' para 'Júlia')
                    nome_bonito = nome_chave.capitalize()
                    
                    # 2. CRIA A MENSAGEM PERSONALIZADA (Aqui está a mágica!)
                    # Essa é a mensagem que vai aparecer no WhatsApp
                    msg_whatsapp = (
                        f"🌞 *Bom dia {nome_bonito}! Paz e Bem.*\n\n"
                        f"Passando para lembrar da escala de transmissão de hoje ({data_br}):\n\n"
                        f"{texto_escala}\n\n"
                        f"Deus abençoe sua missão! 🙏"
                    )
                    
                    # 3. Gera o link
                    # Removemos asteriscos (*) para o WhatsApp não ficar estranho se não quiser negrito
                    texto_zap_codificado = urllib.parse.quote(msg_whatsapp.replace('*', ''))
                    link = f"https://wa.me/{telefone}?text={texto_zap_codificado}"
                    
                    links_gerados += f"🔗 [Enviar para {nome_bonito}]({link})\n"

        # Caso não ache ninguém (ex: erro de digitação no nome), cria um genérico
        if not links_gerados:
            msg_generica = (
                f"🌞 *Bom dia! Paz e Bem.*\n\n"
                f"Passando para lembrar da escala de transmissão de hoje ({data_br}):\n\n"
                f"{texto_escala}\n\n"
                f"Deus abençoe sua missão! 🙏"
            )
            texto_zap = urllib.parse.quote(msg_generica.replace('*', ''))
            links_gerados = f"⚠️ [Nenhum nome detectado - Link Genérico]({f'https://wa.me/?text={texto_zap}'})"

        # Envia para o Telegram
        enviar_telegram(texto_escala, links_gerados)
        
    else:
        print(f"Nenhuma escala para {data_americana}")

if __name__ == "__main__":
    main()
