# Vulnerable
cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
# Fixed: parameterised
cur.execute("SELECT * FROM users WHERE email = %s", (email,))
