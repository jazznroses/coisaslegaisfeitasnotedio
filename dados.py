import pygame
import random
import time

def rolar_dado():
    return random.randint(1, 6)

print("\n --- DADOS DO JABURU --- \n")
print("\n O JABURU MASTER ESTÁ JOGANDO OS DADOS! \n")
time.sleep(3)

dado = rolar_dado()
dado2 = rolar_dado()
soma_inicial = dado + dado2

print(f"Dados iniciais: {dado} e {dado2} (Total: {soma_inicial})")

if soma_inicial in (7, 11):
    print("\n Você ganhou de primeira! \n")
elif soma_inicial in (2, 3, 12):
    print("\n Você perdeu de primeira! \n")
else:
    ponto = soma_inicial
    print(f"\n Ponto estabelecido: {ponto}!")
    print(f"Para ganhar, você precisa tirar {ponto} novamente. Se tirar 7, você perde.")
    
    while True:
        escolha = int(input("\n Digite 0 para jogar os dados novamente ou 1 para sair: "))
        if escolha != 0:
            print("\n Você saiu do jogo! \n")
            break
            
        print("\n Jogando dados... \n")
        time.sleep(1.5)
        
        novo_dado1 = rolar_dado()
        novo_dado2 = rolar_dado()
        nova_soma = novo_dado1 + novo_dado2
        
        print(f"Novos dados: {novo_dado1} e {novo_dado2} (Total: {nova_soma})")
        
        if nova_soma == ponto:
            print(f"\n Você tirou {ponto} de novo! Você ganhou! \n")
            break
        elif nova_soma == 7:
            print("\n Você tirou 7! Você perdeu! \n")
            break
