from PyQt5.QtWidgets import QMessageBox
import subprocess
from common import Common

class FirmUpgrade(Common):
    def run_command(self, command):
        try:
            self.log_output.append(f"执行命令: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.log_output.append("命令执行成功")
                self.log_output.append(result.stdout)
                return result.stdout
            else:
                self.log_output.append("命令执行失败")
                self.log_output.append(result.stderr)
                return None
        except Exception as e:
            self.log_output.append(f"执行命令出错: {str(e)}")
            return None


    def download_boot(self):
        boot_file = self.boot_file.text()

        if not boot_file:
            QMessageBox.warning(self, "警告", "请选择引导程序文件")
            return

        output = self.run_command(f"rkdevtool db {boot_file}")
        if output:
            self.log_output.append(output)


    def upgrade_loader(self):
        loader_file = self.upgrade_file.text()

        if not loader_file:
            QMessageBox.warning(self, "警告", "请选择引导程序文件")
            return

        output = self.run_command(f"rkdevtool ul {loader_file}")
        if output:
            self.log_output.append(output)


    def pack_boot(self):
        output = self.run_command("rkdevtool pack")
        if output:
            self.log_output.append(output)


    def unpack_boot(self):
        boot_file = self.unpack_file.text()

        if not boot_file:
            QMessageBox.warning(self, "警告", "请选择引导程序文件")
            return

        output = self.run_command(f"rkdevtool unpack {boot_file}")
        if output:
            self.log_output.append(output)


    def tag_spl(self):
        tag = self.tag_value.text()
        spl_file = self.spl_file.text()

        if not tag or not spl_file:
            QMessageBox.warning(self, "警告", "请填写所有字段")
            return

        output = self.run_command(f"rkdevtool tagspl {tag} {spl_file}")
        if output:
            self.log_output.append(output)


    def read_capability(self):
        output = self.run_command("rkdevtool rcb")
        if output:
            self.log_output.append(output)


    def browse_boot_file(self):
        self.browse_file(self.boot_file, "选择引导程序文件", "二进制文件 (*.bin *.img)")