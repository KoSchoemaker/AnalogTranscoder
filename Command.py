import subprocess

class Command:
    @staticmethod
    def run(cmd):
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # merge stderr into stdout
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Could not run command {cmd}: {e}")
            print(e.output)
            return
        return process