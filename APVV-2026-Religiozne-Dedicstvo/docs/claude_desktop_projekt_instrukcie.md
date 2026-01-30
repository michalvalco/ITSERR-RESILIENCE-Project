# Inštrukcie pre Claude Desktop Projekt

## Ako vytvoriť projekt v Claude Desktop

1. Otvorte Claude Desktop aplikáciu
2. Kliknite na **"Projects"** v ľavom menu
3. Kliknite na **"New Project"**
4. Zadajte názov: **"APVV Grant - Náboženské dedičstvo"**

## Vlastné inštrukcie pre projekt

Skopírujte nasledujúci text do poľa **"Custom Instructions"** (Project Instructions):

---

```
## Kontext projektu

Pomáhaš s prípravou žiadosti o grant APVV VV 2025 s názvom:
"Digitálne sprístupnenie a výskumné využitie náboženského dedičstva Slovenska"

### Kľúčové termíny
- **Deadline:** 11. február 2026
- **Max. financovanie:** 301 800 EUR
- **Dĺžka projektu:** max. 48 mesiacov
- **Začiatok:** 1. september 2026

### Riešiteľský tím
- **Zodpovedný riešiteľ:** Prof. Dr. Michal Valčo, PhD. (EBF UK)
- **Spoluriešiteľ:** Mgr. Radoslav Hanus, PhD. (EBF UK)
- **Spoluriešiteľka:** PhDr. Eva Kowalská, DrSc. (HÚ SAV)

### Partnerská organizácia
- Historický ústav SAV, v. v. i.

### Spolupracujúce inštitúcie
- Ústredná knižnica SAV (oddelenie starých fondov)
- Slovenský národný archív
- Slovenská národná knižnica (Literárny archív)
- Lyceálne knižnice (Kežmarok, Prešov)
- RESILIENCE/ITSERR (európska infraštruktúra)

### Hlavné ciele projektu
1. Mapovanie archívnych fondov náboženského dedičstva
2. Vypracovanie metodiky popisu a katalogizácie
3. Pilotná digitalizácia vybraných fondov
4. Vytvorenie online portálu
5. Integrácia do RESILIENCE infraštruktúry

### Štýl a jazyk
- Píš formálnym akademickým štýlom v slovenčine
- Pre anglické verzie používaj britskú angličtinu
- Dodržiavaj terminológiu APVV výzvy
- Odkazuj na relevantné slovenské aj európske projekty

### Dôležité odkazy
- GitHub repo: https://github.com/michalvalco/APVV-2026-Religiozne-Dedicstvo
- APVV výzva: https://www.apvv.sk/grantove-schemy/vseobecne-vyzvy/vv-2025.html
- RESILIENCE: https://www.resilience-ri.eu/
- ITSERR: https://www.itserr.it/

### Pri písaní žiadosti
- Zdôrazňuj medzinárodnú dimenziu (RESILIENCE)
- Vyzdvihuj unikátnosť slovenských fondov
- Uvádzaj konkrétne archívy a zbierky
- Odkazuj na existujúce digitalizačné projekty
```

---

## Odporúčané súbory na nahratie do projektu

Nahrajte do projektu nasledujúce súbory:

### Z GitHub repozitára
1. `01_ziadost/draft/struktura_ziadosti.md` - Náčrt štruktúry projektu
2. `04_mapovanie/digitalizovane_fondy.md` - Prehľad existujúcich zdrojov
3. `05_admin/timeline.md` - Harmonogram prípravy

### Z APVV stránky
1. Úplné znenie výzvy (PDF)
2. Príloha 2: Hodnotiace kritériá (PDF)
3. Príloha 3: Zásady tvorby rozpočtu (PDF)
4. Príloha 4 alebo 5: Vzor žiadosti (PDF)

---

## Workflow: Claude Desktop + GitHub

### 1. Písanie a konzultácie → Claude Desktop
Použite Claude Desktop Projekt na:
- Písanie drafov jednotlivých častí žiadosti
- Konzultácie formulácií
- Preklad do angličtiny
- Kontrolu súladu s hodnotiacimi kritériami

### 2. Verzionovanie a kolaborácia → GitHub
Po dokončení draftu:
1. Skopírujte text do príslušného súboru v repozitári
2. Commitnite zmeny s jasným popisom
3. Kolegovia môžu komentovať a navrhovať zmeny

### 3. Finalizácia → Claude Code
Pre technické úlohy (štruktúra súborov, formátovanie, git operácie):
- Použite Claude Code v termináli
- Pracujte priamo v repozitári

---

## Príklady promptov pre Claude Desktop

### Písanie vecného zámeru
```
Napíš úvodnú časť vecného zámeru projektu (cca 500 slov), ktorá:
1. Predstaví problematiku náboženského dedičstva na Slovensku
2. Zdôrazní potrebu digitalizácie a sprístupnenia
3. Uvedie prepojenie na európsku infraštruktúru RESILIENCE
```

### Preklad do angličtiny
```
Prelož nasledujúci text do akademickej angličtiny, zachovaj odbornú terminológiu:
[vložte slovenský text]
```

### Kontrola hodnotiacich kritérií
```
Skontroluj, či nasledujúci text spĺňa hodnotiace kritérium "Vedecká kvalita projektu" podľa prílohy 2 výzvy APVV VV 2025:
[vložte text]
```

### Formulácia výstupov
```
Naformuluj 5 konkrétnych merateľných výstupov projektu pre pracovný balík WP1 (Mapovanie archívnych fondov), vrátane kvantifikácie.
```

---

## Synchronizácia medzi prostrediami

### Po práci v Claude Desktop
1. Skopírujte finálny text
2. Otvorte GitHub repozitár
3. Vložte do príslušného súboru v `01_ziadost/draft/`
4. Commitnite zmeny

### Po práci v Claude Code
1. Zmeny sú automaticky v repozitári
2. V Claude Desktop aktualizujte nahrané súbory, ak je potrebné

---

*Tento dokument je súčasťou repozitára APVV-2026-Religiozne-Dedicstvo*
