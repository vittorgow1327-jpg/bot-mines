import random
import asyncio
import threading
from io import BytesIO
from http.server import BaseHTTPRequestHandler, HTTPServer

from PIL import Image, ImageDraw, ImageFont
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8580099046:AAFIZMXgn82MR2fPIGrULWKXbeq3Wmy_CIE"
CHAT_ID = "@minesturbosinais"
LINK_JOGO = "https://jogadagames.com/?ref=6"

bot = Bot(token=TOKEN)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot rodando")

def rodar_servidor():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

# Posições aproximadas das 25 casas na imagem base
POSICOES = [
    (48, 50), (132, 50), (217, 50), (302, 50), (386, 50),
    (48, 136), (132, 136), (217, 136), (302, 136), (386, 136),
    (48, 222), (132, 222), (217, 222), (302, 222), (386, 222),
    (48, 308), (132, 308), (217, 308), (302, 308), (386, 308),
    (48, 394), (132, 394), (217, 394), (302, 394), (386, 394),
]

def criar_imagem_mines(casas):
    base = Image.open("base.png").convert("RGBA")
    draw = ImageDraw.Draw(base)

    try:
        fonte = ImageFont.truetype("DejaVuSans-Bold.ttf", 58)
    except:
        fonte = ImageFont.load_default()

    for casa in casas:
        x, y = POSICOES[casa - 1]

        # quadrado amarelo por cima da casa
        draw.rounded_rectangle(
            [x, y, x + 76, y + 76],
            radius=10,
            fill=(255, 174, 20, 255)
        )

        # estrela branca
        draw.text((x + 18, y + 8), "★", font=fonte, fill=(255, 255, 255, 255))

    buffer = BytesIO()
    base.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def gerar_sinal():
    casas = random.sample(range(1, 26), 4)  # sempre aleatório

    texto = """✅ SINAL LIBERADO ✅
💣 5 MINAS
🤑 ATÉ 2 TENTATIVAS
⏰ VÁLIDO POR 15 MINUTOS
⚠️ Atenção veja as mensagens fixadas:

🔞 Não existe garantias de ganhos - Jogue com responsabilidade"""

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

        await asyncio.sleep(1800)  # 30 em 30 minutos

threading.Thread(target=rodar_servidor).start()
asyncio.run(rodar_bot())
