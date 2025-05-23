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

            if frame < len(caminho):
                ponto = caminho[frame]
                x, y = pos[ponto]
                ax.plot(x, y, 'o', color='red', markersize=20, label='Ambulância')

            if frame > 0:
                subcaminho = [(caminho[i], caminho[i+1]) for i in range(frame) if i+1 < len(caminho)]
                nx.draw_networkx_edges(G, pos, edgelist=subcaminho, edge_color='red', width=3, ax=ax)

            info_linha1 = f"🚑 Local atual: {caminho[frame] if frame < len(caminho) else caminho[-1]}"
            info_linha2 = f"🕒 Tempo estimado: {tempo_total} min"
            info_linha3 = f"📍 Caminho restante: {' → '.join(caminho[frame:]) if frame < len(caminho) else 'Chegou ao destino'}"

            ax.text(0.5, -0.15, info_linha1 + ' | ' + info_linha2 + ' | ' + info_linha3,
                    transform=ax.transAxes, fontsize=12, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))

        ani = animation.FuncAnimation(fig, atualizar, frames=len(caminho), interval=1000, repeat=False)
        plt.show()


# Criar grafo com nomes reais
grafo = Grafo()

# Adicionando locais (cruzamentos e hospitais)
locais = ['Praça Central', 'Av. Rio Branco', 'Rua das Flores', 'Hospital Municipal', 'Av. Paulista', 'Hospital da Zona Sul']
for local in locais:
    grafo.adicionar_vertice(local)

# Adicionando ruas com tempos médios (em minutos)
grafo.adicionar_aresta('Praça Central', 'Av. Rio Branco', 4)
grafo.adicionar_aresta('Praça Central', 'Rua das Flores', 2)
grafo.adicionar_aresta('Av. Rio Branco', 'Rua das Flores', 1)
grafo.adicionar_aresta('Av. Rio Branco', 'Hospital Municipal', 5)
grafo.adicionar_aresta('Rua das Flores', 'Hospital Municipal', 8)
grafo.adicionar_aresta('Rua das Flores', 'Av. Paulista', 10)
grafo.adicionar_aresta('Hospital Municipal', 'Av. Paulista', 2)
grafo.adicionar_aresta('Av. Paulista', 'Hospital da Zona Sul', 3)

ambulancia = 'Praça Central'
hospitais = ['Hospital Municipal', 'Hospital da Zona Sul']

# Calcular rota
hospital, tempo_total, caminho = grafo.encontrar_hospital_mais_proximo(ambulancia, hospitais)

print(f"Hospital mais próximo: {hospital}")
print(f"Tempo estimado: {tempo_total} minutos")
print(f"Caminho: {' -> '.join(caminho)}")

# Anima a rota
grafo.animar_rota(ambulancia, hospitais, caminho, tempo_total)
