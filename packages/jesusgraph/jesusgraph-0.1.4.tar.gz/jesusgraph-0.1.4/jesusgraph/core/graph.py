from typing import Dict, Any, Callable, Optional, List, Union, Tuple
from jesusgraph.core.execution import ExecutionState
from jesusgraph.core.blessingstate import BlessingState
import asyncio


# Tipos genéricos para os nós (suportando diferentes retornos)
NodeFunction = Callable[[Dict[str, Any]], Union[Dict[str, Any], List, Tuple[str, Any]]]

# Nós especiais
START = "START"
END = "END"

class JesusGraphCore:
    """
    Framework para orquestração de fluxos baseado em grafos.
    
    O JesusGraph permite criar fluxos de processamento conectando nós
    que representam tarefas. Cada nó recebe um estado e produz atualizações
    para esse estado.
    """
    
    def __init__(self):
        """
        Inicializa um novo grafo de processamento.
        
        Cria um grafo vazio com nós especiais START e END pré-configurados.
        O grafo mantém um dicionário de estado que será passado entre os nós
        durante a execução.
        
        Attributes:
            nodes: Mapeamento de nomes para funções de processamento
            edges: Mapeamento de origens para listas de destinos (adjacências)
            entry_point: Referência ao ponto de entrada (reservado para uso futuro)
        """
        # Registro de nós (mapeamento nome -> função)
        self.nodes: Dict[str, NodeFunction] = {}
        
        # Estrutura do grafo (lista de adjacências)
        self.edges: Dict[str, List[str]] = {}
        
        # Ponto de entrada (será definido ao conectar um nó ao START)
        self.entry_point: Optional[str] = None
        
        # Inicializar nós especiais (não contêm funções, apenas servem como marcadores)
        self.edges[START] = []  # Nó de início do grafo
        self.edges[END] = []    # Nó de término do grafo

    def add_node(self, name:str, function:NodeFunction):
        """
        Adiciona um nó ao grafo.
        
        Args:
            name: Nome único do nó
            function: Função que recebe e atualiza o estado
            
        Returns:
            Self para encadeamento de métodos
            
        Raises:
            ValueError: Se o nome já existe ou é um nome reservado
        """
        if name in [START, END]:
            raise ValueError(f"Não pode usar nomes reservados: {START}, {END}")
        
        if name in self.nodes:
            raise ValueError(f"Node {name} already exists.")
        self.nodes[name] = function

        return self
    
    # Métodos de conveniência para melhorar a experiência do usuário
    def set_entry_node(self, node_name: str):
        """Define o nó de entrada do grafo."""
        return self.add_edge(START, node_name)
        
    def set_end_node(self, node_name: str):
        """Define o nó de saída do grafo."""
        return self.add_edge(node_name, END)
        
    def connecte(self, source: str, target: str):
        """Alias para add_edge por compatibilidade com exemplos."""
        return self.add_edge(source, target)
    
    def add_edge(self, source: str, target: str):
        """
        Adiciona uma conexão entre dois nós do grafo.
        
        Args:
            source: Nó de origem
            target: Nó de destino
            
        Returns:
            Self para encadeamento de métodos
            
        Raises:
            ValueError: Se algum dos nós não existir
        """
        # Verificações especiais para START e END
        if source == START:
            if target not in self.nodes:
                raise ValueError(f"Node {target} does not exist.")
            self.edges[START] = [target]
            return self
        
        if target == END:
            if source not in self.nodes:
                raise ValueError(f"Node {source} does not exist.")
            if source not in self.edges:
                self.edges[source] = []
            if END not in self.edges[source]:
                self.edges[source].append(END)
            return self
        
        # Verificação normal
        if source not in self.nodes or target not in self.nodes:
            raise ValueError(f"One or both nodes do not exist: {source}, {target}")
        
        # Adicionar aresta
        if source not in self.edges:
            self.edges[source] = []
        self.edges[source].append(target)

        return self
    
    async def run(self, initial_state: Optional[Union[Dict[str, Any], BlessingState, ExecutionState]] = None) -> BlessingState:
        """
        Executa o grafo com o estado inicial fornecido.

        Args:
            initial_state: Estado inicial para o fluxo (opcional), pode ser um dict, BlessingState ou ExecutionState

        Returns:
            BlessingState: Estado final após a execução completa do grafo
        """

        # Garantir que tudo rode via ExecutionState
        if isinstance(initial_state, ExecutionState):
            state = initial_state
        else:
            state = ExecutionState(initial_state)

        if not self.edges[START]:
            raise ValueError("Grafo sem nó inicial. Conecte um nó ao START.")

        # Determinar o ponto de entrada
        if not state.current_node:
            current_node = self.edges[START][0]
        elif state.paused:
            if state.current_node in self.edges and self.edges[state.current_node]:
                current_node = self.edges[state.current_node][0]
            else:
                return BlessingState(state.get_blessing_dict())
        else:
            current_node = state.current_node

        # 🚀 Execução do grafo
        while current_node != END:
            state.update_node(current_node)

            try:
                if current_node in self.nodes:
                    node_function = self.nodes[current_node]

                    #  Convertemos o estado atual para um BlessingState (mesmo que o dev só use dict)
                    blessing = BlessingState(state.get_blessing_dict())

                    # ⚡️ Executar o nó (sincrono ou async)
                    result = await node_function(blessing) if asyncio.iscoroutinefunction(node_function) else node_function(blessing)

                    #  Processar o resultado
                    if isinstance(result, BlessingState):
                        for key, value in result.items():
                            state.set_blessing(key, value)
                    elif isinstance(result, dict):
                        for key, value in result.items():
                            state.set_blessing(key, value)
                    elif isinstance(result, (list, tuple)) and len(result) == 2:
                        name, value = result
                        state.set_blessing(name, value)
                    else:
                        raise ValueError(f"Nó '{current_node}' deve retornar um dict, BlessingState ou [chave, valor]. Recebido: {type(result)}")

                    if state.needs_human_input:
                        return BlessingState(state.get_blessing_dict())

            except Exception as e:
                state.set_error(current_node, e)
                return BlessingState(state.get_blessing_dict())

            # 👉 Avançar para o próximo nó
            if current_node not in self.edges or not self.edges[current_node]:
                break

            current_node = self.edges[current_node][0]

        # ✅ Estado final sempre como BlessingState
        return BlessingState(state.get_blessing_dict())

    def resume(self, state: ExecutionState) -> ExecutionState:
        """
        Retoma a execução de um grafo pausado.
        
        Args:
            state: Estado de uma execução anterior pausada
            
        Returns:
            Estado atualizado após a continuação
        """
        if not state.paused:
            return state  # Nada a fazer se não estiver pausado
        
        state.resume()  # Marca como não pausado
        
        return self.run(state)  # Continua a execução

    def run_sync(self, initial_state: Optional[Union[Dict[str, Any], BlessingState, ExecutionState]] = None) -> BlessingState:
        """
        Executa o grafo de forma síncrona.
        
        Args:
            initial_state: Estado inicial para o fluxo (opcional)
            
        Returns:
            BlessingState: Estado final após a execução completa do grafo
        """
        return asyncio.run(self.run(initial_state))
