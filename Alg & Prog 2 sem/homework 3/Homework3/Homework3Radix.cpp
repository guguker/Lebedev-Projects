#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono> // �������� chrono ��� ������� �������

using namespace std;
using namespace std::chrono;

// ���������� ������� ���� ��� ������:)
// ���� ������� ��� - �������� �� ���� � �������� ������ :)
vector<int> combineBuckets(const vector<vector<int>>& buckets) {
    vector<int> combinedArray;
    for (const auto& bucket : buckets) {
        combinedArray.insert(combinedArray.end(), bucket.begin(), bucket.end());
    }
    return combinedArray;
}

// ��������� �� �������
void sortByDigit(vector<int>& arr, int digitPlace) {
    vector<vector<int>> buckets(10);
    for (int num : arr) {
        int bucketIndex = (num / digitPlace) % 10;
        buckets[bucketIndex].push_back(num);
    }
    arr = combineBuckets(buckets);
}

// ��� ���������� ������� ����������
void radixSort(vector<int>& arr) {
    int maxVal = *max_element(arr.begin(), arr.end());
    int digitPlace = 1;
    while (maxVal / digitPlace > 0) {
        sortByDigit(arr, digitPlace);
        digitPlace *= 10;
    }
}

// ������� ������ 20 ��������� ������� ��� �����������
void printFirstElements(const vector<int>& arr) {
    for (int i = 0; i < 20 && i < arr.size(); ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    srand(time(0));

    int N = 1000000000;        // <- ���������� ��������� �������
    int RANGE = 100; // <- �������� ��������

    vector<int> arr;
    arr.reserve(N); // ����������� ������ �������

    // ������ �� N ��������� ����� �� 1 �� RANGE
    for (int i = 0; i < N; ++i) {
        arr.push_back(rand() % RANGE + 1);
    }

    cout << "Original array (first 20 elements):\n";
    printFirstElements(arr);

    auto start = high_resolution_clock::now();

    radixSort(arr);

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - start);

    cout << "Sorted array (first 20 elements):\n";
    printFirstElements(arr);

    cout << "Time taken by radixSort: " << duration.count() << " milliseconds" << endl;

    return 0;
}