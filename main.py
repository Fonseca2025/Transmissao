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

# Agenda telefônica (Mapeia NOME -> WHATSAPP)
# Dica: As chaves estão em minúsculo para facilitar a busca
AGENDA = {
    "albert": "5538998557578",
    "enzo": "5538984032914",
    "marcia": "5538988243015", "márcia": "5538988243015",
    "lucas": "5538992556263",
    "paulo": "5538998857945", # Vai achar "Paulo Lopes"
    "duda": "5538988047091",
    "wellington": "5538991289962",
    "júlia": "5538992627352", "julia": "5538992627352",
    "ávilo": "5538991126733", "avilo": "5538991126733",
    "josé": "5538998920057", "jose": "5538998920057", # Vai achar "José Bhento"
    "julimar": "5538999493437", "júlimar": "5538999493437",
    "evelyn": "5538991183066",
    "alice": "5538988294593",
    "gabi": "5538988228118"
}

def enviar_telegram(mensagem_principal, botoes_links):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Monta o texto final com os links de ação
    texto_final = f"{mensagem_principal}\n\n👇 *Links Rápidos para Envio:*\n{botoes_links}"

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

    # 1. Carregar Escala
    try:
        with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro no arquivo JSON: {e}")
        exit(1)
    
    texto_escala = dados.get(data_americana)
    
    if texto_escala:
        # 2. Preparar a mensagem base (bonitinha)
        msg_base = (
            f"🌞 *Bom dia! Paz e Bem.*\n\n"
            f"Passando para lembrar da escala de transmissão de hoje ({data_br}):\n\n"
            f"{texto_escala}\n\n"
            f"Deus abençoe sua missão! 🙏"
        )

        # 3. Detectar quem está na escala e criar links
        texto_escala_lower = texto_escala.lower() # Converte tudo pra minusculo pra buscar
        links_gerados = ""
        nomes_encontrados = []

        # Varre a agenda para ver se o nome da pessoa está no texto da escala
        for nome_chave, telefone in AGENDA.items():
            if nome_chave in texto_escala_lower:
                # Evita duplicar nomes (ex: Márcia e marcia)
                if telefone not in nomes_encontrados:
                    nomes_encontrados.append(telefone)
                    
                    # Cria o link do WhatsApp
                    texto_zap = urllib.parse.quote(msg_base.replace('*', ''))
                    link = f"https://wa.me/{telefone}?text={texto_zap}"
                    
                    # Adiciona na lista de botões (ex: 📲 Enviar para Júlia)
                    nome_formatado = nome_chave.capitalize()
                    links_gerados += f"🔗 [Enviar para {nome_formatado}]({link})\n"

        # Se não achou ninguém da lista (ex: nome escrito errado), cria um link genérico
        if not links_gerados:
            texto_zap = urllib.parse.quote(msg_base.replace('*', ''))
            links_gerados = f"🔗 [Enviar para Contato (Selecionar)]({f'https://wa.me/?text={texto_zap}'})"

        # 4. Enviar tudo
        enviar_telegram(msg_base, links_gerados)
        
    else:
        print(f"Nenhuma escala para {data_americana}")

if __name__ == "__main__":
    main()
