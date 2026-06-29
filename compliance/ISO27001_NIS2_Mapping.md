# Compliance Mapping: ISO 27001 & NIS2

| Kontroll | ISO 27001:2022 | NIS2 Artikel 21 | Arkitektonisk lösning |
| :--- | :--- | :--- | :--- |
| **Access Control** | A.5.15 / A.9.1 | Grundläggande säkerhet | OIDC + RBAC/ABAC (se 05_IAM.md) |
| **Logging** | A.8.15 | Incidenthantering | Immutable Audit Log (WORM) |
| **Cryptography** | A.8.24 | Kryptering | KMS/HSM (se Systems_overview.md) |
| **Supply Chain** | A.5.19-23 | Säkerhet i leveranskedjan | SAST/SCA i CI/CD-pipeline |

*NIS2-fokus:* Systemet adresserar specifikt kravet på "säkerhet i nätverks- och informationssystem" genom zero-trust segmentering.