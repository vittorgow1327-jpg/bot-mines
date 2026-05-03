import random
from datetime import datetime, timedelta
import asyncio
from telegram import Bot
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = "SEU_TOKEN_AQUI"
CHAT_ID = "@minesturbosinais"

bot = Bot(token=TOKEN)

# 🔹 servidor fake (pra Render não derrubar)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot rodando")

def rodar_servidor():
    server = HTTPServer(('0.0.0.0', 10000), Handler)
    server.serve_forever()

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
            await bot.send_message(chat_id=CHAT_ID, text=gerar_sinal())
            print("Sinal enviado")
        except Exception as e:
            print("Erro:", e)

        await asyncio.sleep(1200)

# roda servidor em paralelo
threading.Thread(target=rodar_servidor).start()

# roda bot
asyncio.run(rodar_bot())
