## Conversor de Áudio para Texto (OpenAI Whisper)

Ferramenta simples em Python que transcreve arquivos de áudio locais para texto em português usando o modelo Whisper da OpenAI e salva tudo em `transcricoes_api.csv`.

### Requisitos
- Python 3.10+
- ffmpeg instalado no sistema
- Uma chave de API da OpenAI (`OPENAI_API_KEY`)

### Instalação
1. Clone/baixe este repositório.
2. Instale o ffmpeg (Ubuntu/Debian):
   ```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
   ```
3. Crie o ambiente virtual e instale as dependências:
   ```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -U pip
./.venv/bin/pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente:
   - Copie o arquivo de exemplo e preencha sua chave:
     ```bash
cp .env.example .env
     ```
   - Edite `.env` e defina `OPENAI_API_KEY`.

### Uso
1. Coloque seus arquivos de áudio na pasta do projeto.
2. Formatos suportados: `.ogg`, `.mp3`, `.wav`, `.m4a`.
3. Execute a transcrição:
   ```bash
./.venv/bin/python main.py
   ```
4. Saída: o arquivo `transcricoes_api.csv` será criado com as colunas `Horario` e `Transcricao`.

Observação: os arquivos são ordenados por um horário extraído do nome no padrão "nome at HH-MM-SS.ext" quando presente. Se não houver esse padrão, o nome do arquivo é usado como fallback.

### Configuração da chave da OpenAI
- Defina `OPENAI_API_KEY` no arquivo `.env`. O programa aborta com uma mensagem clara se a variável não estiver definida.

### Compactação/Aceleração de áudio para reduzir custos
- A velocidade de processamento do áudio é controlada por `AUDIO_SPEED` no `.env` (padrão `2.0`).
- Valores aceitos: entre `0.5` e `2.0`. `2.0` equivale a acelerar em 2x, reduzindo o tempo de áudio enviado e o custo.
- Requer `ffmpeg` instalado.

### Título sugerido
- Conversor de Áudio para Texto (OpenAI Whisper)

### Licença
Uso pessoal/educacional. Adapte conforme necessário.
