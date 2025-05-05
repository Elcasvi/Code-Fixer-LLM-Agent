#include "Lexer.h"
#include <string>
#include <regex>
#include <cctype>
using namespace std;

void Lexer::skipWhitespace() {
    while (position < sourceCode.size() && isspace(sourceCode[position])) {
        ++position;
    }
}

Token Lexer::processComment() {
    size_t start = position;
    ++position;//Skip #

    while (position < sourceCode.size() && sourceCode[position] != '\n') {
        ++position;
    }//Comment ends

    return {TokenType::Comment, sourceCode.substr(start, position - start), start};
}

Lexer::Lexer(const string& source) : sourceCode(source), position(0) {
    regexPatterns = {
        {regex(R"(\b(True|False|None|and|or|not|if|elif|else|for|while|break|continue|def|class|return|lambda|try|except|finally|raise|assert|with|as|is|in|nonlocal|global|yield|await|del|pass)\b)"), TokenType::Keyword},// Keywords (Python specific)
        {regex(R"(\d+(\.\d+)?)"), TokenType::Literal},// Literals (numbers only - you might want to add strings later)
        {regex(R"("(?:\\.|[^"\\])*")"), TokenType::Literal},  // Double quoted strings
        {regex(R"('(?:\\.|[^'\\])*')"), TokenType::Literal},   // Single quoted strings
        {regex(R"([a-zA-Z_]\w*)"), TokenType::Identifier},// Identifiers
        {std::regex(R"((==|!=|<=|>=|\+\+|\*\*|<<|>>|//|\+=|-=|\*=|\/=|%=))"), TokenType::Punctuation},// Punctuation (multi-character first!)
        {regex(R"([\(\)\{\}\[\]\.,;:=+\-*/%<>!&|^~@])"), TokenType::Punctuation}// Punctuation (Python operators and symbols)
    };
}

Token Lexer::getNextToken() {
    skipWhitespace();

    if (position >= sourceCode.size()) {
        return {TokenType::Error, "EOF", position};
    }


    if (sourceCode[position] == '#') {
        return processComment();
    }


    string remaining = sourceCode.substr(position);
    for (const auto& [regex, type] : regexPatterns) {
        smatch match;
        if (regex_search(remaining, match, regex, regex_constants::match_continuous)) {
            string value = match.str();
            size_t start = position;
            position += value.length();
            return {type, value, start};
        }
    }

    // Handle unrecognized token
    string errorVal(1, sourceCode[position]);
    size_t errorPos = position++;
    return {TokenType::Error, errorVal, errorPos};
}
