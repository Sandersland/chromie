import subprocess
import os


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
    chrome = find_chrome()
    subprocess.call(
        [f"{chrome}/Contents/MacOS/Google Chrome", f"--load-extension{args.filepath}"]
    )
