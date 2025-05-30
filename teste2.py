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
        G = nx.Graph()
        for origem, vizinhos in self.adjacencias.items():
            for destino, peso in vizinhos:
                if not G.has_edge(origem, destino):
                    G.add_edge(origem, destino, weight=peso)

        pos = nx.spring_layout(G, seed=42)
        pesos = nx.get_edge_attributes(G, 'weight')

        fig, ax = plt.subplots(figsize=(10, 8))
        fig.subplots_adjust(bottom=0.25)

        def desenhar_mapa():
            ax.clear()
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
            ax.text(0.5, 0.5, str(i), transform=ax.transAxes,
                    fontsize=40, ha='center', va='center', color='red')
            plt.pause(1)


        def atualizar(frame):
            desenhar_mapa()

            # Arestas percorridas até o momento
            if frame > 0:
                subcaminho = [(caminho[i], caminho[i+1]) for i in range(frame) if i+1 < len(caminho)]
                nx.draw_networkx_edges(G, pos, edgelist=subcaminho, edge_color='red', width=3, ax=ax)

            # Nó atual da ambulância
            if frame < len(caminho):
                ponto = caminho[frame]
                x, y = pos[ponto]
                ax.plot(x, y, 's', color='darkblue', markersize=20, label='Ambulância')

            # Legenda no topo com fundo branco
            info_linha1 = f"Local atual: {caminho[frame] if frame < len(caminho) else caminho[-1]}"
            info_linha2 = f"Tempo estimado: {tempo_total} minutos"
            info_linha3 = f"Caminho restante: {' → '.join(caminho[frame:]) if frame < len(caminho) else 'Chegou ao destino'}"

            ax.text(0.5, 1.08, info_linha1, transform=ax.transAxes,
                    fontsize=12, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))
            ax.text(0.5, 1.03, info_linha2, transform=ax.transAxes,
                    fontsize=11, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))
            ax.text(0.5, 0.98, info_linha3, transform=ax.transAxes,
                    fontsize=10, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))

        ani = animation.FuncAnimation(fig, atualizar, frames=len(caminho), interval=100, repeat=False)
        plt.show()


# Criar grafo com nomes reais
grafo = Grafo()

# Adicionando locais reais de Maricá
locais = [
    'Praça Orlando de Barros Pimentel',
    'RJ-106 (Rodovia Amaral Peixoto)',
    'Rua Abreu Rangel',
    'Hospital Conde Modesto Leal',
    'Av. Roberto Silveira',
    'UPA de Inoã'
]

for local in locais:
    grafo.adicionar_vertice(local)

# Adicionando ruas com tempos médios (em minutos)
grafo.adicionar_aresta('Praça Orlando de Barros Pimentel', 'RJ-106 (Rodovia Amaral Peixoto)', 4)
grafo.adicionar_aresta('Praça Orlando de Barros Pimentel', 'Rua Abreu Rangel', 2)
grafo.adicionar_aresta('RJ-106 (Rodovia Amaral Peixoto)', 'Rua Abreu Rangel', 1)
grafo.adicionar_aresta('RJ-106 (Rodovia Amaral Peixoto)', 'Hospital Conde Modesto Leal', 5)
grafo.adicionar_aresta('Rua Abreu Rangel', 'Hospital Conde Modesto Leal', 8)
grafo.adicionar_aresta('Rua Abreu Rangel', 'Av. Roberto Silveira', 10)
grafo.adicionar_aresta('Hospital Conde Modesto Leal', 'Av. Roberto Silveira', 2)
grafo.adicionar_aresta('Av. Roberto Silveira', 'UPA de Inoã', 3)

ambulancia = 'Praça Orlando de Barros Pimentel'
hospitais = ['Hospital Conde Modesto Leal', 'UPA de Inoã']


# Calcular rota
hospital, tempo_total, caminho = grafo.encontrar_hospital_mais_proximo(ambulancia, hospitais)

print(f"Hospital mais próximo: {hospital}")
print(f"Tempo estimado: {tempo_total} minutos")
print(f"Caminho: {' -> '.join(caminho)}")

# Anima a rota
grafo.animar_rota(ambulancia, hospitais, caminho, tempo_total)
