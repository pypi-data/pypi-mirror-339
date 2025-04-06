from typing import Any, Dict, Optional, Iterator, Tuple, List

class BlessingState(Dict):
    """
    Gerencia o estado de bênçãos dentro do JesusGraph.

    Esta classe armazena e gerencia os valores recebidos durante a execução
    do grafo. Cada bênção tem um nome único e pode conter qualquer tipo de dado.
    
    O usuário pode interagir com as bênçãos de várias formas:
    - Usando os métodos específicos (addBlessing, getBlessing)
    - Usando a notação de dicionário (state["nome"])
    - Iterando sobre os itens (for name, value in state.items())
    """

    # Constante para evitar conflito de nomes
    _LAST_BLESSING_KEY = "__lastBlessing__"  # Usando underscores para reduzir chance de colisão

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        """
        Inicializa o estado com um dicionário opcional de bênçãos.
        
        Args:
            initial_state: Dicionário inicial de bênçãos (opcional)
        """
        self._blessings: Dict[str, Any] = {}
        
        # Se um estado inicial foi fornecido, adicione-o
        if initial_state:
            for key, value in initial_state.items():
                self.addBlessing(key, value)

    def addBlessing(self, name: str, value: Any) -> 'BlessingState':
        """
        Adiciona uma nova bênção ao estado.

        Args:
            name (str): Nome da bênção (ex: 'resposta_ia')
            value (Any): Valor da bênção (pode ser qualquer tipo: string, dict, lista, etc)

        Returns:
            BlessingState: o próprio objeto para encadeamento de métodos
        
        Raises:
            ValueError: Se tentar usar o nome reservado para lastBlessing
        """
        if name == self._LAST_BLESSING_KEY:
            raise ValueError(f"'{self._LAST_BLESSING_KEY}' é um nome reservado. Use addLastBlessing() ou a propriedade 'last'.")
        
        self._blessings[name] = value
        return self
    
    def UpsertLastBlessing(self, value: Any) -> 'BlessingState':
        """
        Adiciona ou atualiza o valor da última bênção, substituindo qualquer valor anterior.
        """
        # Atualizar diretamente ambas as chaves
        self._blessings["lastBlessing"] = value
        self._blessings[self._LAST_BLESSING_KEY] = value
        
        return self

    def getBlessing(self, name: str) -> Any:
        """
        Retorna uma bênção específica pelo nome.

        Args:
            name (str): Nome da bênção desejada

        Returns:
            Any: Valor armazenado ou None se não existir
        """
        return self._blessings.get(name, None)
    
    def updateBlessing(self, name: str, value: Any) -> 'BlessingState':
        """ 
        Atualiza o valor de uma bênção existente.

        Args:
            name (str): Nome da bênção a ser atualizada
            value (Any): Novo valor a ser atribuído
        
        Returns:
            BlessingState: o próprio objeto para encadeamento de métodos
            
        Raises:
            ValueError: Se a bênção não existir
        """
        if name not in self._blessings:
            raise ValueError(f"A blessing '{name}' ainda não existe. Use .addBlessing() para criar.")
        self._blessings[name] = value
        return self

    def hasBlessing(self, name: str) -> bool:
        """
        Verifica se uma bênção existe no estado.
        
        Args:
            name (str): Nome da bênção a verificar
        
        Returns:
            bool: True se a bênção existir, False caso contrário
        """
        return name in self._blessings

    def allBlessings(self) -> Dict[str, Any]:
        """
        Retorna todas as bênçãos armazenadas.

        Returns:
            Dict[str, Any]: Dicionário com todas as bênçãos
        """
        return self._blessings.copy()
        
    def items(self) -> Iterator[Tuple[str, Any]]:
        """
        Permite iterar sobre as bênçãos como em um dicionário.
        
        Returns:
            Um iterador sobre os pares (nome, valor) das bênçãos
        """
        return self._blessings.items()
        
    def keys(self) -> Iterator[str]:
        """
        Retorna os nomes de todas as bênçãos.
        
        Returns:
            Um iterador sobre os nomes das bênçãos
        """
        return self._blessings.keys()
        
    def values(self) -> Iterator[Any]:
        """
        Retorna os valores de todas as bênçãos.
        
        Returns:
            Um iterador sobre os valores das bênçãos
        """
        return self._blessings.values()
    

    def addLastBlessing(self, value: Any) -> 'BlessingState':
        """
        Adiciona ou atualiza o valor da última bênção, substituindo qualquer valor anterior.
        Útil quando só se deseja rastrear o resultado final de um fluxo, sem acumular estados.

        Args:
            value (Any): Valor a ser armazenado como última bênção 
                        (tipicamente um dicionário com dados do resultado final)

        Returns:
            BlessingState: o próprio objeto para encadeamento de métodos
        """
        name = "lastBlessing"
        self._blessings[name] = value
        return self

    def getLastBlessing(self) -> Any:
        """
        Retorna o valor da última bênção registrada.
        
        Se a última bênção estiver definida, retorna seu valor. Caso contrário,
        tenta identificar e retornar a última bênção adicionada ao estado.
        Se não houver nenhuma bênção, retorna um valor padrão (dicionário vazio).

        Returns:
            Any: Valor da última bênção, ou valor padrão se nenhuma existir
        """
        # 1. Verificar se existe uma lastBlessing explícita
        if self._LAST_BLESSING_KEY in self._blessings:
            return self._blessings[self._LAST_BLESSING_KEY]
        
        # 2. Se não existir, determinar qual é a última usando lógica de prioridade
        if self._blessings:
            # Lógica para identificar o valor mais relevante no estado atual
            # Opção 1: Último item adicionado (usando ordem de inserção do dict em Python 3.7+)
            last_key = list(self._blessings.keys())[-1]
            
            # Verificar se a chave é uma chave especial/interna
            if last_key.startswith("__") and last_key.endswith("__"):
                # Se for uma chave especial/interna, tentar encontrar a primeira chave não especial
                normal_keys = [k for k in self._blessings.keys() if not (k.startswith("__") and k.endswith("__"))]
                if normal_keys:
                    last_key = normal_keys[-1]
            
            return self._blessings[last_key]
        
        # 3. Se não houver nenhuma bênção, retornar um valor padrão útil
        # (um dicionário vazio é mais útil que None em muitos casos)
        return {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Equivalente a getBlessing, mas com interface de dicionário.
        
        Args:
            key: Nome da blessing
            default: Valor padrão se não existir
            
        Returns:
            Valor da blessing ou valor padrão
        """
        return self._blessings.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """
        Permite acessar as bênçãos com colchetes, como em um dicionário:
            state["usuario"]

        Args:
            key (str): Nome da bênção

        Returns:
            Any: Valor da bênção ou None
        """
        return self._blessings.get(key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Permite definir bênçãos com colchetes:
            state["resultado"] = {...}

        Args:
            key (str): Nome da bênção
            value (Any): Valor a ser armazenado
        """
        self._blessings[key] = value

    def __contains__(self, key: str) -> bool:
        """
        Permite verificar se uma bênção existe:
            if "usuario" in state:

        Args:
            key (str): Nome da bênção

        Returns:
            bool: True se existe, False se não
        """
        return key in self._blessings

    def __str__(self) -> str:
        """
        Representação amigável do estado com todas as bênçãos.
        """
        blessings = {k: v for k, v in self._blessings.items() if k != self._LAST_BLESSING_KEY}
        last_value = self.getLastBlessing() if self.has_last() else None
        
        if last_value is not None:
            return f"Blessings: {blessings}, Last: {last_value}"
        else:
            return f"Blessings: {blessings}"
        
    def __len__(self) -> int:
        """
        Retorna o número de bênçãos armazenadas.
        """
        return len(self._blessings)

    def __iter__(self) -> Iterator[str]:
        """
        Permite iterar diretamente sobre as chaves do estado.
        """
        return iter(self._blessings)

    @property
    def last(self):
        """
        Propriedade para acesso facilitado ao último valor.
        Retorna sempre um valor, mesmo que nenhuma bênção esteja definida.
        Equivalente a getLastBlessing().
        """
        return self.getLastBlessing()
    
    @last.setter
    def last(self, value):
        """
        Define o último valor através de atribuição.
        Equivalente a addLastBlessing(value).
        """
        self.addLastBlessing(value)

    def has_last(self) -> bool:
        """
        Verifica se uma bênção 'last' foi explicitamente definida.
        
        Returns:
            bool: True se uma bênção 'last' foi definida, False caso contrário
        """
        return self._LAST_BLESSING_KEY in self._blessings

    def updateLastBlessing(self, value: Any) -> 'BlessingState':
        """
        Atualiza o valor da última bênção registrada e o armazena na chave especial "lastBlessing".
        
        Este método simplifica o fluxo para o desenvolvedor, permitindo que ele atualize
        o estado sem se preocupar com nomes de chaves específicos.

        Args:
            value (Any): Valor a ser armazenado como última bênção.
            
        Returns:
            BlessingState: O próprio objeto para encadeamento de métodos.
        """
        # Atualizar a chave especial "lastBlessing"
        self._blessings[self._LAST_BLESSING_KEY] = value
        
        # Também armazenar o valor na chave "lastBlessing" para consistência
        self._blessings["lastBlessing"] = value
        
        return self




