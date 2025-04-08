import httpx
import json
import os

class AI:
    def __init__(self):
        self.api_key = os.getenv("CLA_KEY")
        base_url = os.getenv("CLA_BASE_URL").rstrip("/")
        self.ai_model = os.getenv("CLA_MODEL")
        self.api_url = base_url + "/v1/chat/completions"

    async def send_message(self, message, so):
        """
        Envia uma mensagem para o modelo e imprime a resposta em tempo real.
        
        :param message: Mensagem a ser enviada para o modelo.
        :param so: Sistema operacional (Linux, Windows, Mac).
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.ai_model,
            "messages": [
                {"role": "system", "content": f"Você é um assistente de linha de comando."},
                {"role": "system", "content": f"Você deve responder apenas com comandos para terminal."},
                {"role": "system", "content": f"Não deve responder com explicações, aspas ou formatações."},
                {"role": "system", "content": f"Sistema: {so} | Diretório atual: {os.getcwd()}"},
                {"role": "user", "content": f"{message}"}
            ],
            "stream": True,
            "max_tokens": 150
        }

        final_response = []
        print('\n', end="")
        print("***************************[CL-Assistant]***************************")
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", self.api_url, headers=headers, json=data) as response:

                if response.status_code != 200:
                    print(f"Erro na API: {response}")
                    return
                async for line in response.aiter_lines():
                    if line.strip().startswith("data: "):
                        content = line.removeprefix("data: ").strip()
                        try:
                            content = json.loads(content)['choices'][0]['delta']['content']
                        except:
                            content = ""

                        final_response.append(content)
                        print(content, end="", flush=True)        
        print('\n', end="")
        print("********************************************************************")
        key = input("Deseja executar o comando? [S/n]")
        if key.lower() == 's':
            os.system("".join(final_response))