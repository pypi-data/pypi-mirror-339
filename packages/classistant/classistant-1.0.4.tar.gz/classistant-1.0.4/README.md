# CL-Assistant 🤖🖥️

**CL-Assistant** (Command Line Assistant) é um assistente de linha de comando movido por inteligência artificial, criado para te ajudar a **gerar comandos de terminal** com base em instruções em linguagem natural.

Com ele, você descreve o que deseja fazer, e o CL-Assistant retorna o comando exato para executar no seu terminal. Ideal para devs que valorizam agilidade e produtividade.

---

## ✨ Funcionalidades

- 💡 Sugere comandos de terminal a partir de descrições em linguagem natural
- 🖥️ Detecta automaticamente o sistema operacional e o seu diretório padrão para gerar comandos mais adequados
- 🌐 Possibilidade de simular comandos para **outros sistemas operacionais** com a flag `--so`
- 🔒 Usa uma API LLM (modelo de linguagem) configurável por variáveis de ambiente
- ⚡ Interface simples e direta via CLI
- 🧠 Powered by AI

---

## 📦 Instalação

Você pode instalar o pacote `classistant` via `pip`:

```bash
pip install classistant
```

O projeto se chama **CL-Assistant**, importa como `classistant` e é usado no terminal com o comando `cla`.

---

## 🔐 Configuração (Windows)

Antes de usar, defina duas variáveis de ambiente:

- `CLA_KEY`: Sua chave de autenticação para a API. (OpenAI ou DeepSeek)
- `CLA_BASE_URL`: URL base da API (ex: `https://api.exemplo.com`)
- `CLA_MODEL`: URL base da API (ex: `deepseek-chat`, `gpt-4o-mini`, etc.)

Você pode definir as variáveis de ambiente diretamente no terminal (PowerShell ou CMD):

```powershell
setx CLA_KEY "suachaveaqui"
setx CLA_BASE_URL "https://api.deepseek.com/"
setx CLA_MODEL "deepseek-chat"
```

> ⚠️ Após usar `setx`, **feche e reabra o terminal** para que as variáveis estejam disponíveis.

Se preferir, também pode definir as variáveis manualmente:

1. Abra o menu **Iniciar** e busque por **"Variáveis de Ambiente"**  
2. Clique em **"Variáveis de Ambiente"**  
3. Em **"Variáveis de usuário"**, clique em **"Novo..."**  
4. Crie as variáveis `CLA_KEY`, `CLA_BASE_URL` e `CLA_MODEL` com os valores apropriados  

--- 

## 🔐 Configuração (Linux)

Antes de usar, defina duas variáveis de ambiente:

- `CLA_KEY`: Sua chave de autenticação para a API da OpenAI ou DeepSeek
- `CLA_BASE_URL`: URL base da API (ex: `https://api.exemplo.com`)
- `CLA_MODEL`: Modelo a ser utilizado (ex: `deepseek-chat`, `gpt-4o-mini`, etc.)

Exemplo no terminal:

```bash
export CLA_KEY=suachaveaqui
export CLA_BASE_URL=https://api.deepseek.com
export CLA_MODEL=deepseek-chat
```

Ou adicione isso ao seu `.bashrc`, `.zshrc` ou arquivo `.env`.

## 🚀 Como usar

### Comando básico

Descreva sua necessidade com uma frase:

```bash
cla "criar um ambiente virtual com Python"
```

E o CL-Assistant retorna:

```bash
python -m venv venv
```

---

## 🌍 Usando a flag `--so`

Por padrão, o CL-Assistant detecta automaticamente o sistema operacional (Windows, Linux ou macOS).  
Se quiser que o comando seja gerado **para um sistema diferente**, use a flag `--so`.

```bash
cla "excluir arquivos temporários" --so windows
```

Resultado:

```bash
del *.tmp
```

Sistemas suportados:

- `linux`
- `windows`
- `mac`

---

## 🛠️ Exemplos adicionais

```bash
cla "listar todos os arquivos .log recursivamente"
```

```bash
find . -name "*.log"
```

```bash
cla "verificar o uso de memória" --so mac
```

```bash
vm_stat
```

---

## 🤖 Como funciona

O comando `cla` envia sua solicitação para uma API compatível com modelos de linguagem (LLM),  
que interpreta sua instrução e retorna um comando de terminal correspondente em tempo real por streaming.

Você pode usar qualquer modelo de linguagem (LLM) compatível com a API da OpenAI — incluindo modelos locais, da própria OpenAI, ou de provedores equivalentes que sigam o mesmo formato de requisição.

---

## 🧪 Requisitos

- Python 3.9+
- Dependência principal: `httpx`

---

## 📄 Licença

MIT © [Paulo Lira](https://github.com/PauloLiraDev)