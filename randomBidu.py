#%% IMPORT

import numpy as np
import matplotlib.pyplot as plt
import time

#%% VARIÁVEIS
def valores():
    n = 200
    tamanho = np.arange(int(n/2 - 0.05*n), int(n/2 + 0.05*n), 1)
    Pot = 0.01
    return n, tamanho, Pot

#%% CONDIÇÕES DE CONTORNO
    
def contorno():
    
    #Definindo uma malha
    n , tamanho, Pot = valores()
    
    #Fixando extremidades
    extremidades = np.zeros((n,n), dtype=bool)
    potencial = np.zeros((n,n))
    
    #Zero no "infinito"
    potencial[0,:] = 0
    potencial[n-1,:] = 0
    potencial[:,0] = 0
    potencial[:,n-1] = 0
    
    extremidades[0, :] = True
    extremidades[n-1, :] = True
    extremidades[:, 0] = True
    extremidades[:, n-1] = True
    
    #CAPACITOR
        
    potencial[tamanho.astype(int),int(n/2 + 0.05*n)] = -1*Pot
    potencial[tamanho.astype(int),int(n/2 - 0.05*n)] = Pot 
    
    extremidades[tamanho.astype(int),int(n/2 + 0.05*n)] = True
    extremidades[tamanho.astype(int),int(n/2 - 0.05*n)] = True
    
    return potencial, extremidades

#%% CÁLCULO DO POTENCIAL

def potencial():
    
    #Passando informações de contorno
    potencial, extremidades = contorno()
    n, tamanho,_ = valores()
    
    #Andando:
    
    variacoes = [[1,0],[-1,0],[0,1],[0,-1]]
    
    for i in range(int(n/4),int(3*n/4+1)):
        for j in range(int(n/4),int(3*n/4+1)):
            
            lugar = np.array([i,j])
            
            p = 0
            
            potencial_b = np.array([0])
            
            while p < 100000:
                
                if extremidades[lugar[0],lugar[1]] != True:
                    
                    while extremidades[lugar[0],lugar[1]] != True:
            
                        lugar = lugar + variacoes[int(np.random.randint(4, size=1))]
                        
                    potencial_b = potencial_b + potencial[lugar[0]][lugar[1]]
                
                else:
                
                    potencial_b = potencial_b + potencial[lugar[0]][lugar[1]]
                
                p = p + 1
            
            potencial[i,j] = (potencial_b)/100000
            
    return potencial
            
#%% Sei lá]
        
def plot_numerico(potencial,i):
    
    n,_,_ = valores()
    
    #Potencial
    print('Gráfico (Numérico):')
    plt.figure()
    plt.ylim(n/4, 3*n/4)
    plt.xlim(n/4, 3*n/4)
    potencial = np.transpose(potencial)
    plt.pcolor(potencial)
    plt.colorbar()
    plt.savefig("Potencial"+str(i)+".png")
    
    #Equipotenciais
    x = np.arange(n)
    y = np.arange(n)
    X, Y = np.meshgrid(x,y)
    plt.figure()
    CS = plt.contour(X, Y, potencial)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.savefig("Equipotencial"+str(i)+".png") 

    return 0

#%% MALHA DOS VIZINHOS
def vizinhos(potencial):
    #Esquerda
    potencial_esquerda = np.roll(potencial, 1, axis=1)
    #Direita
    potencial_direita = np.roll(potencial, -1, axis=1)
    #Em baixo
    potencial_baixo = np.roll(potencial, -1, axis=0)
    #Em cima
    potencial_cima = np.roll(potencial, 1, axis=0)
    return potencial_esquerda, potencial_direita, potencial_baixo, potencial_cima

#%% POTENCIAL NUMÉRICO - RESOLUÇÃO DA EQUAÇÃO DE LAPLACE
def laplace(potencial):
    _, condutor_bool = contorno()
    for i in range(30):
        potencial_esquerda, potencial_direita, potencial_baixo, potencial_cima = vizinhos(potencial)
        potencial_novo = np.where(condutor_bool == False, 1/4 * (potencial_esquerda + potencial_direita
                                                             + potencial_cima + potencial_baixo), potencial)
        potencial = potencial_novo
    return potencial

#%% CÁLCULOS
pot ,_= contorno()
plot_numerico(pot,1)

start = time.time()
poten = potencial()
plot_numerico(poten,2)
end = time.time()

potenci = laplace(poten)
plot_numerico(potenci,3)

print('Tempo de simulação: ' + str(end - start))
