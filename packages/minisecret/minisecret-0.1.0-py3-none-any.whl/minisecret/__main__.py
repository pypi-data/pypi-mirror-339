
from .minisecret import MiniSecret
import sys

def main():
    ms = MiniSecret()

    def print_usage():
        print("Usage:")
        print("  minisecret put <key> <value>")
        print("  minisecret get <key> [--secure]")
        print("  minisecret list")

    if len(sys.argv) == 4 and sys.argv[1] == "put":
        ms.put(sys.argv[2], sys.argv[3])
        print(f"✅ Stored secret: '{sys.argv[2]}'")

    elif len(sys.argv) >= 3 and sys.argv[1] == "get":
        key = sys.argv[2]
        use_secure = "--secure" in sys.argv
        value = ms.secure_get(key) if use_secure else ms.get(key)
        if value is None:
            print(f"❌ Secret '{key}' not found.")
        else:
            print(value)

    elif len(sys.argv) == 2 and sys.argv[1] == "list":
        keys = ms.list_keys()
        print("🔐 Stored keys:", keys)

    else:
        print_usage()
