from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

password = "John@123"

hash1 = password_hash.hash(password)
hash2 = password_hash.hash(password)

print("Hash 1:", hash1)
print("Hash 2:", hash2)

print("Password verified:", password_hash.verify(password, hash1))