from PyQt6 import QtCore, QtGui, QtWidgets
import time

class Node:
    """Node của cây nhị phân tìm kiếm (BST)."""
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert_bst(root, key):
    """Chèn một giá trị vào cây."""
    if root is None:
        return Node(key)
    else:
        if root.val < key:
            root.right = insert_bst(root.right, key)
        else:
            root.left = insert_bst(root.left, key)
    return root

def tree_to_list(root, result, depth=0):
    """Chuyển cây thành danh sách các giá trị theo chiều sâu."""
    if root:
        if len(result) <= depth:
            result.append([])
        result[depth].append(root.val)
        tree_to_list(root.left, result, depth + 1)
        tree_to_list(root.right, result, depth + 1)

class SortVisualizationWidget(QtWidgets.QWidget):
    def __init__(self, data, sort_type="heap", parent=None):
        super().__init__(parent)
        self.data = data
        self.sort_type = sort_type
        self.animation_speed = 1.6  # Tốc độ hoạt hình
        self.setWindowTitle("Mô Phỏng Thuật Toán Sắp Xếp")
        self.resize(700, 400)

        # Scene và View để vẽ biểu đồ
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 680, 380)

        # Các nút để chọn thuật toán và bắt đầu
        self.start_button = QtWidgets.QPushButton("Bắt đầu Sắp Xếp", self)
        self.start_button.setGeometry(10, 360, 200, 30)
        self.start_button.clicked.connect(self.start_sorting)

        self.draw_data(self.data, ['red' for _ in range(len(self.data))])

    def build_tree(self, data):
        """Xây dựng cây nhị phân từ dữ liệu."""
        root = None
        for value in data:
            root = insert_bst(root, value)
        return root

    def draw_tree(self, root, color_array):
        """Vẽ cây nhị phân từ gốc."""
        self.scene.clear()
        node_list = []
        tree_to_list(root, node_list)
        c_height = 360
        c_width = 680
        spacing = 5

        for depth, nodes in enumerate(node_list):
            x_spacing = c_width / (len(nodes) + 1)
            y_pos = depth * (c_height / len(node_list))
            for i, value in enumerate(nodes):
                x_pos = (i + 1) * x_spacing
                color = color_array[depth]  # Sử dụng màu sắc khác nhau cho từng độ sâu
                self.draw_node(value, x_pos, y_pos, color)

    def draw_node(self, value, x, y, color):
        """Vẽ một node tại vị trí x, y với màu."""
        rect = QtWidgets.QGraphicsRectItem(x - 15, y - 15, 30, 30)
        rect.setBrush(QtGui.QColor(color))
        self.scene.addItem(rect)
        text = QtWidgets.QGraphicsTextItem(str(value))
        text.setPos(x - 10, y - 10)
        self.scene.addItem(text)

    def heapify(self, data, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and data[left] > data[largest]:
            largest = left

        if right < n and data[right] > data[largest]:
            largest = right

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            self.draw_tree(self.build_tree(data), ['green' if x == i or x == largest else 'red' for x in range(len(data))])
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed / 2)
            self.heapify(data, n, largest)

    def heap_sort_visualization(self, data):
        n = len(data)

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(data, n, i)

        for i in range(n - 1, 0, -1):
            data[i], data[0] = data[0], data[i]
            self.draw_tree(self.build_tree(data), ['green' if x == 0 or x == i else 'red' for x in range(len(data))])
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed / 2)
            self.heapify(data, i, 0)

    def insertion_sort_visualization(self, data):
        """Insertion Sort với cập nhật biểu đồ"""
        n = len(data)

        for i in range(1, n):
            key_item = data[i]
            j = i - 1
            while j >= 0 and data[j] > key_item:
                data[j + 1] = data[j]
                j -= 1

                # Vẽ lại biểu đồ với màu sắc thay đổi
                self.draw_data(data, ['green' if k == j + 1 or k == i else 'red' for k in range(n)])
                QtCore.QCoreApplication.processEvents()
                time.sleep(self.animation_speed / 2)  # Giảm thời gian để hoạt hình mượt mà hơn

            data[j + 1] = key_item
            self.draw_data(data, ['green' if k == j + 1 else 'red' for k in range(n)])  # Chỉ sử dụng 2 màu

        # Vẽ biểu đồ hoàn thành
        self.draw_data(data, ['green' for _ in range(n)])

    def draw_data(self, data, color_array):
        """Vẽ biểu đồ cột từ dữ liệu và tô màu cột (hỗ trợ giá trị âm)"""
        self.scene.clear()
        c_height = 360
        c_width = 680
        x_width = c_width / (len(data) + 1)
        offset = 20
        spacing = 5

        max_value = max(map(abs, data))  # Lấy giá trị tuyệt đối lớn nhất
        zero_line = c_height / 2  # Đường trung tâm cho giá trị 0

        for i, value in enumerate(data):
            normalized_height = abs(value) / max_value  # Chiều cao chuẩn hóa
            height = normalized_height * (c_height / 2 - 10)  # Chiều cao cột

            # Tính tọa độ Y cho cột
            if value >= 0:
                y0 = zero_line - height
            else:
                y0 = zero_line

            # Vị trí X và kích thước cột
            x0 = i * x_width + offset + spacing
            x1 = x_width - spacing + 5  # Tăng kích thước cột
            y1 = height

            # Vẽ cột và tô màu
            rect = QtWidgets.QGraphicsRectItem(x0, y0, x1, y1)
            rect.setBrush(QtGui.QColor(color_array[i]))
            self.scene.addItem(rect)

            # Hiển thị giá trị lên cột (canh chỉnh đúng vị trí)
            text = QtWidgets.QGraphicsTextItem(str(value))
            if value >= 0:
                text.setPos(x0 + spacing, y0 - 20)
            else:
                text.setPos(x0 + spacing, y0 + height + 5)
            self.scene.addItem(text)

        # Vẽ đường trung tâm (giá trị 0)
        zero_line_pen = QtGui.QPen(QtGui.QColor("black"), 2)
        self.scene.addLine(offset, zero_line, c_width, zero_line, zero_line_pen)

    def start_sorting(self):
        """Khởi chạy thuật toán sắp xếp theo loại"""
        if self.sort_type == "heap":
            self.heap_sort_visualization(self.data)
        elif self.sort_type == "insertion":
            self.insertion_sort_visualization(self.data)
