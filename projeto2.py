#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:39:05 2019

@author: hiro
"""
import numpy as np
import matplotlib.pyplot as plt

#%% VARIÁVEIS
def n_malha():
    return 100

def epsilon():
    return 0.001

def tamanho_solido():
    return 0.2

#%% DEFINIÇÃO DA MALHA E DAS CONDIÇÕES DE CONTORNO
def condutor(caso):
    n = n_malha()
    condutor_bool = np.zeros((n,n), dtype=bool)
    potencial = np.ones((n,n))
    solido_lado = int(n*tamanho_solido())
    solido = np.arange(int((n - solido_lado)/2), int((n + solido_lado)/2))
    if caso==0:
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
           potencial[i, solido] = 100
    return potencial, condutor_bool

#%% MALHA DOS VIZINHOS
def vizinhos(potencial):
    n = n_malha()
    #Zeros
    zero_coluna = np.zeros((n,1)) #Array COLUNA de 0
    zero_linha = np.zeros((1,n)) #Array LINHA de 0
    #Esquerda
    potencial_esquerda = np.delete(potencial, n-1, axis=1)
    potencial_esquerda = np.concatenate((zero_coluna, potencial_esquerda), axis =1)
    #Direita
    potencial_direita = np.delete(potencial, 0, axis=1)
    potencial_direita = np.concatenate((potencial_direita, zero_coluna), axis =1)
    #Em baixo
    potencial_baixo = np.delete(potencial, 0, axis=0)
    potencial_baixo = np.concatenate((potencial_baixo, zero_linha), axis =0)
    #Em cima
    potencial_cima = np.delete(potencial, n-1, axis=0)
    potencial_cima = np.concatenate((zero_linha, potencial_cima), axis =0)
    return potencial_esquerda, potencial_direita, potencial_baixo, potencial_cima

#%% POTENCIAL NUMÉRICO - RESOLUÇÃO DA EQUAÇÃO DE LAPLACE
def laplace(caso):
    potencial, condutor_bool = condutor(caso)
    eps = epsilon()
    if caso==0:
        diferenca_max = eps + 1
        while diferenca_max>=eps:
            potencial_esquerda, potencial_direita, potencial_baixo, potencial_cima = vizinhos(potencial)
            
            potencial_novo = np.where(condutor_bool == False, 1/4 * (potencial_esquerda + potencial_direita
                                                                 + potencial_cima + potencial_baixo), potencial)
            diferenca = np.absolute(potencial_novo - potencial)
            diferenca_max = np.amax(diferenca)
            potencial = potencial_novo
    return potencial

#%% POTENCIAL ANALÍTICO
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

#%% PLOT POTENCIAL ANALÍTICO
    
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


#%% CÁLCULOS

casos = {'Quadrado': 0}
caso = casos['Quadrado']
potencial = laplace(caso)
plot_numerico(potencial)
plot_analitico(potencial)



