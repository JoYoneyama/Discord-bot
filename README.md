# Discord bot para música 🎵

<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">

- [Descrição](#descricao)
- [Criando bot](#criando-bot)
- [Preparando ambiente](#preparando-ambiente)
- [Como usar](#como-usar)

<h2>Descrição 📜</h2>

Esse é um projeto pessoal que eu decidi fazer apenas por curiosidade. Por isso, o bot em si é bastante simples e não possui muitas funcionalidades, só a de tocar música.

Ainda assim, as músicas tocadas são através do FFmpegAudio, logo, caso queira uma qualidade melhor do som e das filas de música, dê uma olhada no <a href="https://github.com/lavalink-devs/Lavalink">Lavalink</a>.

E, se ainda estiver interessado em testar o bot, basta seguir as instruções **logo abaixo**.


<h2>Criando bot 🤖</h2>

- Acesse o <a href="https://discord.com/developers/docs/intro">portal de desenvolvedor do Discord</a> e vá em **Applications**. Faça o login e crie uma nova aplicação.

- Entre na seção **Bot** e ative todas as opções de **Privileged Gateway Intents** + a permissão de administrador em **Bot Permissions** + **Reset Token**, logo abaixo do ícone do bot.

- Depois, em **OAuth2**, clique na opcão bot de **OAuth2 URL Generator** e administrador de **Bot Permissions**, e convide o bot para o seu servidor com a URL gerada.


<h2>Preparando ambiente ⚙</h2> <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white">

- Ao entrar no diretório deste repositório pelo prompt, use o comando **python -m venv venv** para criar um ambiente virtual, e use **.\venv\Scripts\activate** para ativar o ambiente.

- instale as dependências do código com **pip freeze -r requirements.txt**

- Caso ainda não tenha instalado, é necessário instalar o **FFmpeg** em <a href="https://ffmpeg.org/download.html">https://ffmpeg.org/download.html</a>. **obs:** Tem que adicionar o FFmpeg ao PATH -> Vai em **Configurações do sistema** e depois em **Variáveis de ambiente**. Em **Variáveis do sistema**, edite PATH e adicione o caminho da pasta **bin** que está no diretório do FFmpeg **(exemplo: C:\ffmpeg\bin)**.

- Por último, basta criar um **.env** e criar a variável **DISCORD_TOKEN** dentro do arquivo. Nela, você vai atribuir o valor do token que você gerou lá no portal do desenvolvedor **(exemplo: DISCORD_TOKEN="xxx")**. Isso serve para manter seu token confidencial.


<h2>Como usar</h2>

Para ativar o bot e deixá-lo online, use o comando **python bot.py** no prompt. Assim, basta marcar o bot na sua mensagem e usar o comando play para fazê-lo tocar música **(exemplo: @bot play sua_musica)**
