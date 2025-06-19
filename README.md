# 🏁 Car Game

Jogo **top-down** de corrida feito com **Pygame**.
Pilote seu carro por pistas labirínticas, evite cercas e marque o melhor tempo!

---

## ✨ Visão Geral

* **Objetivo:** completar cada pista no menor tempo possível.
* **Mecânica-chave:** colisões provocam explosão e reinício da volta.
* **Extras:** alternância **dia/noite** com shader de iluminação, ranking automático dos 3 melhores tempos.

---

## ⚙️ Requisitos

| Software | Versão mínima | Instalação           |
| -------- | ------------- | -------------------- |
| Python   | 3.8           | `python --version`   |
| Pygame   | 2.1           | `pip install pygame` |

---

## 📂 Estrutura de Pastas

```
cargamecg-main/
├─ images/
│  ├─ car_1.png          # sprite principal do carro
│  ├─ car_2.png          # sprite opcional (não usado)
│  ├─ light2_2.png       # máscara de luz (PNG c/ transparência)
│  └─ explosion.png      # sprite de explosão
├─ track_1.png … track_5.png  # cinco pistas labirínticas
├─ main_myrace.py        # loop principal do jogo
├─ shader.py             # sistema de sombra (fog)
└─ light.py              # iluminação dinâmica
```

---

## ▶️ Como Executar

```bash
cd cargamecg-main
python main_myrace.py
```

A janela abrirá no tamanho da pista atual.

---

## 🎮 Controles

| Tecla  | Ação                     |
| ------ | ------------------------ |
| ↑ / ↓  | Acelerar / Ré            |
| ← / →  | Girar esquerda / direita |
| Espaço | Alternar dia ⇄ noite     |
| Enter  | Próxima pista            |
| Esc    | Sair                     |

---

## 🛠️ Mecânicas Internas

| Sistema          | Descrição                                                                                                                                     | Arquivo(s)          |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| Movimentação     | Velocidade varia ±0.25 px/frame; posição = cos/sin(angle) × velocidade.                                                                       | main\_myrace.py     |
| Colisão          | Cor do pixel central do carro determina terreno:<br>- Cinza = asfalto<br>- Vermelho = cerca → explode<br>- Amarelo = chegada → registra tempo | main\_myrace.py     |
| Explosão & Reset | Exibe explosion.png por 25 frames, depois retorna ao ponto branco de spawn.                                                                   | main\_myrace.py     |
| Cronômetro       | Inicia na 1ª movimentação; mantém top-3 em `tempos_melhores`.                                                                                 | main\_myrace.py     |
| Iluminação       | `shader.py` cria fog multiplicativo; `light.py` renderiza máscara rotacionada pelo ângulo do carro.                                           | shader.py, light.py |

---

## ➕ Adicionando Novas Pistas

Desenhe um PNG com as cores-chave:

* **Verde** = grama
* **Cinza** = asfalto
* **Vermelho** = cerca
* **Amarelo** = chegada
* **Branco** = ponto de spawn

Salve como `track_6.png`, `track_7.png`, …

O loader detecta automaticamente qualquer arquivo numerado sequencialmente.

---

## 🌱 Ideias para Evolução

* Fantasma/Replay do melhor tempo ou modo 2 jogadores local.
* Obstáculos dinâmicos (tráfego, barreiras móveis).
* Áudio (motor, colisões, crowd).
* Menus completos e persistência dos recordes (JSON).
* Melhoria no spawn do veículo em cada pista.
* Melhoria no enquadramento para diferentes tamanhos de pista.
