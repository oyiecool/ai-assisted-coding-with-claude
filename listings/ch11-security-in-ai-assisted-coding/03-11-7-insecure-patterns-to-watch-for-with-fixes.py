# Vulnerable
subprocess.run(f"tar czf {name}.tgz {path}", shell=True)
# Fixed: argument list, no shell
subprocess.run(["tar", "czf", f"{name}.tgz", path], check=True)
