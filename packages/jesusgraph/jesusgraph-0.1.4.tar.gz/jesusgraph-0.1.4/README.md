🌟 Recursos Principais
🧩 Modularidade: Divida fluxos complexos em componentes menores e reutilizáveis
🔄 Estado Compartilhado: Transmita dados entre nós de forma consistente
🧠 Flexibilidade: Organize nós em qualquer padrão direcionado
🛡️ Tratamento de Erros: Capture e gerencie falhas em qualquer ponto do fluxo
🔄 Encadeabilidade: Construa grafos através de uma API fluente e elegante
📊 Conceitos Básicos
Nós (Nodes)
Os nós são as unidades fundamentais de processamento. Cada nó é uma função que:

Recebe um estado atual (BlessingState)
Realiza algum processamento
Retorna um estado atualizado
Arestas (Edges)
As arestas definem o fluxo entre os nós, indicando a ordem de execução.

🧠 Casos de Uso
Processamento de dados sequenciais
Fluxos de trabalho de negócios
Pipelines de ETL (Extração, Transformação, Carregamento)
Orquestração de microserviços
Fluxos de aprovação e validação
Integração de APIs
Automação de processos
🤝 Contribuição
Contribuições são bem-vindas! Veja como contribuir:

Faça um fork do repositório
Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)
Faça commit das suas mudanças (git commit -m 'Adiciona nova funcionalidade')
Faça push para a branch (git push origin feature/nova-funcionalidade)
Abra um Pull Request
📄 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

📚 Documentação Adicional
Para documentação detalhada e mais exemplos, visite nossa wiki.

Desenvolvido com ❤️ por Carlos Viana

Estado (BlessingState)
O BlessingState é um contêiner para dados compartilhados entre os nós, onde cada valor é uma "bênção".

🔍 Exemplo Básico

```python
from jesusgraph import JesusGraph, BlessingState

# Definir funções de processamento
def cumprimentar(blessing: BlessingState) -> BlessingState:
    nome = blessing.getBlessing("nome") or "visitante"
    blessing.addBlessing("mensagem", f"Olá, {nome}!")
    return blessing

def despedir(blessing: BlessingState) -> BlessingState:
    nome = blessing.getBlessing("nome") or "visitante"
    blessing.addBlessing("despedida", f"Até logo, {nome}!")
    return blessing

# Criar e configurar o grafo
grafo = JesusGraph()

# Adicionar nós
grafo.add_node("cumprimentar", cumprimentar)
grafo.add_node("despedir", despedir)

# Configurar o fluxo
grafo.set_entry_node("cumprimentar")  # Define o nó inicial
grafo.connecte("cumprimentar", "despedir")  # Conecta os nós
grafo.set_end_node("despedir")  # Define o nó final

# Executar o grafo
resultado = grafo.run({"nome": "João"})

# Verificar resultados
print(resultado.getBlessing("mensagem"))  # Olá, João!
print(resultado.getBlessing("despedida"))  # Até logo, João!
```
🚢 Exemplo Completo: Sistema de Pedidos
Veja como implementar um fluxo de processamento de pedidos:

```python
from jesusgraph import JesusGraph, BlessingState

# Funções de processamento
def receber_pedido(blessing: BlessingState) -> BlessingState:
    cliente = blessing.getBlessing("cliente_nome") or "Cliente Anônimo"
    blessing.addBlessing("pedido_id", "PED-12345")
    blessing.addBlessing("status", "RECEBIDO")
    return blessing

def calcular_valor(blessing: BlessingState) -> BlessingState:
    itens = blessing.getBlessing("itens") or []
    total = sum(item.get("preco", 0) for item in itens)
    blessing.addBlessing("valor_total", total)
    blessing.addBlessing("status", "CALCULADO")
    return blessing

def preparar_pedido(blessing: BlessingState) -> BlessingState:
    blessing.addBlessing("status", "PREPARADO")
    return blessing

def entregar_pedido(blessing: BlessingState) -> BlessingState:
    blessing.addBlessing("status", "ENTREGUE")
    blessing.addBlessing("entrega_concluida", True)
    return blessing

# Criar grafo
grafo = JesusGraph()

# Adicionar nós e configurar o fluxo
grafo.add_node("receber", receber_pedido)
grafo.add_node("calcular", calcular_valor)
grafo.add_node("preparar", preparar_pedido)
grafo.add_node("entregar", entregar_pedido)

# Configurar o fluxo
grafo.set_entry_node("receber")
grafo.connecte("receber", "calcular")
grafo.connecte("calcular", "preparar")
grafo.connecte("preparar", "entregar")
grafo.set_end_node("entregar")

# Executar com dados iniciais
pedido = {
    "cliente_nome": "Maria Silva",
    "itens": [
        {"nome": "Pizza", "preco": 45.90},
        {"nome": "Refrigerante", "preco": 8.50}
    ]
}

resultado = grafo.run(pedido)
print(f"Status final: {resultado.getBlessing('status')}")
print(f"Pedido entregue: {resultado.getBlessing('entrega_concluida')}")
```

🔧 API Principal
JesusGraph

# Criar um novo grafo
grafo = JesusGraph()

# Adicionar um nó
grafo.add_node(nome, funcao)

# Criar conexões entre nós
grafo.add_edge(origem, destino)
grafo.connecte(origem, destino)  # Alias para add_edge

# Configurar pontos de entrada/saída
grafo.set_entry_node(nome_do_no)
grafo.set_end_node(nome_do_no)

# Executar o grafo
resultado = grafo.run(estado_inicial)

# Retomar a execução de um grafo pausado
resultado = grafo.resume(estado_pausado)


BlessingState

# Criar um estado vazio
estado = BlessingState()

# Adicionar uma bênção
estado.addBlessing("chave", valor)

# Obter o valor de uma bênção
valor = estado.getBlessing("chave")

# Verificar se uma bênção existe
if estado.hasBlessing("chave"):
    # fazer algo

# Atualizar uma bênção existente
estado.updateBlessing("chave", novo_valor)

# Obter todas as bênçãos como dicionário
todas_bencaos = estado.allBlessings()

# Uso como dicionário
estado["chave"] = valor
valor = estado["chave"]
if "chave" in estado:
    # fazer algo

