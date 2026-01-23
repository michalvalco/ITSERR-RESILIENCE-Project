# Epistemic Modesty Indicators: Architecture Detail

**Status:** Implementation Guide
**References:** `system_design.md` Section 3.2
**Implementation:** `src/itserr_agent/epistemic/`

---

## Overview

The Epistemic Modesty Indicators system provides clear differentiation of response types to prevent false certainty about interpretive matters. This is not merely a labeling system—it embodies the project's commitment to epistemic humility in AI-assisted religious studies research.

---

## Philosophical Foundation

### The Problem of AI Confidence

Standard LLMs present information with uniform confidence, regardless of whether the content is:
- A verifiable fact ("Gadamer published Truth and Method in 1960")
- An interpretive synthesis ("This suggests a connection to...")
- A matter of theological judgment ("The correct interpretation is...")

This uniformity is dangerous in religious studies, where:
1. Scholarly claims often involve contested interpretations
2. Theological truth claims transcend AI competence
3. Value judgments about religious practices require human wisdom

### Our Solution: Explicit Epistemic Marking

Every substantive claim is tagged with its epistemic status, making the nature of the content transparent to the researcher.

---

## Indicator Taxonomy

### [FACTUAL]

**Definition:** Verifiable information that can be checked against sources.

**Characteristics:**
- Can be confirmed through primary sources
- Represents scholarly consensus or direct citation
- Does not involve interpretive judgment

**Examples:**
| Content | Why FACTUAL |
|---------|-------------|
| "Gadamer published Truth and Method in 1960" | Verifiable date |
| "According to Ricoeur, 'the symbol gives rise to thought'" | Direct quotation |
| "The Council of Chalcedon met in 451 CE" | Historical fact |
| "This term appears 47 times in the Pauline corpus" | Countable data |

**Confidence Signal:** High—can be verified by researcher.

---

### [INTERPRETIVE]

**Definition:** AI-assisted analysis involving pattern recognition, synthesis, or comparative observation.

**Characteristics:**
- Involves AI contribution beyond retrieval
- Should be verified by researcher
- Represents "might be useful" rather than "is true"

**Examples:**
| Content | Why INTERPRETIVE |
|---------|------------------|
| "This passage echoes themes found in Augustine" | Pattern recognition |
| "The structure suggests a chiastic arrangement" | Structural analysis |
| "Gadamer and Ricoeur seem to diverge on this point" | Comparative observation |
| "This concept connects to your earlier discussion of..." | Synthesis across sessions |

**Confidence Signal:** Moderate—AI contribution, verify before relying on it.

---

### [DEFERRED]

**Definition:** Matters requiring human judgment that AI cannot and should not determine.

**Characteristics:**
- Theological truth claims
- Value judgments about religious practices
- "Correct" interpretation of contested texts
- Questions of spiritual significance

**Examples:**
| Content | Why DEFERRED |
|---------|--------------|
| "Whether this represents authentic divine revelation" | Theological judgment |
| "The correct interpretation of this contested passage" | Interpretive authority |
| "Whether this practice should be considered liturgically valid" | Normative judgment |
| "The spiritual significance of this symbol" | Matters of faith |

**Confidence Signal:** Explicit deferral—this is beyond AI competence.

---

## Classification Pipeline

### Architecture

```
User Query → Agent Response → Classification Pipeline → Tagged Response
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
             Heuristic Check    Pattern Check      LLM Verification
             (fast, rule-based) (regex, markers)  (fallback, nuanced)
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                                       ▼
                              Tagged Response
```

### Stage 1: Heuristic Check (Fast Path)

Rule-based classification for clear cases:

```python
def heuristic_classify(sentence: str) -> IndicatorType | None:
    # Direct citation → FACTUAL
    if has_citation_pattern(sentence):
        return IndicatorType.FACTUAL

    # Explicit deferral language → DEFERRED
    if contains_deferred_markers(sentence):
        return IndicatorType.DEFERRED

    # Multiple interpretive markers → INTERPRETIVE
    if count_interpretive_markers(sentence) >= 2:
        return IndicatorType.INTERPRETIVE

    # Unclear—proceed to next stage
    return None
```

### Stage 2: Pattern Check (Regex)

More sophisticated pattern matching:

```python
CITATION_PATTERNS = [
    r"\([^)]*\d{4}[^)]*\)",      # (Author 2020)
    r"\[[^\]]+\d+[^\]]*\]",       # [1] or [Author, 2020]
    r"p{1,2}\.\s*\d+",            # p. 123, pp. 45-67
    r"according to \w+",          # according to Gadamer
]

DEFERRED_PATTERNS = [
    r"the\s+correct\s+interpretation",
    r"spiritually\s+(true|significant)",
    r"god['']?s\s+(will|intention)",
    r"(should|must)\s+be\s+(believed|accepted)",
]

INTERPRETIVE_PATTERNS = [
    r"(suggests?|appears?|seems?)\s+to",
    r"(might|could|may)\s+(indicate|suggest)",
    r"(pattern|connection|theme)\s+",
    r"(similar|parallel|echoes?)\s+",
]
```

### Stage 3: LLM Verification (Fallback)

For ambiguous cases, use LLM judgment:

```python
CLASSIFICATION_PROMPT = """
Classify this sentence into exactly one category:

FACTUAL: Verifiable information (dates, quotes, bibliographic data)
INTERPRETIVE: AI-assisted analysis (patterns, connections, synthesis)
DEFERRED: Requires human judgment (theological claims, value judgments)

Sentence: "{sentence}"

Respond with only the category name.
"""
```

**Note:** LLM verification adds latency and cost. Use sparingly—only when heuristics fail.

---

## Indicator Placement

### Inline Tags

Tags are placed immediately before the content they modify:

```
[FACTUAL] Gadamer defines the hermeneutical circle as the process
by which understanding of parts and whole mutually inform each other.

[INTERPRETIVE] This definition appears to connect with your earlier
interest in how pre-understanding shapes interpretation.

[DEFERRED] Whether Gadamer's approach ultimately provides adequate
grounding for theological interpretation remains a matter of
scholarly and theological debate that you must assess.
```

### Sentence-Level vs. Paragraph-Level

**Current approach:** Sentence-level tagging for granular clarity.

**Consideration:** Some responses may warrant paragraph-level tagging for readability:

```
[INTERPRETIVE] The following analysis connects several themes from
your recent research. Gadamer's concept of effective-historical
consciousness seems to parallel Ricoeur's emphasis on the productive
role of distanciation. Both thinkers resist the subject-object
dichotomy of Enlightenment epistemology, though they arrive at this
position through different routes.
```

**Decision:** Make granularity configurable. Default to sentence-level for precision.

---

## Integration with GNORM

### Mapping Confidence Scores

GNORM provides confidence scores (0-1) for named entity annotations. We map these to epistemic indicators:

```python
def map_gnorm_confidence(confidence: float, config: AgentConfig) -> IndicatorType:
    if confidence >= config.high_confidence_threshold:  # default: 0.85
        return IndicatorType.FACTUAL
    elif confidence >= config.low_confidence_threshold:  # default: 0.5
        return IndicatorType.INTERPRETIVE
    else:
        # Low confidence still INTERPRETIVE, but flagged for review
        return IndicatorType.INTERPRETIVE  # with review flag
```

### Annotation Display

```
GNORM identified the following entities in this passage:

[FACTUAL] "Augustine" - Person (confidence: 0.94)
[FACTUAL] "Hippo" - Place (confidence: 0.89)
[INTERPRETIVE] "divine illumination" - Concept (confidence: 0.67)
  ⚠️ This annotation should be verified

[INTERPRETIVE] Note: Entity extraction is probabilistic. High-confidence
annotations can be treated as factual; lower-confidence annotations
represent the model's best guess and should be verified.
```

---

## Edge Cases and Guidelines

### Mixed Content

Some sentences contain both factual and interpretive elements:

**Input:** "Gadamer published Truth and Method in 1960, which suggests his thinking was influenced by post-war European philosophy."

**Handling:** Split and tag separately:
```
[FACTUAL] Gadamer published Truth and Method in 1960.
[INTERPRETIVE] This timing suggests his thinking was influenced by
post-war European philosophy.
```

### Hedged Factual Claims

Scholarly hedging ("most scholars agree") doesn't make a claim interpretive—it's still about verifiable scholarly consensus:

**Input:** "Most scholars agree that Paul wrote Romans around 57 CE."

**Classification:** [FACTUAL] - The claim is about scholarly consensus, which is verifiable.

### AI-Generated Examples

When the AI generates examples to illustrate a point, these are interpretive:

**Input:** "For instance, the parable of the Good Samaritan might be read as a critique of religious exclusivism."

**Classification:** [INTERPRETIVE] - The example involves interpretation.

### Theological Descriptions vs. Claims

Describing theological positions is FACTUAL; affirming them is DEFERRED:

| Statement | Classification |
|-----------|----------------|
| "Aquinas argued that God's existence can be demonstrated through natural reason" | FACTUAL |
| "God's existence can be demonstrated through natural reason" | DEFERRED |
| "The Lutheran tradition emphasizes justification by faith alone" | FACTUAL |
| "Justification is by faith alone" | DEFERRED |

---

## User Interface Considerations

### Visual Differentiation

Indicators should be visually distinct:

```
CLI:
  [FACTUAL] in green
  [INTERPRETIVE] in yellow
  [DEFERRED] in red/magenta

Web UI:
  Color-coded badges or highlighting
  Tooltip explanations on hover
```

### Legend/Help

Provide accessible explanation of indicators:

```
📘 FACTUAL: Verifiable information - check the source
📙 INTERPRETIVE: AI analysis - verify before relying on it
📕 DEFERRED: Human judgment needed - you decide
```

### Indicator Density

If a response becomes cluttered with indicators, consider:
1. Summary indicator at paragraph level
2. Expandable detail view
3. "View indicators" toggle

---

## Quality Assurance

### Classification Validation

Periodically validate classification accuracy:

```python
VALIDATION_CASES = [
    ("Aquinas died in 1274", IndicatorType.FACTUAL),
    ("This suggests a trinitarian structure", IndicatorType.INTERPRETIVE),
    ("This is the correct interpretation", IndicatorType.DEFERRED),
    # ... more test cases
]

def validate_classifier(classifier: EpistemicClassifier) -> float:
    correct = sum(
        1 for text, expected in VALIDATION_CASES
        if classifier.classify_sentence(text).indicator_type == expected
    )
    return correct / len(VALIDATION_CASES)
```

### Feedback Loop

Allow users to flag misclassifications:

```python
@dataclass
class ClassificationFeedback:
    sentence: str
    assigned_indicator: IndicatorType
    correct_indicator: IndicatorType
    user_rationale: str | None
    timestamp: datetime
```

---

## Implementation Checklist

- [ ] Indicator enum with metadata (description, examples)
- [ ] Heuristic classification rules
- [ ] Regex pattern library
- [ ] LLM fallback classifier
- [ ] GNORM confidence mapping
- [ ] Mixed content splitting
- [ ] CLI formatting with colors
- [ ] Validation test suite
- [ ] User feedback mechanism

---

## Configuration Options

```python
class EpistemicConfig:
    # Classification
    default_indicator: IndicatorType = INTERPRETIVE
    use_llm_fallback: bool = True

    # Thresholds
    high_confidence_threshold: float = 0.85
    low_confidence_threshold: float = 0.5

    # Display
    indicator_granularity: str = "sentence"  # or "paragraph"
    show_confidence_scores: bool = False

    # GNORM integration
    gnorm_map_to_indicators: bool = True
    flag_low_confidence_gnorm: bool = True
```

---

## References

- `system_design.md` - Parent architecture document
- `01_research/epistemic_modesty_framework.md` - Theoretical foundation
- ITSERR project guidelines on AI ethics
