from PyQt6 import QtCore, QtGui, QtWidgets
import time
# Các cách duyệt cây của thuật toán
def preorder_traversal(data, n, i, result):
    """Duyệt cây theo thứ tự trước (Preorder)"""
    if i < n:
        result.append(data[i])
        preorder_traversal(data, n, 2 * i + 1, result)
        preorder_traversal(data, n, 2 * i + 2, result)

def inorder_traversal(data, n, i, result):
    """Duyệt cây theo thứ tự giữa (Inorder)"""
    if i < n:
        inorder_traversal(data, n, 2 * i + 1, result)
        result.append(data[i])
        inorder_traversal(data, n, 2 * i + 2, result)

def postorder_traversal(data, n, i, result):
    """Duyệt cây theo thứ tự sau (Postorder)"""
    if i < n:
        postorder_traversal(data, n, 2 * i + 1, result)
        postorder_traversal(data, n, 2 * i + 2, result)
        result.append(data[i])
# Sử dụng đệ quy để đảm bảo tính chất đống của thuật toán
def heapify(data, n, i, key_index, draw_data_callback=None):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and data[left][key_index] > data[largest][key_index]:
        largest = left

    if right < n and data[right][key_index] > data[largest][key_index]:
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        if draw_data_callback:
            draw_data_callback(data, ['yellow' if x == i else 'blue' if x == largest else 'red' for x in range(len(data))])
            QtCore.QCoreApplication.processEvents()
            time.sleep(1.6 / 2)
        heapify(data, n, largest, key_index, draw_data_callback)

def heap_sort(data, key_index, draw_data_callback=None):
    n = len(data)

    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, key_index, draw_data_callback)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        if draw_data_callback:
            draw_data_callback(data, ['purple' if x == 0 else 'orange' if x == i else 'green' if x > i else 'red' for x in range(len(data))])
            QtCore.QCoreApplication.processEvents()
            time.sleep(1.6 / 2)
        heapify(data, i, 0, key_index, draw_data_callback)

    return data

def insertion_sort(data, key_index, n=None, draw_data_callback=None):
    if n is None:
        n = len(data)

    if n <= 1:
        return

    # Gọi đệ quy cho n-1 phần tử đầu tiên
    insertion_sort(data, key_index, n - 1, draw_data_callback)

    # Chèn phần tử cuối cùng vào vị trí phù hợp
    last = data[n - 1]
    j = n - 2

    while j >= 0 and last[key_index] < data[j][key_index]:
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


