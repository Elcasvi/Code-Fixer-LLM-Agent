// Lexer.cpp
#include "Lexer.h"
#include <cctype>
#include <iostream>

void Lexer::skipWhitespace() {
    while (position < sourceCode.size() && std::isspace(sourceCode[position])) {
        ++position;
    }
}

Token Lexer::processComment() {
    size_t start = position;
    ++position; // Skip '#'
    while (position < sourceCode.size() && sourceCode[position] != '\n') {
        ++position;
    }
    return {TokenType::Comment, sourceCode.substr(start, position - start), start};
}

Lexer::Lexer(const std::string& source) : sourceCode(source), position(0) {
    regexPatterns = {
        // Class patterns first
        {std::regex(R"(\bclass\b)"), TokenType::class_definition},
        {std::regex(R"(\()"), TokenType::open_parenthesis},
        {std::regex(R"(\))"), TokenType::close_parenthesis},

        // Return type operator
        {std::regex(R"(->)"), TokenType::return_type_operator},

        // Other patterns
        {std::regex(R"(:)"), TokenType::Colon},
        {std::regex(R"(#[^\n]*)"), TokenType::Comment}
    };
}

Token Lexer::getNextToken() {
    while (true) {
        skipWhitespace();

        if (position >= sourceCode.size()) {
            return {TokenType::Eof, "$", position};
        }

        std::string remaining = sourceCode.substr(position);
        std::smatch match;

        // Handle states
        if (currentState == State::ExpectReturnType) {
            if (std::regex_search(remaining, match, std::regex(R"([a-zA-Z_][a-zA-Z0-9_]*)"), std::regex_constants::match_continuous)) {
                std::string value = match.str();
                size_t start = position;
                position += value.length();
                currentState = State::Default;
                return {TokenType::type_name, value, start};
            }
        } else if (currentState == State::ExpectParentClass) {
            if (std::regex_search(remaining, match, std::regex(R"([a-zA-Z_][a-zA-Z0-9_]*)"), std::regex_constants::match_continuous)) {
                std::string value = match.str();
                size_t start = position;
                position += value.length();
                return {TokenType::parent_class, value, start};
            } else if (sourceCode[position] == ',') {
                size_t start = position;
                position++;
                return {TokenType::Comma, ",", start};
            } else if (sourceCode[position] == ')') {
                size_t start = position;
                position++;
                currentState = State::Default;
                return {TokenType::close_parenthesis, ")", start};
            }
        } else if (currentState == State::ExpectClassName) {
            if (std::regex_search(remaining, match, std::regex(R"([a-zA-Z_][a-zA-Z0-9_]*)"), std::regex_constants::match_continuous)) {
                std::string value = match.str();
                size_t start = position;
                position += value.length();
                currentState = State::Default;
                return {TokenType::class_name, value, start};
            }
        }

        // Handle comments
        if (sourceCode[position] == '#') {
            return processComment();
        }

        // Match regex patterns
        for (const auto& [regex, type] : regexPatterns) {
            if (std::regex_search(remaining, match, regex, std::regex_constants::match_continuous)) {
                std::string value = match.str();
                size_t start = position;
                position += value.length();

                switch (type) {
                    case TokenType::class_definition:
                        currentState = State::ExpectClassName;
                        break;
                    case TokenType::open_parenthesis:
                        currentState = State::ExpectParentClass;  // <-- Key change
                        break;
                    case TokenType::Comma:
                        // Stay in ExpectParentClass
                        break;
                    case TokenType::return_type_operator:
                        currentState = State::ExpectReturnType;
                        break;
                    default:
                        break;
                }

                return {type, value, start};
            }
        }

        // Skip unrecognized characters
        position++;
    }
}


std::vector<Token> Lexer::getAllTokens() {
    std::vector<Token> tokens;
    Token token;
    do {
        token = getNextToken();
        tokens.push_back(token);
    } while (token.type != TokenType::Eof);
    return tokens;
}