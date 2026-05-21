import pygame
import sys
import random
import math

print("=== SISTEMA DE APOSTAS DA ROLETA AMERICANA ===")
print("Como você deseja apostar?")
print("1 - Em um Número específico (Paga 35 para 1)")
print("2 - Em uma Cor (Vermelho/Preto paga 1 para 1 | Verde paga 35 para 1)")

tipo_aposta = 0
while tipo_aposta not in [1, 2]:
    try:
        tipo_aposta = int(input("Escolha a opção (1 ou 2): "))
    except ValueError:
        print("Por favor, digite um número válido.")

numero_apostado = -1
cor_apostada = -1

if tipo_aposta == 1:
    print("\nVocê escolheu apostar em número.")
    while numero_apostado < 0 or numero_apostado > 37:
        try:
            numero_apostado = int(input("Digite um número de 0 a 36 (ou 37 para o '00'): "))
        except ValueError:
            print("Número inválido.")
else:
    print("\nVocê escolheu apostar em cor.")
    print("1 - Vermelho")
    print("2 - Preto")
    print("3 - Verde (0 ou 00)")
    while cor_apostada not in [1, 2, 3]:
        try:
            cor_apostada = int(input("Escolha a cor (1, 2 ou 3): "))
        except ValueError:
            print("Opção inválida.")

print("\nAba aberta! Foque na janela da Roleta e pressione ESPAÇO para lançar a bolinha!")

pygame.init()
LARGURA, ALTURA = 900, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Roleta Americana Profissional com Apostas")
relogio = pygame.time.Clock()

BRANCO = (255, 255, 255)
VERDE_CASSINO = (14, 105, 50)
VERDE_ROBERTA = (0, 150, 50)
VERMELHO = (210, 30, 30)
PRETO = (30, 30, 30)
OURO = (212, 175, 55)

NUMEROS_AMERICANOS = [
    0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1,
    37, 0, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2
]

def obter_cor(numero):
    if numero == 0 or numero == 37:
        return VERDE_ROBERTA
    vermelhos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    return VERMELHO if numero in vermelhos else PRETO

def formatar_numero(numero):
    if numero == 37:
        return "00"
    return str(numero)

class Roleta:
    def __init__(self, centro_x, centro_y, raio_externo):
        self.centro = (centro_x, centro_y)
        self.raio_externo = raio_externo
        self.angulo_rotacao = 0
        self.velocidade_rotacao = 0.5
        self.total_fatias = len(NUMEROS_AMERICANOS)
        self.tamanho_fatia = 360 / self.total_fatias

    def atualizar(self):
        self.angulo_rotacao = (self.angulo_rotacao + self.velocidade_rotacao) % 360

    def desenhar(self, superficie):
        pygame.draw.circle(superficie, (60, 30, 10), self.centro, self.raio_externo)
        pygame.draw.circle(superficie, OURO, self.centro, self.raio_externo - 10, 3)
        pygame.draw.circle(superficie, (80, 80, 80), self.centro, self.raio_externo - 15)

        fonte = pygame.font.SysFont("Arial", 14, bold=True)
        
        for i, num in enumerate(NUMEROS_AMERICANOS):
            angulo_graus = self.angulo_rotacao + (i * self.tamanho_fatia)
            angulo_rad = math.radians(angulo_graus)
            
            raio_fatias_ext = self.raio_externo - 15
            raio_fatias_int = self.raio_externo - 60
            
            x_ext = self.centro[0] + raio_fatias_ext * math.cos(angulo_rad)
            y_ext = self.centro[1] + raio_fatias_ext * math.sin(angulo_rad)
            
            angulo_meio = math.radians(angulo_graus + self.tamanho_fatia / 2)
            x_meio = self.centro[0] + (raio_fatias_ext - 22) * math.cos(angulo_meio)
            y_meio = self.centro[1] + (raio_fatias_ext - 22) * math.sin(angulo_meio)
            
            pygame.draw.circle(superficie, obter_cor(num), (int(x_meio), int(y_meio)), 14)
            
            x_int = self.centro[0] + raio_fatias_int * math.cos(angulo_rad)
            y_int = self.centro[1] + raio_fatias_int * math.sin(angulo_rad)
            pygame.draw.line(superficie, OURO, (x_int, y_int), (x_ext, y_ext), 1)
            
            texto = fonte.render(formatar_numero(num), True, BRANCO)
            texto_rotacionado = pygame.transform.rotate(texto, -angulo_graus - 90)
            rect_texto = texto_rotacionado.get_rect()
            rect_texto.center = (
                self.centro[0] + (raio_fatias_ext - 22) * math.cos(angulo_meio),
                self.centro[1] + (raio_fatias_ext - 22) * math.sin(angulo_meio)
            )
            superficie.blit(texto_rotacionado, rect_texto)
            
        pygame.draw.circle(superficie, (40, 40, 40), self.centro, self.raio_externo - 60)
        pygame.draw.circle(superficie, OURO, self.centro, 25)
        pygame.draw.circle(superficie, (200, 200, 200), self.centro, 10)


class Bolinha:
    def __init__(self, roleta):
        self.roleta = roleta
        self.raio = 8
        self.cor = (240, 240, 240)
        self.estado = "PARADA"
        self.angulo = 0
        self.velocidade = 0
        self.raio_orbita = 0
        self.indice_encaixe = 0

    def lancar(self):
        self.estado = "GIRANDO"
        self.angulo = random.uniform(0, 360)
        self.velocidade = random.uniform(-12, -8)
        self.raio_orbita = self.roleta.raio_externo - 25

    def atualizar(self):
        if self.estado == "GIRANDO":
            self.angulo += self.velocidade
            self.velocidade *= 0.985
            
            if abs(self.velocidade) < 4:
                self.raio_orbita -= 1.2
                
            if self.raio_orbita <= (self.roleta.raio_externo - 22):
                self.estado = "ENCAIXANDO"
                
        elif self.estado == "ENCAIXANDO":
            angulo_relativo = (self.angulo - self.roleta.angulo_rotacao) % 360
            self.indice_encaixe = int(angulo_relativo / self.roleta.tamanho_fatia)
            self.estado = "PARADA"

        elif self.estado == "PARADA":
            self.angulo = self.roleta.angulo_rotacao + (self.indice_encaixe * self.roleta.tamanho_fatia) + (self.roleta.tamanho_fatia / 2)
            self.raio_orbita = self.roleta.raio_externo - 22

    def obter_numero_atual(self):
        if self.estado == "PARADA":
            return NUMEROS_AMERICANOS[self.indice_encaixe]
        return None

    def desenhar(self, superficie):
        if self.estado != "ENCAIXANDO":
            x = self.roleta.centro[0] + self.raio_orbita * math.cos(math.radians(self.angulo))
            y = self.roleta.centro[1] + self.raio_orbita * math.sin(math.radians(self.angulo))
            pygame.draw.circle(superficie, (50, 50, 50), (int(x)+2, int(y)+2), self.raio)
            pygame.draw.circle(superficie, self.cor, (int(x), int(y)), self.raio)


roleta = Roleta(LARGURA // 2, ALTURA // 2 - 40, 240)
bolinha = Bolinha(roleta)
fonte_painel = pygame.font.SysFont("Arial", 20, bold=True)

ja_jogou = False

if tipo_aposta == 1:
    texto_aposta = f"Sua Aposta: Número {formatar_numero(numero_apostado)}"
else:
    cor_txt = "VERMELHO" if cor_apostada == 1 else "PRETO" if cor_apostada == 2 else "VERDE"
    texto_aposta = f"Sua Aposta: Cor {cor_txt}"

resultado_texto = f"{texto_aposta} | Pressione ESPAÇO para jogar!"
cor_resultado_fundo = (40, 40, 40)

while True:
    tela.fill(VERDE_CASSINO)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if bolinha.estado == "PARADA" and not ja_jogou:
                    bolinha.lancar()
                    ja_jogou = True
                    resultado_texto = "A bola está correndo..."
                    cor_resultado_fundo = (40, 40, 40)

    roleta.atualizar()
    bolinha.atualizar()

    roleta.desenhar(tela)
    bolinha.desenhar(tela)

    num_sorteado = bolinha.obter_numero_atual()
    if num_sorteado is not None and bolinha.estado == "PARADA" and resultado_texto == "A bola está correndo...":
        cor_sorteada = obter_cor(num_sorteado)
        nome_cor = "VERDE" if cor_sorteada == VERDE_ROBERTA else "VERMELHO" if cor_sorteada == VERMELHO else "PRETO"
        
        ganhou = False
        if tipo_aposta == 1:
            if numero_apostado == num_sorteado:
                ganhou = True
        else:
            if cor_apostada == 1 and cor_sorteada == VERMELHO: ganhou = True
            if cor_apostada == 2 and cor_sorteada == PRETO: ganhou = True
            if cor_apostada == 3 and cor_sorteada == VERDE_ROBERTA: ganhou = True

        if ganhou:
            if tipo_aposta == 2 and cor_apostada != 3:
                pagamento = "Ganhou! Pagamento 1:1"
            else:
                pagamento = "GANHOU! Prêmio Máximo 35:1!"
            resultado_texto = f"Deu {formatar_numero(num_sorteado)} ({nome_cor}). {pagamento} | Reinicie para jogar novamente."
            cor_resultado_fundo = VERDE_ROBERTA
        else:
            resultado_texto = f"Deu {formatar_numero(num_sorteado)} ({nome_cor}). Você perdeu! | Reinicie para jogar novamente."
            cor_resultado_fundo = VERMELHO

    barra_status = pygame.Rect(0, ALTURA - 100, LARGURA, 100)
    pygame.draw.rect(tela, cor_resultado_fundo, barra_status)
    pygame.draw.rect(tela, OURO, barra_status, 4)

    txt_render = fonte_painel.render(resultado_texto, True, BRANCO)
    txt_rect = txt_render.get_rect(center=(LARGURA // 2, ALTURA - 50))
    tela.blit(txt_render, txt_rect)

    pygame.display.flip()
    relogio.tick(60)
