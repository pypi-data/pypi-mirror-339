import argparse
import os
import subprocess



def main():
    parser = argparse.ArgumentParser(description="A simple CLI tool for yzc.")
    parser.add_argument('--hello', action='store_true', help="Print Hello, World!")
    parser.add_argument('--get_ixrtplugin_sample', action='store_true', help="Run a sample script in the current directory")

    args = parser.parse_args()

    if args.hello:
        print("Hello, World!")

    if args.get_ixrtplugin_sample:
        # 定义文件 URL 和解压后的目录名称
        file_url = "http://8.148.226.184/index.php/s/TnzTDJCasg7xdSG/download/UsePluginV2DynamicExt.tar.gz"
        tar_file_name = "UsePluginV2DynamicExt.tar.gz"
        extract_dir_name = "UsePluginV2DynamicExt"

        # 获取当前工作目录
        current_dir = os.getcwd()

        # 定义文件路径
        tar_file_path = os.path.join(current_dir, tar_file_name)

        try:
            # Step 1: 使用 wget 下载文件
            print(f"Downloading file from {file_url}...")
            subprocess.run(["wget", file_url, "-O", tar_file_path], check=True)
            print(f"File downloaded to {tar_file_path}")

            # Step 2: 使用 tar 解压文件
            print(f"Extracting {tar_file_name}...")
            subprocess.run(["tar", "-xzvf", tar_file_path], check=True)
            subprocess.run(["rm", tar_file_path], check=True)
            

            # Step 3: 进入解压后的目录
            print(f"Changing directory to {extract_dir_name}...")
            os.chdir(os.path.join(current_dir, extract_dir_name))
            print(f"Current working directory: {os.getcwd()}")


        except subprocess.CalledProcessError as e:
            print(f"Command execution failed with error:\n{e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()