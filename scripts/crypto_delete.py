import os

class KMSManager:
    def __init__(self):
        # Simulering av en KMS-databas
        self.key_store = {"doc_id_123": "aes-key-abc-xyz"}

    def delete_key(self, doc_id):
        """
        Raderar krypteringsnyckeln för ett specifikt dokument.
        Detta gör det krypterade objektet i WORM-lagringen oåtkomligt (oläsbart).
        """
        if doc_id in self.key_store:
            print(f"[INFO] Förstör krypteringsnyckel för {doc_id}...")
            del self.key_store[doc_id]
            print(f"[SUCCESS] Nyckel raderad. Data är nu permanent oläsbar (Crypto-erase).")
            return True
        else:
            print(f"[ERROR] Nyckel för {doc_id} hittades ej.")
            return False

# Exempel på användning
if __name__ == "__main__":
    kms = KMSManager()
    kms.delete_key("doc_id_123")