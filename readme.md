# Assistente de Estratégia para Lotto365

Este é um software de desktop desenvolvido em Python com uma Interface Gráfica (GUI) para auxiliar na criação de estratégias de apostas para o jogo Lotto365.

O programa não prevê resultados, mas atua como uma ferramenta poderosa que gera sugestões de apostas com base em estatísticas e regras matemáticas inseridas pelo usuário. Em vez de calcular as estatísticas, o usuário alimenta o programa com os dados que observa no site de apostas, e o motor de cálculo utiliza essas informações para construir combinações otimizadas.

## ✨ Funcionalidades Principais

- **Interface Gráfica Intuitiva:** Desenvolvido com Tkinter, o programa permite que o usuário insira todos os dados de forma visual e interativa.
- **Seleção de Números Interativa:** Grades de botões clicáveis para marcar facilmente os "Números Populares" e "Números Frios", com validação para evitar que um número seja ambos.
- **Entrada de Estatísticas Avançadas:** Campos para inserir as porcentagens de ocorrência para Cor da Bola, Ímpar/Par e Hi-Lo para cada uma das 5 posições do sorteio.
- **Preenchimento Automático:** Campos de porcentagem para pares (Ímpar/Par, Hi/Lo) se auto-completam para somar 100%, agilizando o preenchimento.
- **Motor de Cálculo Sofisticado:** Um sistema de pontuação que avalia milhares de combinações candidatas com base em múltiplas regras:
    - **Filtro de Exclusão:** Remove completamente os "Números Frios" das sugestões.
    - **Bônus de Popularidade:** Recompensa combinações que incluem os "Números Populares".
    - **Harmonia Posicional:** Pontua combinações baseando-se nas porcentagens de propriedades (cor, paridade, etc.) para cada posição específica.
    - **Filtros Matemáticos:** Oferece bônus para combinações que contêm números da sequência de Fibonacci, Números Primos ou Quadrados Perfeitos.
- **Geração de Sugestões Diversificadas:** A lógica de seleção final escolhe as 5 melhores combinações de forma a maximizar a variedade entre elas, evitando sugestões muito repetitivas.
- **Sugestões para Múltiplos Mercados:** Gera 5 sugestões para o sorteio de 5 números e 10 sugestões ranqueadas para a aposta no "Primeiro Número".
- **Sistema de Feedback (Aprendizagem):** Permite que o usuário marque as sugestões de que gostou, salvando essas preferências em um banco de dados local (SQLite) para influenciar e refinar os cálculos de sugestões futuras.

## 🚀 Como Usar

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd lotto_analyzer
    ```
2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute a aplicação:**
    ```bash
    python main.py
    ```
5.  Preencha os campos na interface gráfica com as estatísticas desejadas e clique em "Gerar Sugestões".

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Tkinter** para a Interface Gráfica
- **SQLite3** para o banco de dados de feedback

## ✍️ Autor

**Luiz Otavio Sales** ([@ghostc0der](https://github.com/ghostc0der))

## 📄 Licença

Este projeto está sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.