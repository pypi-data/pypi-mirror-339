"""
pyfj 命令行工具
"""

import os
import subprocess
import sys
import click


class ProjectRenamer:
    """项目重命名器，用于克隆GitHub仓库并重命名项目"""

    def __init__(self, repo_url, old_name, new_name):
        """初始化项目重命名器

        Args:
            repo_url: 仓库URL
            old_name: 原项目名
            new_name: 新项目名
        """
        self.repo_url = repo_url
        self.old_name = old_name
        self.new_name = new_name
        self.replaced_count = 0
        self.processed_files = []

    def run_command(self, command):
        """运行shell命令

        Args:
            command: 要执行的命令

        Returns:
            命令的返回码
        """
        process = subprocess.run(command,
                                 shell=True,
                                 check=True,
                                 text=True,
                                 capture_output=True)
        return process.returncode

    def replace_in_file(self, file_path):
        """替换文件中的项目名

        Args:
            file_path: 文件路径

        Returns:
            是否成功替换
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 替换字符串
            new_content = content.replace(self.old_name, self.new_name)

            # 将修改后的内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

            return True
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            return False

    def check_environment(self):
        """检查运行环境是否满足要求

        Returns:
            bool: 环境是否满足要求
        """
        try:
            # 检查是否安装了Git
            result = subprocess.run(["git", "--version"],
                                    check=False,
                                    capture_output=True,
                                    text=True)

            if result.returncode != 0:
                print("错误: 未检测到Git安装，请先安装Git后再运行此脚本。")
                print("下载链接: https://git-scm.com/downloads")
                return False

            return True

        except FileNotFoundError:
            print("错误: 未检测到Git安装，请先安装Git后再运行此脚本。")
            print("下载链接: https://git-scm.com/downloads")
            return False

    def clone_repository(self):
        """克隆仓库到新文件夹"""
        self.run_command(f"git clone {self.repo_url} {self.new_name}")

    def collect_files(self):
        """收集需要处理的文件列表"""
        self.processed_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if ".git" not in root:  # 排除.git目录
                    file_path = os.path.join(root, file)
                    self.processed_files.append(file_path)

    def rename_files_content(self):
        """重命名文件内容中的项目名"""
        self.replaced_count = 0
        for file_path in self.processed_files:
            try:
                if os.path.isfile(
                        file_path) and not file_path.endswith('.pyc'):
                    if self.replace_in_file(file_path):
                        self.replaced_count += 1
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")

    def rename_directory(self):
        """重命名包含旧项目名的目录"""
        if os.path.exists(self.old_name):
            os.rename(self.old_name, self.new_name)

    def create_project(self):
        """创建新项目"""
        # 检查环境
        if not self.check_environment():
            print("环境检查未通过，退出程序。")
            sys.exit(1)

        # 1. 克隆仓库
        self.clone_repository()

        # 2. 切换到克隆的目录
        os.chdir(self.new_name)

        # 3. 收集文件
        self.collect_files()

        # 4. 替换文件内容
        self.rename_files_content()

        # 5. 重命名目录
        self.rename_directory()

        print(f"项目{self.new_name}已创建完成")
        return True

    def rename_project(self):
        """重命名已有项目"""
        if not os.path.exists(self.old_name):
            print(f"错误：项目文件夹 '{self.old_name}' 不存在")
            return False

        if os.path.exists(self.new_name):
            print(f"错误：目标文件夹 '{self.new_name}' 已存在")
            return False

        # 1. 进入项目目录的父目录
        old_dir = os.path.abspath(self.old_name)
        parent_dir = os.path.dirname(old_dir)

        # 2. 重命名目录
        os.rename(self.old_name, self.new_name)

        # 3. 进入新目录
        os.chdir(self.new_name)

        # 4. 收集文件
        self.collect_files()

        # 5. 替换文件内容
        self.rename_files_content()

        # 6. 重命名目录
        self.rename_directory()

        print(f"项目已从 '{self.old_name}' 重命名为 '{self.new_name}'")
        return True


@click.group()
def cli():
    """PyFJ - 一个用于管理Django Ninja项目的工具"""
    pass


@cli.command()
@click.option('--name', prompt='项目名称', help='新项目的名称')
def create(name):
    """创建新的Django Ninja项目"""
    if not name:
        print("错误：项目名称不能为空")
        sys.exit(1)

    if os.path.exists(name):
        print(f"错误：文件夹{name}已存在")
        sys.exit(1)

    renamer = ProjectRenamer(
        repo_url="https://github.com/olivetree123/django_ninja_template.git",
        old_name="django_ninja_template",
        new_name=name)

    renamer.create_project()


@cli.command()
@click.option('--name', prompt='项目当前名称', help='项目当前名称')
@click.option('--new_name', prompt='项目新名称', help='项目新名称')
def rename(name, new_name):
    """将现有项目重命名为新名称"""
    if not name or not new_name:
        print("错误：项目名称不能为空")
        sys.exit(1)

    if name == new_name:
        print("错误：新旧项目名称不能相同")
        sys.exit(1)

    click.echo(f"准备将项目从 {name} 重命名为 {new_name}")

    renamer = ProjectRenamer(
        repo_url="",  # 重命名不需要仓库URL
        old_name=name,
        new_name=new_name)

    renamer.rename_project()


def main():
    """命令行入口点"""
    try:
        cli()
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
