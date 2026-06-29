# Dataflödesdiagram (DFD)

Dataflödesdiagrammen kartlägger hur information rör sig genom systemet, var den lagras och vilka aktörer som interagerar med den. För att identifiera hot (vilket görs i nästa fas med STRIDE) har vi markerat viktiga Trust Boundaries (tillitsgränser) där data passerar från en säkerhetszon till en annan.
DFD Level 0: Kontextdiagram

Level 0 ger ett helikopterperspektiv. Det visar hela systemet som en enda process och belyser vilka externa parter som systemet kommunicerar med.

```mermaid
flowchart LR
    %% Externa entiteter (Rektanglar)
    User["Handläggare / Webbklient"]
    ExtSystem["Externt Ärendehanteringssystem"]
    IdP["Myndighetens IdP (SSO)"]

    %% Huvudprocess (Rundad rektangel)
    System("ArchiveSecure AB")

    %% Flöden
    User -->|Auth request| IdP
    IdP -->|Authorization Code / Tokens| User
    
    User -->|"API requests (JWT)"| System
    ExtSystem -->|"M2M API requests"| System
    
    System -->|Sökresultat / Dokument / Arkiv-ID| User
    System -->|Kvittens API| ExtSystem
```

Level 0 beskriver ArchiveSecure som ett centralt arkivsystem som hanterar både interaktiva användare (handläggare) och externa systemintegrationer.

Autentisering sker via en extern Identity Provider (IdP) som utfärdar säkerhets-tokens baserade på OIDC/SAML. Dessa tokens används av klienter för att autentisera API-anrop mot ArchiveSecure-systemet.

Systemet returnerar antingen sökresultat, arkivdokument eller arkivkvitton beroende på operationstyp.

## DFD Level 1: Huvudprocesser

Level 1 bryter ner systemet i dess huvudsakliga logiska processer och visar var data lagras. Här blir tillitsgränserna mellan externa användare och vår interna logik tydlig.
```mermaid
flowchart TD

subgraph TrustBoundary_Internet ["Trust Boundary: Externa aktörer"]
    User["Handläggare"]
    ExtSystem["Externt Ärendehanteringssystem"]
end

subgraph TrustBoundary_App ["Trust Boundary: Applikation"]
    P1("1.0 API Gateway (PEP)")
    P2("2.0 Ingest & Validering")
    P3("3.0 Sök & Hämta")
end

subgraph TrustBoundary_Data ["Trust Boundary: Data"]
    D1[("D1 Metadata DB")]
    D2[("D2 WORM Storage")]
    D3[("D3 Immutable Audit Log")]
end

User -->|Request + JWT| P1
ExtSystem -->|M2M Request| P1

P1 --> P2
P1 --> P3

P2 --> D2
P2 --> D1
P2 --> D3

P3 --> D1
P3 --> D2
P3 --> D3

P3 -->|Result| User
```
Level 1 bryter ner systemet i tre huvudkomponenter:

- API Gateway (Policy Enforcement Point)
- Ingest & Validering (arkivering av data)
- Sök & Hämtning (åtkomst till arkivdata)

All extern trafik passerar API Gateway, där autentisering och auktorisering sker innan vidare routing till interna tjänster.

Systemet är uppdelat i tre separata datazoner:

- Metadata lagras i en krypterad databas
- Dokument lagras i oföränderlig WORM-lagring
- Alla operationer loggas i en immutable audit log

Detta säkerställer spårbarhet, dataintegritet och skydd mot manipulation.


## DFD Level 2: Detaljerat flöde för Arkivering (Ingest)

Level 2 zoomar in på en specifik, affärskritisk process. Här tittar vi på vad som händer internt i "2.0 Ingest & Validering" när ett nytt, känsligt dokument laddas upp till e-arkivet. Detta flöde är kritiskt för att säkerställa att ingen skadlig kod kommer in och att datan krypteras innan den når lagringen.


```mermaid
flowchart TD
    Input["Upload (via Gateway)"]
    Virus["2.1 Virus scanning"]
    Policy["2.2 Policy & classification"]
    
    %% KMS Interaktion
    subgraph Crypto_Logic ["Crypto Engine (Local Service)"]
        KMS_Call["1. Call KMS (Generate Key)"]
        Encrypt["2. Encrypt Data locally with Raw DEK"]
    end
    
    KMS["KMS / HSM"]
    
    Store["3. Store (Encrypted Data + Wrapped DEK)"]
    
    Input --> Virus --> Policy
    Policy -->|Approved| KMS_Call
    KMS_Call <-->|Return: Raw DEK + Wrapped DEK| KMS
    KMS_Call --> Encrypt
    Encrypt --> Store
    
    Store --> WORM[("WORM Storage")]
    Store --> DB[("Metadata DB (Stores Wrapped DEK)")]
```

Processen startar när en validerad request når ingest-tjänsten via API Gateway.

Följande steg sker:

1. Filen skannas för skadlig kod och filformatvalideras.
Policy engine verifierar att användaren har rätt att arkivera datan.
2. En Data Encryption Key (DEK) tillhandahålls via Key Management System (KMS).
3. Dokumentet krypteras
4. Krypterad data lagras i WORM storage och metadata sparas i databasen.
5. Alla steg loggas i en immutable audit log för spårbarhet.

Om någon kontroll misslyckas avbryts processen och en säkerhetsincident loggas.

Här krypterar vi med vår publika nyckel och när vi ska ta ut den dekrypterar vi med våran privata nyckel