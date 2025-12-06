import hashlib
import hmac
from urllib.parse import parse_qsl


def verify_telegram_init_data(init_data: str, bot_token: str) -> tuple[bool, dict]:
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    their_hash = pairs.pop("hash", None)
    if not their_hash:
        return False, {}

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))

    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()

    calc_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    ok = hmac.compare_digest(calc_hash, their_hash)

    return ok, pairs
