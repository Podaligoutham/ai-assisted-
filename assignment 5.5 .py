import getpass
import hashlib
import os

# Privacy and security issues in the insecure version:
# 1. Passwords are stored in plaintext.
# 2. Personal data is stored without encryption or strong file permissions.
# 3. The file may be exposed if the system is compromised.
# 4. Passwords should never be kept in readable text.
# 5. Use a strong hashing algorithm and a unique salt per password.


def save_user_insecure(name, email, password):
    with open("users_insecure.txt", "a", encoding="utf-8") as file:
        file.write(f"{name},{email},{password}\n")


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt, password_hash


def save_user_secure(name, email, password):
    salt, password_hash = hash_password(password)
    with open("users_secure.txt", "a", encoding="utf-8") as file:
        file.write(f"{name},{email},{salt.hex()},{password_hash.hex()}\n")


def main():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")

    # Insecure example for demonstration purposes.
    save_user_insecure(name, email, password)

    # Secure recommendation.
    save_user_secure(name, email, password)

    print("User data saved successfully.")


if __name__ == "__main__":
    main()
