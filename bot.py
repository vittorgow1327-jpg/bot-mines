import random
from datetime import datetime, timedelta
import asyncio
from telegram import Bot

TOKEN = "SEU_TOKEN_AQUI"
CHAT_ID = "@minesturbosinais"

bot = Bot(token=TOKEN)

def gerar_sinal():
    casas = random.sample(range(1, 26), 4)
    validade = datetime.now() + timedelta(minutes=27)

    return f"""
✅SINAL LIBERADO✅

💣5 MINAS
🤑ATÉ 2 TENTATIVAS

⭐CASAS: {' | '.join(map(str, casas))}

⏰VALIDO ATÉ {validade.strftime('%H:%M')}

🎰LINK DO JOGO - https://vitorferreira-enterprises.com/jogada-sinais

⚠️Atenção veja as mensagens fixadas:

🔞Não existe garantias de ganhos - Jogue com responsabilidades
"""

async def rodar_bot():
    while True:
        try:
            mensagem = gerar_sinal()
            await bot.send_message(chat_id=CHAT_ID, text=mensagem)
            print("Sinal enviado")
        except Exception as e:
            print("Erro:", e)

        await asyncio.sleep(1200)  # 20 minutos

asyncio.run(rodar_bot())
