import os
from pathlib import Path

target = Path("bin/omp-verify-traceability")
if not target.exists():
    target = Path("bin/omp-verify-traceability.py")

if not target.exists():
    print("[-] bin/omp-verify-traceability not found. Please run this from your project root.")
    exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines()

start_idx = -1
for i, line in enumerate(lines):
    if "table_match = re.search" in line:
        start_idx = i
        break

if start_idx != -1:
    end_idx = start_idx
    for j in range(start_idx, min(start_idx + 25, len(lines))):
        if "split(" in lines[j] or "rows =" in lines[j]:
            end_idx = j
            break
            
    # Swap the broken multiline string with a clean, parenthesized implicit concatenation
    lines[start_idx:end_idx+1] = [
        "    table_match = re.search(",
        "        r\"\\\\|\\\\s*Requirement\\\\s*\\\\|\\\\s*Verification(?: ID)?\\\\s*\\\\|\\\\s*Method\\\\s*\\\\|\\\\s*Test File\\\\s*\\\\|\\\\s*Initial Failure\\\\s*\\\\|\\\\s*Status\\\\s*\\\\|\",",
        "        r\"\\\\s*\\\\n\\\\|\\\\s*[-| :]+\\\\s*\\\\|\",",
        "        r\"\\\\s*\\\\n(.*?)\",",
        "        r\"(?:\\\\n\\\\s*\\\\|\\\\s*Requirement\\\\s*\\\\|\\\\s*Verification(?: ID)?\\\\s*\\\\|\\\\s*Method\\\\s*\\\\|\\\\s*Test File\\\\s*\\\\|\\\\s*Initial Failure\\\\s*\\\\|\\\\s*Status\\\\s*\\\\|)?$\",",
        "        content,",
        "        re.DOTALL | re.MULTILINE | re.IGNORECASE",
        "    )",
        "    if not table_match:",
        "        raise ValueError(\"No verification table found in verification file.\")",
        "    table_rows_text = table_match.group(1)",
        "    rows = table_rows_text.strip().split(\"\\\\n\")"
    ]
    
    target.write_text("\n".join(lines), encoding="utf-8")
    print("[+] Successfully repaired bin/omp-verify-traceability compilation syntax and regex!")
else:
    print("[-] Could not locate re.search block in bin/omp-verify-traceability. Assuming already healthy.")