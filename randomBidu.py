#%% IMPORT

import numpy as np
import matplotlib.pyplot as plt
import time

#%% VARIÁVEIS
def valores():
    n = 100 #Malha total
    tamanho = np.arange(int(n/2 - 0.05*n), int(n/2 + 0.05*n), 1) #Capacitor é 0.1n
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
    
    print(potencial, extremidades)
    
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
            
            p = 0
            
            potencial_b = np.zeros(1)
            
            while p < 10000:
                
                lugar = np.array([i,j])
                
                if extremidades[lugar[0],lugar[1]] != True:
                    
                    while extremidades[lugar[0],lugar[1]] != True:
            
                        lugar = lugar + variacoes[int(np.random.randint(4, size=1))]
                        
                    potencial_b = np.append(potencial_b, potencial[lugar[0]][lugar[1]])
                    #potencial_b = potencial_b + float(potencial[lugar[0]][lugar[1]])
                    print(potencial_b)
                
                if extremidades[lugar[0],lugar[1]] == True:
                
                    potencial_b = np.append(potencial_b, potencial[lugar[0]][lugar[1]])
                    #potencial_b = potencial_b + float(potencial[lugar[0]][lugar[1]])
                
                p = p + 1
            
            potencial[i,j] = (np.sum(potencial_b))/10000
            
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
    
#%% CÁLCULOS
pot ,_= contorno()
plot_numerico(pot,1)

start = time.time()
poten = potencial()
plot_numerico(poten,2)
end = time.time()

print('Tempo de simulação: ' + str(end - start))
