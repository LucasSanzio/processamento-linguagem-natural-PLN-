# Projeto de Pré-processamento de PLN (Super Aprimorado)

Este projeto implementa um pipeline avançado de pré-processamento de texto em português, realizando tokenização, normalização diferenciada, identificação de expressões, remoção de stop words, geração de n-gramas, lematização com agrupamento semântico e garantindo uma saída final totalmente em letras minúsculas.

## Funcionalidades Detalhadas

O script `pre_processamento_pln_super_aprimorado.py` executa as seguintes etapas de pré-processamento:

1.  **Carregamento de Recursos:**
    *   Carrega o modelo de língua portuguesa `pt_core_news_sm` da biblioteca spaCy.
    *   Carrega a lista de stop words em português e o tokenizador `punkt` da biblioteca NLTK.
    *   Inclui tratamento de erro caso os recursos não sejam encontrados, com instruções para o usuário.

2.  **Definição do Corpus:** O texto base para análise é definido no início do script.

3.  **Pré-processamento Inicial (Proteção de Entidades e Expressões):
    *   **Identificação de Entidade Nomeada:** Utiliza o spaCy para identificar entidades do tipo Pessoa (PER). Especificamente, "Sra. Rosa" é identificada e temporariamente substituída por um placeholder (`__SRA_ROSA_ENTIDADE__`) para proteger sua integridade e capitalização original durante as etapas iniciais de normalização.
    *   **Identificação de Expressões Comuns:** Uma lista predefinida de expressões (ex: "rosa em flor") é procurada no texto (de forma case-insensitive). Se encontrada, a expressão é substituída por um placeholder (ex: `__EXPRESSAO_ROSA_EM_FLOR__`).

4.  **Tokenização e Normalização Inicial:**
    *   O texto (com os placeholders) é processado. As partes do texto que não são placeholders são convertidas para letras minúsculas e tokenizadas usando expressões regulares (`re.findall(r'\b\w+\b', parte.lower())`).
    *   Os placeholders são mantidos como tokens únicos.

5.  **Remoção de Stop Words (com Restauração de Entidades/Expressões):
    *   Os placeholders são revertidos para suas formas textuais originais capturadas (ex: "Sra. Rosa", "rosa em flor").
    *   As stop words em português são removidas da lista de tokens.

6.  **Geração de N-gramas:**
    *   **Unigramas:** São os tokens resultantes após a remoção de stop words e restauração das entidades/expressões.
    *   **Bigramas:** Sequências de dois tokens consecutivos.
    *   **Trigramas:** Sequências de três tokens consecutivos.
    *   A função `ngrams` da biblioteca NLTK é utilizada.

7.  **Lematização, Agrupamento Semântico e Minusculização Final:**
    *   Os tokens filtrados (incluindo as entidades/expressões como tokens únicos) são unidos em uma string para processamento pelo lematizador spaCy.
    *   Durante a lematização:
        *   Se o token original corresponde à entidade "Sra. Rosa", um identificador interno (`SRA_ROSA_PESSOA_ID`) é usado.
        *   Se o token original corresponde à expressão "rosa em flor", um identificador interno (`EXPRESSAO_ROSA_EM_FLOR_ID`) é usado.
        *   Caso contrário, o lema fornecido pelo spaCy é utilizado.
    *   **Agrupamento Semântico:** Um mapa semântico (`mapa_semantico_flor`) é aplicado para consolidar palavras relacionadas (ex: "rosa", "rosas", "flor", e as lematizações problemáticas "roso", "rosar") sob um conceito unificado (ex: "flor_conceito").
    *   **Conversão para Representação Final e Minusculização:**
        *   O identificador `SRA_ROSA_PESSOA_ID` é convertido para "sra. rosa (pessoa)".
        *   O identificador `EXPRESSAO_ROSA_EM_FLOR_ID` é convertido para "expressao_rosa_em_flor".
        *   Todos os lemas e representações finais são convertidos para letras minúsculas (ex: "Jardim" se torna "jardim").

O script imprimirá no console o corpus original e os resultados detalhados de cada uma dessas etapas.

## Configuração do Ambiente (Python 3.12.5)

Siga os passos abaixo para configurar o ambiente de execução do projeto com Python 3.12.5:

1.  **Crie um Ambiente Virtual:**
    Abra seu terminal e execute (substitua `python3.12` pelo seu comando específico para Python 3.12.5, como `python3` ou `python` se for o padrão do sistema):
    ```bash
    python3.12 -m venv venv_pln_super_aprimorado
    ```

2.  **Ative o Ambiente Virtual:**
    *   No Linux ou macOS:
        ```bash
        source venv_pln_super_aprimorado/bin/activate
        ```
    *   No Windows (usando Git Bash ou PowerShell):
        ```bash
        venv_pln_super_aprimorado\Scripts\activate
        ```
    O nome `(venv_pln_super_aprimorado)` aparecerá no início do prompt do seu terminal.

3.  **Instale as Bibliotecas Necessárias:**
    Com o ambiente virtual ativado, instale `nltk` e `spacy`:
    ```bash
    pip install nltk spacy
    ```
    Ou, explicitamente com a versão do Python:
    ```bash
    python3.12 -m pip install nltk spacy
    ```

4.  **Baixe os Dados Adicionais para NLTK e spaCy:**
    *   **NLTK:** No terminal com o ambiente virtual ativo, execute o interpretador Python 3.12.5:
        ```bash
        python3.12
        ```
        Dentro do Python, execute:
        ```python
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')
        exit()
        ```
    *   **spaCy:** Com o ambiente virtual ativo, execute no terminal:
        ```bash
        python3.12 -m spacy download pt_core_news_sm
        ```

## Como Executar o Projeto

1.  Certifique-se de que o ambiente virtual (`venv_pln_super_aprimorado`) está ativado.
2.  Navegue até o diretório onde salvou o arquivo `pre_processamento_pln_super_aprimorado.py`.
3.  Execute o script Python 3.12.5:
    ```bash
    python3.12 pre_processamento_pln_super_aprimorado.py
    ```

O script processará o corpus de exemplo e exibirá as saídas de cada etapa no console.

## Estrutura de Arquivos Sugerida

```
seu_projeto_pln/
├── venv_pln_super_aprimorado/            # Ambiente virtual (Python 3.12.5)
├── pre_processamento_pln_super_aprimorado.py # Script Python PLN super aprimorado
└── README.md                             # Este arquivo de instruções
```

## Corpus Textual Utilizado no Exemplo

`"A Sra. Rosa plantou uma rosa no jardim. O céu estava azul e a brisa era suave. Ela pensou: \"Seria maravilhoso se todos os dias fossem assim, tão tranquilos quanto uma rosa em flor.\""`

