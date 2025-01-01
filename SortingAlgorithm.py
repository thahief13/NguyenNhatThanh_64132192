from PyQt6 import QtCore, QtGui, QtWidgets
import time
# Heapify cho việc duy trì tính chất đống của heap
def heapify(data, n, i, key_index, ascending=True, draw_data_callback=None):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and ((data[left][key_index] > data[largest][key_index]) if ascending else (data[left][key_index] < data[largest][key_index])):
        largest = left

    if right < n and ((data[right][key_index] > data[largest][key_index]) if ascending else (data[right][key_index] < data[largest][key_index])):
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        if draw_data_callback:
            draw_data_callback(data, ['yellow' if x == i else 'blue' if x == largest else 'red' for x in range(len(data))])
            QtCore.QCoreApplication.processEvents()
            time.sleep(1.6 / 2)
        heapify(data, n, largest, key_index, ascending, draw_data_callback)

# Sắp xếp heap
def heap_sort(data, key_index, ascending=True, draw_data_callback=None):
    n = len(data)

    # Xây dựng heap (chuyển đổi mảng thành heap)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, key_index, ascending, draw_data_callback)

    # Đẩy phần tử lớn nhất về cuối và gọi lại heapify cho phần còn lại
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        if draw_data_callback:
            draw_data_callback(data, ['purple' if x == 0 else 'orange' if x == i else 'green' if x > i else 'red' for x in range(len(data))])
            QtCore.QCoreApplication.processEvents()
            time.sleep(1.6 / 2)
        heapify(data, i, 0, key_index, ascending, draw_data_callback)

    return data

# Hàm sắp xếp Insertion Sort
def insertion_sort(data, key_index, n=None, ascending=True, draw_data_callback=None):
    if n is None:
        n = len(data)

    if n <= 1:
        return

    insertion_sort(data, key_index, n - 1, ascending, draw_data_callback)

    last = data[n - 1]
    j = n - 2

    while j >= 0 and ((last[key_index] < data[j][key_index]) if ascending else (last[key_index] > data[j][key_index])):
        data[j + 1] = data[j]
        j -= 1

        if draw_data_callback:
            draw_data_callback(data, ['yellow' if x == j + 1 else 'blue' if x == n - 1 else 'red' for x in range(len(data))])
            QtCore.QCoreApplication.processEvents()
            time.sleep(1.6 / 2)

    data[j + 1] = last

    if draw_data_callback:
        draw_data_callback(data, ['green' if x == j + 1 else 'red' for x in range(len(data))])

    return data