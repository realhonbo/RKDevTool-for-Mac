from PyQt5.QtWidgets import (QVBoxLayout, QMessageBox, QGroupBox)
from common import Common

class AdvancedOps(Common):
    def create_device_info_group(self, parent_layout):
        group = QGroupBox("设备信息")
        layout = QVBoxLayout()

        buttons = [
            ("btn_list_device", "列出设备", self.list_devices),
            ("btn_test_device", "测试设备", self.test_device),
            ("btn_reset_device", "重置设备", self.reset_device),
            ("btn_read_chip_info", "读取芯片信息", self.read_chip_info),
            ("btn_read_flash_id", "读取Flash ID", self.read_flash_id),
            ("btn_read_flash_info", "读取Flash信息", self.read_flash_info)
        ]
        self.create_button(layout, buttons)

        group.setLayout(layout)
        parent_layout.addWidget(group)


    def create_partition_group(self, parent_layout):
        group = QGroupBox("分区表操作")
        layout = QVBoxLayout()

        bottons = [
            ("btn_print_partition", "打印分区表", self.print_partition),
        ]
        self.create_button(layout, bottons)

        gpt_widgets = [("gpt_file", "GPT分区表文件")]
        gpt_buttons = [
            ("btn_browse_gpt", "浏览...", self.browse_gpt_file),
            ("btn_write_gpt", "写入", self.write_gpt)
        ]
        self.create_fop_group(layout, "写入GPT分区表", gpt_widgets, gpt_buttons)

        param_widgets = [("param_file", "参数文件")]
        param_buttons = [
            ("btn_browse_param", "浏览...", self.browse_param_file),
            ("btn_write_param", "写入", self.write_param)
        ]
        self.create_fop_group(layout, "写入参数", param_widgets, param_buttons)

        part_widgets = [
            ("part_name", "分区名"),
            ("part_file", "文件")
        ]
        part_buttons = [
            ("btn_browse_part", "浏览...", self.browse_part_file),
            ("btn_write_part", "写入", self.write_partition)
        ]
        self.create_fop_group(layout, "按分区名写入", part_widgets, part_buttons)

        group.setLayout(layout)
        parent_layout.addWidget(group)


    def list_devices(self):
        self.run_command("rkdevtool ld")


    def test_device(self):
        self.run_command("rkdevtool td")


    def reset_device(self):
        self.run_command("rkdevtool rd")


    def read_chip_info(self):
        self.run_command("rkdevtool rci")


    def read_flash_id(self):
        self.run_command("rkdevtool rid")


    def read_flash_info(self):
        self.run_command("rkdevtool rfi")


    def print_partition(self):
        output = self.run_command("rkdevtool ppt")
        if output:
            self.log_output.append(output)


    def write_gpt(self):
        gpt_file = self.gpt_file.text()

        if not gpt_file:
            QMessageBox.warning(self, "警告", "请选择GPT分区表文件")
            return

        reply = QMessageBox.question(self, "确认", "确定要写入GPT分区表吗？此操作会修改分区结构！",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            output = self.run_command(f"rkdevtool gpt {gpt_file}")
            if output:
                self.log_output.append(output)


    def write_param(self):
        param_file = self.param_file.text()

        if not param_file:
            QMessageBox.warning(self, "警告", "请选择参数文件")
            return

        output = self.run_command(f"rkdevtool prm {param_file}")
        if output:
            self.log_output.append(output)


    def write_partition(self):
        part_name = self.part_name.text()
        part_file = self.part_file.text()

        if not part_name or not part_file:
            QMessageBox.warning(self, "警告", "请填写所有字段")
            return

        output = self.run_command(f"rkdevtool wlx {part_name} {part_file}")
        if output:
            self.log_output.append(output)


    def browse_upgrade_file(self):
        self.browse_file(self.upgrade_file, "选择引导程序文件", "二进制文件 (*.bin *.img)")


    def browse_unpack_file(self):
        self.browse_file(self.unpack_file, "选择引导程序文件", "二进制文件 (*.bin *.img)")


    def browse_spl_file(self):
        self.browse_file(self.spl_file, "选择SPL文件", "二进制文件 (*.bin *.img)")


    def browse_gpt_file(self):
        self.browse_file(self.gpt_file, "选择GPT分区表文件", "分区表文件 (*.gpt *.txt)")


    def browse_param_file(self):
        self.browse_file(self.param_file, "选择参数文件", "参数文件 (*.txt *.param)")


    def browse_part_file(self):
        self.browse_file(self.part_file, "选择分区文件")