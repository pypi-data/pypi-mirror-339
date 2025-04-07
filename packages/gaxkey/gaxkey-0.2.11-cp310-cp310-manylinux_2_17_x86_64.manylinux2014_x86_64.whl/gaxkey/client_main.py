import argparse

from . import _core


def main():
    parser = argparse.ArgumentParser(
        description="GAXKey - the Activation Tool of GAX products"
    )

    # 添加产品选择选项组
    product_group = parser.add_mutually_exclusive_group(required=False)
    # product_group.add_argument(
    #     "--gaxmip", action="store_true", help="Activate the GAXMip solver"
    # )
    # product_group.add_argument(
    #     "--gaxsat", action="store_true", help="Activate the GAXSat solver"
    # )
    # product_group.add_argument(
    #     "--gaxsmt", action="store_true", help="Activate the GAXSmt solver"
    # )
    product_group.add_argument(
        "--gaxkcompiler", action="store_true", help="Activate the GAXKCompiler solver"
    )
    product_group.add_argument(
        "--server",
        type=str,
        help="Set the license server host, e.g. http://127.0.0.1:15200",
    )
    product_group.add_argument(
        "--check",
        type=str,
        metavar="PRODUCT",
        help="Check the license of the product is valid or not",
    )

    # 添加激活码参数
    parser.add_argument("activation_code", type=str, nargs="?", help="Activation code")

    # 添加集群选项
    parser.add_argument(
        "--cluster", action="store_true", help="Activate for cluster mode"
    )

    args = parser.parse_args()

    # 处理设置服务器的情况
    if args.server:
        if _core.set_license_server(args.server):
            print(f"Set server host success, server: {args.server}")
            return 0
        return -1
    # 处理检查许可证的情况
    if args.check:
        valid, msg = _core.is_valid(args.check.replace("gax", "seed"))
        if valid:
            print(f"The license of the product is valid.")
            return 0
        else:
            print(f"The license of the product is not valid, error: {msg}")
            return -1

    # 确保有激活码
    if not args.activation_code:
        parser.print_help()
        return -1

    # 确定要激活的产品
    product = None
    if args.gaxkcompiler:
        product = "seedkcompiler"
    # if args.gaxmip:
    #     product = "gaxmip"
    # elif args.gaxsat:
    #     product = "gaxsat"
    # elif args.gaxsmt:
    #     product = "gaxsmt"
    # elif args.gaxkcompiler:
    #     product = "gaxkcompiler"

    if not product:
        parser.print_help()
        return -1

    # 确定激活类型
    cluster_type = 1 if args.cluster else 0

    # 调用激活函数
    if _core.activate(product, args.activation_code, cluster_type):
        return 0
    return -1


if __name__ == "__main__":
    import sys

    sys.exit(main()) 