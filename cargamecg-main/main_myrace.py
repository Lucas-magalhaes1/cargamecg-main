import pygame, sys, math, time
from shader import *
from light import *
from pygame.locals import *

pygame.init()

# Carregar a primeira pista para obter suas dimensões
pista = pygame.image.load(f'track_1.png')
largura_pista, altura_pista = pista.get_size()

# Configurar a janela para ser igual ao tamanho da pista
janela = pygame.display.set_mode((largura_pista, altura_pista))
pygame.display.set_caption("MinhaCorrida - [Espaço] para alternar dia/noite")

centro_tela = pygame.Vector2(largura_pista // 2, altura_pista // 2)

sombra = shader(janela)
sombra.setup((7, 7, 7))

modo_noite = 1
pistas = []
contador_pistas = 1

# Carregar pistas
while True:    
    try:
        pistas.append(pygame.image.load(f'track_{contador_pistas}.png'))
    except:
        break
    contador_pistas += 1

# Cores para detecção
cor_rua = (100, 100, 100, 255)
cor_cerca = (255, 5, 5, 255)
cor_chegada = (255, 255, 5, 255)
cor_branca = (255, 255, 255)

# Função para encontrar o ponto branco (ponto de início)
def encontrar_ponto_branco(pista):
    largura, altura = pista.get_size()
    for y in range(altura):
        for x in range(largura):
            cor = pista.get_at((x, y))
            if cor[:3] == cor_branca:  # Verifica se o pixel é branco (ignora a transparência)
                return pygame.Vector2(x, y)
    return pygame.Vector2(100, 165)  # Valor padrão se não encontrar nenhum ponto branco

indice_pista = 0

# Jogador 1
jogador = pygame.Rect(100, 165, 20, 20)
carro_original = pygame.image.load("car_1.png").convert_alpha()
img_jogador = pygame.transform.scale(carro_original, (40, 20))
explosao = pygame.image.load("explosion.png")

# Estado jogador
frente = tras = esquerda = direita = False
velocidade = 0
angulo = 0
explodiu = 0
contador_explosao = 0

velocidade_max = 10
alteracao_angulo = 0.5

# Temporizador
inicio_tempo = None
tempo_decorrido = 0
tempos_melhores = []

relogio = pygame.time.Clock()
fps = 50

# Luz
luz = light(sombra, "images/light2_2.png")

# Fonte para o velocímetro e o tempo
fonte = pygame.font.Font(None, 36)

executando = True
while executando:
    pos_jogador = pygame.Vector2(jogador.center)
    camera_offset = pos_jogador - centro_tela
    if contador_explosao == 1:
        jogador.left, jogador.top = 100, 165

    if contador_explosao == 0:
        if frente and velocidade < velocidade_max:
            velocidade += 0.25
        if tras:
            velocidade -= 0.25

        if esquerda and abs(velocidade) > 2:
            angulo -= alteracao_angulo * velocidade
        if direita and abs(velocidade) > 2:
            angulo += alteracao_angulo * velocidade

        if not frente and velocidade > 0:
            velocidade -= 0.25
        if not tras and velocidade < 0:
            velocidade += 0.25

        desloc_x = math.cos(math.radians(angulo)) * velocidade
        desloc_y = math.sin(math.radians(angulo)) * velocidade

        jogador.left += round(desloc_x)
        jogador.top += round(desloc_y)

        imagem_rotacionada = pygame.transform.rotate(img_jogador, -angulo)
    else:
        contador_explosao -= 1

    # Iniciar o temporizador quando o jogo começar
    if inicio_tempo is None:
        inicio_tempo = time.time()

    # Atualizar o tempo decorrido
    if inicio_tempo:
        tempo_decorrido = time.time() - inicio_tempo

    for evento in pygame.event.get():
        if evento.type == QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
            executando = False

        elif evento.type == KEYDOWN:
            if evento.key == K_RETURN:
                indice_pista = (indice_pista + 1) % len(pistas)
                # Atualiza a posição do carro para o ponto branco da pista
                ponto_inicial = encontrar_ponto_branco(pistas[indice_pista])
                jogador.left, jogador.top = ponto_inicial.x, ponto_inicial.y
                angulo = 0
                # Resetar o temporizador
                inicio_tempo = time.time()

            elif evento.key == K_SPACE:
                modo_noite *= -1

            elif evento.key == K_UP:
                frente = True
            elif evento.key == K_DOWN:
                tras = True
            elif evento.key == K_LEFT:
                esquerda = True
            elif evento.key == K_RIGHT:
                direita = True

        elif evento.type == KEYUP:
            if evento.key == K_UP:
                frente = False
            elif evento.key == K_DOWN:
                tras = False
            elif evento.key == K_LEFT:
                esquerda = False
            elif evento.key == K_RIGHT:
                direita = False

    # Desenhar pista com deslocamento inverso
    janela.fill((0, 0, 0))
    janela.blit(pistas[indice_pista], (-camera_offset.x, -camera_offset.y))

    # Jogador sempre no centro da tela
    if contador_explosao == 0 and not explodiu:
        janela.blit(imagem_rotacionada, imagem_rotacionada.get_rect(center=centro_tela))
    else:
        janela.blit(explosao, explosao.get_rect(center=centro_tela))

    # Colisão
    if contador_explosao == 0:
        try:
            pos_colisao = jogador.left + 10, jogador.top + 10
            try:
                cor = pistas[indice_pista].get_at(pos_colisao)
            except IndexError:
                cor = (0, 0, 0, 255)
            if cor != cor_rua:
                if velocidade > 3: velocidade = 2
                if velocidade < -3: velocidade = -2

            if cor == cor_cerca or cor == cor_chegada:
                explodiu = 1
                # Salvar o tempo quando o carro bater
                tempos_melhores.append(tempo_decorrido)
                tempos_melhores.sort()
                tempos_melhores = tempos_melhores[:3]  # Mantém os 3 melhores tempos
                inicio_tempo = None  # Reset do temporizador
        except:
            explodiu = 1

    # Atualizar luz
    luz.setup(luz.pos, 360 - angulo)
    luz.rect.center = centro_tela  # luz foca onde o carro está na tela (no centro)
    if modo_noite > 0:
        sombra.render(luz)

    if explodiu:
        janela.blit(explosao, jogador)
        pygame.display.update()
        explodiu = 0
        angulo = 0
        contador_explosao = 25

    # Desenhar o velocímetro
    texto_velocidade = fonte.render(f"Velocidade: {int(velocidade)} km/h", True, (255, 0, 0))
    janela.blit(texto_velocidade, (largura_pista - 200, 10))

    # Exibir os melhores tempos
    for i, tempo in enumerate(tempos_melhores):
        texto_tempo = fonte.render(f"Melhor {i+1}: {tempo:.2f} s", True, (255, 255, 0))
        janela.blit(texto_tempo, (10, 10 + i * 40))

    pygame.display.update()
    relogio.tick(fps)

pygame.quit()
