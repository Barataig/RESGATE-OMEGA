# 🚑 Sistema de Roteamento de Ambulâncias - Maricá

Este projeto simula o envio de ambulâncias em uma cidade usando grafos e o algoritmo de Dijkstra para encontrar a rota mais rápida entre um hospital e um local de ocorrência. A interface é construída com `Tkinter`, e a animação do percurso é feita com `Matplotlib`.

---

## 📌 Funcionalidades

- Interface gráfica para seleção de hospital e local da ocorrência.
- Cálculo da rota mais rápida de ida e volta usando Dijkstra.
- Animação do percurso da ambulância sobre um mapa da cidade.
- Mensagens informativas sobre o tempo estimado e o caminho percorrido.

---

## 🛠️ Tecnologias e Bibliotecas

- Python 3
- `networkx` – para estrutura de grafo
- `matplotlib` – para visualização e animação do mapa
- `tkinter` – para interface gráfica
- `heapq`, `random` – bibliotecas padrão do Python

---

## 📦 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

3. Instale as dependências:

As seguintes bibliotecas precisam estar instaladas:
```bash
pip install matplotlib
pip install networkx
```
### ⚠️ Outras bibliotecas usadas

Estas já fazem parte da instalação padrão do Python:

- `heapq`
- `random`
- `tkinter` (pode precisar ser instalado separadamente no Linux)

4. **Adicione o arquivo `mapa_marica.png`** à pasta do projeto. Este arquivo é necessário para a visualização do mapa.

---

## ▶️ Como Executar

Execute o script principal:

```bash
python nome_do_arquivo.py
```

A interface gráfica será aberta. Escolha um hospital e um local de ocorrência para iniciar o envio da ambulância.

---

## 🧠 Lógica do Sistema

- A cidade é modelada como um grafo com vértices (locais) e arestas (ruas com tempo estimado aleatório).
- O algoritmo de Dijkstra é utilizado para calcular o caminho mais curto.
- A ambulância percorre o caminho de ida e volta e essa trajetória é animada em tempo real.
- A interface exibe o tempo estimado e a rota utilizada.

---

## 🗺️ Locais Modelados

- Praça Orlando de Barros Pimentel  
- RJ-106 (Rodovia Amaral Peixoto)  
- Rua Abreu Rangel  
- Hospital Conde Modesto Leal 🏥  
- Av. Roberto Silveira  
- UPA de Inoã 🏥  

---

## 📁 Estrutura do Projeto

```
├── mapa_marica.png         # Imagem usada como fundo do mapa
├── main.py                 # Código principal
├── requirements.txt        # Bibliotecas necessárias
└── README.md               # Este arquivo
```

---

## ✅ Requisitos

- Python 3.8 ou superior

---

## 📌 Observações

- Os pesos das arestas (tempos de deslocamento) são gerados aleatoriamente a cada execução.
- Se o arquivo `mapa_marica.png` não for encontrado, o programa exibirá um erro.

---

## 📜 Licença

Este projeto é livre para fins educacionais.