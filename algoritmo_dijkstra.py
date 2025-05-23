import heapq  # Biblioteca para usar fila de prioridade (mínimo primeiro)

def dijkstra(grafo, inicio):
    # Inicializa todas as distâncias com infinito
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0  # A distância até o nó de início é zero

    anteriores = {no: None for no in grafo}  # Armazena o caminho mais curto
    fila = [(0, inicio)]  # Fila de prioridade com (distância, nó)

    while fila:
        distancia_atual, no_atual = heapq.heappop(fila)  # Pega o nó com menor distância

        # Se a distância atual for maior que a armazenada, ignora
        if distancia_atual > distancias[no_atual]:
            continue

        # Para cada vizinho do nó atual
        for vizinho, peso in grafo[no_atual]:
            nova_distancia = distancia_atual + peso  # Calcula a nova distância

            # Se essa nova distância for menor, atualiza
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = no_atual
                heapq.heappush(fila, (nova_distancia, vizinho))  # Adiciona à fila

    return distancias, anteriores  # Retorna os menores caminhos e os predecessores

def reconstruir_caminho(anteriores, destino):
    caminho = []
    while destino:
        caminho.insert(0, destino)  # Insere no início da lista
        destino = anteriores[destino]  # Vai para o nó anterior
    return caminho

def encontrar_hospital_mais_proximo(grafo, pos_ambulancia, hospitais):
    # Executa o Dijkstra a partir da posição da ambulância
    distancias, anteriores = dijkstra(grafo, pos_ambulancia)

    hospital_mais_proximo = None
    menor_tempo = float('inf')
    melhor_caminho = []

    # Verifica qual hospital tem o menor tempo
    for hospital in hospitais:
        if distancias[hospital] < menor_tempo:
            menor_tempo = distancias[hospital]
            hospital_mais_proximo = hospital
            melhor_caminho = reconstruir_caminho(anteriores, hospital)

    return hospital_mais_proximo, menor_tempo, melhor_caminho

# Grafo: nó -> [(vizinho, tempo)]
grafo_urbano = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2), ('F', 3)],
    'F': [('E', 3)]
}

hospitais = ['D', 'F']
pos_ambulancia = 'A'

hospital, tempo, caminho = encontrar_hospital_mais_proximo(grafo_urbano, pos_ambulancia, hospitais)

print(f"Hospital mais próximo: {hospital}")
print(f"Tempo estimado: {tempo} minutos")
print(f"Caminho: {' -> '.join(caminho)}")
