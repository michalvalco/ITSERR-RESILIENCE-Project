# Zenodo Dataset Analysis Report

**Dataset:** GNORM Liber Extra Annotations
**DOI:** 10.5281/zenodo.14381709
**Analysis Date:** January 25, 2026

---

## Dataset Overview

| Dataset | Documents | Format |
|---------|-----------|--------|
| Complete corpus | 186 | All formats (webanno, conll, tei, etc.) |
| Expert annotations | 39 | webanno TSV 3.3 |
| INCEpTION export | 186 | UIMA CAS XMI |

---

## Expert Annotation Statistics

| Metric | Value |
|--------|-------|
| Documents | 39 |
| Total annotation tokens | 18,425 |
| Unique legal references | 462 |
| Average per document | 472.4 |

### Top 10 Documents by Annotation Density

| Document | Annotations |
|----------|-------------|
| 2.02 DE FORO COMPETENTI | 3,943 |
| 1.02 DE CONSTITUTIONIBUS | 3,080 |
| 1.33 DE MAIORITATE ET OBEDIENTIA | 2,784 |
| 2.23 DE PRAESUMPTIONIBUS | 2,364 |
| 1.11 DE TEMPORIBUS ORDINATIONUM | 2,203 |
| 2.03 DE LIBELLI OBLATIONE | 747 |
| 1.38 DE PROCURATORIBUS | 444 |
| 2.10 DE ORDINE COGNITIONUM | 349 |
| 1.42 DE ALIENATIONE IUDICII... | 344 |
| 1.01 DE SUMMA TRINITATE... | 341 |

---

## Directory Structure

```
data/raw/
├── allegations_all/           # Complete corpus (186 docs)
│   ├── conll/                 # CoNLL format
│   ├── conllu/                # CoNLL-U format
│   ├── nif/                   # NLP Interchange Format
│   ├── tei/                   # TEI XML
│   ├── txt/                   # Plain text
│   ├── uima_cas/              # UIMA CAS XMI
│   └── webanno/               # WebAnno TSV 3.3
│
├── allegations_inception/     # INCEpTION project export
│   ├── annotation_ser/        # Serialized annotations
│   ├── source/                # Source documents
│   └── exportedproject.json   # Project metadata
│
├── extra_allegation_inception/ # Expert INCEpTION export
│   ├── annotation_ser/
│   ├── gazeteers/
│   └── source/
│
└── extra_allegations_expert/  # Expert annotations (39 docs)
    ├── conll/
    ├── conllu/
    ├── nif/
    ├── tei/
    ├── txt/
    ├── uima_cas/
    └── webanno/               # Contains expert.tsv files
```

---

## Annotation Format

### WebAnno TSV 3.3 Format

```
#FORMAT=WebAnno TSV 3.3
#T_SP=webanno.custom.Glossa|Tipo

#Text=Example sentence with legal reference 28. q. 1 § quod autem
1-1    0-7     Example    _
1-2    8-16    sentence   _
...
1-12   128-130 28         Allegazione normativa[1]
1-13   130-131 .          Allegazione normativa[1]
1-14   132-133 q          Allegazione normativa[1]
1-15   133-134 .          Allegazione normativa[1]
1-16   135-136 1          Allegazione normativa[1]
1-17   137-138 §          Allegazione normativa[1]
1-18   139-143 quod       Allegazione normativa[1]
1-19   144-149 autem      Allegazione normativa[1]
```

**Columns:**
1. Token ID (sentence-token)
2. Character offsets (start-end)
3. Token text
4. Annotation label (`_` for none, `Allegazione normativa[N]` for legal reference)

---

## Entity Type

| Type | Italian | English | Count |
|------|---------|---------|-------|
| `Allegazione normativa` | Legal allegation | Legal reference/citation | 462 unique |

---

## Relevance for Stöckel Corpus

### Similarities
- Dense citation networks (legal → theological)
- Abbreviated reference formats
- Marginal gloss apparatus

### Differences to Address
- Biblical citations (not in GNORM)
- Patristic references (Augustine, Jerome, etc.)
- Reformation-era contemporary sources
- German vernacular text

### Recommended Approach
1. Use expert annotations (39 docs) for understanding annotation patterns
2. Study `2.02 DE FORO COMPETENTI` (highest density) as reference
3. Adapt annotation schema for theological entity types

---

*Generated from GNORM Zenodo dataset analysis*
