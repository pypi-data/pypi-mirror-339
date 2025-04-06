import os
import sys
import subprocess
from typing import List
from pathlib import Path

def get_shebang_interpreter(script_path: str) -> List[str]:
    with open(script_path, "r") as f:
        first_line = f.readline().strip()
    if first_line.startswith("#!"):
        return first_line[2:].split()
    else:
        raise RuntimeError("Script has no shebang line")


def reexec_with_shebang(script_path: str):
    if os.environ.get("_REEXEC_DONE") == "1":
        return  # Already re-executed

    shebang_interpreter = get_shebang_interpreter(script_path)
    abs_script = os.path.abspath(script_path)
    args = [*shebang_interpreter, abs_script, *sys.argv[1:]]

    env = os.environ.copy()
    env["_REEXEC_DONE"] = "1"

    completed_process=subprocess.run(args, env=env, capture_output=True)
    sys.exit(completed_process.returncode)

