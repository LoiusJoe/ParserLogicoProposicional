# Validador de Expressões Lógicas em Notação LaTeX

Um analisador léxico e sintático para expressões de lógica proposicional escritas em notação LaTeX. Este projeto implementa uma máquina de estados finitos para análise léxica e um parser LL(1) para validação sintática de expressões lógicas.

## Descrição

Este validador é capaz de analisar expressões de lógica proposicional escritas em notação LaTeX e determinar se estão lexical e gramaticalmente corretas. O sistema valida apenas a forma da expressão, seguindo rigorosamente a gramática definida.

### Gramática Suportada

```
FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA
CONSTANTE = true | false
PROPOSICAO = [0-9][0-9a-z]*
FORMULAUNARIA = ABREPAREN OPERADORUNARIO FORMULA FECHAPAREN
FORMULABINARIA = ABREPAREN OPERATORBINARIO FORMULA FORMULA FECHAPAREN
ABREPAREN = (
FECHAPAREN = )
OPERATORUNARIO = \neg
OPERATORBINARIO = \wedge | \vee | \rightarrow | \leftrightarrow
```

O validador suporta:
- Valores lógicos constantes (`true` e `false`)
- Proposições que começam com um dígito, seguidas por zero ou mais dígitos ou letras minúsculas
- Fórmulas unárias com o operador `\neg` (negação)
- Fórmulas binárias com operadores `\wedge` (AND), `\vee` (OR), `\rightarrow` (implicação) e `\leftrightarrow` (bi-implicação)
- Combinações aninhadas de qualquer complexidade dessas expressões

## Funcionalidades

- Análise léxica através de uma máquina de estados finitos
- Análise sintática usando um parser LL(1)
- Validação de balanceamento de parênteses
- Verificação da correta formação de proposições
- Validação da estrutura de operadores unários e binários

## Uso

1. Crie um arquivo de texto (ou utilize os arquivos dados como exemplo) com as expressões lógicas a serem validadas:
   - A primeira linha deve conter um número inteiro indicando quantas expressões estão no arquivo
   - Cada linha subsequente deve conter uma expressão lógica a ser validada

   Exemplo de arquivo (`entrada.txt`):
   ```
   5
   true
   (\neg 0)
   (\wedge 0 1)
   (\vee true false)
   (\leftrightarrow 0 (\wedge 1 2))
   ```

2. Execute o validador:
   ```
   python validador.py entrada.txt
   ```

3. O programa gerará uma saída para cada expressão, indicando se é "valida" ou "invalida".

### Exemplos de Expressões Válidas

- `true`
- `false`
- `0`
- `0abc123`
- `(\neg 0)`
- `(\wedge 0 1)`
- `(\vee true false)`
- `(\rightarrow (\neg 0) 1)`
- `(\leftrightarrow 0 (\wedge 1 2))`
- `(\neg (\wedge 0 (\vee 1 2)))`

### Exemplos de Expressões Inválidas

- `false)` - Parêntese desbalanceado
- `\neg 0` - Falta de parênteses para operador unário
- `(\wedge 0)` - Operador binário com apenas um argumento
- `(\vee P0 1)` - Proposição inválida (não começa com dígito)
- `(\rightarrow (\neg 0) (abc))` - Proposição inválida (não começa com dígito)

## Estrutura do Projeto

- `validador.py`: O código principal contendo o analisador léxico e o parser
- `arquivo_entrada.txt`, `arq2.txt`, `arq..3.txt`: arquivos de exemplo para teste

## Detalhes de Implementação

### Analisador Léxico

O analisador léxico implementa uma máquina de estados finitos que converte a entrada em uma sequência de tokens:
- Identifica constantes lógicas (`true`, `false`)
- Reconhece proposições que seguem o padrão `[0-9][0-9a-z]*`
- Detecta operadores lógicos (`\neg`, `\wedge`, `\vee`, `\rightarrow`, `\leftrightarrow`)
- Identifica parênteses de abertura e fechamento

### Parser LL(1)

O parser implementa uma análise descendente recursiva (top-down), consumindo os tokens e verificando se seguem as regras da gramática:
- Verifica se a estrutura da expressão segue a gramática definida
- Valida que os operadores unários e binários são usados corretamente
- Confirma que as proposições seguem o formato especificado
