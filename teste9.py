import heapq
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import tkinter as tk
from tkinter import ttk, messagebox

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

    def animar_rota(self, ambulancia, hospitais, caminho, tempo_total):
        G = nx.Graph()
        for origem, vizinhos in self.adjacencias.items():
            for destino, peso in vizinhos:
                if not G.has_edge(origem, destino):
                    G.add_edge(origem, destino, weight=peso)

        pos = {
            'Praça Orlando de Barros Pimentel': (0.55, 0.64),
            'RJ-106 (Rodovia Amaral Peixoto)': (3.50, 1.75),
            'Rua Abreu Rangel': (0.34, -0.83),
            'Hospital Conde Modesto Leal': (5.30, 1.40),
            'Av. Roberto Silveira': (3.50, 0.24),
            'UPA de Inoã': (1.50, -1.70)
        }

        pesos = nx.get_edge_attributes(G, 'weight')

        fig, ax = plt.subplots(figsize=(10, 8))
        fig.subplots_adjust(bottom=0.25)

        try:
            imagem_mapa = plt.imread("mapa_marica.png")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo 'mapa_marica.png' não encontrado. Coloque a imagem na mesma pasta do script.")
            return

        extensao = [-1, 7, -3, 3]

        def desenhar_mapa():
            ax.clear()
            ax.imshow(imagem_mapa, extent=extensao, aspect='auto', zorder=0)
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

        for i in range(3, 0, -1):
            ax.clear()
            ax.text(0.5, 0.5, str(i), transform=ax.transAxes,
                    fontsize=50, ha='center', va='center', color='red')
            plt.pause(1)

        def atualizar(frame):
            desenhar_mapa()

            if frame > 0:
                subcaminho = [(caminho[i], caminho[i+1]) for i in range(frame) if i+1 < len(caminho)]
                nx.draw_networkx_edges(G, pos, edgelist=subcaminho, edge_color='red', width=3, ax=ax)

            if frame < len(caminho):
                ponto = caminho[frame]
                x, y = pos[ponto]
                circulo_externo = mpatches.Circle((x, y), 0.1, color='red', zorder=10)
                ax.add_patch(circulo_externo)

            info_linha1 = f"Local atual: {caminho[frame] if frame < len(caminho) else caminho[-1]}"
            info_linha2 = f"Tempo estimado: {tempo_total} minutos"
            info_linha3 = f"Caminho restante: {' → '.join(caminho[frame:]) if frame < len(caminho) else 'Chegou ao destino'}"

            ax.text(0.5, 1.08, info_linha1, transform=ax.transAxes,
                    fontsize=12, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))
            ax.text(0.5, 1.01, info_linha2, transform=ax.transAxes,
                    fontsize=12, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))
            ax.text(0.5, 0.94, info_linha3, transform=ax.transAxes,
                    fontsize=11, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8))

        ani = animation.FuncAnimation(fig, atualizar, frames=len(caminho), interval=2100, repeat=False)
        plt.show()


def peso_aleatorio():
    return random.randint(1, 10)


# Construção do grafo

grafo = Grafo()
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

grafo.adicionar_aresta('Praça Orlando de Barros Pimentel', 'RJ-106 (Rodovia Amaral Peixoto)', peso_aleatorio())
grafo.adicionar_aresta('Praça Orlando de Barros Pimentel', 'Rua Abreu Rangel', peso_aleatorio())
grafo.adicionar_aresta('RJ-106 (Rodovia Amaral Peixoto)', 'Rua Abreu Rangel', peso_aleatorio())
grafo.adicionar_aresta('RJ-106 (Rodovia Amaral Peixoto)', 'Hospital Conde Modesto Leal', peso_aleatorio())
grafo.adicionar_aresta('Rua Abreu Rangel', 'Hospital Conde Modesto Leal', peso_aleatorio())
grafo.adicionar_aresta('Rua Abreu Rangel', 'Av. Roberto Silveira', peso_aleatorio())
grafo.adicionar_aresta('Hospital Conde Modesto Leal', 'Av. Roberto Silveira', peso_aleatorio())
grafo.adicionar_aresta('Av. Roberto Silveira', 'UPA de Inoã', peso_aleatorio())

# Interface Tkinter

hospitais = ['Hospital Conde Modesto Leal', 'UPA de Inoã']

root = tk.Tk()
root.title("Sistema de Ambulância - Maricá")
root.geometry("500x300")

ttk.Label(root, text="Selecione o hospital de origem:").pack(pady=5)
combobox_hospital = ttk.Combobox(root, values=hospitais, state="readonly")
combobox_hospital.pack(pady=5)

ttk.Label(root, text="Selecione o local da ocorrência:").pack(pady=5)
locais_ocorrencia = [l for l in locais if l not in hospitais]
combobox_ocorrencia = ttk.Combobox(root, values=locais_ocorrencia, state="readonly")
combobox_ocorrencia.pack(pady=5)

def enviar_ambulancia():
    hospital = combobox_hospital.get()
    destino = combobox_ocorrencia.get()

    if not hospital or not destino:
        messagebox.showwarning("Atenção", "Selecione o hospital de origem e o local da ocorrência.")
        return

    if hospital == destino:
        messagebox.showerror("Erro", "O hospital e o local da ocorrência devem ser diferentes.")
        return

    _, anteriores_ida = grafo.dijkstra(hospital)
    caminho_ida = grafo.reconstruir_caminho(anteriores_ida, destino)
    tempo_ida = sum(peso for u, v in zip(caminho_ida, caminho_ida[1:]) 
                    for w, peso in grafo.adjacencias[u] if w == v)

    _, anteriores_volta = grafo.dijkstra(destino)
    caminho_volta = grafo.reconstruir_caminho(anteriores_volta, hospital)
    tempo_volta = sum(peso for u, v in zip(caminho_volta, caminho_volta[1:]) 
                      for w, peso in grafo.adjacencias[u] if w == v)

    caminho_total = caminho_ida + caminho_volta[1:]
    tempo_total = tempo_ida + tempo_volta

    rota_str = " -> ".join(caminho_total)
    messagebox.showinfo("Rota Calculada",
                        f"Hospital: {hospital}\nOcorrência: {destino}\n"
                        f"Tempo ida: {tempo_ida} min\nTempo volta: {tempo_volta} min\n"
                        f"Tempo total: {tempo_total} min\nRota: {rota_str}")

    grafo.animar_rota(hospital, hospitais, caminho_total, tempo_total)

btn = ttk.Button(root, text="Enviar Ambulância", command=enviar_ambulancia)
btn.pack(pady=20)

root.mainloop()
