#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:39:05 2019
@author: hiro
"""
import numpy as np
import matplotlib.pyplot as plt
import time

#testando a bagaca no terminal

#%% VARIÁVEIS
def n_malha():
    return 200

def epsilon():
    return 0.00001

def tamanho_solido():
    return 0.2
    
def largura_capacitor():
    return 0.2
    
def distancia_placas():
    return 0.1
    
def pot_placa():
    return 100

def pot_solido():
    return 100

#%% DEFINIÇÃO DA MALHA E DAS CONDIÇÕES DE CONTORNO
def condutor(caso):
    n = n_malha()
    pot_sol = pot_solido()
    V = pot_placa()
    condutor_bool = np.zeros((n,n), dtype=bool)
    potencial = np.ones((n,n))
    
    #com licenca
    #caso = 1
    #obrigado
        
    #Quadrado
    if caso==0:
        solido_lado = int(n*tamanho_solido())
        solido = np.arange(int((n - solido_lado)/2), int((n + solido_lado)/2))
    
        condutor_bool[0, :] = True
        condutor_bool[n-1, :] = True
        condutor_bool[:, 0] = True
        condutor_bool[:, n-1] = True

        potencial[0,:] = 0
        potencial[n-1,:] = 0
        potencial[:,0] = 0
        potencial[:,n-1] = 0
       
        for i in solido:
           condutor_bool[i, solido] = True
           potencial[i, solido] = pot_sol
    
    #circulo
    if caso==1:
        raio = n*tamanho_solido()/2 #raio do solido
        raio_ext = n/2            #raio da superficie
        solido = np.arange(int(n/2-raio),int(n/2+raio))
        
        for i in range(n):
            for j in range(n):
                if( (i-n/2)**2+(j-n/2)**2 >= raio_ext**2):
                    condutor_bool[i,j] = True
                    potencial[i,j] = 0
                    
        for i in solido:
            for j in solido:
                if( (i-n/2)**2+(j-n/2)**2 <= raio**2):
                    condutor_bool[i,j] = True
                    potencial[i,j] = pot_sol
                    
    #capacitor
    if caso==2:
        largura = int(n*largura_capacitor())
        altura = int(n*distancia_placas()/2)
        placa = np.arange(int((n - largura)/2), int((n + largura)/2))
    
        condutor_bool[0, :] = True
        condutor_bool[n-1, :] = True
        condutor_bool[:, 0] = True
        condutor_bool[:, n-1] = True

        potencial[0,:] = 0
        potencial[n-1,:] = 0
        potencial[:,0] = 0
        potencial[:,n-1] = 0
        
        condutor_bool[int(n/2+altura), placa] = True
        condutor_bool[int(n/2-altura), placa] = True
        potencial[int(n/2+altura), placa] = V
        potencial[int(n/2-altura), placa] = -1*V
                    
    return potencial, condutor_bool                

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
def laplace(caso):
    potencial, condutor_bool = condutor(caso)
    eps = epsilon()
    diferenca_max = eps + 1
    while diferenca_max>=eps:
        potencial_esquerda, potencial_direita, potencial_baixo, potencial_cima = vizinhos(potencial)
        potencial_novo = np.where(condutor_bool == False, 1/4 * (potencial_esquerda + potencial_direita
                                                             + potencial_cima + potencial_baixo), potencial)
        diferenca = np.absolute(potencial_novo - potencial)
        diferenca_max = np.amax(diferenca)
        potencial = potencial_novo
    return potencial

#%% POTENCIAL ANALÍTICO (CASO DA BARRA)
def potencial_analitico(caso):
    eps = epsilon()
    n = n_malha()
    x = np.arange(n)
    y = np.arange(n)
    X, Y = np.meshgrid(x,y)
    dif_max = eps +1
    i = 1
    Z = np.zeros(X.shape)
    if caso==0:
        while dif_max>=eps/1000:
            Z_novo = 400/((2*i - 1)*np.pi) *np.sin(((2*i - 1) *np.pi * X)/n)*(np.exp((2*i -1)*np.pi*(Y/n - 1)) + np.exp(-(2*i -1)*np.pi*(Y/n + 1)))/(1- np.exp(-2**(2*n-1)*np.pi)) + Z
            dif = np.absolute(Z_novo - Z)
            dif_max = np.amax(dif)
            Z = Z_novo
            i = i +1
    return X, Y,Z

#%% PLOT POTENCIAL NUMÉRICO

def plot_numerico(potencial):
    #Potencial
    print('Gráfico (Numérico):')
    plt.figure()
    potencial = np.transpose(potencial)
    plt.pcolor(potencial)
    plt.colorbar()
    plt.show()
    
    #Equipotenciais
    x = np.arange(n_malha())
    y = np.arange(n_malha())
    X, Y = np.meshgrid(x,y)
    plt.figure()
    CS = plt.contour(X, Y, potencial)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.show()  

    return 0

#%% PLOT POTENCIAL ANALÍTICO (CASO DA BARRA)
    
def plot_analitico(potencial):
    print('Gráfico (Analítico):')
    #Potencial
    X, Y,Z = potencial_analitico(caso)
    plt.figure()
    plt.pcolor(Z)
    plt.colorbar()
    plt.show()
    
    #Equipotenciais
    plt.figure()
    CS = plt.contour(X, Y, Z)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.show()  
    
    return 0

#%% CAMPO ELÉRTICO
def plot_campo(potencial, levels=10, linewidth=1, density=0.5,
               arrowsize=1.5, surface_label = False, fig='',
               fig1_name='Mapa_de_Cor.png', fig2_name='Campo.png'):
    
    #Potencial
    plt.figure(figsize=(7, 6))
    plt.pcolor(potencial)
    plt.colorbar()
#    plt.show()
    plt.savefig(fig+fig1_name, dpi=200)
    
    #Equipotenciais e linhas de campo
    x = np.linspace(-1, 1, n_malha())
    y = np.linspace(-1, 1, n_malha())
    X, Y = np.meshgrid(x, y)
    
    def grad_2d(f, x, y):
        
        dx = np.roll(f, 1, axis=0) - np.roll(f, -1, axis=0) 
        dy = np.roll(f, 1, axis=1) - np.roll(f, -1, axis=1)
        
        return dx, dy
    
    Ex, Ey = grad_2d(potencial, x, y)
    
    fig2, ax2 = plt.subplots()
    fig2.set_size_inches((7,7))

    CS = ax2.contour(X, Y, potencial, cmap=plt.cm.inferno, levels = levels)
    if surface_label: plt.clabel(CS, inline=1, fontsize=14)

    color = 2 * (np.hypot(Ex, Ey))**(1/2)
    ax2.streamplot(y, x, Ey, Ex, color=color, linewidth=linewidth, cmap=plt.cm.inferno, 
                  density=density, arrowstyle='->', arrowsize=arrowsize)
#    ax.set_xlabel('$x$')
#    ax.set_ylabel('$y$')
    ax2.set_xlim(-1.05,1.05)
    ax2.set_ylim(-1.05,1.05)
    ax2.set_aspect('equal')
#    plt.show()
    plt.savefig(fig+fig2_name, dpi=200)

#%% CÁLCULOS

casos = {'Quadrado': 0, 'Circulo':1}
caso = casos['Quadrado']
#excuse me
caso = 2
#thank you
potencial = laplace(caso)
potencial2 = laplace(casos['Circulo'])
X, Y, Z = potencial_analitico(caso=0)
#plot_numerico(potencial)

plot_campo(potencial, surface_label=True, density=1, fig='PlacasParalelas_')
plot_campo(potencial2, surface_label=True, fig='Circulo_')


plot_campo(Z, surface_label=True, levels=8, fig='Barra_')
