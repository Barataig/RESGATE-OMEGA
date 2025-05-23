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

    def animar_rota(self, ambulancia, hospitais, caminho):
        G = nx.Graph()
        for origem, vizinhos in self.adjacencias.items():
            for destino, peso in vizinhos:
                if not G.has_edge(origem, destino):
                    G.add_edge(origem, destino, weight=peso)

        pos = nx.spring_layout(G, seed=42)
        pesos = nx.get_edge_attributes(G, 'weight')

        fig, ax = plt.subplots(figsize=(8, 6))

        def desenhar_mapa():
            ax.clear()
            # Cor dos nós
            cor_nos = []
            for no in G.nodes():
                if no == ambulancia:
                    cor_nos.append('yellow')
                elif no in hospitais:
                    cor_nos.append('green')
                else:
                    cor_nos.append('lightblue')

            nx.draw(G, pos, with_labels=True, node_color=cor_nos, node_size=800, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, ax=ax)
            nx.draw_networkx_edges(G, pos, ax=ax)

        # Contagem regressiva
        for i in range(3, 0, -1):
            ax.clear()
            desenhar_mapa()
            ax.text(0.5, 0.5, str(i), transform=ax.transAxes,
                    fontsize=40, ha='center', va='center', color='red')
            plt.pause(1)

        # Animação do ponto (ambulância) no caminho
        def atualizar(frame):
            ax.clear()
            desenhar_mapa()

            # Desenha a ambulância no ponto atual do caminho
            if frame < len(caminho):
                ponto = caminho[frame]
                x, y = pos[ponto]
                ax.plot(x, y, 'o', color='red', markersize=20, label='Ambulância')
                ax.legend(loc='upper left')

            # Destacar caminho já percorrido
            if frame > 0:
                subcaminho = [(caminho[i], caminho[i+1]) for i in range(frame) if i+1 < len(caminho)]
                nx.draw_networkx_edges(G, pos, edgelist=subcaminho, edge_color='red', width=3, ax=ax)

            ax.set_title("Ambulância em movimento")

        ani = animation.FuncAnimation(fig, atualizar, frames=len(caminho), interval=1000, repeat=False)
        plt.show()

grafo = Grafo()

# Adicionando cruzamentos
for v in ['A', 'B', 'C', 'D', 'E', 'F']:
    grafo.adicionar_vertice(v)

# Adicionando ruas
grafo.adicionar_aresta('A', 'B', 4)
grafo.adicionar_aresta('A', 'C', 2)
grafo.adicionar_aresta('B', 'C', 1)
grafo.adicionar_aresta('B', 'D', 5)
grafo.adicionar_aresta('C', 'D', 8)
grafo.adicionar_aresta('C', 'E', 10)
grafo.adicionar_aresta('D', 'E', 2)
grafo.adicionar_aresta('E', 'F', 3)

ambulancia = 'A'
hospitais = ['D', 'F']

# Calcula o caminho
hospital, tempo, caminho = grafo.encontrar_hospital_mais_proximo(ambulancia, hospitais)

print(f"Hospital mais próximo: {hospital}")
print(f"Tempo estimado: {tempo} minutos")
print(f"Caminho: {' -> '.join(caminho)}")

# Anima a rota
grafo.animar_rota(ambulancia, hospitais, caminho)
