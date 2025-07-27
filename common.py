from PyQt5.QtWidgets import (QHBoxLayout, QPushButton,
    QLineEdit, QFileDialog, QGroupBox)

class Common:
    def browse_file(self, line_edit, title="选择文件", filter="所有文件 (*)"):
        file_path, _ = QFileDialog.getOpenFileName(self, title, self.last_file_path, filter)
        if file_path:
            line_edit.setText(file_path)
            self.last_file_path = file_path


    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "选择输出文件", self.last_file_path)
        if file_path:
            self.rd_output_f.setText(file_path)
            self.last_file_path = file_path


    def browse_input_file(self):
        self.browse_file(self.wr_file, "选择输入文件")


    def create_button(self, parent_layout, buttons):
        btn_layout = QHBoxLayout()
        for attr, text, handler in buttons:
            button = QPushButton(text)
            button.clicked.connect(handler)
            btn_layout.addWidget(button)
            setattr(self, attr, button)
        parent_layout.addLayout(btn_layout)


    def create_fop_group(self, parent_layout, title, widgets, buttons):
        group = QGroupBox(title)
        group_layout = QHBoxLayout()

        for attr, placeholder in widgets:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(placeholder)
            group_layout.addWidget(line_edit)
            setattr(self, attr, line_edit)

        for attr, text, handler in buttons:
            button = QPushButton(text)
            button.clicked.connect(handler)
            group_layout.addWidget(button)
            setattr(self, attr, button)

        group.setLayout(group_layout)
        parent_layout.addWidget(group)