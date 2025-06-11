# Sistema de Roteamento de Ambulâncias – Maricá

## Propósito
Este projeto demonstra, de forma didática, como usar o **Algoritmo de Dijkstra** para encontrar a rota mais rápida entre um hospital e um local de ocorrência, simulando tanto **ida quanto retorno** da ambulância em um mapa simplificado da cidade de **Maricá (RJ)**. 

## Visão geral do funcionamento
1. **Construção do grafo** – cada ponto de interesse (hospitais, ruas, praças) vira um **vértice** e cada ligação vira uma **aresta** com peso (tempo/distância) gerado aleatoriamente ou calibrado pelo usuário.
2. **Interface gráfica** – uma pequena GUI em **Tkinter** permite escolher o hospital de origem e o ponto da ocorrência.
3. **Cálculo de rotas** – o algoritmo é executado duas vezes (ida e volta), retornando: caminho, tempos parciais e tempo total.
4. **Visualização animada** – uma animação em **Matplotlib** exibe o mapa (imagem `mapa_marica.png`) e destaca graficamente o progresso da ambulância.

## Requisitos de sistema
- **Python ≥ 3.10** (testado com 3.12)
- Sistema operacional: Windows, macOS ou Linux.

### Bibliotecas Python necessárias
| Biblioteca | Instalação | Função |
|------------|------------|--------|
| `networkx` | `pip install networkx` | Estrutura de grafo |
| `matplotlib` | `pip install matplotlib` | Visualização & animação |
| `pillow` | `pip install pillow` | Carregamento da imagem do mapa |
| `tkinter` | embutido na distribuição standard do Python (em Linux pode requerer `python3-tk`) | Interface gráfica |

Arquivo _recomendado_ `requirements.txt`:
```
networkx>=3.0
matplotlib>=3.8
pillow>=10.0
```

## Instalação passo‑a‑passo
```bash
# 1) clone ou baixe este repositório
$ git clone https://github.com/<seu-usuario>/ambulancia-marica.git
$ cd ambulancia-marica

# 2) crie ambiente virtual (opcional, mas recomendado)
$ python -m venv venv
$ source venv/bin/activate   # Windows: venv\Scripts\activate

# 3) instale dependências
(venv)$ pip install -r requirements.txt
```

## Como executar
1. **Garanta que** `mapa_marica.png` **está na mesma pasta** do script (ou ajuste o caminho no código).
2. Execute:
```bash
(venv)$ python ambulancia_marica.py
```
3. Na janela que se abrir, selecione:
   - **Hospital de origem** (verde, ponto de partida)
   - **Local da ocorrência** (azul‑claro)
4. Clique em **“Enviar Ambulância”**.

A animação abrirá em uma nova janela e exibirá um breve _count‑down_ antes de mostrar o trajeto.

## Interpretando a visualização
| Cor/Elemento | Significado |
|--------------|-------------|
| **Verde** | Hospitais existentes |
| **Azul‑claro** | Outros pontos do grafo |
| **Amarelo** | Posição atual da ambulância (estacionada) |
| **Círculo vermelho animado** | Ambulância em movimento |
| **Arestas vermelhas** | Segmentos já percorridos |
| Texto superior | Local atual, tempo estimado total e caminho restante |

O **tempo total** mostrado é a soma dos pesos das arestas (ida + volta). Para simulações mais realistas, ajuste os pesos para refletir distâncias reais ou estimativas de trânsito.

## Organização do código (versão única)
- **`Grafo`** – Classe que encapsula vértices, arestas e o algoritmo de Dijkstra.
- Interface **Tkinter** – Permite escolher parâmetros e exibe mensagens.
- Função **`animar_rota`** – Responsável por gerar a animação em Matplotlib.

Para dividir em módulos:
```
ambulancia_marica/
 ├── grafo.py          # classe Grafo
 ├── gui.py            # interface Tkinter
 ├── visualizacao.py   # animação & helpers
 ├── main.py           # ponto de entrada
 └── mapa_marica.png
```

## Personalizando
- **Adicionar vértices/arestas**: inclua o nome no array `locais` e chame `adicionar_aresta()` conforme necessário.
- **Pesos realistas**: substitua `peso_aleatorio()` por valores fixos ou cálculo dinâmico (ex.: API de trânsito).
- **Mapa**: substitua `mapa_marica.png` por outra imagem e ajuste o dicionário `pos` (coordenadas relativas).
- **Nova tecnologia**: existe um _branch_ em desenvolvimento que migra a visualização para **Pygame** mantendo o menu e tempo de animação.

## Autores
- Igor Barata
- Gabriel Teixeira

## Licença
Distribuído sob a **Licença MIT**. Sinta‑se livre para usar, modificar e distribuir, desde que preserve o aviso de copyright e a licença nos arquivos de origem.

> © 2025, Autores acima citados. Este software é fornecido “no estado em que se encontra”, sem garantia de qualquer tipo.

---

**Bom estudo e boas simulações!**