#ifndef LEXER_H
#define LEXER_H
#include <string>
#include <vector>
#include <regex>

enum class TokenType {
    class_definition,
    class_name,
    function_definition,
    function_name,
    Colon,
    open_parenthesis,
    close_parenthesis,
    parent_class,
    return_type_operator,
    type_name,
    Comma,
    Comment,
    Error,
    Eof
};

struct Token {
    TokenType type;
    std::string value;
    size_t position;
};

enum class State {
    Default,
    ExpectClassName,
    ExpectParentClass,
    ExpectReturnType
};

class Lexer {
private:
    std::string sourceCode;
    size_t position;
    State currentState = State::Default;
    std::vector<std::pair<std::regex, TokenType>> regexPatterns;

    void skipWhitespace();
    Token processComment();

public:
    explicit Lexer(const std::string& source);
    Token getNextToken();
    std::vector<Token> getAllTokens();
};

#endif // LEXER_H