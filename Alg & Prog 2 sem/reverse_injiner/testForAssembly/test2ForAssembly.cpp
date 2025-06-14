#include <iostream>

int main() {
    int rows, cols;

    std::cout << "¬ведите количество строк: ";
    std::cin >> rows;
    std::cout << "¬ведите количество столбцов: ";
    std::cin >> cols;

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            // ¬ложенные услови€ с примером
            if (i % 2 == 0) {
                if (j % 2 == 0) {
                    std::cout << "[" << i << "," << j << "] Ч обе координаты чЄтные\n";
                }
                else {
                    std::cout << "[" << i << "," << j << "] Ч i чЄтное, j нечЄтное\n";
                }
            }
            else {
                if (j % 3 == 0) {
                    std::cout << "[" << i << "," << j << "] Ч i нечЄтное, j кратно 3\n";
                }
                else {
                    std::cout << "[" << i << "," << j << "] Ч i нечЄтное, j не кратно 3\n";
                }
            }
        }
    }

    return 0;
}