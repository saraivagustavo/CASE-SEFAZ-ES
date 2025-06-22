import sqlite3
# *******************************************************
# ************** CONFIGURAÇÕES DO BANCO DE DADOS ********   
# *******************************************************

#nome do arquivo do banco de dados
DB_NAME = "processoSeletivo.db"

# *******************************************************
# ******* MÉTODOS DE CRIAÇÃO E INSERÇÃO DE DADOS ********
# *******************************************************

def f_criarTabelas():
    """
    Cria as tabelas SELECAO_CANDIDATO e SELECAO_TESTE no banco de dados SQLite.
    Define as colunas, chaves primárias, auto-incremento, valores padrão e
    restrições de check e chave estrangeira.
    
    Este método garante que o esquema do banco de dados esteja configurado
    corretamente para as operações subsequentes, utilizando 'IF NOT EXISTS'.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Tabela SELECAO_CANDIDATO
        # ID_CANDIDATO: INTEGER, Auto-incremento, chave primária 
        # NME_CANDIDATO: TEXT, Nome do candidato 
        # DAT_INSCRICAO: TIMESTAMP, Valor padrão: data e hora da inserção 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SELECAO_CANDIDATO (
                ID_CANDIDATO INTEGER PRIMARY KEY AUTOINCREMENT,
                NME_CANDIDATO TEXT NOT NULL,
                DAT_INSCRICAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Tabela SELECAO_CANDIDATO criada ou já existente.")

        # Tabela SELECAO_TESTE
        # ID_TESTE: INTEGER, Auto-incremento, chave primária 
        # ID_CANDIDATO: INTEGER, Chave estrangeira referenciando SELECAO_CANDIDATO 
        # NUM_FIBONACCI: INTEGER, Começa em 1, seguindo a sequência de Fibonacci 
        # NUM_PAR: INTEGER, 0 (falso) ou 1 (verdadeiro) - indica se o número é par 
        # NUM_IMPAR: INTEGER, 0 (falso) ou 1 (verdadeiro) - indica se o número é ímpar 
        # NUM_PAR E NUM_IMPAR com check constraint: só podem ter os valores 0 ou 1 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SELECAO_TESTE (
                ID_TESTE INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_CANDIDATO INTEGER NOT NULL,
                NUM_FIBONACCI INTEGER NOT NULL,
                NUM_PAR INTEGER NOT NULL CHECK(NUM_PAR IN (0, 1)),
                NUM_IMPAR INTEGER NOT NULL CHECK(NUM_IMPAR IN (0, 1)),
                FOREIGN KEY (ID_CANDIDATO) REFERENCES SELECAO_CANDIDATO(ID_CANDIDATO)
            )
        ''')
        print("Tabela SELECAO_TESTE criada ou já existente.")

        conn.commit() #confirma as alterações no banco de dados

    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        if conn:
            conn.close() #garante que a conexão com o banco de dados seja sempre fechada certinha

def f_inserirCandidato(nomeCandidato):
    """
    Insere um novo candidato fictício na tabela SELECAO_CANDIDATO. 
    Retorna o ID do candidato inserido.
    A data de inscrição é automaticamente preenchida pelo DEFAULT CURRENT_TIMESTAMP do SQL.
    """
    conn = None
    candidatoID = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO SELECAO_CANDIDATO (NME_CANDIDATO) VALUES (?)", (nomeCandidato,))
        candidatoID = cursor.lastrowid #pega o id gerado automaticamente pela coluna AUTOINCREMENT do banco de dados
        conn.commit() #confirma a inserção no banco de dados
        print(f"Candidato '{nomeCandidato}' inserido com ID: {candidatoID}")
    except sqlite3.Error as e:
        print(f"Erro ao inserir candidato: {e}")
    finally:
        if conn:
            conn.close()
    return candidatoID

# *******************************************************
# ************** MÉTODOS DE FIBONACCI *******************
# *******************************************************

def f_gerarSeqFibonacci(n):
    """
    Gera os primeiros 'n' números da sequência de Fibonacci. 
    Retorna uma lista de números Fibonacci.
    """
    sequenciaFibonacci = []
    if n >= 1:
        sequenciaFibonacci.append(1) #primeiro número da sequência é 1 (conforme o enunciado)
    if n >= 2:
        sequenciaFibonacci.append(1) #segundo número da sequência também vai ser 1
    for _ in range(2, n):
        proximoNumero = sequenciaFibonacci[-1] + sequenciaFibonacci[-2] #próximo número é a soma dos dois anteriores, regra de Fibonacci 
        sequenciaFibonacci.append(proximoNumero)
    return sequenciaFibonacci[:n] #:n aqui para garantir que a lista vai ter os exatos 'n' números

def f_inserirTestesFibonacci(idCandidato):
    """
    Gera a sequência de Fibonacci e insere 30 registros na tabela SELECAO_TESTE. 
    Para cada número, verifica se é par ou ímpar e preenche os campos NUM_PAR e NUM_IMPAR
    com 1 ou 0, conforme as restrições da tabela do banco de dados.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        #gera os primeiros 30 números da sequência de Fibonacci
        numerosFibonacci = f_gerarSeqFibonacci(30)
        print(f"Sequência Fibonacci gerada ({len(numerosFibonacci)} números): {numerosFibonacci}")

        for numero in numerosFibonacci:
            #verifica se o número é par ou ímpar 
            numPar = 1 if numero % 2 == 0 else 0   #1 se for par, 0 caso contrário 
            numImpar = 1 if numero % 2 != 0 else 0 #1 se for ímpar, 0 caso contrário 

            #insere o número obtido na tabela SELECAO_TESTE, associando ao id do candidato
            cursor.execute(
                "INSERT INTO SELECAO_TESTE (ID_CANDIDATO, NUM_FIBONACCI, NUM_PAR, NUM_IMPAR) VALUES (?, ?, ?, ?)",
                (idCandidato, numero, numPar, numImpar)
            )
        conn.commit() #confirma todas as inserções da sequência de Fibonacci
        print(f"30 registros de teste de Fibonacci inseridos para o candidato ID: {idCandidato}")

    except sqlite3.Error as e:
        print(f"Erro ao inserir testes de Fibonacci: {e}")
    finally:
        if conn:
            conn.close()

# *******************************************************
# ************ MÉTODOS DE CONSULTAS SQL *****************
# *******************************************************

def f_listarSequenciaFibonacci():
    """
    Lista todos os números da sequência Fibonacci armazenados na tabela SELECAO_TESTE. 
    A ordenação é feita pelo ID_TESTE para manter a ordem de inserção original.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        print("\n### Sequência Fibonacci Completa ###")
        cursor.execute("SELECT NUM_FIBONACCI FROM SELECAO_TESTE ORDER BY ID_TESTE ASC")
        resultados = cursor.fetchall() # Recupera todas as linhas da consulta

        if resultados:
            #extração e formatação dos resultados para melhor apresentação
            #cada resultado é uma tupla, então pego o primeiro elemento de cada tupla
            #str() para garantir que os números sejam convertidos para string antes de juntar eles no print
            #join() para criar uma string com os números separados por vírgula e depois imprimir
            print("Números Fibonacci encontrados:")
            seq = [str(res[0]) for res in resultados]
            print(f"Sequência: {', '.join(seq)}")
        else:
            print("Nenhum número Fibonacci encontrado.")

    except sqlite3.Error as e:
        print(f"Erro ao listar sequência Fibonacci: {e}")
    finally:
        if conn:
            conn.close()

def f_listarMaioresNumeros(n=5):
    """
    Lista os N maiores números da sequência Fibonacci armazenados na tabela SELECAO_TESTE. 
    A consulta utiliza ORDER BY DESC e LIMIT para eficiência na recuperação dos maiores valores.
    Por padrão, lista os 5 maiores.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        print(f"\n### Os {n} Maiores Números da Sequência Fibonacci ###")
        #seleciona os números, ordena de forma decrescente e limita aos 'n' maiores (nesse caso de acordo com o pdf, 5)
        cursor.execute(f"SELECT NUM_FIBONACCI FROM SELECAO_TESTE ORDER BY NUM_FIBONACCI DESC LIMIT {n}")
        resultados = cursor.fetchall()

        if resultados:
            for i, res in enumerate(resultados):
                print(f"{i+1}º Maior: {res[0]}")
        else:
            print(f"Nenhum número Fibonacci encontrado para listar os {n} maiores.")

    except sqlite3.Error as e:
        print(f"Erro ao listar os {n} maiores números Fibonacci: {e}")
    finally:
        if conn:
            conn.close()

def f_qntdParesImpares():
    """
    Conta quantos números pares eímpares foram armazenados na tabela SELECAO_TESTE. 
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        print("\n--- Contagem de Números Pares e Ímpares ---")
        #verifica onde NUM_PAR é 1 para contar os pares que foram inseridos
        cursor.execute("SELECT COUNT(*) FROM SELECAO_TESTE WHERE NUM_PAR = 1")
        totalPares = cursor.fetchone()[0] #obtém o resultado da contagem
        print(f"Total de números pares: {totalPares}")

        #verifica onde NUM_IMPAR é 1 para contar os ímpares que foram inseridos
        cursor.execute("SELECT COUNT(*) FROM SELECAO_TESTE WHERE NUM_IMPAR = 1")
        totalImpares = cursor.fetchone()[0] #obtém o resultado da contagem
        print(f"Total de números ímpares: {totalImpares}")

    except sqlite3.Error as e:
        print(f"Erro ao contar pares e ímpares: {e}")
    finally:
        if conn:
            conn.close()

def f_excluirMaiorQue(valor):
    """
    Deleta todos os números da tabela SELECAO_TESTE que forem maiores que determinado valor escolhido lá embaixo. 
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        print(f"\n### Deletando números maiores que {valor} ###")
        cursor.execute("DELETE FROM SELECAO_TESTE WHERE NUM_FIBONACCI > ?", (valor,))
        registrosDeletados = cursor.rowcount #retorna o número de linhas afetadas pela operação
        conn.commit() #confirma a exclusão no banco de dados
        print(f"{registrosDeletados} registros deletados da tabela SELECAO_TESTE.") #exibe quantos registros foram deletados da tabela

    except sqlite3.Error as e:
        print(f"Erro ao deletar números: {e}")
    finally:
        if conn:
            conn.close()

# *******************************************************
# **************** EXECUÇÃO PRINCIPAL *******************
# *******************************************************

if __name__ == "__main__":
    #1-cria o banco de dados e as tabelas, garantindo que o ambiente esteja pronto.
    f_criarTabelas()

    #definição do nome do candidato para inserção inicial.
    nomeCandidato = "Gustavo Saraiva"

    #2-insere o candidato na tabela SELECAO_CANDIDATO.
    #o id do candidato inserido é capturado para ser usado como chave estrangeira na tabela de testes.
    idCandidatoInserido = f_inserirCandidato(nomeCandidato) 

    if idCandidatoInserido: #verifica se a inserção do candidato funcionou corretamente
        #3-insere 30 registros na tabela SELECAO_TESTE com base na sequência de Fibonacci.
        f_inserirTestesFibonacci(idCandidatoInserido)
    else:
        print("Não foi possível inserir os testes de Fibonacci sem um ID de candidato válido.")

    #3.execução das consultas SQL solicitadas no enunciado do problema para análise dos dados.
    #Liste a sequência Fibonacci.
    f_listarSequenciaFibonacci()

    #Liste os 5 maiores números da sequência inserida.
    f_listarMaioresNumeros(5)

    #Conte quantos números pares e quantos ímpares foram armazenados.
    f_qntdParesImpares()

    #Delete todos os números que forem maiores que 5000.
    f_excluirMaiorQue(5000)

    #Liste a sequência Fibonacci. (para verificar se os números maiores que 5000 foram realmente excluídos)
    f_listarSequenciaFibonacci()