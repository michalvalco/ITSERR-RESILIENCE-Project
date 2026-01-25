# GNORM Technical Briefing Questions

**Prepared by:** Michal Valčo
**Briefing Dates:** February 11-12, 2026
**Purpose:** Understand GNORM capabilities for integration with ethically-grounded AI agent prototype
**Primary Contact:** Dr. Arianna Maria Pavone (WP3 Coordinator, University of Palermo)
**Additional Contacts:** Andrea Esuli (ISTI-CNR, CRF annotation lead), Vincenzo Roberto Imperia, Andrea Ravasco

---

## Related Documentation

This document should be read alongside the existing implementation:

- **Architecture:** [`docs/architecture/gnorm-integration.md`](../docs/architecture/gnorm-integration.md) — System design and component overview
- **Implementation:** [`03_prototype/src/itserr_agent/integrations/gnorm.py`](../03_prototype/src/itserr_agent/integrations/gnorm.py) — Working client code
- **Configuration:** [`03_prototype/.env.example`](../03_prototype/.env.example) — GNORM environment variables
- **Stöckel Pilot:** [`03_prototype/stockel_annotation/CHAPTER_SELECTION.md`](../03_prototype/stockel_annotation/CHAPTER_SELECTION.md) — Chapter selection rationale

---

## What We Already Know (from CEUR Vol-3937 Paper)

Before the briefing, it's worth noting what the published paper has already revealed:

**Technical achievements:**
- CRF (Conditional Random Fields) outperformed BERT and Latin BERT for allegatio extraction
- CRF "rich" configuration: **97.8% accuracy**, 21 min training on desktop CPU, 1.1 MB model
- Latin BERT: 92.4% accuracy, 13 min on 4× A40 GPUs, 423 MB model
- **41,784 legal references** automatically annotated in Liber Extra's Ordinary Gloss
- **1,795 distinct referenced sections** indexed from Corpus Iuris Canonici and Corpus Iuris Civilis

**Code availability:**
- GitHub: `github.com/aesuli/CIC_annotation` (annotation pipeline)
- Zenodo: Dataset with training data and annotations

**Current focus:** Medieval canon law (Liber Extra, Decretales Gregorii IX)
**Expanding to:** Babylonian Talmud (Marco Papasidero's work)

---

## What We've Already Implemented (Prototype Status)

The prototype already has a working GNORM integration framework. During the briefing, we need to **validate these assumptions** and fill in the placeholders:

### GNORMClient (`integrations/gnorm.py`)

**Implemented:**
- Async HTTP client using `httpx.AsyncClient`
- Context manager pattern for proper resource cleanup
- Configurable base URL, timeout, and API key via environment variables
- Bearer token authentication (header format assumed)
- Request payload: `{"text": str, "language": str, "entity_types": list[str]?}`
- Response parsing into `GNORMAnnotation` dataclass

**Needs Confirmation:**
- [ ] API endpoint path (currently assumes `/annotate`)
- [ ] Exact request/response JSON schema
- [ ] Authentication mechanism (Bearer token correct?)
- [ ] Confidence score scale (assumed 0.0–1.0)

### GNORMAnnotation Dataclass

**Current fields:**
```python
entity_text: str      # The annotated text span
entity_type: str      # Entity category
start_offset: int     # Character position (start)
end_offset: int       # Character position (end)
confidence: float     # 0.0–1.0 (assumed)
metadata: dict | None # Additional data
```

**Epistemic mapping implemented:**
- `confidence ≥ 0.85` → `[FACTUAL]`
- `confidence < 0.85` → `[INTERPRETIVE]`
- Threshold is configurable via `ITSERR_HIGH_CONFIDENCE_THRESHOLD`

### GNORMTool (Human-Centered Pattern)

**Implemented:**
- Category: `EXTERNAL` (requires user confirmation + first-time gate)
- Formatted output with epistemic indicators
- Error handling with graceful degradation

### Configuration Options

```bash
# Current .env settings
ITSERR_GNORM_API_URL=http://localhost:8000  # Placeholder
ITSERR_GNORM_TIMEOUT=30
ITSERR_GNORM_API_KEY=                        # To be obtained
ITSERR_HIGH_CONFIDENCE_THRESHOLD=0.85
```

---

## Priority Questions (Must-Answer for Integration)

### 1. API Access & Endpoints

*These are essential for writing the integration code:*

- [ ] **Is there a REST API endpoint available?** Or is GNORM currently batch-processing only?
- [ ] **What is the API base URL?** (If exists)
- [ ] **What authentication is required?** (API key, bearer token, none for research access?)
- [ ] **Can I get sandbox/dev credentials** for the fellowship period?

### 2. Request/Response Format

*Needed to implement the `GNORMClient` class correctly:*

- [ ] **What is the exact request payload structure?**
  ```json
  // Current assumption in prototype:
  {
    "text": "string",
    "language": "la",  // Latin?
    "options": {}
  }
  ```
- [ ] **What is the exact response structure?**
  ```json
  // Current assumption:
  {
    "annotations": [
      {
        "entity": "Dig. 1.1.1",
        "type": "legal_reference",
        "start_offset": 10,
        "end_offset": 20,
        "confidence": 0.95
      }
    ],
    "metadata": {}
  }
  ```
- [ ] **How are confidence scores scaled?** (0-1, 0-100, or categorical?)
- [ ] **What annotation types are returned?** (legal references only, or also persons, places, etc.?)

### 3. Confidence Score Semantics

*Critical for mapping to epistemic indicators:*

My prototype maps GNORM confidence → epistemic indicators:
- `confidence ≥ 0.85` → `[FACTUAL]` (high reliability)
- `0.50 ≤ confidence < 0.85` → `[INTERPRETIVE]` (AI-assisted, needs evaluation)
- `confidence < 0.50` → `[INTERPRETIVE]` + review flag

**Questions:**
- [ ] **Does this threshold mapping make sense** given how CRF confidence scores are calibrated?
- [ ] **What does a 0.97 vs 0.75 vs 0.40 confidence actually mean** in GNORM's output?
- [ ] **Are there annotation types that should always be human-reviewed** regardless of confidence?

### 4. Text Input Requirements

*For preprocessing in the agent pipeline:*

- [ ] **What text encoding is expected?** (UTF-8, specific Latin character handling?)
- [ ] **Is there a maximum text length per request?**
- [ ] **Should abbreviations be expanded** before submission, or does GNORM handle them?
- [ ] **How does GNORM handle modern vs. medieval Latin?**

---

## Secondary Questions (Important but Less Urgent)

### 5. Generalizability Beyond Canon Law

*For understanding future applicability to Leonard Stöckel corpus and theological texts:*

- [ ] **How domain-specific is the current model?** (Canon law only, or transferable?)
- [ ] **What would be needed to adapt GNORM for:**
  - Patristic texts with biblical citations?
  - Reformation-era theological texts?
  - Biblical commentary traditions?
- [ ] **Is there a mechanism for fine-tuning** on new domains?
- [ ] **What training data format would be required** if we wanted to contribute Stöckel annotations?

### 6. The "Allegationes as Performative Acts" Question

*From my letter to Arianna - the hermeneutical dimension:*

The paper notes that allegationes in canon law glosses function not just as references but as **argumentative moves**—they're performative as much as informational.

- [ ] **How did the team think about preserving this dimension** in the annotation design?
- [ ] **Does the data model capture citation function** (authority appeal, counter-argument, etc.) or just citation identity?
- [ ] **Are there plans to model citation networks** showing argumentative flow?

### 7. Integration with Existing Tools

- [ ] **How does GNORM relate to CRITERION** (the critical editions tool)?
- [ ] **Is there a common annotation format** (TEI, Web Annotation, custom XML)?
- [ ] **Can GNORM annotations be exported** for use in other systems?

---

## Practical Logistics

### 8. Access During & After Fellowship

- [ ] **How will I access GNORM during Feb 10-27?** (Local installation, hosted endpoint, VPN?)
- [ ] **Can my prototype continue using GNORM after the fellowship** for research/publication purposes?
- [ ] **What attribution/acknowledgment is required** when publishing results using GNORM?

### 9. Technical Support

- [ ] **Who should I contact with technical questions** during prototype development?
- [ ] **Is there a Slack/Teams channel** for ITSERR developers?
- [ ] **Are there code examples** beyond the GitHub repo I can study?

---

## Stöckel Corpus Adaptation Questions

*These questions arise from analyzing GNORM's pipeline for adaptation to 16th-century Protestant theological texts.*

### 11. Citation Format Differences

**Context:** The GNORM pipeline is trained on medieval canon law citations (e.g., "X 2.1.3" for Decretales). Stöckel's *Annotationes* uses theological citation formats that differ significantly.

**Questions:**
- [ ] **How sensitive is the CRF model to citation format changes?**
  - Canon law: `X 2.1.3`, `Dig. 1.1.1`, `C. 33 q. 2 c. 1`
  - Theological: `Aug. de civ. Dei lib. 14`, `Rom. 3:23`, `Chrys. in Matt. hom. 12`
- [ ] **Would you recommend retraining from scratch** or fine-tuning on domain-specific data?
- [ ] **Which CRF features are most transferable** across citation domains?

### 12. Biblical Citation Handling

**Context:** Biblical citations have a distinct structure (Book Chapter:Verse) not present in canon law.

**Questions:**
- [ ] **Has GNORM encountered biblical citations** in the Liber Extra glosses? (Patristic sources often cite Scripture)
- [ ] **What feature modifications would you suggest** for book:chapter:verse patterns?
- [ ] **How should we handle abbreviated book names?** (Rom., Gen., Ioan. vs. Romans, Genesis, John)
- [ ] **Should biblical citations be a separate entity type** or a subtype of existing categories?

### 13. Patristic Author Abbreviations

**Context:** Stöckel uses standard humanist abbreviations for Church Fathers that differ from legal abbreviations.

| Author | Typical Abbreviation | Example Citation |
|--------|---------------------|------------------|
| Augustine | Aug. | Aug. de civ. Dei lib. 14 |
| Jerome | Hieron. | Hieron. ad Gal. |
| Chrysostom | Chrys. | Chrys. in Matt. hom. 12 |
| Ambrose | Ambr. | Ambr. de off. |

**Questions:**
- [ ] **Can the existing author detection features transfer?** Or do they need new training examples?
- [ ] **How did you handle abbreviation expansion** in the training data?
- [ ] **Is there a lookup table approach** that could be reused for patristic authors?

### 14. Mixed Language Handling

**Context:** Stöckel's Latin text occasionally includes German phrases or marginal notes, and biblical citations may reference vernacular translations.

**Questions:**
- [ ] **Did you encounter multilingual passages** in the Liber Extra?
- [ ] **How should the pipeline handle code-switching** between Latin and German?
- [ ] **Does the tokenization need adjustment** for 16th-century orthography?

### 15. Training Data Requirements

**Context:** We plan to create manual annotations using INCEpTION for pilot study chapters.

**Questions:**
- [ ] **What is the minimum training data size** for reasonable CRF performance?
  - GNORM expert set: 39 documents, 18,425 tokens
  - Stöckel pilot target: 3 chapters, ~150 references
- [ ] **Is 100-150 annotated references sufficient** for a proof-of-concept?
- [ ] **What annotation format should we export from INCEpTION** for compatibility?
  - WebAnno TSV 3.3?
  - UIMA CAS XMI?
  - Other?

### 16. Structural Differences

**Context:** The *Annotationes* is a commentary on Melanchthon's *Loci Communes*, not a legal gloss apparatus.

| Feature | Liber Extra Gloss | Stöckel Annotationes |
|---------|-------------------|----------------------|
| Base text structure | Legal titles/chapters | Theological topics (*loci*) |
| Gloss relationship | Marginal annotations to legal text | Expansions of doctrinal topics |
| Citation function | Legal authority appeals | Doctrinal proof-texting |
| Cross-references | To other legal texts | To Scripture, Fathers, Reformers |

**Questions:**
- [ ] **How important is structural context** (lemma position, gloss markers) for the CRF?
- [ ] **Can we adapt the "Lemma glossato" category** for biblical/theological terms?
- [ ] **Should we mark Melanchthon's original text** vs. Stöckel's annotations distinctly?

---

## Questions About GNORM's Roadmap

### 17. Future Development

- [ ] **What's the timeline for the Talmud extension?** (Marco Papasidero's work)
- [ ] **Are there plans for a public API** beyond the research consortium?
- [ ] **What additional entity types are planned?** (persons, places, concepts beyond legal references?)

---

## Notes During Briefing

### Day 1 - Feb 11 (Technical Overview with Arianna)

**API Details:**
```
Base URL: 
Auth method: 
Request format: 
Response format: 
Confidence scale: 
```

**Key insights:**




**Follow-up needed:**




### Day 2 - Feb 12 (Hands-on / Deep Dive)

**Tested scenarios:**




**Issues encountered:**




**Clarifications received:**




---

## Quick Reference Card

*Fill in during briefing for immediate development use*

| Parameter | Value |
|-----------|-------|
| **API Base URL** | |
| **Auth Type** | |
| **Auth Header Format** | |
| **Request Content-Type** | |
| **Response Content-Type** | |
| **Confidence Scale** | |
| **High Confidence (FACTUAL) Threshold** | |
| **Review Flag Threshold** | |
| **Max Text Length** | |
| **Rate Limit** | |
| **Support Contact (Email)** | |
| **Support Contact (Slack/Teams)** | |

---

## Post-Briefing Action Items

- [ ] Update `integrations/gnorm.py` with correct API details
- [ ] Update `core/config.py` with proper GNORM settings
- [ ] Test integration with real GNORM endpoint
- [ ] Adjust confidence → epistemic indicator mapping based on briefing insights
- [ ] Document any domain limitations discovered
- [ ] Schedule follow-up meeting if technical questions remain

---

*Document prepared: January 25, 2026*
*Last updated: January 25, 2026 (Stöckel-specific questions added)*
