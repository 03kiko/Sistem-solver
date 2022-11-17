# --Equations System solver--
def produto_interno(tuplo1, tuplo2):
    """
    Devolve o produto interno de dois vetores.

    Argumentos:
        tuplo1: tuplo (constituído por números inteiros ou reais)
        tuplo2: tuplo (constituído por números inteiros ou reais)
    No fundo, é feito o produto interno entre dois tuplos, que representam
    vetores, com igual dimensão. O resultado do produto interno é
    apresentado como um número real.

    produto_interno: tuplo x tuplo --> real
    """
    
    produto=0.0
    
    for i in range(len(tuplo1)):
        produto+=tuplo1[i]*tuplo2[i]
    
    return produto


def verifica_convergencia(matriz, vetor_c, sol_atual_x,precisao):
    """
    Devolve True ou False consoante se verifique que o valor absoluto do erro de todas as equações é inferior à precisão recebida.
    
    Argumentos:
        matriz: tuplo (é quadrada, os elementos são tuplos e representam as
                       linhas da matriz e cada linha contém os seus coeficientes)
        vetor_c:tuplo (tamanho igual à matriz)
        sol_atual_x: tuplo (tamanho igual à matriz)
        precisão: real
    No fundo, calcula-se o erro fazendo o valor absoluto da diferença 
    entre o produto interno dos coeficientes de cada linha e a solução
    atual de x e a constante respetiva dessa linha. Se o erro for inferior
    à precisão em todas as linhas é devolvido True, senão é devolvido False. 
    
    verifica_convergencia: tuplo x tuplo x tuplo x real --> booleano
    """
    
    contador=0
    
    for i_linha in range(len(matriz)):
        fi_x=produto_interno(matriz[i_linha],sol_atual_x)
    
        if abs(fi_x-vetor_c[i_linha])<precisao:
            contador+=1    
    
    return contador==len(matriz)


def retira_zeros_diagonal(matriz,constantes):
    """
    Devolve um tuplo cujos elementos são a matriz e o vetor das constantes mas com as linhas/números trocadas(os) retirando-se eventuais 0s das diagonais da matriz. 
    
    Argumentos:
        matriz: tuplo (é quadrada, os elementos são tuplos e representam as
                       linhas da matriz e cada linha contém os seus coeficientes)
        vetor_c:tuplo (tamanho igual à matriz)
    No fundo, esta devolve uma nova matriz com as mesmas linhas da recebida
    no argumento, mas com as linhas trocadas de modo a que não existam 0s nas
    diagonais. O mesmo acontece com o vetor das constantes que acompanha
    a reordenação.
    
    retira_zeros_diagonal: tuplo x tuplo --> tuplo x tuplo
    """

    matriz_lista=list(matriz)
    constantes_lista=list(constantes)
    
    for i_linha in range(len(matriz_lista)):
        
        if matriz_lista[i_linha][i_linha]==0:
            
            for j_linha in range(len(matriz_lista)):
                
                if matriz_lista[j_linha][i_linha]!=0 and matriz_lista[i_linha][j_linha]!=0:
                    matriz_lista[i_linha],matriz_lista[j_linha]=matriz_lista[j_linha],matriz_lista[i_linha]
                    constantes_lista[i_linha]=constantes_lista[j_linha]
                    constantes_lista[j_linha]=constantes[i_linha]
                    break
        
        #A troca de linhas é feita da seguinte forma: ao encontrar
        #um 0 na coluna "i" correspondente à diagonal de uma linha "i", esta é
        #trocada pela primeira linha "j" que encontrar, procurando desde o início
        #da matriz, que não contenha um 0 na coluna "i", sempre que na linha "i" 
        #não exista um 0 na coluna "j".

    return (tuple(matriz_lista),tuple(constantes_lista))



def eh_diagonal_dominante(matriz):
    """
    Devolve True caso esta seja diagonal dominante, caso contrário devolve False.

    Argumentos:
        matriz: tuplo (é quadrada, os elementos são tuplos e representam as
                       linhas da matriz e cada linha contém os seus coeficientes)
    No fundo, verifica-se se para todas as linhas se o valor
    absoluto do coeficiente da diagonal da linha é maior ou igual que a
    soma dos restantes coeficientes da linha.Se isso se verificar então,
    a matriz é diagonal dominante. 
    
    eh_diagonal_dominante: tuplo --> booleano
    """
    
    contador=0
    for linha in range(len(matriz)):

        soma=0
        
        for items_excepto_diagonal in range(len(matriz[linha])):
            
            if matriz[linha][linha]!=matriz[linha][items_excepto_diagonal]:
                soma+=abs(matriz[linha][items_excepto_diagonal])
        
        if abs(matriz[linha][linha])>=soma:
            contador+=1
    
    return len(matriz)==contador


def resolve_sistema(matriz,constantes,precisao):
    """
    Devolve um tuplo que é a solução do sistema aplicando o método de Jacobi.

    Argumentos:
        matriz: tuplo (é quadrada, os elementos são tuplos e representam as
                       linhas da matriz e cada linha contém os seus coeficientes)
        vetor_c:tuplo (tamanho igual à matriz)
        precisao: real (positivo)
    No fundo, esta função recorre às funções "eh_diagonal_dominante",
    "retira_zero_diagonal","verifica_convergencia" e "produto_interno e 
    aplica o método de Jacobi para resolver o sistema. A função auxiliar
    "validar_argumentos", gera ValueError com a mensagem: "resolve_sistema:
    argumentos inválidos" em caso de existirem argumentos errados. Também se
    a matriz não for diagonal dominante gera-se ValueError com a mensagem:
    "resolve_sistema: matriz nao diagonal dominante".

    resolve_sistema: tuplo x tuplo x real --> tuplo
    """

    def validar_argumentos(matriz,constantes,precisao):
        if (matriz==() or 
            constantes==() or
            not isinstance(matriz,tuple) or
            not isinstance(constantes,tuple)):

            raise ValueError ('resolve_sistema: argumentos invalidos') 
            #Verifica se a matriz é um tuplo não vazio e se as constantes são tuplos.

        for linha in matriz: 
            
            if not isinstance(linha,tuple): 
                raise ValueError ('resolve_sistema: argumentos invalidos')
                #Verifica se cada linha da matriz é um tuplo.

            if len(matriz)!=len(linha): 
                raise ValueError ('resolve_sistema: argumentos invalidos')             
                #Verifica se a matriz é quadrada.
            
            for coeficiente in linha:
        
                if not isinstance(coeficiente,(int,float)): 
                    raise ValueError ('resolve_sistema: argumentos invalidos')
                    #Verifica se os coeficientes da matriz são reais ou inteiros.

        for constante in constantes:
            
            if not isinstance(constante,(int,float)):
                raise ValueError ('resolve_sistema: argumentos invalidos')                
                #Verifica se as constantes são reais ou inteiras.
        
        if len(matriz)!=len(constantes):
            raise ValueError ('resolve_sistema: argumentos invalidos')         
            #Verifica se existe o mesmo número de linhas na matriz que constantes.
        
        if not isinstance(precisao,float) or precisao<=0:
            raise ValueError ('resolve_sistema: argumentos invalidos')
            #Verifica se a precisão é um real positivo.

    validar_argumentos(matriz,constantes,precisao)
    
    zeros_retirados=retira_zeros_diagonal(matriz,constantes)
    matriz,constantes=zeros_retirados[0],zeros_retirados[1]

    
    if not eh_diagonal_dominante(matriz):
        raise ValueError ('resolve_sistema: matriz nao diagonal dominante')

    x=(0,)*len(matriz) #solução inicial igual a 0
    x_solucao=list(x)

    while not verifica_convergencia(matriz,constantes,x_solucao,precisao):
        
        for linha in range(len(matriz)):
            x_solucao[linha]=(x_solucao[linha] +
            (constantes[linha]-produto_interno(matriz[linha],x))/matriz[linha][linha])
        #Enquanto não se verificar a convergencia é feita uma nova estimativa
        #para a solução.

        x=tuple(x_solucao)
    
    return x
