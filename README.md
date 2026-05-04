A-Maze-ing  
This project has been created as part of the 42 curriculum by pdo-sant.

## 1. Descrição
Este projeto consiste em um gerador de labirintos desenvolvido em Python 3.10+ que cria estruturas aleatórias a partir de um arquivo de configuração. O objetivo é gerar labirintos (podendo ser "perfeitos", com apenas um caminho entre a entrada e saída) e salvá-los em um formato hexadecimal padronizado, permitindo também a visualização clara no terminal com suporte a cores e interação do usuário.

## 2. Instruções
Instalação e Compilação  
O projeto utiliza um Makefile para automatizar as tarefas obrigatórias:

- Instalar dependências: `make install` (instala os pacotes listados em requirements.txt).
- Linting (Obrigatório): `make lint` para verificar padrões de código com flake8 e tipagem estática com mypy.

Execução  
Para rodar o programa principal, utilize o comando:  
`python3 a_maze_ing.py config.txt`  
Ou via Makefile: `make run`.

## 3. Configuração
O arquivo de configuração (ex: config.txt) deve conter obrigatoriamente as seguintes chaves:

- WIDTH: Largura do labirinto (células).
- HEIGHT: Altura do labirinto (células).
- ENTRY: Coordenadas de entrada (x,y).
- EXIT: Coordenadas de saída (x,y).
- OUTPUT_FILE: Nome do arquivo onde o labirinto será salvo.
- PERFECT: Define se o labirinto deve ser perfeito (True/False).

## 4. Algoritmo de Geração
O algoritmo escolhido para este projeto foi o Recursive Backtracking.

Por que esta escolha?  
Este algoritmo é amplamente utilizado por ser eficiente na criação de "spanning trees", o que garante a geração de um labirinto perfeito (conforme exigido se a flag PERFECT=True estiver ativa) com caminhos longos e sinuosos.

Busca de Caminho:  
Para encontrar o caminho mais curto salvo no OUTPUT_FILE, foi utilizado o algoritmo BFS (Breadth-First Search), que garante encontrar a menor rota entre a entrada e a saída.

## 5. Reutilização de Código
A lógica de geração foi encapsulada em uma classe única chamada `MazeGenerator` dentro de um módulo independente.

Módulo:  
O pacote instalável está localizado na raiz como `mazegen-pdo-sant-1.0.0-py3-none-any.whl`.

Como usar:

## 6. Recursos e Uso de IA
Referências:

- Documentação oficial do Python 3.10+.
- Padrões de codificação PEP 8 e PEP 257.
- Teoria dos Grafos: Spanning Trees e BFS.

Uso de Inteligência Artificial:  
Seguindo as diretrizes do Capítulo II, a IA foi utilizada como uma ferramenta de suporte técnico e aprendizagem, e não para gerar o projeto de forma automatizada. As principais tarefas realizadas com auxílio da IA foram:

- Explicação de Conceitos: Compreensão profunda do funcionamento dos algoritmos BFS e Backtracking para aplicação manual na lógica do labirinto.
- Estruturação de Projeto: Auxílio na configuração técnica do arquivo pyproject.toml e na organização da estrutura de pastas para cumprir os requisitos de reutilização de código (Capítulo VI).
- Resolução de Problemas Técnicos: Diagnóstico de erros de importação relativa em Python e configuração do ambiente de linting (mypy e flake8).
- Checklist de Requisitos: Consolidação das regras obrigatórias do manual para garantir que nenhum detalhe da "Moulinette" fosse esquecido.

## 7. Gestão do Projeto
Papéis: Projeto individual realizado por pdo-sant.

Ferramentas: VS Code, Git, NumPy para manipulação de matrizes e as ferramentas de build do Python.

Evolução:  
O planejamento inicial focou na lógica de bits para as paredes; a maior evolução ocorreu na implementação da visualização ASCII colorida lado a lado para garantir clareza visual no terminal.