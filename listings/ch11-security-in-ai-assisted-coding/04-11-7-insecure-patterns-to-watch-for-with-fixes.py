# Vulnerable: user can request "../../etc/passwd"
return open(os.path.join(BASE, filename)).read()
# Fixed: resolve and confirm the path stays inside BASE
target = (BASE / filename).resolve()
if not target.is_relative_to(BASE.resolve()):
    raise PermissionError("invalid path")
