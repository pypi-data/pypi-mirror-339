import argparse
import asyncio
from cla.chat import AI
import platform
import os

__version__ = "1.0.4"

async def main(command:str, so:str):
    """
    Função principal que inicializa a classe AI e envia a mensagem.
    :param command: Comando a ser enviado para o modelo.
    :param so: Sistema operacional (Linux, Windows, Mac). Automaticamente detectado se não for fornecido.
    """
    ai = AI()
    await ai.send_message(command, so)


def cli():
    parser = argparse.ArgumentParser(description="Command Line Assistant (CLA)")

    missing = []

    if "CLA_KEY" not in os.environ:
        missing.append("A chave da API 'CLA_KEY' não está definida no ambiente. Pode ser uma chave da OpenAI ou DeepSeek.")

    if "CLA_BASE_URL" not in os.environ:
        missing.append("A URL base 'CLA_BASE_URL' não está definida no ambiente. Pode ser a Base URL da OpenAI ou DeepSeek.")

    if "CLA_MODEL" not in os.environ:
        missing.append("O modelo 'CLA_MODEL' não está definido no ambiente. Pode ser o modelo da OpenAI ou DeepSeek. Ex: 'deepseek-chat'.")

    if missing:
        for message in missing:
            print(f"\033[91m{message}\033[0m")
        exit(1)

    parser.add_argument("comando", nargs="+", help="Comando em linguagem natural para o CLA")
    parser.add_argument("--so", help="Sistema operacional (Linux, Windows, Mac)", default=platform.system())
    parser.add_argument("--version", action="version", version=f"CL-Assistant - versão {__version__}")

    args = parser.parse_args()

    comando = " ".join(args.comando)
    
    asyncio.run(main(comando, args.so))
