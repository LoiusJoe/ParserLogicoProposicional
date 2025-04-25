# Diego Henrique Zanella
# Gabriel Hortmann de Campos Bueno
# Jonathan Domingos Rodrigues

import sys
import re

class TokenType:
    """Tipos de tokens que podem ser encontrados na expressão lógica."""
    TRUE = "TRUE"
    FALSE = "FALSE"
    PROPOSICAO = "PROPOSICAO"
    ABRE_PAREN = "ABRE_PAREN"
    FECHA_PAREN = "FECHA_PAREN"
    NEG = "NEG"
    WEDGE = "WEDGE"
    VEE = "VEE"
    RIGHTARROW = "RIGHTARROW"
    LEFTRIGHTARROW = "LEFTRIGHTARROW"
    EOF = "EOF"
    INVALID = "INVALID"

class Token:
    """Representa um token na expressão lógica."""
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

class LexicalAnalyzer:
    """Analisador léxico que simula uma máquina de estados finitos."""
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0
        self.current_char = self.input[0] if len(self.input) > 0 else None

    def advance(self):
        """Avança para o próximo caractere."""
        self.position += 1
        if self.position < len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        """Ignora espaços em branco."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        """Retorna o próximo token na expressão."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Constantes booleanas
            if self.match_sequence("true"):
                return Token(TokenType.TRUE, "true")
            
            if self.match_sequence("false"):
                return Token(TokenType.FALSE, "false")

            # Parênteses
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.ABRE_PAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.FECHA_PAREN, ')')

            # Operadores LaTeX
            if self.current_char == '\\':
                if self.match_sequence("\\neg"):
                    return Token(TokenType.NEG, "\\neg")
                
                if self.match_sequence("\\wedge"):
                    return Token(TokenType.WEDGE, "\\wedge")
                
                if self.match_sequence("\\vee"):
                    return Token(TokenType.VEE, "\\vee")
                
                if self.match_sequence("\\rightarrow"):
                    return Token(TokenType.RIGHTARROW, "\\rightarrow")
                
                if self.match_sequence("\\leftrightarrow"):
                    return Token(TokenType.LEFTRIGHTARROW, "\\leftrightarrow")

                # Se chegou aqui, é um operador inválido
                start_pos = self.position
                while self.current_char is not None and not self.current_char.isspace() and self.current_char != '(' and self.current_char != ')':
                    self.advance()
                return Token(TokenType.INVALID, self.input[start_pos:self.position])

            # Proposições (começam com um dígito)
            if self.current_char.isdigit():
                return self.get_proposicao()

            # Caractere inválido
            invalid_char = self.current_char
            self.advance()
            return Token(TokenType.INVALID, invalid_char)

        # Fim da entrada
        return Token(TokenType.EOF, None)

    def match_sequence(self, sequence):
        """Verifica se a sequência começa na posição atual e avança se sim."""
        if self.position + len(sequence) <= len(self.input):
            if self.input[self.position:self.position + len(sequence)] == sequence:
                self.position += len(sequence)
                if self.position < len(self.input):
                    self.current_char = self.input[self.position]
                else:
                    self.current_char = None
                return True
        return False

    def get_proposicao(self):
        """Extrai uma proposição (dígito seguido de dígitos ou letras minúsculas)."""
        start_pos = self.position
        # Primeiro caractere deve ser um dígito (já verificado antes da chamada)
        self.advance()
        
        # Caracteres seguintes podem ser dígitos ou letras minúsculas
        while (self.current_char is not None and 
               (self.current_char.isdigit() or (self.current_char.isalpha() and self.current_char.islower()))):
            self.advance()
            
        value = self.input[start_pos:self.position]
        
        # Verificar se segue o padrão correto: [0-9][0-9a-z]*
        if re.match(r'^[0-9][0-9a-z]*$', value):
            return Token(TokenType.PROPOSICAO, value)
        else:
            return Token(TokenType.INVALID, value)

class Parser:
    """Parser LL(1) para a gramática de expressões lógicas."""
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected):
        """Gera um erro de parsing."""
        raise SyntaxError(f"Erro de sintaxe: esperado {expected}, encontrado {self.current_token.type}")

    def eat(self, token_type):
        """Consome o token atual se ele for do tipo esperado."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def parse(self):
        """Inicia o processo de parsing."""
        self.formula()
        # Após analisar a fórmula, devemos ter chegado ao fim da entrada
        if self.current_token.type != TokenType.EOF:
            raise SyntaxError("Tokens extras após o fim da expressão")
        return True

    def formula(self):
        """
        FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA
        """
        if self.current_token.type in (TokenType.TRUE, TokenType.FALSE):
            # CONSTANTE
            self.eat(self.current_token.type)
        elif self.current_token.type == TokenType.PROPOSICAO:
            # PROPOSICAO
            self.eat(TokenType.PROPOSICAO)
        elif self.current_token.type == TokenType.ABRE_PAREN:
            # Pode ser FORMULAUNARIA ou FORMULABINARIA
            self.eat(TokenType.ABRE_PAREN)
            
            if self.current_token.type == TokenType.NEG:
                # FORMULAUNARIA
                self.eat(TokenType.NEG)
                self.formula()
                self.eat(TokenType.FECHA_PAREN)
            elif self.current_token.type in (TokenType.WEDGE, TokenType.VEE, TokenType.RIGHTARROW, TokenType.LEFTRIGHTARROW):
                # FORMULABINARIA
                self.eat(self.current_token.type)  # consome o operador binário
                self.formula()  # primeira fórmula
                self.formula()  # segunda fórmula
                self.eat(TokenType.FECHA_PAREN)
            else:
                self.error("operador")
        else:
            self.error("fórmula válida")

def validate_expression(expression):
    """Valida uma expressão lógica."""
    try:
        lexer = LexicalAnalyzer(expression)
        parser = Parser(lexer)
        parser.parse()
        return "valida"
    except Exception as e:
        return "invalida"

def main():
    """Função principal."""
    if len(sys.argv) != 2:
        print("Uso: python validador.py arquivo_entrada.txt")
        return

    try:
        with open(sys.argv[1], 'r') as file:
            lines = file.readlines()
            
            # Primeira linha contém o número de expressões
            num_expressions = int(lines[0].strip())
            
            # Validar cada expressão
            for i in range(1, min(num_expressions + 1, len(lines))):
                expression = lines[i].strip()
                result = validate_expression(expression)
                print(result)
                
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {sys.argv[1]}")
    except ValueError:
        print("Formato inválido na primeira linha do arquivo")

if __name__ == "__main__":
    main()
