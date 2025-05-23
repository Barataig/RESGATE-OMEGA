import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.adjacencias = {}

    def adicionar_vertice(self, nome):
        if nome not in self.adjacencias:
            self.adjacencias[nome] = []

    def adicionar_aresta(self, origem, destino, peso):
        self.adjacencias[origem].append((destino, peso))
        self.adjacencias[destino].append((origem, peso))  # Grafo não direcionado

    def dijkstra(self, inicio):
        distancias = {no: float('inf') for no in self.adjacencias}
        distancias[inicio] = 0
        anteriores = {no: None for no in self.adjacencias}
        fila = [(0, inicio)]

        while fila:
            distancia_atual, no_atual = heapq.heappop(fila)

            if distancia_atual > distancias[no_atual]:
                continue

            for vizinho, peso in self.adjacencias[no_atual]:
                nova_distancia = distancia_atual + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = no_atual
                    heapq.heappush(fila, (nova_distancia, vizinho))

        return distancias, anteriores

    def reconstruir_caminho(self, anteriores, destino):
        caminho = []
        while destino:
            caminho.insert(0, destino)
            destino = anteriores[destino]
        return caminho

    def encontrar_hospital_mais_proximo(self, pos_ambulancia, hospitais):
        distancias, anteriores = self.dijkstra(pos_ambulancia)

        hospital_mais_proximo = None
        menor_tempo = float('inf')
        melhor_caminho = []

        for hospital in hospitais:
            if distancias[hospital] < menor_tempo:
                menor_tempo = distancias[hospital]
                hospital_mais_proximo = hospital
                melhor_caminho = self.reconstruir_caminho(anteriores, hospital)

        return hospital_mais_proximo, menor_tempo, melhor_caminho

    def desenhar_grafo(self, ambulancia, hospitais, caminho):
        G = nx.Graph()

        # Adiciona nós e arestas no grafo do networkx
        for origem, vizinhos in self.adjacencias.items():
            for destino, peso in vizinhos:
                if not G.has_edge(origem, destino):
                    G.add_edge(origem, destino, weight=peso)

        pos = nx.spring_layout(G, seed=42)  # Layout dos nós (posição automática)
        pesos = nx.get_edge_attributes(G, 'weight')

        # Cores dos nós
        cor_nos = []
        for no in G.nodes():
            if no == ambulancia:
                cor_nos.append('orange')
            elif no in hospitais:
                cor_nos.append('green')
            else:
                cor_nos.append('lightblue')

        # Desenha o grafo
        nx.draw(G, pos, with_labels=True, node_color=cor_nos, node_size=800, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos)

        # Destacar o caminho mais curto
        if caminho and len(caminho) > 1:
            caminho_arestas = [(caminho[i], caminho[i + 1]) for i in range(len(caminho) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=caminho_arestas, edge_color='red', width=3)

        plt.title("Mapa da cidade com rota da ambulância")
        plt.show()

# Criando o grafo urbano
grafo = Grafo()

# Adicionando vértices
for v in ['A', 'B', 'C', 'D', 'E', 'F']:
    grafo.adicionar_vertice(v)

# Adicionando ruas (arestas) com tempos médios de percurso
grafo.adicionar_aresta('A', 'B', 4)
grafo.adicionar_aresta('A', 'C', 2)
grafo.adicionar_aresta('B', 'C', 1)
grafo.adicionar_aresta('B', 'D', 5)
grafo.adicionar_aresta('C', 'D', 8)
grafo.adicionar_aresta('C', 'E', 10)
grafo.adicionar_aresta('D', 'E', 2)
grafo.adicionar_aresta('E', 'F', 3)

# Definindo posição da ambulância e os hospitais
ambulancia = 'A'
hospitais = ['D', 'F']

# Encontrar hospital mais próximo
hospital, tempo, caminho = grafo.encontrar_hospital_mais_proximo(ambulancia, hospitais)

# Mostrar resultados
print(f"Hospital mais próximo: {hospital}")
print(f"Tempo estimado: {tempo} minutos")
print(f"Caminho: {' -> '.join(caminho)}")

# Desenhar o grafo com destaque da rota
grafo.desenhar_grafo(ambulancia, hospitais, caminho)
