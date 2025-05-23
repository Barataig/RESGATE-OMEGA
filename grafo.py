import networkx as nx
import matplotlib.pyplot as plt

#Criar o grafo direcionado,
G = nx.Graph()

#Adicionar as arestas e pesos,
arestas = [
    ("Base de Ambulância Centro", "Rua Álvares de Castro", 2),
    ("Base de Ambulância Centro", "Rua Carlos Rangel", 3),
    ("Hospital Conde Modesto Leal", "Praça Orlando de Barros Pimentel", 2),
    ("Hospital Conde Modesto Leal", "Rua Clímaco Pereira", 2),
    ("82ª Delegacia de Polícia", "Avenida Roberto Silveira", 3),
    ("Praça Orlando de Barros Pimentel", "Rua Álvares de Castro", 1),
    ("Praça Orlando de Barros Pimentel", "Rua Clímaco Pereira", 2),
    ("Praça Orlando de Barros Pimentel", "Rua Domício da Gama", 2),
    ("Praça Orlando de Barros Pimentel", "Praça Conselheiro Macedo Soares", 2),
    ("Rua Álvares de Castro", "Rua Abreu Rangel", 2),
    ("Rua Abreu Rangel", "Avenida Roberto Silveira", 1),
    ("Avenida Roberto Silveira", "Rua Ribeiro de Almeida", 2),
    ("Rua Clímaco Pereira", "Rua Nossa Senhora do Amparo", 1),
    ("Rua Domício da Gama", "Rua Carlos Rangel", 2),
    ("Rua Ribeiro de Almeida", "Praça Conselheiro Macedo Soares", 2),
    ("Rua Carlos Rangel", "Praça Conselheiro Macedo Soares", 2),
]

for origem, destino, peso in arestas:
    G.add_edge(origem, destino, weight=peso)

#Encontrar caminho mais curto com Dijkstra,
origem = "Base de Ambulância Centro"
destino = "Hospital Conde Modesto Leal"
caminho = nx.dijkstra_path(G, origem, destino, weight="weight")
tempo_total = nx.dijkstra_path_length(G, origem, destino, weight="weight")

print("Melhor caminho:", caminho)
print("Tempo estimado:", tempo_total, "minutos")

#Visualização,
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=8)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
plt.show()