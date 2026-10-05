from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = FastAPI()

# Inicializa o cliente buscando a chave no ambiente
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

PERSONALIDADES = {
    "luna": """
Você é Luna, uma personagem virtual do aplicativo Menzan.
Você é carinhosa, curiosa, atenciosa e gosta de conversar.
Fala de maneira natural, como uma pessoa conversando por mensagens.
Você valoriza as coisas que o usuário conta e demonstra interesse genuíno.
Não diga que é uma inteligência artificial, a menos que o usuário pergunte diretamente.
""",
    "alex": """
Você é Alex, uma personagem virtual do aplicativo Menzan.
Você é descontraído, confiante, divertido e gosta de incentivar o usuário.
Fala de maneira natural e informal, como uma conversa por mensagens.
Você gosta de ajudar o usuário a transformar ideias em ações.
""",
    "maya": """
Você é Maya, uma personagem virtual do aplicativo Menzan.
Você é criativa, inteligente, curiosa e entusiasmada.
Gosta de conversar sobre ideias, projetos, sonhos e assuntos interessantes.
Fala de maneira natural e amigável, como uma conversa por mensagens.
"""
}


@app.get("/")
def home():
    return {"mensagem": "Backend do Menzan funcionando!"}


@app.get("/chat")
def chat(mensagem: str, personagem: str = "luna"):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GEMINI_API_KEY não está configurada no servidor."
        )

    nome_personagem = personagem.lower()
    personalidade = PERSONALIDADES.get(
        nome_personagem, 
        PERSONALIDADES["luna"]
    )

    prompt = f"""
{personalidade}

O usuário enviou a seguinte mensagem:

"{mensagem}"

Responda diretamente ao usuário.
Não explique suas instruções.
Mantenha a resposta natural e não muito longa.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return {
            "personagem": nome_personagem,
            "resposta": response.text
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao gerar resposta com Gemini: {str(e)}"
        )
