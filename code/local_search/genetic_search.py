from abc import ABC
import random as rd

# OBS: Uma pequena parcela do código foi feito utilizando IA,
#      principalmente na função "main".

class GAInterface(ABC):
    """
    Contrato para a implementação do algoritmo de busca genética.
    """
    def _calc_fitness(
            self, 
            subject: list[int], 
            dist_matrix: list[list[int]]
    ) -> float:
        pass

    def _select(
            self,
            population: list[list[int]],
            fitness_scores: list[float]
    ) -> list[int]:
        pass

    def _crossover(
            self,
            parent1: list[int],
            parent2: list[int]
    ) -> list[int]:
        pass

    def _mutate(
            self,
            child: list[int]
    ) -> list[int]:
        pass

    def recieve_parameters(
            self,
            num_districts: int,
            truck_cap: int,
            collection_volume: list[int]
    ) -> None:
        pass

    def search(self, dist_matrix: list[list[int]]) -> None:
        pass

class GeneticAlgorithm(GAInterface):
    def __init__(
            self,
            population_size: int,
            max_generations: int,
            mutation_rate: float
    ):
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate

        rd.seed(42)

    def _calc_fitness(
            self, 
            subject: list[int], 
            dist_matrix: list[list[int]]
    ) -> float:
        total_dist = 0
        current_load = 0
        trips = 1
        penalty = 0

        for i in range(len(subject)):
            current_gene = subject[i]
            # Se for o separador (-1), o caminhão voltou para descarregar
            if current_gene == -1:
                trips += 1
                current_load = 0
                continue
            current_load += self.collection_volume[current_gene]
            
            # Penalidade 1: Capacidade do caminhão excedida
            if current_load > self.truck_cap:
                penalty += 1000
                
            # Calcula a distância para o próximo bairro (ignorando o -1 como destino físico)
            if i < len(subject) - 1:
                next_gene = subject[i+1]
                if next_gene != -1:
                    total_dist += dist_matrix[current_gene][next_gene]

        # Penalidade 2: Número excessivo de viagens (sabemos que o mínimo são 3)
        if trips > 3:
            penalty += 500 * (trips - 3)
        return total_dist + penalty

    def _select(
            self,
            population: list[list[int]],
            fitness_scores: list[float]
    ) -> list[int]:
        """
        Aplicação de roleta
        """
        inverted_fitness = [1.0 / (f + 1e-6) for f in fitness_scores] 
        total_inverted_fitness = sum(inverted_fitness)
        
        pick = rd.uniform(0, total_inverted_fitness)
        current = 0
        
        for i, ind in enumerate(population):
            current += inverted_fitness[i]
            if current >= pick:
                return ind   
        return population[-1]

    def _crossover(
            self,
            parent1: list[int],
            parent2: list[int]
    ) -> list[int]:
        """
        Crossover de 1 Ponto
        """
        if len(parent1) < 2: return parent1.copy()
        cut_point = rd.randint(1, len(parent1) - 2)
        
        child = parent1[:cut_point]
        
        # Conta quantos separadores (-1) precisamos no total e quantos já temos
        target_separators = parent1.count(-1)
        current_separators = child.count(-1)
        
        for gene in parent2:
            if gene == -1:
                if current_separators < target_separators:
                    child.append(gene)
                    current_separators += 1
            elif gene not in child:
                child.append(gene)
        return child

    def _mutate(
            self,
            child: list[int]
    ) -> list[int]:
        """
        Mutação Swap Simples.
        """
        if rd.random() < self.mutation_rate:
            # Sorteia dois índices aleatórios no cromossomo
            idx1, idx2 = rd.sample(range(len(child)), 2)
            child[idx1], child[idx2] = child[idx2], child[idx1]
        return child

    def recieve_parameters(
            self,
            num_districts: int,
            truck_cap: int,
            collection_volume: list[int]
    ) -> None:
        self.num_districts = num_districts
        self.truck_cap = truck_cap
        self.collection_volume = collection_volume
        self.total_volume: list[float] = sum(collection_volume)

    def search(
            self,
            dist_matrix: list[list[int]]
    ) -> None:
        population = []
        for _ in range(self.population_size):
            shuffled_districts = (rd.sample(range(0, self.num_districts), self.num_districts))
            # Inserimos as etapas de retorno para despejar o lixo acumulado
            chromosome = []
            current_load = 0

            for district in shuffled_districts:
                vol = self.collection_volume[district]
                if current_load + vol > self.truck_cap:
                    chromosome.append(-1)
                    current_load = 0

                chromosome.append(district)
                current_load += vol
            population.append(chromosome)

        best_overall_individual = None
        best_overall_fitness = float('inf')

        for generation in range(0, self.max_generations):
            # Adaptação
            fitness_scores = [self._calc_fitness(ind, dist_matrix) for ind in population]

            current_best_fitness = min(fitness_scores)
            if current_best_fitness < best_overall_fitness:
                best_overall_fitness = current_best_fitness
                best_overall_individual = population[fitness_scores.index(current_best_fitness)].copy()

            new_population = []
            new_population.append(best_overall_individual)

            # Próxima geração
            for _ in range(self.population_size):
                parent1 = self._select(population, fitness_scores)
                parent2 = self._select(population, fitness_scores)

                while parent1 == parent2:
                    parent2 = self._select(population, fitness_scores)

                child = self._crossover(parent1, parent2)
                child = self._mutate(child)
                new_population.append(child)

            population = new_population
            if generation % 10 == 0 or generation == self.max_generations - 1:
                print(f"Geração {generation:02d} | Melhor Fitness = {current_best_fitness:.2f}")

        return best_overall_individual, best_overall_fitness

def main():
    num_districts = 12
    truck_cap = 8
    collection_volume = [2, 1, 3, 2, 1, 3, 1, 2, 3, 1, 2, 1]
    
    dist_matrix = [
        [ 0,  5,  9, 14,  7,  6, 12, 11,  8, 10, 13, 15],
        [ 5,  0,  4, 12,  6,  5, 11, 13,  9,  8, 14, 10],
        [ 9,  4,  0,  6, 10,  8, 12,  9,  7, 11, 13, 14],
        [14, 12,  6,  0,  8,  7,  9, 10, 12, 13,  5,  6],
        [ 7,  6, 10,  8,  0,  5,  8, 11, 10,  9, 12, 13],
        [ 6,  5,  8,  7,  5,  0,  6,  9,  8, 10, 11, 14],
        [12, 11, 12,  9,  8,  6,  0,  4,  7,  8, 10,  9],
        [11, 13,  9, 10, 11,  9,  4,  0,  3,  6,  7,  8],
        [ 8,  9,  7, 12, 10,  8,  7,  3,  0,  5,  9, 10],
        [10,  8, 11, 13,  9, 10,  8,  6,  5,  0,  4,  7],
        [13, 14, 13,  5, 12, 11, 10,  7,  9,  4,  0,  3],
        [15, 10, 14,  6, 13, 14,  9,  8, 10,  7,  3,  0]
    ]

    print("--- Otimização de Rotas de Coleta ---")
    
    # 2. Configura e Executa o Algoritmo
    ga = GeneticAlgorithm(population_size=100, max_generations=50, mutation_rate=0.1)
    ga.recieve_parameters(num_districts, truck_cap, collection_volume)
    
    best_route, best_fitness = ga.search(dist_matrix)

    # 3. Exibição dos Resultados
    print("\n--- Resultados Finais ---")
    print(f"Cromossomo Final: {best_route}")
    print(f"Fitness (Distância + Penalidades): {best_fitness:.2f} km\n")
    
    # Traduzindo o cromossomo para um formato visual mais claro
    print("Detalhamento da Rota:")
    trip_number = 1
    current_trip_districts = []
    
    for gene in best_route:
        if gene == -1:
            print(f"Viagem {trip_number}: Bairros {current_trip_districts}")
            trip_number += 1
            current_trip_districts = []
        else:
            current_trip_districts.append(f"B{gene}")
            
    # Imprime a última viagem (pois a lista não termina com -1)
    if current_trip_districts:
        print(f"Viagem {trip_number}: Bairros {current_trip_districts}")

if __name__ == "__main__":
    main()