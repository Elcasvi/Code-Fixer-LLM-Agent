#include "FileReader.h"
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
using namespace std;
string read_file_to_string(const string& file_name) {
    cout << "Looking for file at: "<< filesystem::absolute(file_name) << "\n";

    const std::ifstream file(file_name);
    if (!file) {
        throw std::runtime_error("File could not be opened: " + file_name);
    }
    ostringstream file_content;
    file_content << file.rdbuf();
    return file_content.str();
}
