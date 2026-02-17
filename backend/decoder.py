import bcrypt


hash_guardado = b"$2b$12$Zib.hCY9WqnTkmIuby8TgO7JytIwjWcNgmaNbEL93aR0f2VJSoxIi"

while True:
    password = input("Probá una contraseña (o escribí salir): ")

    if password.lower() == "salir":
        break

    password_bytes = password.encode("utf-8")

    if bcrypt.checkpw(password_bytes, hash_guardado):
        print("✅ ¡Coincide!")
        break
    else:
        print("❌ No coincide")
