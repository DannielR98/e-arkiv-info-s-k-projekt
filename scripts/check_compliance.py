# Simulerar en compliance-check för NIS2
def verify_security_posture():
    requirements = {
        "mfa_enabled": True,
        "encryption_at_rest": True,
        "immutable_logs": True
    }
    
    failed = [req for req, status in requirements.items() if not status]
    
    if not failed:
        print("NIS2 Compliance Check: PASS")
    else:
        print(f"NIS2 Compliance Check: FAILED. Missing: {failed}")

if __name__ == "__main__":
    verify_security_posture()