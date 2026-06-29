# Dataflödesdiagram (DFD)

Dataflödesdiagrammen kartlägger hur information rör sig genom systemet, var den lagras och vilka aktörer som interagerar med den. För att identifiera hot (vilket görs i nästa fas med STRIDE) har vi markerat viktiga Trust Boundaries (tillitsgränser) där data passerar från en säkerhetszon till en annan.
DFD Level 0: Kontextdiagram

Level 0 ger ett helikopterperspektiv. Det visar hela systemet som en enda process och belyser vilka externa parter som systemet kommunicerar med.

```mermaid
flowchart LR
    %% Externa entiteter (Rektanglar)
    User["Handläggare (Webbklient)"]
    ExtSystem["Externt Ärendehanteringssystem"]
    IdP["Myndighetens IdP (SSO)"]

    %% Huvudprocess (Rundad rektangel)
    System("0.0 ArchiveSecure AB")

    %% Flöden
    User -- "Inloggning / MFA" --> IdP
    IdP -- "SAML/OIDC Token" --> User
    
    User -- "Sökfrågor / Läs & Skrivdokument (Med Token)" --> System
    System -- "Sökresultat / Dokument" --> User
    
    ExtSystem -- "Automatiska arkivpaket (API + Token)" --> System
    System -- "Kvittens & Arkiv-ID" --> ExtSystem
```


## DFD Level 1: Huvudprocesser

Level 1 bryter ner systemet i dess huvudsakliga logiska processer och visar var data lagras. Här blir tillitsgränserna mellan externa användare och vår interna logik tydlig.
```mermaid
flowchart TD
    %% Tillitsgränser
    subgraph TrustBoundary_Internet ["Trust Boundary: Externa Nätverk"]
        User["Handläggare / Externt System"]
    end

    subgraph TrustBoundary_App ["Trust Boundary: Applikationsmiljö"]
        P1("1.0 Access & API Gateway")
        P2("2.0 Ingest & Validering")
        P3("3.0 Sök & Hämta")
    end

    subgraph TrustBoundary_Data ["Trust Boundary: Säker Lagring"]
        D1[("D1: Metadata DB")]
        D2[("D2: WORM Objektlagring")]
        D3[("D3: Immutable Audit Log")]
    end

    %% Dataflöden
    User -- "Request + Token" --> P1
    P1 -- "Auktoriserat flöde" --> P2
    P1 -- "Auktoriserat sök/läs-flöde" --> P3
    
    P2 -- "Skriver oföränderlig fil" --> D2
    P2 -- "Sparar metadata (Krypterat)" --> D1
    P2 -- "Loggar händelse" --> D3
    
    D1 -- "Returnerar pekare" --> P3
    P3 -- "Hämtar fil (Dekrypterar)" --> D2
    D2 -- "Returnerar fil" --> P3
    P3 -- "Loggar åtkomst" --> D3
    P3 -- "Returnerar resultat" --> User
```



## DFD Level 2: Detaljerat flöde för Arkivering (Ingest)

Level 2 zoomar in på en specifik, affärskritisk process. Här tittar vi på vad som händer internt i "2.0 Ingest & Validering" när ett nytt, känsligt dokument laddas upp till e-arkivet. Detta flöde är kritiskt för att säkerställa att ingen skadlig kod kommer in och att datan krypteras innan den når lagringen.

```mermaid
flowchart TD
    %% Inkommande
    Input["Från 1.0 Access Gateway (Validerad Användare)"]

    %% Delprocesser
    P2_1("2.1 Virusskanning & Formatkontroll")
    P2_2("2.2 Nyckelhantering (KMS)")
    P2_3("2.3 Kryptering av payload")
    P2_4("2.4 Skriv till lagring & Databas")

    %% Databaser
    D1[("D1: Metadata DB")]
    D2[("D2: WORM Objektlagring")]
    D3[("D3: Immutable Audit Log")]

    %% Flöden
    Input -- "Fil + Metadata" --> P2_1
    P2_1 -- "Fil är ren, begär nyckel" --> P2_2
    P2_2 -- "Returnerar Data Encryption Key" --> P2_3
    P2_3 -- "Krypterat paket" --> P2_4
    
    P2_4 -- "Spara krypterad payload" --> D2
    P2_4 -- "Spara sökbar metadata" --> D1
    P2_4 -- "Logga: 'Fil X uppladdad av Användare Y'" --> D3
    
    %% Felhantering
    P2_1 -. "Om virus hittas" .-> Drop("Avbryt & Logga Säkerhetslarm")
```