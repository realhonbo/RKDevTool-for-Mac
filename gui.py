#!/usr/bin/env python3
# coding=utf-8
# Create by hehongbo918@gmail.com
# 2025/07

from PyQt5.QtWidgets import (QApplication, QMainWindow,
    QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QTabWidget, QGroupBox)
import sys

from image import ImageProg
from upgrade import FirmUpgrade
from advance import AdvancedOps

class RKDevToolGUI(QMainWindow, ImageProg, FirmUpgrade, AdvancedOps):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RKDevTool for Mac v0.91")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        # create tabs
        self.tabs = QTabWidget()
        self.create_flash_tab()
        self.create_loader_tab()
        self.create_advanced_tab()
        self.main_layout.addWidget(self.tabs)

        self.create_status_bar()
        self.last_file_path = ""


    def create_flash_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.create_flash_read(layout)
        self.create_flash_write(layout)
        self.create_flash_erase(layout)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "镜像下载")


    def create_loader_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        download_widgets = [("boot_file", "引导程序文件")]
        download_buttons = [
            ("btn_browse_boot", "浏览...", self.browse_boot_file),
            ("btn_download_boot", "下载", self.download_boot)
        ]
        self.create_fop_group(layout, "下载引导程序", download_widgets, download_buttons)

        upgrade_widgets = [("upgrade_file", "引导程序文件")]
        upgrade_buttons = [
            ("btn_browse_upgrade", "浏览...", self.browse_upgrade_file),
            ("btn_upgrade_loader", "升级", self.upgrade_loader)
        ]
        self.create_fop_group(layout, "升级引导程序", upgrade_widgets, upgrade_buttons)

        pack_widgets = [("unpack_file", "引导程序文件")]
        pack_buttons = [
            ("btn_pack_boot", "打包引导程序", self.pack_boot),
            ("btn_browse_unpack", "浏览...", self.browse_unpack_file),
            ("btn_unpack_boot", "解包", self.unpack_boot)
        ]
        self.create_fop_group(layout, "打包/解包引导程序", pack_widgets, pack_buttons)

        tag_widgets = [
            ("tag_value", "标签"),
            ("spl_file", "U-Boot SPL文件")
        ]
        tag_buttons = [
            ("btn_browse_spl", "浏览...", self.browse_spl_file),
            ("btn_tag_spl", "标记", self.tag_spl)
        ]
        self.create_fop_group(layout, "标记SPL", tag_widgets, tag_buttons)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "固件升级")


    def create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.btn_read_capability = QPushButton("读取设备能力")
        self.btn_read_capability.clicked.connect(self.read_capability)
        layout.addWidget(self.btn_read_capability)

        self.create_device_info_group(layout)
        self.create_partition_group(layout)

        tab.setLayout(layout)

        log_group = QGroupBox("日志")
        log_layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "高级")


    def create_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RKDevToolGUI()
    window.show()
    sys.exit(app.exec_())