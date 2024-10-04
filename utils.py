
#генерация пароля flask
import hashlib
import typing as t

def model_to_dict(model: t.Any) -> t.Any:
    return {k: getattr(model, k) for k in model.__dict__ if not k.startswith('_')}
    
def generate_password_hash(password: str, salt: str="bobr_kurva"):
    key = hashlib.pbkdf2_hmac(
        'sha256',  # Алгоритм хэша для HMAC
        password.encode('utf-8'),  # Конвертация пароля в байты
        salt.encode('utf-8'),  # Предоставление соли
        100000  # Рекомендуется использовать не менее 100 000 итераций SHA-256
    )
    
    return key.hex()


if __name__ == "__main__":
    print(generate_password_hash("123456"))