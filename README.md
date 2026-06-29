# ArchiveSecure AB - High-Security E-Archive

ArchiveSecure AB är en hög-säker plattform för långtidsarkivering (10–50 år) av känslig myndighetsdata. Systemet är byggt för att efterleva GDPR, OSL, NIS2 och ISO 27001 genom en Zero-Trust-arkitektur.

## Överblick
Systemet minimerar attackytan genom strikt zonindelning. All kommunikation kräver autentisering via OIDC/SAML och varje anrop utvärderas av en Policy Decision Point (PDP). Data skyddas 'at-rest' via applikationsstyrd kryptering med nyckelhantering (KMS/HSM) och lagras på oföränderlig (WORM) objektlagring.

## Arkitekturdetaljer

### 1. Ingress & Autentisering (DMZ Tier)
* **WAF/API Gateway:** Terminerar extern trafik och skyddar mot OWASP Top 10.
* **IdP:** Delegat autentisering till myndighetens SSO-tjänst med krav på MFA.

### 2. Application Tier (Zero Trust)
* **Ingest Service:** Hanterar inkommande paket. Inkluderar isolerad virusskanning och formatvalidering innan kryptering.
* **Retrieval Service:** Hanterar sök och avkryptering. Använder OPA (Open Policy Agent) för att dynamiskt validera om användarens attribut (claims) matchar dokumentets sekretessnivå (ABAC).

### 3. Data & Storage Tier
* **Metadata DB:** Segmenterad och krypterad databas för sökbarhet.
* **WORM-lagring:** Objektlagring med Object Lock för att garantera oföränderlighet enligt arkivlagen.
* **KMS:** Centraliserad nyckelhantering där vi implementerar 'Cryptographic Erasure' för att uppfylla rätten till radering (GDPR) utan att bryta WORM-skyddet.

### 4. Security & Compliance (Security Tier)
* **Immutable Audit Log:** Alla transaktioner loggas asynkront. Loggarna skrivs till WORM-skyddad lagring som är isolerad från systemadministratörer.
* **Compliance:** Vi tillämpar ISO 27001-kontroller (Access, Logging, Crypto) och adresserar NIS2-kraven genom kontinuerlig säkerhetsövervakning (SAST/SCA i CI/CD).

## Compliance Mapping
| Krav | Implementering |
| :--- | :--- |
| **NIS2 Art 21** | Segmentering, Zero-Trust, incidenthantering via SIEM-integration. |
| **ISO 27001** | A.5.15 (Access), A.8.15 (Logging), A.8.24 (Crypto). |
| **GDPR** | ABAC-filtrering, kryptering, Cryptographic Erasure. |