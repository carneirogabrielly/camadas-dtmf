# Importações necessárias
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
#********************************************instruções*********************************************** 
    # Seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada, conforme tabela DTMF.
    # Então, inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF.
    # De posse das duas frequeências, agora voce tem que gerar, por alguns segundos suficientes para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada.
    # Essas senoides têm que ter taxa de amostragem de 44100 amostras por segundo, sendo assim, voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t).
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as duas senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Você pode gravar o som com seu celular ou qualquer outro microfone para o lado receptor decodificar depois. Ou reproduzir enquanto o receptor já capta e decodifica.
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado, como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
# Frequências associadas a cada tecla DTMF
# Frequências associadas a cada tecla DTMF, conforme a nova tabela
dtmf_freqs = {
    '1': (679, 1209), '2': (679, 1336), '3': (679, 1477), 'A': (679, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (825, 1209), '8': (825, 1336), '9': (825, 1477), 'C': (825, 1633),
    'X': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633)
}


def main():
    print("Inicializando encoder")
    print("Aguardando usuário")
    
    # Solicita tecla do usuário
    tecla = input("Digite uma tecla do teclado numérico DTMF: ")
    
    # Frequências correspondentes à tecla
    if tecla in dtmf_freqs:
        f1, f2 = dtmf_freqs[tecla]
        print(f"Gerando Tom referente ao símbolo : {tecla}")
    else:
        print("Tecla inválida! Execute o programa novamente.")
        return
    
    # Parâmetros do sinal
    fs = 44100  # Taxa de amostragem
    duration = 5  # Duração em segundos
    t = np.linspace(0, duration, int(fs * duration))
    A = 1  # Amplitude
    
    # Geração das senoides
    senoide1 = A * np.sin(2 * np.pi * f1 * t)
    senoide2 = A * np.sin(2 * np.pi * f2 * t)
    
    # Soma das senoides para o sinal DTMF
    tone = senoide1 + senoide2
    
    # Executa o som
    print("Executando as senoides (emitindo o som)")
    sd.play(tone, fs)
    sd.wait()  # Aguarda a execução do áudio
    
    # Plota o sinal no domínio do tempo
    plt.figure(figsize=(10, 4))
    plt.plot(t[:1000], tone[:1000])  # Exibe os primeiros 1000 pontos para melhor visualização
    plt.title(f'Sinal de Áudio para a Tecla {tecla}')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()
    
    # Gera a Transformada de Fourier e plota
    print("Gerando gráficos da Transformada de Fourier")
    signal = signalMeu()  
    signal.plotFFT(tone, fs)
    plt.show()

if __name__ == "__main__":
    main()
