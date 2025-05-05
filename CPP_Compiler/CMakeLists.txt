cmake_minimum_required(VERSION 3.31)
project(CPP_Compiler)

set(CMAKE_CXX_STANDARD 23)

add_executable(CPP_Compiler main.cpp
        lexer/FileReader.cpp
        lexer/FileReader.h
        lexer/Lexer.cpp
        lexer/Lexer.h
        lexer/FileReader.h
        lexer/Lexer.h
        parser/Parser.cpp
        parser/Parser.h)
