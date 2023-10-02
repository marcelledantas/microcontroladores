# Neste playground, vamos trabalhar com um bot no Telegram.
# A configuração inicial é um pouco trabalhosa, mas você só precisa fazer 1 vez.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Inicialização do simulador. Escreva todo o seu código dentro da main!
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas, como sempre.
    from requests import get, post
    
    from gpiozero import LED, Button, DistanceSensor, Buzzer
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    from datetime import datetime, timedelta
    from os import system
    from subprocess import Popen
    from urllib.request import urlretrieve
    from mplayer import Player
    
    campainha = Buzzer(16)
    botao1 = Button(11)
    botao2 = Button(12)
    botao3 = Button(13)
    
    led1 = LED(21)
    
    sensor_de_distancia = DistanceSensor(trigger=17, echo=18)
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    player = Player()
   
    # Primeiro, siga o passo-a-passo do vídeo para criar um bot:
    # 1 - Baixe o aplicativo Telegram e crie uma conta lá.
    # 2 - Busque pelo BotFather e inicie uma conversa com ele.
    # 3 - Envie a mensagem /newbot e escolha o nome e o usuário do seu bot.
    # 4 - Copie a chave secreta para a variável abaixo (algo como "12345:ABCDEFGLK...")
    chave = "6363363454:AAFbYsrkFl3BjF3FRCqcLskkGlwecj1Ilzs"
    
    
    # Aí a gente coloca a chave no endereço onde faremos as solicitações
    endereco_base = "https://api.telegram.org/bot" + chave
    
    
    # Podemos testar primeiro se a chave está ok fazendo um pedido para o /getMe
    # Rode o código e veja se a mensagem no Shell mostra os dados do seu bot
    endereco_dados_do_bot = endereco_base + "/getMe"

    #print("Buscando dados sobre o bot...")
    #resultado = get(endereco_dados_do_bot)
    #print(resultado.text)
    
    
    # Agora vamos conversar com o bot
    # 5 - Abra o Telegrma, busque o usuário do seu bot e inicie uma conversa com ele.
    # 6 - Envie uma ou mais mensagens quaisquer.
    # 7 - Abra o seu navegador e acesse http://api.telegram.org/botSUA_CHAVE_SECRETA/getUpdates
    #http://api.telegram.org/bot6363363454:AAFbYsrkFl3BjF3FRCqcLskkGlwecj1Ilzs/getUpdates
    # 8 - Copie o id do chat (procure por "chat": {"id":123456...}).
    id_da_conversa = "1585448160"
    
    
    # Pronto! Agora você pode enviar mensagens via programação!
   
    
   
    def envia_msg_telegram():
        dados = {"chat_id": id_da_conversa, "text": "Olá bot, bom dia!"}
        endereco_para_mensagem = endereco_base + "/sendMessage"
        print("\nEnviando mensagem...")
        resultado = post(endereco_para_mensagem, json=dados)
        print(resultado.text)
    
    
    def envia_foto():        
        endereco_para_foto = endereco_base + "/sendPhoto"
        dados = {"chat_id": id_da_conversa}
        arquivo = {"photo": open("foto_campainha.jpg", "rb")} # foto de exemplo do Playground 04
        print("\nEnviando foto...")
        resultado = post(endereco_para_foto, data=dados, files=arquivo)
        print(resultado.text)
        print("Foto enviada")
      
    def liga_campainha():
        campainha.on()
    
    def desliga_campainha():
        campainha.off()
        endereco_para_mensagem =  endereco_base + "/sendMessage"
        dados = {"chat_id": id_da_conversa, "text": "Alguém tocou a campainha"}
        print("Enviando mensagem para o chat")
        resultado = post(endereco_para_mensagem, json=dados)
        print("Mensagem enviada")
        tira_foto()
        envia_foto()
        
        
    def tira_foto():
        print("Tirando foto")
        system("CommandCam /filename foto_campainha.jpg /delay 500")
        
    def apaga_led1():
        print("Porta fechando")
        led1.off()
   
    global aplicativo
    aplicativo = None
    
    def grava_audio():
        print("Começando a gravar")
        global aplicativo
        comando = ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=Microfone (Realtek(R) Audio)", "-t", "00:30", "audiot.wav"]
        aplicativo = Popen(comando) # executa em plano de fundo
        
    def encerra_gravacao_audio():
        print("Preparando para parar gravação")
        global aplicativo
        if aplicativo != None:
            aplicativo.terminate()
            aplicativo = None
        envia_audio_telegram()
        system("ffmpeg -y -i audiot.wav -acodec libopus audiot.ogg")
                         
    def envia_audio_telegram():
        #convertendo .wav para .ogg para enviar para o Telegram
        print("Envia audio telegram")
        sleep(5)
        endereco_audio = endereco_base + "/sendVoice"
        dados = {"chat_id": id_da_conversa}
        arquivo = {"voice": open("audiot.ogg", "rb")}
        resposta = post(endereco_audio, data=dados, files=arquivo)
        
    def envia_mensagem_opcaos():
        endereco = endereco_base + "/sendMessage"
        mensagem = {"keyboard": [[{"text":"Soar Alarme"}], [{"text": "Abrir"}], [{"text": "Ignorar"}]]}
        dados = {"chat_id": id_da_conversa, "reply_markup": mensagem, "text": "Opcoes"}
        resposta = post(endereco, json=dados)
        print("Depois do envio: mensagem enviada\n")

    print(resposta.text)
    
    #botao3.when_pressed = envia_msg_telegram
    botao1.when_held = liga_campainha
    botao1.when_released = desliga_campainha
    botao2.when_pressed = apaga_led1
    botao3.when_pressed = grava_audio
    botao3.when_released = encerra_gravacao_audio
    
    proximo_id_de_update = 0
    while True:
        endereco = endereco_base + "/getUpdates"
        dados = {"offset": proximo_id_de_update}
        resposta = get(endereco, json=dados)
        dicionario_da_resposta = resposta.json()
        print(dicionario_da_resposta)
        
        for resultado in dicionario_da_resposta['result']:
            print(resultado)
            mensagem = resultado["message"]
            if "text" in mensagem:
                if(mensagem['text'] == "Abrir"):
                    led1.on()
                elif(mensagem['text'] == "Soar Alarme"):
                    campainha.beep(n = 5, on_time = 0.2, off_time = 0.1)
                    #campainha.off()
            elif "voice" in mensagem:
                    id_do_arquivo = mensagem["voice"]["file_id"]
                    endereco = endereco_base + "/getFile"
                    dados = {"file_id": id_do_arquivo}
                    resposta = get(endereco, json = dados)
                    dicionario = resposta.json()
                    final_do_link = dicionario["result"]["file_path"]
                    link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_do_link
                    arquivo_de_destino = "meu_arquivo.ogg"
                    urlretrieve(link_do_arquivo, arquivo_de_destino)
                    player.loadfile("meu_arquivo.ogg")
            elif "photo" in mensagem:
                    foto_mais_resolucao = mensagem["photo"][-1]
                    id_do_arquivo = foto_mais_resolucao["file_id"]
                    # depois baixa o arquivo e faz algo com ele...
            proximo_id_de_update = resultado["update_id"] + 1
        sleep(0.1)

