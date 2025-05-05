#include <iostream>
#include "lexer/FileReader.h"
#include "lexer/Lexer.h"

int main() {
    const std::string code=read_file_to_string("../hello.py");
    Lexer lexer(code);

    Token token;
    do {
        token = lexer.getNextToken();
        std::cout << "Token: " << static_cast<int>(token.type)<< " Value: " << token.value << "\n";
    } while (!(token.type == TokenType::Error && token.value == "EOF"));

    return 0;
}