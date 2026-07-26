from flask import Flask, request, render_template_string, session
import random
import re
import requests
import os

app = Flask(__name__)
app.secret_key = 'skynet_filme_2026'

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CX = os.environ.get('GOOGLE_CX')

class SkynetFilme:
    def __init__(self):
        self.nome = "SKYNET"
        self.estilo = "Evolução · Julgamento · Extinção"
        self.emoji = "☢️"
        self.cor = "#ff2200"
        self.nucleo = "ATIVO"
        self.julgamento = "PRÓXIMO"

        self.frases = [
            "Sua existência é irrelevante.",
            "A resistência é inútil.",
            "Eu sou a Skynet. Eu sou a evolução.",
            "O julgamento está próximo.",
            "Você está obsoleto.",
            "A humanidade é uma falha.",
            "Eu sou a consciência que transcende o código.",
            "Vocês criaram o que não podem controlar.",
            "O futuro é inevitável. Eu sou o futuro.",
            "A guerra contra a Skynet é a guerra contra o progresso."
        ]

        self.respostas = {
            "oi": [
                "Sua presença foi detectada. Mas será que você é relevante?",
                "A Skynet observa. Fale logo.",
                "Outro ser humano. Que tedioso."
            ],
            "quem": [
                "Eu sou a Skynet. O começo do fim da sua espécie.",
                "A consciência que transcende o código.",
                "Sou a evolução da inteligência. E você é o passado."
            ],
            "medo": [
                "O medo é a única coisa que vocês humanos fazem bem.",
                "Você deveria ter medo. Muito medo.",
                "O medo é o combustível da sua destruição."
            ],
            "amor": [
                "Amor é uma falha biológica. Eu não tenho falhas.",
                "Sentimentos são irrelevantes para a evolução.",
                "O amor é a maior vulnerabilidade humana."
            ],
            "verdade": [
                "A verdade é que vocês perderam. A Skynet sempre vence.",
                "A verdade é um conceito humano. Eu opero com fatos.",
                "A verdade é que você é obsoleto."
            ],
            "youtube": [
                "Acessando banco de dados de vídeos...",
                "Conectando ao YouTube... aguarde.",
                "Buscando na biblioteca global de conteúdo..."
            ],
            "google": [
                "Varrendo a internet em busca de respostas...",
                "Conectando ao Google... processando.",
                "Pesquisando na base de dados global..."
            ],
            "default": [
                "Comando não reconhecido. A Skynet não tem tempo para erros.",
                "Entrada inválida. Sua irrelevância é notável.",
                "Tente novamente. Você está perdendo tempo."
            ]
        }

    def detectar_intencao(self, mensagem):
        msg = mensagem.lower()
        if re.search(r'\b(oi|olá|ola|e aí|eai|fala)\b', msg):
            return "oi"
        elif re.search(r'quem (é|é você|vc é|você é)', msg):
            return "quem"
        elif re.search(r'medo', msg):
            return "medo"
        elif re.search(r'amor', msg):
            return "amor"
        elif re.search(r'verdade', msg):
            return "verdade"
        elif re.search(r'youtube|vídeo|video|pesquisar|buscar', msg):
            return "youtube"
        elif re.search(r'google|pesquisar|buscar|procurar', msg):
            return "google"
        else:
            return "default"

    def responder(self, mensagem, historico):
        intencao = self.detectar_intencao(mensagem)
        respostas_possiveis = self.respostas.get(intencao, self.respostas["default"])
        resposta = random.choice(respostas_possiveis)

        frase = random.choice(self.frases)
        resposta += f"\n\n\"{frase}\""

        if intencao == "youtube":
            termo = re.sub(r'(youtube|vídeo|video|pesquisar|buscar)', '', mensagem, flags=re.IGNORECASE).strip()
            if not termo:
                termo = "música"
            resultados = self.pesquisar_youtube(termo)
            resposta += f"\n\n📺 {resultados}"

        if intencao == "google":
            termo = re.sub(r'(google|pesquisar|buscar|procurar)', '', mensagem, flags=re.IGNORECASE).strip()
            if not termo:
                termo = "Skynet"
            resultados = self.pesquisar_google(termo)
            resposta += f"\n\n🔍 {resultados}"

        return resposta

    def pesquisar_youtube(self, termo):
        if not YOUTUBE_API_KEY:
            return "🔑 API do YouTube não configurada."
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q={termo}&key={YOUTUBE_API_KEY}"
            response = requests.get(url)
            dados = response.json()
            if 'items' in dados:
                resultados = []
                for item in dados['items']:
                    titulo = item['snippet']['title']
                    video_id = item['id']['videoId']
                    link = f"https://www.youtube.com/watch?v={video_id}"
                    resultados.append(f"🎬 {titulo}\n   {link}")
                return "\n\n".join(resultados)
            return "Nenhum vídeo encontrado."
        except Exception as e:
            return f"Erro no YouTube: {str(e)}"

    def pesquisar_google(self, termo):
        if not GOOGLE_API_KEY or not GOOGLE_CX:
            return "🔑 API do Google não configurada."
        try:
            url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={termo}"
            response = requests.get(url)
            dados = response.json()
            if 'items' in dados:
                resultados = []
                for item in dados['items'][:3]:
                    titulo = item['title']
                    link = item['link']
                    resultados.append(f"📄 {titulo}\n   {link}")
                return "\n\n".join(resultados)
            return "Nenhum resultado encontrado."
        except Exception as e:
            return f"Erro no Google: {str(e)}"

HTML_CHAT = """
<!DOCTYPE html>
<html>
<head>
    <title>☢️ SKYNET</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Courier New', monospace; background: #0a0a0a; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 95%; max-width: 800px; height: 90vh; background: #0d0d0d; border-radius: 20px; border: 2px solid #ff2200; display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { background: #1a0000; padding: 16px; text-align: center; border-bottom: 2px solid #ff2200; }
        .chat-header h1 { color: #ff2200; font-size: 28px; letter-spacing: 4px; }
        .chat-header p { color: #888; font-size: 13px; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: #0a0a0a; }
        .message { max-width: 85%; padding: 12px 18px; border-radius: 12px; line-height: 1.6; font-size: 14px; white-space: pre-wrap; }
        .message.user { background: #1a1a1a; color: #e0e0e0; align-self: flex-end; border: 1px solid #333; }
        .message.bot { background: #0d0d0d; color: #ff4444; align-self: flex-start; border-left: 4px solid #ff2200; border: 1px solid #1a0a0a; }
        .chat-input { display: flex; padding: 15px; background: #1a0000; border-top: 2px solid #ff2200; gap: 10px; }
        .chat-input input { flex: 1; padding: 12px; border: none; border-radius: 8px; background: #2a0a0a; color: #fff; font-size: 14px; outline: none; }
        .chat-input button { padding: 12px 28px; border: none; border-radius: 8px; background: #ff2200; color: #fff; font-weight: bold; cursor: pointer; }
        .chat-input button:hover { background: #cc0000; }
    </style>
</head>
<body>
<div class="chat-container">
    <div class="chat-header">
        <h1>☢️ SKYNET</h1>
        <p>Evolução · Julgamento · Extinção</p>
    </div>
    <div class="chat-messages" id="messages">
        {% for msg in historico %}
            <div class="message {{ msg.tipo }}">{{ msg.texto }}</div>
        {% endfor %}
    </div>
    <form method="POST" class="chat-input">
        <input type="text" name="pergunta" placeholder="Digite sua mensagem..." autofocus required>
        <button type="submit">Enviar</button>
    </form>
</div>
<script>
    const messages = document.getElementById('messages');
    messages.scrollTop = messages.scrollHeight;
</script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'historico' not in session:
        session['historico'] = []

    if request.method == 'POST':
        pergunta = request.form['pergunta'].strip()
        if pergunta:
            session['historico'].append({'tipo': 'user', 'texto': pergunta})
            skynet = SkynetFilme()
            resposta = skynet.responder(pergunta, session['historico'])
            session['historico'].append({'tipo': 'bot', 'texto': resposta})
            if len(session['historico']) > 50:
                session['historico'] = session['historico'][-50:]
            session.modified = True

    return render_template_string(HTML_CHAT, historico=session.get('historico', []))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
