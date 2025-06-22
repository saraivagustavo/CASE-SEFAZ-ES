# Solução para Case de Estágio - Automação de Processo Seletivo

## Descrição do Projeto

Este projeto consiste em um script Python desenvolvido como parte de um processo seletivo. O objetivo é automatizar partes do cadastro e avaliação de candidatos, utilizando um banco de dados SQLite para armazenamento de dados.

## Funcionalidades Implementadas

O script `[GustavoSaraivaMariano.py]` 

1.  **Criação de Banco de Dados e Tabelas:**
    * Utiliza `sqlite3` para criar um banco de dados local (`processoSeletivo.db`).
    * Cria as tabelas `SELECAO_CANDIDATO` e `SELECAO_TESTE` com as especificações dadas, incluindo chaves primárias, auto-incremento, timestamp padrão, chave estrangeira e `CHECK CONSTRAINTS` para validação de dados.

2.  **Inserção de Dados:**
    * Insere um registro de candidato fictício na tabela `SELECAO_CANDIDATO`.
    * Gera e insere 30 registros na tabela `SELECAO_TESTE`, onde cada registro corresponde a um número da sequência de Fibonacci, indicando se é par ou ímpar.

3.  **Consultas SQL:**
    * Lista a sequência completa de Fibonacci inserida.
    * Lista os 5 maiores números da sequência.
    * Conta a quantidade de números pares e ímpares armazenados.
    * Deleta todos os números maiores que 5000 da sequência.
    * Lista novamente a sequência de Fibonacci para demonstrar o efeito da exclusão.

## Requisitos para Execução

* Python 3.x
* Módulo `sqlite3` (já vem nativo com Python)

## Como Executar

Para rodar este script, siga os passos abaixo:

1.  **Clone o repositório** para o seu ambiente local usando o Git:
    ```bash
    git clone [https://github.com/saraivagustavo/CASE-SEFAZ-ES.git](https://github.com/saraivagustavo/CASE-SEFAZ-ES.git)
    ```

2.  **Navegue até o diretório** do projeto:
    ```bash
    cd CASE-SEFAZ-ES
    ```

3.  **Execute o script Python:**
    ```bash
    GustavoSaraivaMariano.py
    ```
Ao executar, o script criará o arquivo de banco de dados (`processoSeletivo.db`) no mesmo diretório (se ele ainda não existir) e imprimirá as informações das operações e consultas diretamente no seu console.

---

**Autor:**

[Gustavo Saraiva Mariano]
[https://www.linkedin.com/in/gustavo-saraiva-mariano/]
