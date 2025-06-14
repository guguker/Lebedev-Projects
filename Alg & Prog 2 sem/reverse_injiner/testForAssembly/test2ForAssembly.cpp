#include <iostream>

int main() {
    int rows, cols;

    std::cout << "������� ���������� �����: ";
    std::cin >> rows;
    std::cout << "������� ���������� ��������: ";
    std::cin >> cols;

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            // ��������� ������� � ��������
            if (i % 2 == 0) {
                if (j % 2 == 0) {
                    std::cout << "[" << i << "," << j << "] � ��� ���������� ������\n";
                }
                else {
                    std::cout << "[" << i << "," << j << "] � i ������, j ��������\n";
                }
            }
            else {
                if (j % 3 == 0) {
                    std::cout << "[" << i << "," << j << "] � i ��������, j ������ 3\n";
                }
                else {
                    std::cout << "[" << i << "," << j << "] � i ��������, j �� ������ 3\n";
                }
            }
        }
    }

    return 0;
}