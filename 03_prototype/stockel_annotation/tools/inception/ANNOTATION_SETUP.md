# INCEpTION Annotation Setup for Stöckel Corpus

This guide explains how to configure INCEpTION for annotating citations in Leonard Stöckel's *Annotationes in Locos communes* (1561).

## Quick Start

```bash
# 1. Run setup script (downloads INCEpTION)
chmod +x setup_inception.sh
./setup_inception.sh

# 2. Start the server
./start_inception.sh

# 3. Open browser to http://localhost:8080
# Login: admin / admin
```

---

## Project Configuration

### Step 1: Create New Project

1. Log in as **admin**
2. Click **Projects** → **Create Project**
3. Enter project details:
   - **Name:** `Stöckel Annotationes Pilot`
   - **Description:** `Citation annotation pilot study for ITSERR fellowship`

### Step 2: Configure Annotation Layers

Create the following annotation layers to match the GNORM schema:

#### Layer 1: Citation (Span)

| Setting | Value |
|---------|-------|
| Name | `Citation` |
| Type | Span |
| Granularity | Character |
| Allow overlapping | No |
| Allow crossing sentence boundaries | Yes |

**Features:**

| Feature | Type | Values |
|---------|------|--------|
| `citation_type` | String (tagset) | `biblical`, `patristic`, `reformation`, `classical`, `legal` |
| `normalized_form` | String | Free text for standardized reference |
| `confidence` | String (tagset) | `certain`, `probable`, `uncertain` |

#### Layer 2: CitationTarget (Relation)

| Setting | Value |
|---------|-------|
| Name | `CitationTarget` |
| Type | Relation |
| Attach to | Citation |

**Features:**

| Feature | Type | Values |
|---------|------|--------|
| `target_type` | String (tagset) | `work`, `author`, `passage` |

#### Layer 3: StructuralElement (Span)

| Setting | Value |
|---------|-------|
| Name | `StructuralElement` |
| Type | Span |
| Granularity | Sentence |

**Features:**

| Feature | Type | Values |
|---------|------|--------|
| `element_type` | String (tagset) | `chapter`, `section`, `lemma`, `gloss` |
| `title` | String | Free text |

### Step 3: Create Tagsets

Navigate to **Settings** → **Tagsets** and create:

#### Tagset: citation_type
```
biblical     - Biblical reference (OT/NT)
patristic    - Church Father citation
reformation  - Reformation-era author
classical    - Classical author (Cicero, Aristotle, etc.)
legal        - Legal/canonical reference
```

#### Tagset: confidence
```
certain      - Clear, unambiguous citation
probable     - Likely citation, minor ambiguity
uncertain    - Possible citation, needs verification
```

#### Tagset: element_type
```
chapter      - Chapter/locus heading
section      - Section within chapter
lemma        - Term being glossed
gloss        - Explanatory gloss text
```

---

## Importing Documents

### Step 1: Prepare Text Files

The normalized text files are in `../data/normalized/`:
- `annotationes_pp1-5.txt`
- `annotationes_pp6-10.txt`
- ... (12 files total)

### Step 2: Import to INCEpTION

1. In your project, go to **Documents**
2. Click **Import**
3. Select format: **Plain text (UTF-8)**
4. Upload files from `data/normalized/`
5. Click **Import**

### Step 3: Assign Documents

1. Go to **Workload**
2. Assign documents to annotators
3. Set document states to **In Progress**

---

## Annotation Guidelines

### Biblical Citations

**Pattern:** Book + Chapter (+ Verse)

Examples:
- `Rom. 5` → `biblical` | `Romans 5`
- `Psalm. 51` → `biblical` | `Psalm 51`
- `Genef. 3` (OCR for Genesis) → `biblical` | `Genesis 3`
- `Matth. 5` → `biblical` | `Matthew 5`

**Common OCR variants:**
- `Genef.` = Genesis (f for s)
- `Pfal.` = Psalm
- `Efa.` = Isaiah (Esaias)

### Patristic Citations

**Pattern:** Author name (+ work title)

Examples:
- `Augustinus` → `patristic` | `Augustine`
- `Hieronymus in epistola ad...` → `patristic` | `Jerome`
- `Chrysostomus homilia...` → `patristic` | `Chrysostom`

**Common authors:**
- Augustinus/August. = Augustine
- Hieronymus = Jerome
- Chrysostomus = Chrysostom
- Ambrosius = Ambrose
- Cyprianus = Cyprian

### Reformation Citations

**Pattern:** Author name (often indirect)

Examples:
- `Philippus` (= Melanchthon) → `reformation` | `Melanchthon`
- `Lutherus` → `reformation` | `Luther`

### Classical Citations

**Pattern:** Author + work

Examples:
- `Cicero in Tusculanis` → `classical` | `Cicero, Tusculan Disputations`
- `Aristoteles` → `classical` | `Aristotle`
- `Plato` → `classical` | `Plato`

---

## Export Formats

For compatibility with the GNORM pipeline, export annotations as:

1. **UIMA CAS XMI** (primary format for CRF training)
2. **WebAnno TSV 3.3** (alternative format)
3. **CoNLL** (for sequence labeling)

### Export Steps

1. Go to **Documents** → **Export**
2. Select format: `UIMA CAS XMI (XML 1.1)`
3. Download exported files to `../data/annotations/`

---

## Quality Control

### Inter-Annotator Agreement

If multiple annotators:
1. Create a **curation** user
2. Use **Curation** mode to resolve disagreements
3. Export curated annotations

### Annotation Statistics

Track progress in INCEpTION:
- **Dashboard** shows document completion
- **Agreement** tab shows IAA metrics

### Target Metrics

| Metric | Target |
|--------|--------|
| Annotated citations | 100+ |
| Citation types covered | 4+ (biblical, patristic, reformation, classical) |
| IAA (if applicable) | κ > 0.8 |

---

## Troubleshooting

### Server won't start
- Check Java version: `java -version` (need 17+)
- Check port 8080 is free: `lsof -i :8080`
- Check logs: `~/.inception/logs/`

### Import fails
- Ensure files are UTF-8 encoded
- Remove BOM if present
- Check file permissions

### Annotations not saving
- Check browser console for errors
- Ensure sufficient disk space
- Try different browser

---

## Resources

- [INCEpTION User Guide](https://inception-project.github.io/releases/32.0/docs/user-guide.html)
- [INCEpTION Admin Guide](https://inception-project.github.io/releases/32.0/docs/admin-guide.html)
- [WebAnno TSV Format](https://webanno.github.io/webanno/releases/3.6.0/docs/user-guide.html#sect_webannotsv)
- [GNORM Pipeline](https://github.com/aesuli/CIC_annotation)

---

*Last updated: January 26, 2026*
