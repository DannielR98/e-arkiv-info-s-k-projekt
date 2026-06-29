## Systemöversikt: ArchiveSecure AB

ArchiveSecure AB är ett fiktivt, hög-säkert e-arkivsystem utformat för kommuner och statliga myndigheter. Systemet möjliggör långtidslagring (10–50 år) av känsliga dokument och strukturerad data i enlighet med offentlighets- och sekretesslagen (OSL), GDPR, arkivlagen samt kraven i NIS2-direktivet.

Lösningen bygger på en modern mikrotjänstarkitektur där all kommunikation och dataåtkomst styrs av Zero-Trust-principer. Det innebär att inget internt nätverk är implicit betrott och att varje transaktion kräver explicit autentisering och auktorisering.

Huvudanvändare och Aktörer:

    Handläggare (Läs/Skriv): Myndighetspersonal som arkiverar och söker fram dokument.

    Systemadministratörer (Drift): Hanterar plattformens hälsa och infrastruktur.

    Säkerhetsadministratörer / CISO: Granskar audit-loggar, hanterar incidenter och säkerhets-policies.

    Externa Verksamhetssystem (Maskin-till-Maskin): Diarieföringssystem och ärendehanteringssystem som integrerar via API för automatiserad arkivering.

### Övergripande Arkitektur

Arkitekturen är uppdelad i strikta säkerhetszoner för att minimera attackytan och förhindra lateral förflyttning (lateral movement) vid ett eventuellt intrång.

```mermaid
graph TD
    %% Definition av stilar och färger för zoner
    classDef external fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef dmz fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
    classDef app fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
    classDef data fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
    classDef security fill:#f8cecc,stroke:#b85450,stroke-width:2px;

    %% ZONE 1: EXTERNAL
    subgraph External_Zone [EXTERNAL ZONE]
        User([Användare / Externa System])
    end
    class External_Zone external;

    %% ZONE 2: DMZ / INGRESS
    subgraph DMZ_Ingress [DMZ / INGRESS TIER]
        WAF[WAF & DDoS Protection]
        Gateway[API Gateway]
        IdP[Identity Provider / SSO]
    end
    class DMZ_Ingress dmz;

    %% ZONE 3: APPLICATION
    subgraph App_Tier [APPLICATION TIER - ZERO TRUST]
        Ingest[Ingest Service <br/> Validering & Virusskanning]
        Archive[Archive Service <br/> Indexering & AIP-paketering]
        Retrieval[Retrieval Service <br/> Sök, Avkryptering & Maskering]
        LogService[Audit & Logging Service]
    end
    class App_Tier app;

    %% ZONE 4: DATA & STORAGE
    subgraph Data_Tier [DATA & STORAGE TIER]
        DB[(Metadata DB <br/> Krypterad at-rest)]
        WORM[(Objektlagring <br/> WORM / Oföränderlig)]
        KMS[Key Management System <br/> HSM / KMS]
    end
    class Data_Tier data;

    %% ZONE 5: MANAGEMENT & SECURITY
    subgraph Security_Tier [MANAGEMENT & SECURITY TIER]
        ImmutableLog[(Immutable Audit Log <br/> WORM-logg)]
        SIEM[SIEM / SOC Integration]
    end
    class Security_Tier security;

    %% Flöden och relationer
    User -->|TLS 1.3 / mTLS| WAF
    WAF --> Gateway
    Gateway <-->|Autentisering / JWT| IdP
    
    Gateway -->|Verifierat anrop| Ingest
    Gateway -->|Verifierat anrop| Retrieval

    Ingest --> Archive
    Archive --> DB
    Archive --> WORM
    Retrieval --> DB
    Retrieval --> WORM

    %% Nyckelhantering (KMS)
    KMS -.->|Dekryptering/Kryptering| Archive
    KMS -.->|Dekryptering/Kryptering| Retrieval
    KMS -.->|Nyckelrotation| DB
    KMS -.->|Nyckelrotation| WORM

    %% Loggningsflöde
    Ingest & Archive & Retrieval --> LogService
    LogService -->|Enkelriktat / Write-only| ImmutableLog
    ImmutableLog --> SIEM

```

Komponentbeskrivning

    WAF & API Gateway: Terminerar extern trafik, skyddar mot OWASP Top 10-attacker och rate-limitar anrop.

    Identity Provider (IdP): Hanterar all autentisering via OIDC/SAML2 mot myndigheternas egna katalogtjänster. Kräver multifaktorautentisering (MFA).

    Objektlagring (WORM): Den faktiska lagringen av filerna konfigureras med Write Once Read Many-lås på hårdvaru- eller molnnivå för att garantera att arkiverad data inte kan manipuleras, ens av en administratör, under den lagstadgade bevarandetiden.

    Key Management System (KMS): Hanterar livscykeln för de kryptografiska nycklar som används för att kryptera både metadata och dokument at-rest.

### Kritiska Tillgångar (Key Assets)

För att säkerställa att vi applicerar rätt säkerhetskontroller måste vi definiera vad vi skyddar. Följande tillgångar utgör kärnan i ArchiveSecure AB:s skyddsvärde.
Informationstillgångar

    Arkivobjekt (Dokument/Filer): Den primära tillgången. Kan innehålla allt från offentliga protokoll till djupt sekretessklassad information (exempelvis individärenden inom socialtjänsten).

    Arkivmetadata: Beskrivande data (vem, vad, när, varför) kopplat till dokumenten. Innehåller ofta personuppgifter och är affärskritisk för sökbarhet.

    Personuppgifter (PII): Förekommer i både dokument, metadata och användarkonton. Skyddas primärt på grund av GDPR-krav.

System- och Infrastrukturtillgångar

    Kryptografiska Nycklar (Root & Data Encryption Keys): Om dessa komprometteras förloras antingen sekretessen för all data, eller så förloras tillgängligheten (kryptografisk radering). Den absolut mest kritiska tekniska tillgången.

    Audit Logs (Spårbarhetsloggar): Oföränderliga loggar som bevisar vem som har läst, lagt till eller försökt manipulera data. Kritiskt ur ett bevis- och GRC-perspektiv (Governance, Risk, Compliance).

    IAM-reglerverk (Auktoriseringsmatriser): Reglerna som definierar vilken myndighet eller handläggare som har åtkomst till vilka arkivbildare