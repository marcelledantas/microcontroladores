# Neste playground, vamos trabalhar com o microfone e a câmera.
# ATENÇÃO: lembre-se que os comandos variam de acordo com o sistema operacional!
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Inicialização do simulador. Escreva todo o seu código dentro da main!
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas, como sempre.
    from os import system
    from subprocess import Popen
    
    from gpiozero import LED, Button, DistanceSensor
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    from datetime import datetime, timedelta
   
    
    # Vamos começar com a parte de tirar fotos com a câmera web.
    # Mas primeiro temos alguns avisos importantes!
    
    # 1. Caso você não tenha uma câmera web, existem apps que conectam a câmera do seu celular com o computador.
        # Nesse caso, experimente apps como o Camo ou o Iriun.
        
    # 2. Usuários de Windows e Mac precisam anotar o identificador da câmera e do microfone.
        # Windows: rode o arquivo listar_midias.bat e anote os nomes. Integrated Webcam
        # Mac: rode o arquivo listar_midias.command (botão direito > Abrir) e anote os números.
        
    # 3. Usuários de Mac ainda precisam de 2 detalhes extras:
        # Vá na pasta extra/binarios/ffmpeg/mac, clique com o botão direito no ffmpeg e selecione Abrir.
            # (só precisa fazer isso 1 vez, para dar permissão de execução ao binário)
        # Use sempre o Run > Run current script in terminal do Thonny.
        

    
    # Conforme eu comentei na teoria, a ideia aqui é chamar um aplicativo externo por linha de comando, via system.
    # Só que esse app vai variar de acordo com o seu sistema operacional.
    
    
    # DESCOMENTE UMA DAS LINHAS ABAIXO, DE ACORDO COM O SEU SISTEMA OPERACIONAL.
    # EM SEGUIDA, RODE O CÓDIGO E ABRA O ARQUIVO foto_camera.jpg CRIADO NA MESMA PASTA DESTE ARQUIVO PYTHON.
    # CASO A FOTO APAREÇA CORRETAMENTE, COMENTE A LINHA NOVAMENTE.
    
    # WINDOWS
    #system("CommandCam /filename foto_camera.jpg /delay 500")
    
    # MAC (substitua o valor de frames por segundo depois do -r e/ou o número da câmera depois do -i, se necessário)
    #system("ffmpeg -y -pix_fmt uyvy422 -ss 0.5 -f avfoundation -r 30 -i 0 foto_camera.jpg")
    
    # LINUX
    #system("fswebcam --resolution 640x480 --skip 10 foto_camera.jpg")
    
    
    
    # O próximo passo é tentar gravar o áudio do microfone.
    # Vamos começar capturando o som por 3 segundos.
    
    
    # DESCOMENTE UMA DAS LINHAS ABAIXO, DE ACORDO COM O SEU SISTEMA OPERACIONAL.
    # DEPOIS RODE O CÓDIGO, FALE ALGO NO MICROFONE E ABRA O ARQUIVO audio1.wav CRIADO NA MESMA PASTA DESTE ARQUIVO PYTHON.
    # CASO O ÁUDIO TENHA SIDO GRAVADO CORRETAMENTE, COMENTE A LINHA NOVAMENTE.
    
    # WINDOWS (escreva o nome do microfone que aparece ao rodar listar_midias.bat)
    #system('ffmpeg -y -f dshow -i audio="Microfone (Realtek(R) Audio)" -t 00:03 audio1.wav')
    
    # MAC (substitua o número depois do -i se necessário)
    #system("ffmpeg -y -f avfoundation -i :1 -t 3 audio1.wav")
    
    # LINUX
    #system("arecord --duration 3 audio1.wav")
    
    
    
    # Por fim, vamos testar o controle manual do início e do término da gravação.
    # Copiei o mesmo exemplo lá da teoria.
    
       
        
    comando = ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=Microfone (Realtek(R) Audio)", "-t", "00:30", "audio2.wav"]
        
   
    # Mas agora vamos chamar essas funções ao apertar os botões 1 e 2.
    
    botao1 = Button(11)
    botao2 = Button(12)
    botao3 = Button(13)
    
    led1 = LED(21)
    
    sensor_de_distancia = DistanceSensor(trigger=17, echo=18)
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    
 
    
    def tira_foto():
        for i in range(5):
            system("CommandCam /filename foto-" + str(i + 1) +".jpg /delay 500")
            led1.blink(n=1, on_time = 0.1, off_time = 0.1)
            sleep(2)
    
    def exibe_lcd():
        lcd.message("Gravando..")
        system('ffmpeg -y -f dshow -i audio="Microfone (Realtek(R) Audio)" -t 00:05 audio1.wav')
    
       
    botao1.when_pressed = exibe_lcd
    botao2.when_pressed = tira_foto
    
    while True:
                
        sleep(0.1)