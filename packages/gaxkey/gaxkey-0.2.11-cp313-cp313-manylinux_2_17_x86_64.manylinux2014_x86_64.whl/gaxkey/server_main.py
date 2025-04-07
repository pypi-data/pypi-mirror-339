import argparse
import sys

from . import _core


def main():
    """
    License Server入口函数
    启动GAX许可证服务器
    """
    parser = argparse.ArgumentParser(
        description="GAXKey License Server"
    )

    # parser.add_argument(
    #     "--debug", action="store_true", help="Start server in debug mode"
    # )

    args = parser.parse_args()

    # 启动许可证服务器
    try:
        print("Starting GAXKey License Server...")
        if _core.start_license_server():
            return 0
        return -1
    except Exception as e:
        print(f"Error starting license server: {e}")
        return -1


if __name__ == "__main__":
    sys.exit(main()) 