import heapq
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Grafo:
    def __init__(self):
        self.adjacencias = {}

    def adicionar_vertice(self, nome):
        if nome not in self.adjacencias:
            self.adjacencias[nome] = []

    def adicionar_aresta(self, origem, destino, peso):
        self.adjacencias[origem].append((destino, peso))
        self.adjacencias[destino].append((origem, peso))

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

    def animar_rota(self, ambulancia, hospitais, caminho, tempo_total):
        fig_contagem, ax_contagem = plt.subplots(figsize=(6, 4))
        for i in range(3, 0, -1):
            ax_contagem.clear()
            ax_contagem.set_facecolor('white')
            ax_contagem.text(0.5, 0.5, str(i), transform=ax_contagem.transAxes,
                             fontsize=60, ha='center', va='center', color='red')
            ax_contagem.set_xticks([])
            ax_contagem.set_yticks([])
            plt.pause(1)
        plt.close(fig_contagem)

        G = nx.Graph()
        for origem, vizinhos in self.adjacencias.items():
            for destino, peso in vizinhos:
                if not G.has_edge(origem, destino):
                    G.add_edge(origem, destino, weight=peso)

        pos = nx.spring_layout(G, seed=42)
        pesos = nx.get_edge_attributes(G, 'weight')

        fig, ax = plt.subplots(figsize=(10, 7))

        def desenhar_mapa():
            ax.clear()
            cor_nos = []
            for no in G.nodes():
                if no == ambulancia:
                    cor_nos.append('yellow')
                elif no in hospitais:
                    cor_nos.append('green')
                else:
                    cor_nos.append('skyblue')

            nx.draw(G, pos, with_labels=True, node_color=cor_nos, node_size=1000, ax=ax, font_size=10)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, ax=ax)
            nx.draw_networkx_edges(G, pos, ax=ax)

        def atualizar(frame):
            desenhar_mapa()

            if frame < len(caminho):
                ponto = caminho[frame]
                x, y = pos[ponto]
                ax.plot(x, y, 'o', color='red', markersize=20, label='Ambulância')
                ax.legend(loc='upper left')

            if frame > 0:
                subcaminho = [(caminho[i], caminho[i+1]) for i in range(frame) if i+1 < len(caminho)]
                nx.draw_networkx_edges(G, pos, edgelist=subcaminho, edge_color='red', width=3, ax=ax)

            ax.set_title("Ambulância em movimento", fontsize=14)
            ax.text(0.02, 0.98, f"Destino: {caminho[-1]}", transform=ax.transAxes,
                    fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))
            ax.text(0.02, 0.93, f"Tempo estimado: {tempo_total} min", transform=ax.transAxes,
                    fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))
            ax.text(0.02, 0.88, f"Caminho: {' → '.join(caminho)}", transform=ax.transAxes,
                    fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))

        ani = animation.FuncAnimation(fig, atualizar, frames=len(caminho), interval=1000, repeat=False)
        plt.show()

# === CRIAÇÃO DO GRAFO COM NOMES REAIS ===
grafo = Grafo()

# Nomes de cruzamentos e hospitais
cruzamentos = [
    "Av. Brasil", "Rua das Flores", "Praça Central", 
    "Av. das Palmeiras", "Rua do Comércio", "Hospital Central"
]
for v in cruzamentos:
    grafo.adicionar_vertice(v)

# Adicionando ruas (arestas)
grafo.adicionar_aresta("Av. Brasil", "Rua das Flores", 4)
grafo.adicionar_aresta("Av. Brasil", "Praça Central", 2)
grafo.adicionar_aresta("Rua das Flores", "Praça Central", 1)
grafo.adicionar_aresta("Rua das Flores", "Av. das Palmeiras", 5)
grafo.adicionar_aresta("Praça Central", "Av. das Palmeiras", 8)
grafo.adicionar_aresta("Praça Central", "Rua do Comércio", 10)
grafo.adicionar_aresta("Av. das Palmeiras", "Rua do Comércio", 2)
grafo.adicionar_aresta("Rua do Comércio", "Hospital Central", 3)

ambulancia = "Av. Brasil"
hospitais = ["Hospital Central", "Av. das Palmeiras"]

hospital, tempo, caminho = grafo.encontrar_hospital_mais_proximo(ambulancia, hospitais)

# Anima a rota com as informações na tela
grafo.animar_rota(ambulancia, hospitais, caminho, tempo)
