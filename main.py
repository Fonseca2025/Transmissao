import json
import requests
import os
import urllib.parse
from datetime import datetime, timedelta # Adicionei o timedelta aqui
import pytz

# --- CONFIGURAÇÕES ---
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
ARQUIVO_ESCALA = 'escala.json'

# Agenda telefônica
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

def enviar_telegram(texto_mensagem, botoes_links=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Se tiver botões (links), adiciona no texto. Se não, manda só o texto (para o alerta).
    if botoes_links:
        texto_final = f"📅 *Resumo da Escala de Hoje:*\n{texto_mensagem}\n\n👇 *Links Personalizados:*\n{botoes_links}"
    else:
        texto_final = texto_mensagem # Caso seja apenas o alerta de fim de escala

    payload = {
        "chat_id": CHAT_ID,
        "text": texto_final,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ Erro ao enviar: {response.text}")

def main():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_brasil)
    data_americana = agora.strftime('%Y-%m-%d')
    data_br = agora.strftime('%d/%m/%Y')
    
    print(f"📅 Processando dia: {data_americana}")

    # 1. Carregar Escala
    try:
        with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro no arquivo JSON: {e}")
        exit(1)
    
    # --- PARTE 1: ESCALA DO DIA ---
    texto_escala = dados.get(data_americana)
    
    if texto_escala:
        texto_escala_lower = texto_escala.lower()
        links_gerados = ""
        telefones_processados = []

        for nome_chave, telefone in AGENDA.items():
            if nome_chave in texto_escala_lower:
                if telefone not in telefones_processados:
                    telefones_processados.append(telefone)
                    nome_bonito = nome_chave.capitalize()
                    
                    # Mensagem personalizada para o WhatsApp
                    msg_whatsapp = (
                        f"🌞 *Bom dia {nome_bonito}! Paz e Bem.*\n\n"
                        f"Passando para lembrar da escala de transmissão de hoje ({data_br}):\n\n"
                        f"{texto_escala}\n\n"
                        f"Deus abençoe sua missão! 🙏"
                    )
                    texto_zap_codificado = urllib.parse.quote(msg_whatsapp.replace('*', ''))
                    link = f"https://wa.me/{telefone}?text={texto_zap_codificado}"
                    links_gerados += f"🔗 [Enviar para {nome_bonito}]({link})\n"

        if not links_gerados:
            msg_generica = (
                f"🌞 *Bom dia! Paz e Bem.*\n\n"
                f"Passando para lembrar da escala de transmissão de hoje ({data_br}):\n\n"
                f"{texto_escala}\n\n"
                f"Deus abençoe sua missão! 🙏"
            )
            texto_zap = urllib.parse.quote(msg_generica.replace('*', ''))
            links_gerados = f"⚠️ [Link Genérico]({f'https://wa.me/?text={texto_zap}'})"

        enviar_telegram(texto_escala, links_gerados)
        print("✅ Escala do dia enviada.")
    else:
        print(f"Nenhuma escala para hoje ({data_americana}).")

    # --- PARTE 2: ALERTA DE FIM DE ESCALA (NOVO!) ---
    # Verifica daqui a 5 dias
    daqui_5_dias = (agora + timedelta(days=5)).strftime('%Y-%m-%d')
    daqui_5_dias_br = (agora + timedelta(days=5)).strftime('%d/%m/%Y')
    
    # Se NÃO tiver dados para daqui a 5 dias, manda o alerta
    if not dados.get(daqui_5_dias):
        print(f"⚠️ Alerta: Não há escala para {daqui_5_dias}")
        aviso = (
            f"🚨 *ATENÇÃO: A ESCALA ESTÁ ACABANDO!* 🚨\n\n"
            f"O sistema verificou que não há escala cadastrada para daqui a 5 dias ({daqui_5_dias_br}).\n\n"
            f"Por favor, acesse o GitHub e atualize o arquivo `escala.json` com o próximo mês para o robô não parar."
        )
        enviar_telegram(aviso, None) # Manda sem botões, só o aviso

if __name__ == "__main__":
    main()
