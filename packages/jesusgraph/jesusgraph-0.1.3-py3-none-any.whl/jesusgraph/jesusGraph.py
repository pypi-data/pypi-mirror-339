from .core.graph import JesusGraphCore



class JesusGraph:

    def __init__(self):

        #Inicializa os services
        self.graph =  JesusGraphCore()

    def add_node(self, name:str, function):
        """
        Adiciona um nó ao grafo.

        Args:
            name: Nome único do nó
            function: Função que recebe e atualiza o estado

        Returns:
            Self para encadeamento de métodos
        """
        self.graph.add_node(name, function)
        return self

    def connect(self, source, target):
        """
        Conecta dois nós no grafo.

        Args:
            source: Nó de origem
            target: Nó de destino

        Returns:
            Self para encadeamento de métodos

        Raises:
            ValueError: Se algum dos nós não existir
        """
        self.graph.add_edge(source, target)
        return self

    def set_entry_node(self, node_name):
        """
        Define o ponto de entrada do fluxo.

        Args:
            node_name: Nome do nó inicial

        Returns:
            Self para encadeamento de métodos
        """
        self.graph.add_edge("START", node_name)
        return self

    def set_end_node(self, node_name):
        """
        Define um ponto de saída do fluxo.

        Args:
            node_name: Nome do nó final

        Returns:
            Self para encadeamento de métodos
        """
        self.graph.add_edge(node_name, "END")
        return self

    def run(self, *args, **kwargs):
        """
        Executa o grafo com diferentes formas de entrada:
        - grafo.run({"pontuacao": 850})
        - grafo.run("pontuacao", 850)
        """
        # Forma tradicional: dicionário completo
        if len(args) == 1 and isinstance(args[0], dict):
            state = args[0]

        # Forma simplificada: chave e valor
        elif len(args) == 2 and isinstance(args[0], str):
            state = {args[0]: args[1]}

        else:
            raise ValueError("Use grafo.run(dict) ou grafo.run('chave', valor)")

        resultado = self.graph.run(state or {})
        return resultado.user_state
