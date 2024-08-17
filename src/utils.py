from datetime import datetime
from importlib import metadata


def get_available_package_list():
    packages_list = list(metadata.distributions())

    package_row = [["Package", "Version"]]
    for pkg in packages_list:
        package_row.append([pkg.name, pkg.version])

    return package_row


def logger_print(message: str):
    time_frmt = datetime.now().strftime("%d %b %Y, %H:%M:%S")
    print(f"\n[{time_frmt}]\n", message, "\n")
