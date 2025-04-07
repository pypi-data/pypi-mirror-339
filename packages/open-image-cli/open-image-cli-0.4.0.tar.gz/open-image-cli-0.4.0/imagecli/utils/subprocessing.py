import subprocess

class CustomProcess:
    def __init__(self):
        self.stdout: str = None
        self.stderr: str = None
        self.command: str = None
        self.success: bool = True
        self.origin_popen: subprocess.Popen = None


def shell(command, verbose=True) -> subprocess.Popen:
    custom_process = CustomProcess()
    print(f'command: {command}')
    try:
        custom_process.origin_popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE, universal_newlines=True)
        custom_process.stdout, custom_process.stderr = custom_process.origin_popen.communicate()
    except subprocess.CalledProcessError:
        custom_process.success = False
    return custom_process