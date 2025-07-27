from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QFileDialog, QMessageBox, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox)
from PyQt5.QtCore import Qt
from functools import partial
from common import Common

class ImageProg(Common):
    def create_flash_read(self, layout):
        read_group = QGroupBox("Flash Read")
        read_layout = QHBoxLayout()
        widgets = [
            ("rd_sector",	"起始扇区"),
            ("rd_len",		"扇区长度"),
            ("rd_output_f", "输出文件")
        ]
        for attr, placeholder in widgets:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(placeholder)
            read_layout.addWidget(line_edit)
            setattr(self, attr, line_edit)
        buttons = [
            ("btn_browse_output", "浏览...", self.browse_output_file),
            ("btn_read", "读取", self.read_lba)
        ]
        for attr, text, handler in buttons:
            button = QPushButton(text)
            button.clicked.connect(handler)
            read_layout.addWidget(button)
            setattr(self, attr, button)
        read_group.setLayout(read_layout)
        layout.addWidget(read_group)


    def create_flash_write(self, layout):
        write_group = QGroupBox("Flash Write")
        write_layout = QVBoxLayout()

        basic_layout = QHBoxLayout()
        widgets = [
            ("wr_sector", "起始扇区"),
            ("wr_file", "输入文件")
        ]
        for attr, placeholder in widgets:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(placeholder)
            basic_layout.addWidget(line_edit)
            setattr(self, attr, line_edit)

        buttons = [
            ("btn_browse_input", "浏览...", self.browse_input_file),
            ("btn_write", "写入", self.write_lba),
            ("btn_import_partition", "导入分区表", self.import_partition_table)
        ]
        for attr, text, handler in buttons:
            button = QPushButton(text)
            button.clicked.connect(handler)
            basic_layout.addWidget(button)
            setattr(self, attr, button)
        write_layout.addLayout(basic_layout)

        select_control_layout = QHBoxLayout()
        self.select_all_checkbox = QCheckBox("选择全部")
        self.select_all_checkbox.setChecked(True)
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        select_control_layout.addWidget(self.select_all_checkbox)
        select_control_layout.addStretch()

        write_layout.addLayout(select_control_layout)

        self.partition_table = QTableWidget()
        write_layout.addWidget(self.partition_table)

        self.btn_write_selected = QPushButton("写入选中分区")
        self.btn_write_selected.clicked.connect(self.write_selected_partitions)
        write_layout.addWidget(self.btn_write_selected)

        write_group.setLayout(write_layout)
        layout.addWidget(write_group)


    def create_flash_erase(self, layout):
        self.btn_erase = QPushButton("擦除 Flash")
        self.btn_erase.clicked.connect(self.erase_flash)
        layout.addWidget(self.btn_erase)


    def read_lba(self):
        start = self.rd_sector.text()
        length = self.rd_len.text()
        output_file = self.rd_output_f.text()

        if not start or not length or not output_file:
            QMessageBox.warning(self, "警告", "请填写所有字段")
            return

        output = self.run_command(f"rkdevtool rl {start} {length} {output_file}")
        if output:
            self.log_output.append(output)


    def write_lba(self):
        start = self.wr_sector.text()
        input_file = self.wr_file.text()

        if not start or not input_file:
            QMessageBox.warning(self, "警告", "请填写所有字段")
            return

        output = self.run_command(f"rkdevtool wl {start} {input_file}")
        if output:
            self.log_output.append(output)


    def browse_partition_file(self, row):
        name_item = self.partition_table.item(row, 1)
        if not name_item:
            return
        name = name_item.text()
        file_edit = self.partition_table.cellWidget(row, 3)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"选择 {name} 分区镜像",
            "",
            "镜像文件 (*.img *.bin)"
        )
        if file_path:
            file_edit.setText(file_path)


    def import_partition_table(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="选择分区表文件",
            filter="分区表文件 (*.txt *.param);;所有文件 (*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            partitions = []
            for line in content.split('\n'):
                if 'CMDLINE:' not in line:
                    continue
                cmdline = line.split('CMDLINE:')[1].strip()
                parts = cmdline.split('mtdparts=rk29xxnand:')[1].split(',')
                for part in parts:
                    if '(' not in part or ')' not in part:
                        continue
                    size_offset = part.split('(')[0]
                    name = part.split('(')[1].split(')')[0]
                    if '@' in size_offset:
                        offset = size_offset.split('@')[1]
                        partitions.append((name, offset))

            self.partition_table.setColumnCount(5)
            self.partition_table.setHorizontalHeaderLabels(["选择", "分区名", "起始地址", "镜像文件", "操作"])
            self.partition_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
            self.partition_table.setColumnWidth(0, 40)
            self.partition_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
            self.partition_table.setColumnWidth(1, 110)
            self.partition_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
            self.partition_table.setColumnWidth(2, 110)
            self.partition_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
            self.partition_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
            self.partition_table.setColumnWidth(4, 60)

            self.partition_table.setRowCount(len(partitions))
            for row, (name, offset) in enumerate(partitions):
                checkbox = QCheckBox()
                checkbox.setChecked(True)
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                self.partition_table.setCellWidget(row, 0, checkbox_widget)

                self.partition_table.setItem(row, 1, QTableWidgetItem(name))
                self.partition_table.setItem(row, 2, QTableWidgetItem(offset))

                file_edit = QLineEdit()
                self.partition_table.setCellWidget(row, 3, file_edit)
                setattr(self, f"partition_file_{name}", file_edit)

                browse_btn = QPushButton("浏览...")
                browse_btn.setFixedWidth(60)
                browse_btn.clicked.connect(partial(self.browse_partition_file, row))
                self.partition_table.setCellWidget(row, 4, browse_btn)

        except Exception as e:
            QMessageBox.critical(None, "错误", f"导入分区表失败: {str(e)}")
            import traceback
            traceback.print_exc()


    def toggle_select_all(self, state):
        """切换所有分区的选择状态"""
        if not hasattr(self, 'partition_table') or not isinstance(self.partition_table, QTableWidget):
            return

        for row in range(self.partition_table.rowCount()):
            checkbox_widget = self.partition_table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(state == Qt.Checked)


    def write_selected_partitions(self):
        """写入所有被选中的分区"""
        if self.partition_table.rowCount() == 0:
            QMessageBox.warning(self, "警告", "没有可写入的分区")
            return

        success_count = 0
        fail_count = 0

        for row in range(self.partition_table.rowCount()):
            checkbox_widget = self.partition_table.cellWidget(row, 0)
            if not checkbox_widget:
                continue

            checkbox = checkbox_widget.findChild(QCheckBox)
            if not checkbox or not checkbox.isChecked():
                continue

            name_item = self.partition_table.item(row, 1)
            offset_item = self.partition_table.item(row, 2)
            file_edit = self.partition_table.cellWidget(row, 3)

            if not name_item or not offset_item or not file_edit:
                continue

            name = name_item.text()
            offset = offset_item.text()
            file_path = file_edit.text()

            if not file_path:
                self.log_output.append(f"分区 {name} 未选择镜像文件，跳过")
                continue

            self.log_output.append(f"正在写入分区 {name} (起始地址: {offset})...")
            command = f"rkdevtool wlx {name} {file_path}"
            result = self.run_command(command)

            if result:
                success_count += 1
                self.log_output.append(f"分区 {name} 写入成功")
            else:
                fail_count += 1
                self.log_output.append(f"分区 {name} 写入失败")

        msg = f"写入完成: 成功 {success_count} 个, 失败 {fail_count} 个"
        self.log_output.append(msg)
        QMessageBox.information(self, "写入结果", msg)


    def erase_flash(self):
        reply = QMessageBox.question(self, "确认", "确定要擦除Flash吗？此操作不可逆！",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            output = self.run_command("rkdevtool ef")
            if output:
                self.log_output.append(output)