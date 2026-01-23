# Epistemic API Reference

API documentation for the epistemic classification system.

## IndicatorType

Enum defining the three epistemic indicator types.

```python
from itserr_agent.epistemic.indicators import IndicatorType

class IndicatorType(str, Enum):
    FACTUAL = "FACTUAL"
    INTERPRETIVE = "INTERPRETIVE"
    DEFERRED = "DEFERRED"
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `tag` | `str` | Inline tag format (e.g., `"[FACTUAL]"`) |
| `description` | `str` | Human-readable description |
| `examples` | `list[str]` | Example content for this type |

### Methods

#### from_tag

```python
@classmethod
def from_tag(cls, tag: str) -> IndicatorType | None
```

Parse an indicator type from a tag string.

**Example:**

```python
indicator = IndicatorType.from_tag("[FACTUAL]")
# Returns IndicatorType.FACTUAL

indicator = IndicatorType.from_tag("invalid")
# Returns None
```

## EpistemicIndicator

Data class representing an indicator attached to content.

```python
from itserr_agent.epistemic.indicators import EpistemicIndicator

@dataclass
class EpistemicIndicator:
    indicator_type: IndicatorType
    confidence: float  # 0.0 to 1.0
    content: str
    rationale: str | None = None
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `tag` | `str` | The inline tag |
| `tagged_content` | `str` | Content with tag prepended |
| `needs_review` | `bool` | Whether human review is suggested |

### Methods

#### to_dict / from_dict

```python
def to_dict(self) -> dict[str, Any]

@classmethod
def from_dict(cls, data: dict[str, Any]) -> EpistemicIndicator
```

## EpistemicClassifier

Rule-based classifier for epistemic indicators.

```python
from itserr_agent.epistemic.classifier import EpistemicClassifier
from itserr_agent.core.config import AgentConfig
```

### Constructor

```python
EpistemicClassifier(config: AgentConfig)
```

### Methods

#### classify_and_tag

```python
def classify_and_tag(self, content: str) -> str
```

Classify content and insert epistemic indicator tags.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | `str` | Raw content to classify |

**Returns:** Content with epistemic indicator tags inserted

**Example:**

```python
classifier = EpistemicClassifier(config)

raw = "Gadamer published Truth and Method in 1960. This suggests a connection to Heidegger."
tagged = classifier.classify_and_tag(raw)
# "[FACTUAL] Gadamer published Truth and Method in 1960. [INTERPRETIVE] This suggests a connection to Heidegger."
```

#### classify_sentence

```python
def classify_sentence(self, sentence: str) -> EpistemicIndicator
```

Classify a single sentence.

**Returns:** `EpistemicIndicator` for the sentence

**Example:**

```python
indicator = classifier.classify_sentence("According to Barth (CD I/1, p. 47)...")
# indicator.indicator_type == IndicatorType.FACTUAL
# indicator.confidence == 0.9
# indicator.rationale == "Contains citation or source reference"
```

#### classify_gnorm_annotation

```python
def classify_gnorm_annotation(
    self,
    annotation: dict[str, Any],
    confidence_score: float,
) -> IndicatorType
```

Classify a GNORM annotation based on its confidence score.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `annotation` | `dict` | The GNORM annotation data |
| `confidence_score` | `float` | Confidence score (0.0 to 1.0) |

**Returns:** Appropriate `IndicatorType`

#### get_classification_explanation

```python
def get_classification_explanation(
    self,
    indicator: EpistemicIndicator
) -> str
```

Generate a human-readable explanation of the classification.

**Example:**

```python
indicator = classifier.classify_sentence("God desires all to be saved.")
explanation = classifier.get_classification_explanation(indicator)
print(explanation)
# Classified as DEFERRED:
#   Confidence: 85%
#   Rationale: Contains theological or normative content
#   Description: Matters requiring human judgment that AI cannot determine
```

## Marker Lists

Pre-defined keyword lists for classification:

```python
from itserr_agent.epistemic.indicators import (
    FACTUAL_MARKERS,
    INTERPRETIVE_MARKERS,
    DEFERRED_MARKERS,
)
```

### FACTUAL_MARKERS

Keywords suggesting factual content:

```python
FACTUAL_MARKERS = [
    "published", "wrote", "in", "page", "p.", "pp.",
    "according to", "states", "defined as", "is called",
    "born", "died", "dated", "located", "isbn", "doi",
]
```

### INTERPRETIVE_MARKERS

Keywords suggesting interpretive content:

```python
INTERPRETIVE_MARKERS = [
    "suggests", "appears", "seems", "might", "could", "may",
    "possibly", "likely", "pattern", "connection", "theme",
    "similar", "relates", "resembles", "echoes", "parallels",
    "indicates", "implies", "analysis", "comparison",
]
```

### DEFERRED_MARKERS

Keywords suggesting deferred content:

```python
DEFERRED_MARKERS = [
    "should", "ought", "must", "correct", "true", "false",
    "right", "wrong", "better", "worse", "sacred", "divine",
    "salvation", "sin", "holy", "righteous",
    "spiritual significance", "theological truth", "god's will",
    "meaning of life",
]
```

## Usage Examples

### Basic Classification

```python
from itserr_agent.epistemic.classifier import EpistemicClassifier
from itserr_agent.core.config import AgentConfig

config = AgentConfig()
classifier = EpistemicClassifier(config)

# Classify a full response
response = """
Gadamer published Truth and Method in 1960.
His concept of Wirkungsgeschichte suggests that understanding is historically effected.
Whether this approach is theologically adequate requires careful reflection.
"""

tagged = classifier.classify_and_tag(response)
print(tagged)
# [FACTUAL] Gadamer published Truth and Method in 1960.
# [INTERPRETIVE] His concept of Wirkungsgeschichte suggests that understanding is historically effected.
# [DEFERRED] Whether this approach is theologically adequate requires careful reflection.
```

### Sentence-Level Analysis

```python
sentences = [
    "Luther wrote the 95 Theses in 1517.",
    "This appears to echo Augustine's theology of grace.",
    "The true meaning of justification is a matter of faith.",
]

for sentence in sentences:
    indicator = classifier.classify_sentence(sentence)
    print(f"{indicator.tag} ({indicator.confidence:.0%}): {sentence}")
    if indicator.needs_review:
        print("  ⚠️ Flagged for review")
```

### Working with GNORM Results

```python
from itserr_agent.epistemic.classifier import EpistemicClassifier

# GNORM returns annotations with confidence scores
gnorm_annotations = [
    {"text": "Augustine", "type": "person", "confidence": 0.92},
    {"text": "grace", "type": "concept", "confidence": 0.65},
]

for ann in gnorm_annotations:
    indicator_type = classifier.classify_gnorm_annotation(
        annotation=ann,
        confidence_score=ann["confidence"]
    )
    print(f"[{indicator_type.value}] {ann['text']} ({ann['confidence']:.0%})")
# [FACTUAL] Augustine (92%)
# [INTERPRETIVE] grace (65%)
```

### Custom Thresholds

```python
from itserr_agent.core.config import AgentConfig

# Stricter thresholds
config = AgentConfig(
    high_confidence_threshold=0.95,  # Higher bar for FACTUAL
    low_confidence_threshold=0.6,    # Higher bar for review flag
)

classifier = EpistemicClassifier(config)
```
