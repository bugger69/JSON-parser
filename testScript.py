from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
VALIDATOR = ROOT / "validateJSON.py"

for number in range(1, 5):
    test_dir = ROOT / f"test{number}"

    for input_file in sorted(test_dir.glob("*.json")):
        process = subprocess.run(
            [sys.executable, str(VALIDATOR), str(input_file)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        output_lines = [line.strip() for line in process.stdout.splitlines()]
        result = next(
            (line for line in reversed(output_lines) if line in {"valid", "invalid"}),
            None,
        )

        if result is not None:
            output = result
        else:
            output = process.stderr.strip() or process.stdout.strip()
            if not output:
                output = f"Exited with code {process.returncode}"

        print(f"{input_file.relative_to(ROOT)}: {output}")