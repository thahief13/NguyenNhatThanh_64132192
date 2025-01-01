from PyQt6 import QtCore, QtGui, QtWidgets
import time


class SortVisualizationWidget(QtWidgets.QWidget):
    def __init__(self, data, sort_type="heap", parent=None):
        super().__init__(parent)
        self.data = data
        self.sort_type = sort_type
        self.animation_speed = 1.6  # Default animation speed
        self.ascending = True  # Default sorting order
        self.setWindowTitle("Mô Phỏng Thuật Toán Sắp Xếp")
        self.resize(1000, 600)

        # Scene và View để vẽ
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 800, 400)

        # Thông tin hoạt động
        self.activity_label = QtWidgets.QLabel(self)
        self.activity_label.setGeometry(820, 10, 160, 300)
        self.activity_label.setWordWrap(True)
        self.activity_label.setText("Cách hoạt động của thuật toán sẽ được hiển thị tại đây.")

        # Nút bắt đầu sắp xếp
        self.start_button = QtWidgets.QPushButton("Bắt Đầu Sắp Xếp", self)
        self.start_button.setGeometry(820, 320, 160, 30)
        self.start_button.clicked.connect(self.start_sorting)

        # Slider để điều chỉnh tốc độ
        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.speed_slider.setGeometry(820, 360, 160, 30)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(6)  # Default speed (middle)
        self.speed_slider.valueChanged.connect(self.update_speed)

        # ComboBox để đổi thứ tự sắp xếp
        self.order_combobox = QtWidgets.QComboBox(self)
        self.order_combobox.setGeometry(820, 440, 160, 30)
        self.order_combobox.addItem("Tăng dần")
        self.order_combobox.addItem("Giảm dần")
        self.order_combobox.currentIndexChanged.connect(self.toggle_order)

        # Label hiển thị thời gian
        self.time_label = QtWidgets.QLabel("Thời gian: 0.0s", self)
        self.time_label.setGeometry(820, 480, 160, 30)

    def update_speed(self):
        """Cập nhật tốc độ sắp xếp khi thay đổi slider."""
        self.animation_speed = 1.6 / self.speed_slider.value()

    def toggle_order(self):
        """Đổi thứ tự sắp xếp (tăng dần/giảm dần)."""
        self.ascending = self.order_combobox.currentIndex() == 0

    def draw_heap_tree(self, data, highlight_node=None):
        """Vẽ cây nhị phân biểu diễn heap."""
        self.scene.clear()
        levels = len(data).bit_length()  # Số tầng của cây
        x_offset = self.view.width() // 2  # Tâm ngang
        y_step = 50  # Khoảng cách dọc giữa các tầng

        def draw_node(value, x, y, is_highlighted=False):
            """Vẽ một nút trong cây."""
            color = QtGui.QColor("red") if is_highlighted else QtGui.QColor("blue")
            ellipse = QtWidgets.QGraphicsEllipseItem(x - 15, y - 15, 30, 30)
            ellipse.setBrush(color)
            self.scene.addItem(ellipse)
            text = QtWidgets.QGraphicsTextItem(str(value))
            text.setPos(x - 10, y - 10)
            self.scene.addItem(text)

        def draw_edges(x1, y1, x2, y2):
            """Vẽ các đường nối."""
            line = QtWidgets.QGraphicsLineItem(x1, y1, x2, y2)
            self.scene.addItem(line)

        def recurse(index, x, y, step):
            if index >= len(data):
                return
            draw_node(data[index], x, y, index == highlight_node)
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            if left_child < len(data):
                draw_edges(x, y, x - step, y + y_step)
                recurse(left_child, x - step, y + y_step, step // 2)
            if right_child < len(data):
                draw_edges(x, y, x + step, y + y_step)
                recurse(right_child, x + step, y + y_step, step // 2)

        recurse(0, x_offset, 50, x_offset // 2)

    def draw_bar_chart(self, data, highlight_index=None):
        """Vẽ biểu đồ cột đại diện cho dữ liệu."""
        self.scene.clear()
        bar_width = 20
        spacing = 5
        max_height = 300
        x_offset = 10
        y_offset = 50

        max_value = max(data) if data else 1

        for i, value in enumerate(data):
            bar_height = (value / max_value) * max_height
            color = QtGui.QColor("blue") if i == highlight_index else QtGui.QColor("green")
            rect = QtWidgets.QGraphicsRectItem(x_offset + i * (bar_width + spacing), y_offset + max_height - bar_height, bar_width, bar_height)
            rect.setBrush(color)
            self.scene.addItem(rect)
            text = QtWidgets.QGraphicsTextItem(str(value))
            text.setPos(x_offset + i * (bar_width + spacing), y_offset + max_height - bar_height - 20)
            self.scene.addItem(text)

    def heapify(self, data, n, i):
        """Heapify dữ liệu tại chỉ mục i."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and ((data[left] > data[largest]) if self.ascending else (data[left] < data[largest])):
            largest = left

        if right < n and ((data[right] > data[largest]) if self.ascending else (data[right] < data[largest])):
            largest = right

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            self.draw_heap_tree(data, highlight_node=largest)
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed / 2)
            self.activity_label.setText(f"Hoán đổi {data[i]} và {data[largest]}...")  # Mô tả quá trình hoán đổi
            self.heapify(data, n, largest)

    def heap_sort_visualization(self, data):
        """Thuật toán Heap Sort với mô phỏng cây nhị phân."""
        n = len(data)
        start_time = time.time()

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(data, n, i)

        for i in range(n - 1, 0, -1):
            data[i], data[0] = data[0], data[i]
            self.draw_heap_tree(data, highlight_node=0)
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed / 2)
            self.activity_label.setText(f"Hoán đổi {data[i]} và {data[0]}...")  # Mô tả hoán đổi trong bước sắp xếp
            self.heapify(data, i, 0)

        end_time = time.time()
        self.time_label.setText(f"Thời gian: {end_time - start_time:.2f}s")
        self.activity_label.setText("Heap Sort đã hoàn tất!")

    def insertion_sort_visualization(self, data):
        """Thuật toán Insertion Sort với biểu đồ cột."""
        n = len(data)
        start_time = time.time()

        for i in range(1, n):
            key_item = data[i]
            j = i - 1
            while j >= 0 and ((key_item < data[j]) if self.ascending else (key_item > data[j])):
                data[j + 1] = data[j]
                j -= 1
                self.draw_bar_chart(data, highlight_index=j + 1)
                QtCore.QCoreApplication.processEvents()
                time.sleep(self.animation_speed / 2)
                self.activity_label.setText(f"Đang di chuyển {data[j + 1]}...")  # Mô tả di chuyển số
            data[j + 1] = key_item
            self.draw_bar_chart(data, highlight_index=i)
            self.activity_label.setText(f"Đã chèn {key_item} vào vị trí đúng.")  # Mô tả việc chèn số vào đúng vị trí

        end_time = time.time()
        self.time_label.setText(f"Thời gian: {end_time - start_time:.2f}s")
        self.activity_label.setText("Insertion Sort đã hoàn tất!")

    def start_sorting(self):
        """Bắt đầu sắp xếp."""
        if self.sort_type == "heap":
            self.activity_label.setText("Đang thực hiện Heap Sort...")  # Cập nhật mô tả
            self.heap_sort_visualization(self.data)
        elif self.sort_type == "insertion":
            self.activity_label.setText("Đang thực hiện Insertion Sort...")  # Cập nhật mô tả
            self.insertion_sort_visualization(self.data)
