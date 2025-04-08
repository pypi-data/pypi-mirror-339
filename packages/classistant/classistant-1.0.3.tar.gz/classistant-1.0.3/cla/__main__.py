import argparse
import asyncio
from cla.chat import AI
import platform
import os

async def main(question:str, so:str):
    """
    Função principal que inicializa a classe AI e envia a mensagem.
    :param question: Mensagem a ser enviada para o modelo.
    :param so: Sistema operacional (Linux, Windows, Mac). Automaticamente detectado se não for fornecido.
    """
    ai = AI()
    await ai.send_message(question, so)


def cli():
    parser = argparse.ArgumentParser(description="Command Line Assistant (CLA)")

    missing = []

    if "CLA_KEY" not in os.environ:
        missing.append("A chave da API 'CLA_KEY' não está definida no ambiente. Pode ser uma chave da OpenAI ou DeepSeek.")

    if "CLA_BASE_URL" not in os.environ:
        missing.append("A URL base 'CLA_BASE_URL' não está definida no ambiente. Pode ser a Base URL da OpenAI ou DeepSeek.")

    if missing:
        for message in missing:
            print(f"\033[91m{message}\033[0m")
        exit(1)

    parser.add_argument("mensagem", nargs="+", help="Mensagem para o CLA")
    parser.add_argument("--so", help="Sistema operacional (Linux, Windows, Mac)", default=platform.system())


    args = parser.parse_args()
    question = " ".join(args.mensagem)

    asyncio.run(main(question, args.so))
