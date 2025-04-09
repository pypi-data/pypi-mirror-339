import os


def print_tree(path, prefix="", ignore_dirs=None):
    """
    递归打印目录树，包含 | 和 - 符号
    :param path: 目录路径
    :param prefix: 前缀（用于递归）
    :param ignore_dirs: 需要忽略的目录集合
    """
    if ignore_dirs is None:
        ignore_dirs = set()

    # 获取当前目录下的所有文件和目录
    items = os.listdir(path)
    # 过滤掉需要忽略的目录
    items = [item for item in items if item not in ignore_dirs]

    for i, item in enumerate(items):
        # 判断是否是最后一个文件或目录
        is_last = (i == len(items) - 1)
        # 构建当前层的前缀
        print(prefix + ("└── " if is_last else "├── ") + item)

        # 如果是目录，递归打印子目录
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            # 更新前缀
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(full_path, new_prefix, ignore_dirs)


# 示例：忽略 my_project 和 venv 目录
dirs = {".idea", ".venv", ".git"}

print_tree("C:\\Customer\\Project\\python\\my_project", ignore_dirs=dirs)
