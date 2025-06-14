#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono> // �������� chrono ��� ������� �������

using namespace std;
using namespace std::chrono;

// ��� ���������� ������ ����������
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false; // �����������: ���� ������ �� ���������� � ������ ��� ������������
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

// ������� ������
void printFirstElements(const vector<int>& arr, int count = 20) {
    for (int i = 0; i < count && i < arr.size(); ++i) {
        cout << arr[i] << " ";
    }
    cout << "\n";
}

int main() {
    srand(time(0));

    int N = 1000000;       // ���������� ��������� �����
    int RANGE = 100;       // �������� ��������

    vector<int> arr;
    arr.reserve(N);            // ����������� ������ �������

    // ������ �� N ��������� ����� �� 1 �� RANGE
    for (int i = 0; i < N; ++i) {
        arr.push_back(rand() % RANGE + 1);
    }

    cout << "Original array (first 20 elements):\n";
    printFirstElements(arr);

    // �������� ����� �������
    auto start = high_resolution_clock::now();

    bubbleSort(arr);

    // ����������� ����� �������
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - start);

    cout << "Sorted array (first 20 elements):\n";
    printFirstElements(arr);

    cout << "Time taken by bubbleSort: " << duration.count() << " milliseconds" << endl;

    return 0;
}