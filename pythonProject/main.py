import requests
import zipfile
import os
from pathlib import Path
import shutil


def download_and_repackage():
    # 配置
    download_folder = './expansions'
    output_filename = 'FOGMOEYGOCustomCards.ypk'

    # 欢迎
    print("欢迎使用 FOGMOEYGO 自定义卡片下载器。")
    print("请访问我们的官网： https://ygo.fog.moe/")

    # 是否开始下载Y/N
    print("是否开始下载？(Y/N)")
    user_input = input()
    if user_input.lower() != 'y':
        print("用户取消。")
        print("请按任意键退出。")
        input()
        return

    # 检查下载目录是否存在
    if not Path(download_folder).exists():
        print(
            f"文件夹 {download_folder} 不存在。 请在 ygopro 目录运行本程序。")
        print("请按任意键退出。")
        input()
        return

    # 选择下载节点
    while True:
        print("请选择下载节点：(输入对应数字)")
        print("1. GitHub")
        print("2. KKGitHub")
        print("3. GHProxy")
        print("4. GHProxy")
        print("5. GHProxy")
        print("6. 备用节点")
        user_input = input()
        if user_input == '1':
            url = 'https://github.com/FogMoe/YGOCustomCards/archive/refs/heads/main.zip'
        elif user_input == '2':
            url = 'https://kkgithub.com/FogMoe/YGOCustomCards/archive/refs/heads/main.zip'
        elif user_input == '3':
            url = 'https://ghproxy.net/https://github.com/FogMoe/YGOCustomCards/archive/refs/heads/main.zip'
        elif user_input == '4':
            url = 'https://mirror.ghproxy.com/https://github.com/FogMoe/YGOCustomCards/archive/refs/heads/main.zip'
        elif user_input == '5':
            url = 'https://ghproxy.cc/https://github.com/FogMoe/YGOCustomCards/archive/refs/heads/main.zip'
        elif user_input == '6':
            url = 'https://file1.fogmoe.top/YGODiy/YGOCustomCards-main.zip'
        else:
            print("无效输入。")
            continue
        break

    # 下载文件的完整路径
    download_path = os.path.join(download_folder, 'YGOCustomCards-main.zip')

    # 尝试下载ZIP文件
    print("尝试下载文件……")
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        with open(download_path, 'wb') as file:
            file.write(response.content)
        print("下载完毕。")
    except requests.RequestException as e:
        print(f"下载错误： {e}")
        print("请按任意键退出。")
        input()
        return

    # 解压文件
    print("解压文件……")
    extract_folder = os.path.join(download_folder, 'extracted')
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print("解压完毕。")

    # 定位解压后的主文件夹
    main_content_folder = os.path.join(extract_folder, 'YGOCustomCards-main')

    # 重新打包
    print("进行最后的检查……")
    new_zip_path = os.path.join(download_folder, output_filename)
    with zipfile.ZipFile(new_zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(main_content_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, main_content_folder)
                zipf.write(file_path, arcname=arcname)
    print("检查完毕。")
    print("清理临时文件……")

    # 清理下载和解压产生的临时文件
    os.remove(download_path)
    shutil.rmtree(extract_folder)
    print("执行完毕。")

    # 等待用户输入
    print("请按任意键退出。")
    input()


# 使用函数
download_and_repackage()
