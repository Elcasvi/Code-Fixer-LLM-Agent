#include <iostream>
#include "lexer/FileReader.h"
#include "lexer/Lexer.h"
int main() {
    try {
        const std::string code = read_file_to_string("../hello.py");
        Lexer lexer(code);
        auto tokens = lexer.getAllTokens();

        for (const auto& token : tokens) {
            switch (token.type) {
                case TokenType::class_definition:
                    std::cout << "[CLASS_DEF] " << token.value << "\n";
                    break;
                case TokenType::class_name:
                    std::cout << "[CLASS_NAME] " << token.value << "\n";
                    break;
                case TokenType::function_definition:
                    std::cout << "[FUNC_DEF] " << token.value << "\n";
                    break;
                case TokenType::function_name:
                    std::cout << "[FUNC_NAME] " << token.value << "\n";
                    break;
                case TokenType::Colon:
                    std::cout << "[COLON] " << token.value << "\n";
                    break;
                case TokenType::open_parenthesis:
                    std::cout << "[OPEN_PAREN] " << token.value << "\n";
                    break;
                case TokenType::close_parenthesis:
                    std::cout << "[CLOSE_PAREN] " << token.value << "\n";
                    break;
                case TokenType::parent_class:
                    std::cout << "[PARENT_CLASS] " << token.value << "\n";
                    break;
                case TokenType::return_type_operator:
                    std::cout << "[RETURN_OP] " << token.value << "\n";
                    break;
                case TokenType::type_name:
                    std::cout << "[TYPE_NAME] " << token.value << "\n";
                    break;
                case TokenType::Comma:
                    std::cout << "[COMMA] " << token.value << "\n";
                    break;
                case TokenType::Comment:
                    std::cout << "[COMMENT] " << token.value << "\n";
                    break;
                case TokenType::Error:
                    std::cout << "[ERROR] " << token.value << "\n";
                    break;
                case TokenType::Eof:
                    std::cout << "[EOF] "<<token.value<<"\n";
                    break;
                default:
                    std::cout << "[UNKNOWN] " << token.value << "\n";
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
    return 0;
}