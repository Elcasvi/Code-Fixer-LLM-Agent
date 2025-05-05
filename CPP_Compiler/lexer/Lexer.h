#ifndef LEXER_H
#define LEXER_H
#include <string>
#include <vector>
#include <regex>

// Full definitions need to be in header
enum class TokenType {
    Keyword,
    Identifier,
    Literal,
    Punctuation,
    Comment,
    Error
};

struct Token {
    TokenType type;
    std::string value;
    size_t position;
};

class Lexer {
private:
    std::string sourceCode;
    size_t position;
    std::vector<std::pair<std::regex, TokenType>> regexPatterns;

    void skipWhitespace();
    Token processComment();

public:
    explicit Lexer(const std::string& source);
    Token getNextToken();
};

#endif // LEXER_H