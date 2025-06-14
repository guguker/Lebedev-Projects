#include <iostream>

int main() {
    int rows, cols;

    std::cout << "Введите количество строк: ";
    std::cin >> rows;
    std::cout << "Введите количество столбцов: ";
    std::cin >> cols;

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            // Вложенные условия с примером
            if (i % 2 == 0) {
                if (j % 2 == 0) {
                    std::cout << "[" << i << "," << j << "] — обе координаты чётные\n";
                }
                else {
                    std::cout << "[" << i << "," << j << "] — i чётное, j нечётное\n";
                }
            }
            else {
                if (j % 3 == 0) {
                    std::cout << "[" << i << "," << j << "] — i нечётное, j кратно 3\n";
                }
                else {
                    std::cout << "[" << i << "," << j << "] — i нечётное, j не кратно 3\n";
                }
            }
        }
    }

    return 0;
}