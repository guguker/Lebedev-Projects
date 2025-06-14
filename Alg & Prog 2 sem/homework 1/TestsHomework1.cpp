#include "pch.h"
#include "CppUnitTest.h"
#include "../CodeHomework1/CodeHomework1.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTest1
{
    TEST_CLASS(UnitTest1)
    {
    public:
        // ��������, ��� createArray ��������� ������ ������ ���������� �������
        TEST_METHOD(TestCreateArraySize)
        {
            int size = 5;
            std::vector<int> arr = createArray(size);
            Assert::AreEqual(size, static_cast<int>(arr.size()), L"Array size should match input size");
        }

        // ��������, ��� createArray ������ ������ � ����������� ����������
        TEST_METHOD(TestCreateArrayValues)
        {
            std::vector<int> arr = createArray(5);
            for (int i = 0; i < 5; i++)
            {
                Assert::AreEqual(i, arr[i], L"Array values should be sequential from 0");
            }
        }

        // �������� ������ removeElements (������ ������ ���� ������ ����� ��������)
        TEST_METHOD(TestRemoveElements)
        {
            std::vector<int> arr = createArray(10);
            removeElements(arr);
            Assert::IsTrue(arr.empty(), L"Array should be empty after removeElements");
        }

        // �������� ������ removeElements �� ������ ������� (�� ������ ���� ������)
        TEST_METHOD(TestRemoveEmptyArray)
        {
            std::vector<int> arr;
            removeElements(arr);
            Assert::IsTrue(arr.empty(), L"Removing from an empty array should not cause issues");
        }

        // ���� �� �������� � ������� ������� �� 1 ���. ���������
        TEST_METHOD(TestOneMillion)
        {
            int size = 1000000;
            std::vector<int> arr = createArray(size);
            Assert::AreEqual(size, static_cast<int>(arr.size()), L"Array size should match input size for 1 million");

            removeElements(arr);
            Assert::IsTrue(arr.empty(), L"Array should be empty after removeElements for 1 million elements");
        }

        // ���� �� �������� � ������� ������� �� 10 ���. ���������
        TEST_METHOD(TestTenMillion)
        {
            int size = 10000000;
            std::vector<int> arr = createArray(size);
            Assert::AreEqual(size, static_cast<int>(arr.size()), L"Array size should match input size for 10 million");

            removeElements(arr);
            Assert::IsTrue(arr.empty(), L"Array should be empty after removeElements for 10 million elements");
        }
    };
}
