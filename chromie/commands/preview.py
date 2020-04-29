import subprocess
import os

from chromie.utils import ChromiePathFinder


def find_chrome():
    chrome = "Google Chrome.app"
    if os.name == "posix":
        with subprocess.Popen(["mdfind", chrome], stdout=subprocess.PIPE) as proc:
            results = [
                line
                for line in proc.stdout.read().decode("utf-8").split("\n")
                if line.endswith(chrome)
            ]
            if results:
                return results[0]
            None
    else:
        raise NotImplemented("This function has only been developed for macOS.")


def preview(args):
    finder = ChromiePathFinder(args.filepath)
    try:
        chrome = find_chrome()
        subprocess.call(
            [
                f"{chrome}/Contents/MacOS/Google Chrome",
                f'--load-extension={finder("src")}',
            ]
        )
    except KeyboardInterrupt as e:
        exit()
