import random
import asyncio
import threading
from io import BytesIO
from http.server import BaseHTTPRequestHandler, HTTPServer

from PIL import Image, ImageDraw
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8580099046:AAFIZMXgn82MR2fPIGrULWKXbeq3Wmy_CIE"
CHAT_ID = "@minesturbosinais"
LINK_JOGO = "https://vitorferreira-enterprises.com/jogada-sinais"

bot = Bot(token=TOKEN)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot rodando")

def rodar_servidor():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

def criar_imagem_mines(casas):
    tamanho = 800
    img = Image.new("RGB", (tamanho, tamanho), (0, 120, 220))
    draw = ImageDraw.Draw(img)

    grid_inicio = 80
    bloco = 120
    espaco = 18

    for i in range(25):
        linha = i // 5
        coluna = i % 5

        x = grid_inicio + coluna * (bloco + espaco)
        y = grid_inicio + linha * (bloco + espaco)

        numero_casa = i + 1

        if numero_casa in casas:
            cor = (255, 175, 20)
            draw.rounded_rectangle([x, y, x + bloco, y + bloco], radius=18, fill=cor)
            draw.text((x + 38, y + 32), "★", fill="white")
        else:
            cor = (10, 45, 90)
            draw.rounded_rectangle([x, y, x + bloco, y + bloco], radius=18, fill=cor)
            draw.ellipse([x + 45, y + 45, x + 75, y + 75], fill=(40, 90, 160))

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def gerar_sinal():
    casas = random.sample(range(1, 26), 4)

    texto = """
✅ SINAL LIBERADO ✅

💣 5 MINAS
🤑 ATÉ 2 TENTATIVAS

⏰ VÁLIDO POR 15 MINUTOS

🎰 LINK DO JOGO:
https://vitorferreira-enterprises.com/jogada-sinais

⚠️ Atenção veja as mensagens fixadas:

🔞 Não existe garantias de ganhos - Jogue com responsabilidade
"""

    imagem = criar_imagem_mines(casas)

    botoes = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 ENTRAR NO JOGO", url=LINK_JOGO)]
    ])

    return texto, imagem, botoes

async def rodar_bot():
    while True:
        try:
            texto, imagem, botoes = gerar_sinal()

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=imagem,
                caption=texto,
                reply_markup=botoes
            )

            print("Sinal enviado")
        except Exception as e:
            print("Erro:", e)

        await asyncio.sleep(1800)  # 30 minutos

threading.Thread(target=rodar_servidor).start()
asyncio.run(rodar_bot())
