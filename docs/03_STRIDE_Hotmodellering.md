# Hotmodellering med STRIDE

Med utgångspunkt i våra Dataflödesdiagram (DFD Level 1 & 2) och de identifierade tillitsgränserna har vi genomfört en hotmodellering enligt STRIDE-metodiken. Syftet är att systematiskt identifiera vad som kan gå fel när data rör sig mellan olika zoner.

| STRIDE | Hot | Beskrivning | Konsekvens | DFD-Plats |
|:---|:---|:---|:---|:---|
| **S**poofing | Token theft | Stulna JWT används för att imitera legitim handläggare. | Obehörig API-access. | P1 (Gateway) |
| **T**ampering | API Manipulation / IDOR | Manipulation av objekt-ID:n kringgår access policies. | Dataintegritetsbrott. | P1/D2 |
| **R**epudiation | Bristande spårbarhet | Loggar saknar korrelation IDs → händelser kan ej rekonstrueras. | Bristande forensik. | D3 (Audit) |
| **I**nfo Disclosure | Over-permissive ABAC | Felaktiga policyregler exponerar metadata via sökfilter. | GDPR/OSL-brott. | P3 (Retrieval) |
| **D**oS | Resource exhaustion | Upload floods eller zip-bomber mättar ingest-pipeline. | System outage. | P2 (Ingest) |
| **E**levation | Broken authorization | Service-to-service anrop saknar korrekt policy enforcement. | Systemkompromiss. | P2/P3 (Internal) |
