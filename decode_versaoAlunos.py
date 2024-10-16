#Importe todas as bibliotecas
from suaBibSignal import *
from scipy.signal import find_peaks #troquei para encontrar os picos do gráfico
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy.io.wavfile import write


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100  #taxa de amostragem
    sd.default.channels = 1 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas.
    #Muitas vezes a gravação retorna uma lista de listas. Você poderá ter que tratar o sinal gravado para ter apenas uma lista.
    duration =  5 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic   
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    freqDeAmostragem = 44100
    numAmostras = freqDeAmostragem*duration
    #faca um print na tela dizendo que a captação comecará em n segundos. e então 
    #use um time.sleep para a espera.
    for i in range(3):
        print(f"A gravação vai começar em {3-i} segundos!")
        time.sleep(1)
    
    
    #A seguir, faca um print informando que a gravacao foi inicializada
    print("A gravação começou!")
    

    #para gravar, utilize
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    
    sd.wait()
    print("...     FIM")
    # Salvar o áudio como um arquivo .wav
    write("minha_gravacao.wav", freqDeAmostragem, audio)
    print("Áudio salvo como 'minha_gravacao.wav'")

    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, ou uma lista, ou ainda uma lista de listas (isso dependerá do seu sistema, drivers etc...).
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = [dado[0] for dado in audio]
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, 5, numAmostras)
    
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) .
    plt.plot(tempo, dados)
    
    ################## se eu quiser plotar amostras reduzidas #####################
    # amostras_reduzidas = 100  # Plotar 1 a cada 100 pontos (ajuste conforme necessário)
    # plt.plot(tempo[::amostras_reduzidas], dados[::amostras_reduzidas])
    
    # Adicionando título e rótulos de eixos
    plt.title("Gráfico de Tempo vs Dados")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Dados")

    # Exibir o gráfico
    plt.show()
       
    ## Calcule e plote o Fourier do sinal audio. como saída tem-se a amplitude e as frequências.
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    
    #Agora você terá que analisar os valores xf e yf e encontrar em quais frequências estão os maiores valores (picos de yf) de da transformada.
    #Encontrando essas frequências de maior presença (encontre pelo menos as 5 mais presentes, ou seja, as 5 frequências que apresentam os maiores picos de yf). 
    #Cuidado, algumas frequências podem gerar mais de um pico devido a interferências na tranmissão. Quando isso ocorre, esses picos estão próximos. Voce pode desprezar um dos picos se houver outro muito próximo (5 Hz). 
    distancia_picos = 5*duration #numero de amostras em 5 hertz
    i_peaks, _ = find_peaks(yf, distance=distancia_picos)
    valores_picos = [yf[i] for i in i_peaks]
    frequencias_picos = [xf[i] for i in i_peaks]
    maiores_picos = sorted(zip(frequencias_picos, valores_picos), key=lambda x: x[1], reverse=True)[:5] #retorna uma lista de tuplas, o primeiro da tupla é a frequencia e o segundo a amplitude
    #printe os picos encontrados! 
    print(maiores_picos)
    
    
    
    #Alguns dos picos  (na verdade 2 deles) devem ser bem próximos às frequências do DTMF enviadas!
    #Para descobrir a tecla pressionada, você deve encontrar na tabela DTMF frquências que coincidem com as 2 das 5 que você selecionou.
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF
    
    dtmf_table = {
        679: {1209: '1', 1336: '2', 1477: '3', 1633: 'A'},
        770: {1209: '4', 1336: '5', 1477: '6', 1633: 'B'},
        825: {1209: '7', 1336: '8', 1477: '9', 1633: 'C'},
        941: {1209: 'X', 1336: '0', 1477: '#', 1633: 'D'}
    }

    # Encontrar as frequências mais próximas da tabela DTMF
    frequencias_baixas = [679, 770, 825, 941]
    frequencias_altas = [1209, 1336, 1477, 1633]

    # Encontrar a frequência baixa mais próxima
    f1 = min(frequencias_baixas, key=lambda x: min([abs(x - f[0]) for f in maiores_picos]))

    # Encontrar a frequência alta mais próxima
    f2 = min(frequencias_altas, key=lambda x: min([abs(x - f[0]) for f in maiores_picos]))

    # Encontrar a tecla correspondente
    tecla = dtmf_table.get(f1, {}).get(f2, None)

    if tecla:
        print(f"Tecla detectada: {tecla} (frequências: {f1} Hz e {f2} Hz)")
    else:
        print("Nenhuma tecla DTMF foi detectada.")

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla.       
    ## Exiba gráficos do fourier do som gravados 
    plt.plot(xf, yf)
    plt.title("Transformada de Fourier")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
