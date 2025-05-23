import matplotlib.pyplot as plt
import networkx as nx

# Criar grafo vazio
G = nx.Graph()

# Dicionário com tipos de cada ponto
tipos_de_nos = {
    "Hospital Conde Modesto Leal": "hospital",
    "82ª Delegacia de Polícia": "delegacia",
    "Base de Ambulância Centro": "ambulancia",
    "Praça Orlando de Barros Pimentel": "praça",
    "Praça Conselheiro Macedo Soares": "praça",
    "Rua Álvares de Castro": "rua",
    "Rua Abreu Rangel": "rua",
    "Avenida Roberto Silveira": "rua",
    "Rua Clímaco Pereira": "rua",
    "Rua Domício da Gama": "rua",
    "Rua Ribeiro de Almeida": "rua",
    "Rua Carlos Rangel": "rua",
    "Rua Nossa Senhora do Amparo": "rua"
}

# Lista de arestas com tempo estimado
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

# Adiciona os nós ao grafo
for no in tipos_de_nos:
    G.add_node(no, tipo=tipos_de_nos[no])

# Adiciona as arestas com pesos
for origem, destino, peso in arestas:
    G.add_edge(origem, destino, weight=peso)

# Layout fixo para visual bonito
pos = nx.spring_layout(G, seed=42)

# Função para desenhar nós com formas diferentes
def desenhar_forma_por_tipo(tipo, forma, cor):
    nos_do_tipo = [n for n, attr in G.nodes(data=True) if attr['tipo'] == tipo]
    nx.draw_networkx_nodes(G, pos, nodelist=nos_do_tipo, node_shape=forma, node_color=cor, label=tipo, node_size=1500)

# Desenhar cada tipo de nó
desenhar_forma_por_tipo("hospital", "s", "skyblue")        # quadrado
desenhar_forma_por_tipo("delegacia", "^", "tomato")        # triângulo
desenhar_forma_por_tipo("ambulancia", "D", "limegreen")    # losango
desenhar_forma_por_tipo("praça", "o", "lightgrey")         # círculo
desenhar_forma_por_tipo("rua", "o", "lightgrey")           # círculo

# Desenhar as arestas
nx.draw_networkx_edges(G, pos, width=1.5)
# Rótulo das arestas com pesos
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Rótulos dos nós
nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")

# Título e ajustes finais
plt.title("Grafo do Centro de Maricá - Sistema de Rotas de Emergência", fontsize=12)
plt.axis('off')
plt.legend(scatterpoints=1, fontsize=8)
plt.tight_layout()
plt.show()
