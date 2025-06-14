#include <iostream>
#include <string>

int secretFunction(int x) {
    int result = (x * 42 + 13) ^ 0x5A;
    return result;
}


int main() {
    std::string password;
    std::cout << "Enter password: ";
    std::cin >> password;

    if (password == "ozon_lutshe_chem_vash") {
        std::cout << "Access granted.\n";
        int key = secretFunction(1337);
        std::cout << "Secret key is: " << key << "\n";
    }
    else {
        std::cout << "Access denied.\n";
    }

    return 0;
}