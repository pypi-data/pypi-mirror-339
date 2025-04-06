from typing import Dict, Any, List, Optional, Union
import time
import json
from jesusgraph.core.blessingstate import BlessingState

class ExecutionState:
    """
    Gerencia o estado de execução de um grafo, incluindo:
    - estado do usuário (as "blessings")
    - metadados como histórico, pausas, erros e tempo de execução
    """

    def __init__(self, initial_state: Optional[Union[Dict[str, Any], BlessingState]] = None):
        """
        Inicializa um estado de execução.
        
        Args:
            initial_state: Estado inicial opcional (dict ou BlessingState)
        """
        # Garantir que o estado interno seja sempre um BlessingState
        if isinstance(initial_state, BlessingState):
            self.blessing = initial_state
        elif isinstance(initial_state, dict):
            self.blessing = BlessingState()
            for k, v in initial_state.items():
                self.blessing.addBlessing(k, v)
        else:
            self.blessing = BlessingState()

        # Metadados de execução
        self.current_node: Optional[str] = None
        self.history: List[str] = []
        self.error: Optional[Dict[str, Any]] = None
        self.paused: bool = False
        self.paused_at: Optional[str] = None
        self.needs_human_input: bool = False
        self.start_time: float = time.time()
        self.last_update: float = time.time()

    def get_blessing_dict(self) -> Dict[str, Any]:
        """
        Retorna um dicionário com todas as blessings.
        
        Returns:
            Dict: Dicionário com todos os valores armazenados
        """
        return self.blessing.allBlessings()
        
    def set_blessing(self, name: str, value: Any):
        """
        Define ou atualiza uma blessing com o nome e valor especificados.
        
        Args:
            name: Nome da blessing
            value: Valor a ser armazenado
        """
        if self.blessing.hasBlessing(name):
            self.blessing.updateBlessing(name, value)
        else:
            self.blessing.addBlessing(name, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o estado para um dicionário com metadados incluídos.
        
        Returns:
            Dict: Estado completo incluindo metadados de execução
        """
        return {
            **self.blessing.allBlessings(),
            '__execution__': {
                'current_node': self.current_node,
                'history': self.history,
                'error': self.error,
                'paused': self.paused,
                'paused_at': self.paused_at,
                'needs_human_input': self.needs_human_input,
                'start_time': self.start_time,
                'last_update': self.last_update
            }
        }

    @classmethod
    def from_dict(cls, state_dict: Dict[str, Any]) -> 'ExecutionState':
        """
        Cria um ExecutionState a partir de um dicionário.
        
        Args:
            state_dict: Dicionário com estado e metadados
            
        Returns:
            ExecutionState: Nova instância configurada com os dados fornecidos
        """
        state_copy = state_dict.copy()
        execution_meta = state_copy.pop('__execution__', {})
        instance = cls(state_copy)  # será convertido para BlessingState dentro do __init__

        instance.current_node = execution_meta.get('current_node')
        instance.history = execution_meta.get('history', [])
        instance.error = execution_meta.get('error')
        instance.paused = execution_meta.get('paused', False)
        instance.paused_at = execution_meta.get('paused_at')
        instance.needs_human_input = execution_meta.get('needs_human_input', False)
        instance.start_time = execution_meta.get('start_time', time.time())
        instance.last_update = execution_meta.get('last_update', time.time())

        return instance

    def update_node(self, node_name: str):
        """
        Atualiza o nó atual e histórico de execução.
        
        Args:
            node_name: Nome do nó atual
        """
        self.current_node = node_name
        self.history.append(node_name)
        self.last_update = time.time()

    def set_error(self, node_name: str, exception: Exception):
        """
        Registra um erro no fluxo.
        
        Args:
            node_name: Nome do nó onde ocorreu o erro
            exception: Exceção que ocorreu
        """
        self.error = {
            'node': node_name,
            'exception': str(exception),
            'type': type(exception).__name__,
            'timestamp': time.time()
        }

    def pause_for_human(self, node_name: str, reason: str = ""):
        """
        Pausa o fluxo para intervenção humana.
        
        Args:
            node_name: Nome do nó onde a pausa ocorreu
            reason: Motivo da pausa (opcional)
        """
        self.paused = True
        self.paused_at = node_name
        self.needs_human_input = True
        self.set_blessing('__human_input__', {
            'reason': reason,
            'timestamp': time.time()
        })

    def resume(self):
        """
        Retoma a execução após pausa.
        """
        self.paused = False
        self.needs_human_input = False
        if self.blessing.hasBlessing('__human_input__'):
            human_input = self.blessing.getBlessing('__human_input__')
            if isinstance(human_input, dict):
                human_input['resolved'] = True
                human_input['resolved_at'] = time.time()
                self.set_blessing('__human_input__', human_input)

    def is_complete(self) -> bool:
        """
        Verifica se a execução está completa.
        
        Returns:
            bool: True se não está em pausa e não possui erros
        """
        return not self.paused and not self.error

    def has_error(self) -> bool:
        """
        Verifica se a execução encontrou algum erro.
        
        Returns:
            bool: True se encontrou erro, False caso contrário
        """
        return self.error is not None

    # Métodos de acesso convenientes que usam o BlessingState por baixo dos panos
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor pelo nome.
        
        Args:
            key: Nome da blessing
            default: Valor padrão se não existir
            
        Returns:
            Valor armazenado ou valor padrão
        """
        return self.blessing.getBlessing(key) or default

    def set(self, key: str, value: Any):
        """
        Define ou atualiza um valor.
        
        Args:
            key: Nome da blessing
            value: Valor a ser armazenado
        """
        self.set_blessing(key, value)

    def update(self, values: Dict[str, Any]):
        """
        Atualiza múltiplos valores de uma vez.
        
        Args:
            values: Dicionário com os valores a atualizar
        """
        for k, v in values.items():
            self.set_blessing(k, v)
            
    def __getitem__(self, key: str) -> Any:
        """
        Permite acessar as bênçãos com colchetes.
        
        Args:
            key: Nome da blessing
            
        Returns:
            Valor armazenado ou None
        """
        return self.blessing[key]
        
    def __setitem__(self, key: str, value: Any):
        """
        Permite definir bênçãos com colchetes.
        
        Args:
            key: Nome da blessing
            value: Valor a ser armazenado
        """
        self.blessing[key] = value
        
    def __contains__(self, key: str) -> bool:
        """
        Permite verificar se uma blessing existe com o operador 'in'.
        
        Args:
            key: Nome da blessing
            
        Returns:
            True se existe, False caso contrário
        """
        return key in self.blessing
