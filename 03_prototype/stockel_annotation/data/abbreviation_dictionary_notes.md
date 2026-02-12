# Abbreviation Dictionary: Notes and Methodology

**Version:** 0.1 (preliminary, from initial scan of Postilla transcriptions)  
**Date:** 12 February 2026  
**Source material:** Postilla, 1596 — Transcriptions folders 01–05

---

## What This File Is

`abbreviation_dictionary_v0.1.csv` is a preliminary inventory of citation abbreviations found in or expected from Leonard Stöckel's Postilla (1596). It serves two purposes:

1. **For Arianna:** Shows we've thought about Layer 2 adaptation (abbreviation lookup) and have concrete material to discuss
2. **For the project:** Seed dictionary to be expanded as we process more pages

## How the CSV Is Structured

| Column | Purpose |
|--------|---------|
| `abbreviation` | The abbreviated form as it appears in the text |
| `expansion_latin` | Full Latin form |
| `expansion_english` | English translation (for readability) |
| `type` | Category: `biblical`, `patristic`, `patristic_work`, `confessional`, `structural` |
| `language` | Source language (all Latin so far) |
| `citation_format_example` | Actual or expected citation as it appears in text |
| `variants` | Alternative spellings/abbreviation forms attested or expected |
| `notes` | Disambiguation, OCR concerns, special handling needed |

## What We Found in the Transcriptions

### Citation Format Patterns

Stöckel uses **at least four distinct citation formats**, sometimes within the same page:

1. **Marginal references** — abbreviation + chapter number in the margin (e.g., `Marci 1.` / `Rom. 6.` appearing as marginal notes alongside the body text)
2. **Inline references** — woven into Latin prose (e.g., `iuxta testimonium Iohannis 1.`)
3. **Full introductory formulas** — `sicut ait Paulus` followed by the reference
4. **Clustered references** — multiple references strung together: `Actor: 20. 1. Cor: 16. Apocal: 1:`

### Separator Inconsistency

This is significant for the CRF and rule-based layers. Stöckel (or his printer Gutgesel) uses **both periods and colons** as separators, sometimes mixing them:

- `Rom. 13.` (period-period)
- `Actor: 20.` (colon-period)  
- `Apocal: 1:` (colon-colon)
- `1. Cor: 16.` (period-colon-period)

The CIC_annotation rule layer uses regex — these patterns need to be accounted for.

### Marginal Notes as a Distinct Feature

Unlike the Liber Extra (which has glosses in a structured apparatus), Stöckel's Postilla has **marginal annotations** that are part of the original printed text. These include:

- Biblical references (most common)
- Topical headings (`Hunc Christum esse promissum Regem & Messiam`)
- Structural markers (`Probatur ex circumstantia:`, `Discrimen quadruplex`)

The transcriptions capture these as separate lines or inline annotations. The pipeline will need to handle them — they are a rich source of citation data but require different parsing than body text.

### What's Attested vs. Expected

The CSV marks entries as either **attested** (found in the transcriptions we read) or **expected** (standard Reformation abbreviations likely to appear in the full corpus). Specifically:

**Attested in transcriptions read so far:**
- Matt., Marci, Luca/Lucae/Lucæ, Iohan./Ioh., Actor., Rom., 1. Cor./2. Corinth:, Philip./Philipp., 1. Ioan., Gen./Gene., Psal./Psalmo, Dan., Zachar., 2. Reg., Apocal., cap., fol.

**Expected but not yet attested** (will appear in full corpus):
- Aug. (Augustine), Hier. (Jerome), Ambr. (Ambrose), Chrys. (Chrysostom)
- CA, FC, Apol., Cat. Mai./Min., Loc. Com.
- Most confessional abbreviations

## What Still Needs to Be Done

### Immediate (before showing to Arianna)
- [ ] Scan remaining transcription folders (06–10) for additional patterns
- [ ] Verify the `Postila, od s. 69.docx` file — may contain additional transcribed material
- [ ] Add entries for Old Testament prophetic books (Isa., Ier., Ezech., etc.)
- [ ] Add entries for Pentateuch books (Exod., Levit., Num., Deut.)

### During fellowship (with Arianna's input)
- [ ] Compare structure to the CIC abbreviation dictionary format
- [ ] Determine matching logic: exact match only, or prefix/fuzzy matching?
- [ ] Decide whether variants should be separate rows or handled by regex
- [ ] Add confidence levels for expected vs. attested entries

### Longer-term (annotation team work)
- [ ] Systematic compilation from full Stöckel corpus (3,000–4,000 pages)
- [ ] Cross-check against standard Reformation abbreviation references
- [ ] Add German-language abbreviation variants (for German passages in texts)
- [ ] Add early Slovak abbreviation forms (for Category 2 and 3 materials)

## Key Technical Observations for Arianna

1. **The separator inconsistency** (period vs. colon) is the single biggest challenge for the rule-based layer. In CIC, legal citation format is standardised. In Stöckel, it is not.

2. **Character-level features matter here.** The variation between `Lucae` and `Lucæ`, or between `Iohan.` and `Ioh.` and `Ioann.`, is at the character level. This supports the argument for adding character n-gram features to the CRF (Question Q7 in the Working Agenda).

3. **Marginal references are structurally distinct.** They function like the CIC glossae but are typographically different. The pipeline may need to process margins separately from body text, or at minimum tag them differently.

4. **The catechetical format** (numbered questions: "1. Quis est status?") creates structural patterns that could confuse the CRF if it mistakes question numbers for citation numbers.

---

*This is a working document. Update as the dictionary expands.*
