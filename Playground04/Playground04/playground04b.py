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

    print("Buscando dados sobre o bot...")
    resultado = get(endereco_dados_do_bot)
    print(resultado.text)
    
    
    # Agora vamos conversar com o bot
    # 5 - Abra o Telegrma, busque o usuário do seu bot e inicie uma conversa com ele.
    # 6 - Envie uma ou mais mensagens quaisquer.
    # 7 - Abra o seu navegador e acesse http://api.telegram.org/botSUA_CHAVE_SECRETA/getUpdates
    #http://api.telegram.org/bot6363363454:AAFbYsrkFl3BjF3FRCqcLskkGlwecj1Ilzs/getUpdates
    # 8 - Copie o id do chat (procure por "chat": {"id":123456...}).
    id_da_conversa = "1585448160"
    
    
    # Pronto! Agora você pode enviar mensagens via programação!
    dados = {"chat_id": id_da_conversa, "text": "Jaimeco!"}
    endereco_para_mensagem = endereco_base + "/sendMessage"
    
    # DESCOMENTE AS LINHAS ABAIXO PARA TESTAR, E DEPOIS COMENTE DE NOVO.
    
    print("\nEnviando mensagem...")
    resultado = post(endereco_para_mensagem, json=dados)
    print(resultado.text)
    
    
    # Se você quiser enviar uma foto, é só abrir o arquivo e usar a sendPhoto.
    endereco_para_foto = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"photo": open("foto_telegram.jpg", "rb")} # foto de exemplo do Playground 04
    
    # DESCOMENTE AS LINHAS ABAIXO PARA TESTAR, E DEPOIS COMENTE DE NOVO.
    
    print("\nEnviando foto...")
    resultado = post(endereco_para_foto, data=dados, files=arquivo)
    print(resultado.text)
    

    # Para obter as mensagens enviadas pelo usuário ao bot, usamos a getUpdates.
    # Na teoria, a gente usou o while True para ficar buscando mensagens continuamente.
    # Neste playground, vamos chamar só uma vez, para simplificar.
    proximo_id_de_update = 0
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update}
    
    # DESCOMENTE AS LINHAS ABAIXO PARA TESTAR, E DEPOIS COMENTE DE NOVO
    
    print("\nBuscando novas mensagens...")
    resposta = get(endereco, json=dados)
    dicionario_da_resposta = resposta.json()
    print(dicionario_da_resposta)


    # VERIFIQUE OS DADOS RETORNADOS E ENCONTRE O PRIMEIRO "update_id".
    for resultado in dicionario_da_resposta['result']:
        mensagem = resultado['message']
        if 'text' in mensagem:
            texto = mensagem['text']
        elif 'voice' in mensagem:
            id_arquivo_enviado = mensagem['voice']['file_id']
        elif 'photo' in mensagem:
            foto_mais_resolucao = mensagem['photo'][-1]
            id_do_arquivo = foto_mais_resolucao['file_id']
        proximo_id_de_update = resultado['update_id'] + 1
        break
    
    # AGORA ATUALIZE A VARIÁVEL proximo_id_de_update ALI EM CIMA PARA ESSE VALOR + 1.
    #proximo_id_de_update = 0
    print("\nBuscando novas mensagens2...")
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update}
    resposta = get(endereco, json=dados)
    dicionario_da_resposta = resposta.json()
    print(dicionario_da_resposta)
    # RODE NOVAMENTE O PROGRAMA E VEJA QUE O PRIMEIRO RESULTADO NÃO APARECE MAIS.
    
    # OBS: uma vez que você fornece um offset, as mensagens anteriores nunca mais serão retornadas.
    
    
    
    # EXPERIMENTE INTEGRAR O BOT COM OS DISPOSITIVOS DO SIMULADOR!
    # Sugestão 1: enviar uma mensagem ao apertar um botão.
    botao1 = Button(11)
    
    def envia_msg_bot():
        print("\nEnviando mensagem ao bot playbot...")
        dados = {"chat_id": id_da_conversa, "text": "Boa noite bot! Apertei o botao 1"}
        endereco_para_mensagem = endereco_base + "/sendMessage"
        resultado = post(endereco_para_mensagem, json=dados)
        
    botao1.when_pressed = envia_msg_bot
    
    # Sugestão 2: usar o while True para tocar a campainha sempre que o usuário enviar uma mensagem pelo celular.
    campainha = Buzzer(16)
    
    def toca_campainha():
        campainha.beep(n = 1)
    
    while True:
        
        endereco = endereco_base + "/getUpdates"
        dados = {"offset": proximo_id_de_update}
        resposta = get(endereco, json=dados)
        dicionario_da_resposta = resposta.json()
        print(dicionario_da_resposta)
        
        for resultado in dicionario_da_resposta['result']:
            if 'update_id' in resultado:
                toca_campainha()
                proximo_id_de_update = resultado['update_id'] + 1
                        
        
        sleep(0.1)