import json
import requests
import os
import urllib.parse
import random 
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÕES ---
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
ARQUIVO_ESCALA = 'escala.json'
TESTAR_RESUMO_SEMANAL = False 

# Lista de 20 Saudações e Versículos
SAUDACOES_BIBLICAS =[
    "Paz e Bem! 'Este é o dia que o Senhor fez para nós, alegremo-nos e nele exultemos.' (Sl 118,24) ✨",
    "Que o Senhor abençoe profundamente o seu dia! 'Tudo posso naquele que me fortalece.' (Fl 4,13) 💪",
    "Paz e Bem! 'O Senhor te abençoe e te guarde.' (Nm 6,24) 🕊️",
    "Um dia abençoado para você! 'Entregue o seu caminho ao Senhor; confie nele, e ele agirá.' (Sl 37,5) 🌿",
    "Que a alegria do Senhor seja a sua força na missão! (Ne 8,10) 😊",
    "Paz de Cristo! 'Deem graças ao Senhor, porque ele é bom; o seu amor dura para sempre.' (Sl 107,1) ❤️",
    "Bom trabalho! 'Tudo o que fizerem, façam de todo o coração, como para o Senhor.' (Cl 3,23) 🙌",
    "A paz do Senhor! 'Alegrem-se na esperança, sejam pacientes na tribulação, perseverem na oração.' (Rm 12,12) ✨",
    "Paz e Bem! 'O Senhor é o meu pastor; de nada terei falta.' (Sl 23,1). 🛡️",
    "Abençoada missão! 'Vão pelo mundo todo e preguem o evangelho' (Mc 16,15). 🌍",
    "Paz e Bem! Que São Judas Tadeu interceda pela sua vida e pela sua missão! 🟢🔴",
    "Que a coragem e a fé do glorioso São Judas Tadeu inspirem nossa transmissão. 🙏",
    "A graça e a paz de Deus estejam com você! Que São Judas ilumine seu caminho e seu serviço. ✨",
    "Assim como São Judas levou a Palavra de Deus, que nossa transmissão alcance muitos corações. 📡❤️",
    "Paz e Bem! 'O Senhor é a minha luz e a minha salvação' (Sl 27,1). Que São Judas rogue por nós e por nossa equipe! 🕯️",
    "Que a poderosa intercessão de São Judas Tadeu, o santo das causas impossíveis, te acompanhe em cada detalhe. 🟢🔴",
    "Paz de Cristo! Que o Apóstolo São Judas Tadeu nos ajude a transmitir o amor de Deus com alegria e técnica. 😊📸",
    "Confie suas aflições ao Senhor e peça a intercessão do nosso amado padroeiro, São Judas. 🌿",
    "Excelente missão! Que São Judas Tadeu abençoe suas mãos, sua visão e seu serviço na transmissão. 🙌",
    "Que a paz de Jesus preencha seu coração! São Judas Tadeu, rogai por nós e pela nossa paróquia! 🎙️⛪"
]

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

def enviar_telegram(texto_pronto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto_pronto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, json=payload)

def main():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_brasil)
    
    # Verifica se é o Lembrete de Véspera (Ex: Sábado à noite)
    modo_vespera = os.environ.get('MODO_VESPERA') == 'true'
    
    if modo_vespera:
        dia_alvo = agora + timedelta(days=1)
        palavra_tempo = "amanhã"
        saudacao_inicial = "🌙 *Boa noite"
    else:
        dia_alvo = agora
        palavra_tempo = "hoje"
        saudacao_inicial = "🌞 *Bom dia"
        
    data_americana = dia_alvo.strftime('%Y-%m-%d')
    data_br = dia_alvo.strftime('%d/%m/%Y')

    try:
        with open(ARQUIVO_ESCALA, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        exit(1)
    
    frase_sorteada_individual = random.choice(SAUDACOES_BIBLICAS)
    
    # --- PARTE 1: ESCALA DO DIA ---
    texto_escala = dados.get(data_americana)
    
    if texto_escala:
        texto_escala_lower = texto_escala.lower()
        links_gerados = ""
        telefones_processados =[]

        for nome_chave, telefone in AGENDA.items():
            if nome_chave in texto_escala_lower:
                if telefone not in telefones_processados:
                    telefones_processados.append(telefone)
                    nome_bonito = nome_chave.capitalize()
                    
                    # 🔔 A MÁGICA ESTÁ AQUI: Mensagem do WhatsApp com Gatilho de Confirmação!
                    msg_whatsapp = (
                        f"{saudacao_inicial}, {nome_bonito}!*\n"
                        f"_{frase_sorteada_individual}_\n\n"
                        f"Passando para lembrar da escala de transmissão de {palavra_tempo} ({data_br}):\n\n"
                        f"{texto_escala}\n\n"
                        f"Deus abençoe sua missão! 🙏\n\n"
                        f"✅ Por favor, responda com um 'OK' para confirmar sua presença!"
                    )
                    texto_zap_codificado = urllib.parse.quote(msg_whatsapp.replace('*', '').replace('_', ''))
                    link = f"https://wa.me/{telefone}?text={texto_zap_codificado}"
                    links_gerados += f"🔗[Enviar para {nome_bonito}]({link})\n"

        if not links_gerados:
            msg_generica = (
                f"{saudacao_inicial}!*\n"
                f"_{frase_sorteada_individual}_\n\n"
                f"Passando para lembrar da escala de transmissão de {palavra_tempo} ({data_br}):\n\n"
                f"{texto_escala}\n\n"
                f"Deus abençoe sua missão! 🙏\n\n"
                f"✅ Por favor, responda com um 'OK' para confirmar sua presença!"
            )
            texto_zap = urllib.parse.quote(msg_generica.replace('*', '').replace('_', ''))
            links_gerados = f"⚠️[Link Genérico]({f'https://wa.me/?text={texto_zap}'})"

        msg_telegram = f"📅 *Resumo da Escala de {palavra_tempo.capitalize()}:*\n{texto_escala}\n\n👇 *Links Personalizados:*\n{links_gerados}"
        enviar_telegram(msg_telegram)

    # --- PARTE 2 e 3: SÓ RODA SE NÃO FOR VÉSPERA (De manhã) ---
    if not modo_vespera:
        # Resumo da Semana
        if agora.weekday() == 0 or TESTAR_RESUMO_SEMANAL:
            resumo_semana = ""
            frase_sorteada_grupo = random.choice(SAUDACOES_BIBLICAS)
            while frase_sorteada_grupo == frase_sorteada_individual:
                frase_sorteada_grupo = random.choice(SAUDACOES_BIBLICAS)
            
            segunda_feira_atual = agora - timedelta(days=agora.weekday())
            for i in range(7):
                dia_calculado = segunda_feira_atual + timedelta(days=i)
                data_str = dia_calculado.strftime('%Y-%m-%d')
                data_br_curta = dia_calculado.strftime('%d/%m')
                escala_do_dia = dados.get(data_str, "Sem escala definida")
                resumo_semana += f"*{data_br_curta}* - {escala_do_dia}\n\n"
                
            texto_grupo = (
                f"Olá equipe! 👋\n_{frase_sorteada_grupo}_\n\n"
                f"Confiram a nossa escala de transmissão para esta semana:\n\n{resumo_semana}"
                f"Uma abençoada semana de missão a todos nós! ✨"
            )
            texto_zap_grupo = urllib.parse.quote(texto_grupo.replace('_', ''))
            link_grupo = f"https://wa.me/?text={texto_zap_grupo}"
            msg_telegram_semana = f"📢 *ESCALA DA SEMANA*\n\nAqui está a escala da semana toda pronta para o grupo!\n\n👇 *Clique abaixo para mandar no grupo:*\n👥[📲 ENVIAR PARA O GRUPO]({link_grupo})"
            enviar_telegram(msg_telegram_semana)

        # Alerta Fim de Escala
        daqui_5_dias = (agora + timedelta(days=5)).strftime('%Y-%m-%d')
        if not dados.get(daqui_5_dias):
            daqui_5_dias_br = (agora + timedelta(days=5)).strftime('%d/%m/%Y')
            aviso = f"🚨 *ATENÇÃO: A ESCALA ESTÁ ACABANDO!* 🚨\n\nNão há escala cadastrada para daqui a 5 dias ({daqui_5_dias_br}). Atualize o arquivo `escala.json` no GitHub."
            enviar_telegram(aviso)

if __name__ == "__main__":
    main()
