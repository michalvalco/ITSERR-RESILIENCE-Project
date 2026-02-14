#!/usr/bin/env python3
"""
Zero-Shot CRF Experiment: GNORM Legal-Citation Model on Stöckel Theological Text

Runs the GNORM CRF model (trained on Liber Extra legal references) zero-shot
on Stöckel's Annotationes in Locos communes (1561) to observe what a
legal-citation NER model picks up in theological text.

This is an interesting cross-domain experiment:
  - The GNORM model was trained to recognise *allegationes normativae* (legal
    citations) in 13th-century glossed canon law text.
  - Stöckel's text contains *biblical and patristic citations* in 16th-century
    Latin theological commentary.
  - Both domains share structural citation patterns (abbreviated source +
    numeric reference), so non-trivial transfer is plausible.

The script:
  1. Loads a pre-trained CRF model (sklearn-crfsuite pickle)
  2. Tokenises the Stöckel normalised text
  3. Extracts the same features the GNORM pipeline uses
  4. Runs zero-shot prediction
  5. Reports what the model labels as entities and generates analysis

Usage:
    python zero_shot_crf_experiment.py <model_file> [--input-dir DIR] [--output-dir DIR]
    python zero_shot_crf_experiment.py --feature-demo   # Show feature extraction only

Dependencies:
    sklearn-crfsuite >= 0.3.6  (listed in pyproject.toml [annotation] extras)
    scikit-learn >= 1.4.0
"""

import argparse
import pickle
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import sklearn_crfsuite
    HAS_CRFSUITE = True
except ImportError:
    HAS_CRFSUITE = False

# Paths
DEFAULT_INPUT_DIR = Path(__file__).parent.parent / "data" / "normalized"
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "data" / "zero_shot_results"


@dataclass
class ExperimentStats:
    """Track experiment statistics."""
    files_processed: int = 0
    total_tokens: int = 0
    total_entities: int = 0
    entity_tokens: int = 0
    entities_by_label: dict = field(default_factory=dict)
    entity_texts: list = field(default_factory=list)
    precision_at_biblical: int = 0  # entities that are actually biblical refs
    entity_contexts: list = field(default_factory=list)


# =============================================================================
# FEATURE EXTRACTION (mirrors GNORM train_crfsuite.py)
# =============================================================================


def word_features(tokens: list[str], idx: int) -> dict[str, Any]:
    """
    Extract features for a single token, replicating the GNORM pipeline.

    Feature set (from GNORM_PIPELINE_ANALYSIS.md):
    - Current word features: lowercase, isupper, istitle, isdigit
    - Context window: 6 tokens before and after
    - Number normalization: digits → __NUM__
    - Boundary markers: __BOS__, __EOS__
    - Character n-grams: suffix/prefix up to 3 characters
    """
    word = tokens[idx]
    normalized = re.sub(r'\d', '0', word)  # Normalize digits

    features: dict[str, Any] = {
        "bias": 1.0,
        "word.lower()": word.lower(),
        "word.normalized": normalized.lower(),
        "word[-3:]": word[-3:] if len(word) >= 3 else word,
        "word[-2:]": word[-2:] if len(word) >= 2 else word,
        "word[:3]": word[:3] if len(word) >= 3 else word,
        "word[:2]": word[:2] if len(word) >= 2 else word,
        "word.isupper()": word.isupper(),
        "word.istitle()": word.istitle(),
        "word.isdigit()": word.isdigit(),
        "word.isalpha()": word.isalpha(),
        "word.len": len(word),
        "word.has_period": "." in word,
        "word.has_colon": ":" in word,
        "word.has_number": bool(re.search(r'\d', word)),
    }

    # Context window: 6 tokens before and after
    for offset in range(-6, 7):
        if offset == 0:
            continue
        prefix = f"{offset:+d}"
        context_idx = idx + offset
        if 0 <= context_idx < len(tokens):
            ctx_word = tokens[context_idx]
            features[f"{prefix}:word.lower()"] = ctx_word.lower()
            features[f"{prefix}:word.isupper()"] = ctx_word.isupper()
            features[f"{prefix}:word.istitle()"] = ctx_word.istitle()
            features[f"{prefix}:word.isdigit()"] = ctx_word.isdigit()
        else:
            # Boundary markers
            if context_idx < 0:
                features[f"{prefix}:BOS"] = True
            else:
                features[f"{prefix}:EOS"] = True

    return features


def extract_features(tokens: list[str]) -> list[dict[str, Any]]:
    """Extract features for all tokens in a sequence."""
    return [word_features(tokens, i) for i in range(len(tokens))]


# =============================================================================
# TOKENISATION
# =============================================================================


def tokenize_for_crf(text: str) -> list[tuple[str, int, int]]:
    """
    Tokenise text for CRF features, preserving character offsets.

    Uses simple whitespace + punctuation splitting consistent with GNORM.
    Returns list of (token_text, start_offset, end_offset).
    """
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        # Skip whitespace
        while i < n and text[i].isspace():
            i += 1
        if i >= n:
            break

        start = i
        char = text[i]

        # Single-character punctuation tokens
        if char in ".,;:!?()[]{}«»–—\"'§†‡<>/":
            tokens.append((char, start, start + 1))
            i += 1
        else:
            # Alphanumeric or other runs
            while (i < n and not text[i].isspace()
                   and text[i] not in ".,;:!?()[]{}«»–—\"'§†‡<>/"):
                i += 1
            tokens.append((text[start:i], start, i))

    return tokens


def sentences_from_text(text: str) -> list[str]:
    """
    Split text into sentence-like chunks for CRF processing.

    Splits on blank lines (paragraph boundaries), which is the convention
    used in the GNORM BIOES format.
    """
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]


# =============================================================================
# PREDICTION AND ANALYSIS
# =============================================================================


def predict_with_model(
    model: Any,
    tokens: list[str],
) -> list[str]:
    """Run CRF prediction on a token sequence."""
    features = extract_features(tokens)
    return model.predict([features])[0]


def extract_entities(
    tokens: list[tuple[str, int, int]],
    labels: list[str],
) -> list[tuple[str, str, int, int]]:
    """
    Extract entity spans from BIOES labels.

    Returns list of (entity_text, entity_label, start_offset, end_offset).
    """
    entities = []
    current_tokens: list[str] = []
    current_label = ""
    current_start = 0
    current_end = 0

    for (tok_text, tok_start, tok_end), label in zip(tokens, labels):
        if label.startswith("S-"):
            # Single-token entity
            entity_label = label[2:]
            entities.append((tok_text, entity_label, tok_start, tok_end))
        elif label.startswith("B-"):
            # Begin new entity
            current_tokens = [tok_text]
            current_label = label[2:]
            current_start = tok_start
            current_end = tok_end
        elif label.startswith("I-") and current_tokens:
            # Continue entity
            current_tokens.append(tok_text)
            current_end = tok_end
        elif label.startswith("E-") and current_tokens:
            # End entity
            current_tokens.append(tok_text)
            current_end = tok_end
            entity_text = " ".join(current_tokens)
            entities.append((entity_text, current_label, current_start, current_end))
            current_tokens = []
        elif label == "O":
            # Reset if we were in an entity (malformed sequence)
            if current_tokens:
                entity_text = " ".join(current_tokens)
                entities.append((entity_text, current_label, current_start, current_end))
                current_tokens = []

    # Handle unclosed entity at end
    if current_tokens:
        entity_text = " ".join(current_tokens)
        entities.append((entity_text, current_label, current_start, current_end))

    return entities


def get_context(text: str, start: int, end: int, window: int = 40) -> str:
    """Get surrounding context for an entity."""
    ctx_start = max(0, start - window)
    ctx_end = min(len(text), end + window)
    before = text[ctx_start:start].replace("\n", " ")
    entity = text[start:end]
    after = text[end:ctx_end].replace("\n", " ")
    return f"...{before}[{entity}]{after}..."


def is_likely_biblical_ref(entity_text: str) -> bool:
    """Heuristic check if an entity looks like a biblical reference."""
    biblical_abbrevs = {
        "gen", "exod", "levit", "num", "deut", "iosu", "iudic", "ruth",
        "reg", "sam", "paral", "chron", "esdr", "nehem", "esther",
        "iob", "psalm", "psal", "prov", "eccles", "cant",
        "isa", "hierem", "ier", "thren", "ezech", "dan",
        "ose", "ioel", "amos", "abd", "ion", "mich", "nahum", "habac",
        "sophon", "agg", "zachar", "malach",
        "matth", "matt", "marc", "luc", "ioan", "iohan", "ioh",
        "act", "actor", "rom", "cor", "galat", "ephes", "philip",
        "coloss", "thess", "tim", "tit", "philem", "hebr",
        "petr", "iac", "iud", "apocal", "apoc",
    }
    lower = entity_text.lower()
    for abbrev in biblical_abbrevs:
        if abbrev in lower:
            return True
    # Check for numeric pattern (chapter:verse style)
    if re.search(r'\d+[.:]\s*\d+', entity_text):
        return True
    return False


# =============================================================================
# EXPERIMENT RUNNER
# =============================================================================


def run_experiment(
    model_path: Path,
    input_dir: Path,
    output_dir: Path,
) -> ExperimentStats:
    """Run the zero-shot CRF experiment on Stöckel normalised text."""
    stats = ExperimentStats()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load model
    print(f"Loading CRF model: {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print(f"Model classes: {model.classes_}")
    print(f"Model transitions: {len(model.transition_features_)}")

    # Process each normalised text file
    input_files = sorted(input_dir.glob("annotationes_pp*.txt"))
    if not input_files:
        print(f"No input files found in {input_dir}")
        return stats

    print(f"\nProcessing {len(input_files)} files...\n")

    all_entities: list[tuple[str, str, str, str]] = []  # (file, entity, label, context)

    for input_file in input_files:
        print(f"  {input_file.name}", end="")
        text = input_file.read_text(encoding="utf-8")

        # Skip header lines
        lines = text.split("\n")
        content_lines = [l for l in lines if not l.startswith("#")]
        text = "\n".join(content_lines)

        file_entities = []
        paragraphs = sentences_from_text(text)

        for para in paragraphs:
            tokens = tokenize_for_crf(para)
            if not tokens:
                continue

            token_texts = [t[0] for t in tokens]
            stats.total_tokens += len(token_texts)

            try:
                labels = predict_with_model(model, token_texts)
            except Exception as e:
                print(f" [ERROR: {e}]")
                continue

            entities = extract_entities(tokens, labels)

            # Count tokens that are part of entities (non-"O" labels) once per paragraph
            stats.entity_tokens += sum(1 for l in labels if l != "O")

            for entity_text, entity_label, start, end in entities:
                context = get_context(para, start, end)
                file_entities.append((entity_text, entity_label, context))

        stats.files_processed += 1
        stats.total_entities += len(file_entities)

        for entity_text, entity_label, context in file_entities:
            all_entities.append((input_file.name, entity_text, entity_label, context))
            stats.entity_texts.append(entity_text)
            stats.entity_contexts.append(context)

            # Count by label
            stats.entities_by_label[entity_label] = (
                stats.entities_by_label.get(entity_label, 0) + 1
            )

            # Check if actually a biblical ref
            if is_likely_biblical_ref(entity_text):
                stats.precision_at_biblical += 1

        print(f" → {len(file_entities)} entities found")

    # Write detailed results
    _write_results(all_entities, stats, output_dir)

    return stats


def run_feature_demo(input_dir: Path) -> None:
    """Demonstrate feature extraction on a sample of Stöckel text."""
    input_files = sorted(input_dir.glob("annotationes_pp*.txt"))
    if not input_files:
        print(f"No input files found in {input_dir}")
        return

    # Read first file
    text = input_files[0].read_text(encoding="utf-8")
    lines = text.split("\n")
    content_lines = [l for l in lines if not l.startswith("#")]
    text = "\n".join(content_lines)

    paragraphs = sentences_from_text(text)
    if not paragraphs:
        print("No paragraphs found")
        return

    # Take first paragraph
    para = paragraphs[0]
    tokens = tokenize_for_crf(para)
    token_texts = [t[0] for t in tokens]

    print("=" * 60)
    print("FEATURE EXTRACTION DEMO")
    print("=" * 60)
    print(f"\nSource: {input_files[0].name}")
    print(f"Paragraph (first 200 chars): {para[:200]}...")
    print(f"Tokens: {len(token_texts)}")
    print()

    # Show features for first 10 tokens
    features = extract_features(token_texts)
    for i in range(min(10, len(tokens))):
        tok = token_texts[i]
        feat = features[i]
        print(f"Token [{i}]: '{tok}'")
        for key in sorted(feat.keys()):
            if not key.startswith(("-", "+")):  # Skip context features for readability
                print(f"  {key}: {feat[key]}")
        print()


def _write_results(
    all_entities: list[tuple[str, str, str, str]],
    stats: ExperimentStats,
    output_dir: Path,
) -> None:
    """Write experiment results to output files."""
    # Detailed entity list
    results_path = output_dir / "zero_shot_entities.tsv"
    with open(results_path, "w", encoding="utf-8") as f:
        f.write("file\tentity_text\tlabel\tis_biblical\tcontext\n")
        for file_name, entity_text, label, context in all_entities:
            is_bib = is_likely_biblical_ref(entity_text)
            f.write(f"{file_name}\t{entity_text}\t{label}\t{is_bib}\t{context}\n")

    # Analysis report
    report_path = output_dir / "ZERO_SHOT_REPORT.md"
    entity_counter = Counter(stats.entity_texts)

    report = f"""# Zero-Shot CRF Experiment Report

## Experiment Design

**Model:** GNORM CRF (trained on Liber Extra legal citations)
**Target text:** Stöckel, *Annotationes in Locos communes* (1561)
**Method:** Zero-shot transfer — no theological training data

## Summary Statistics

| Metric | Value |
|--------|-------|
| Files processed | {stats.files_processed} |
| Total tokens | {stats.total_tokens} |
| Total entities found | {stats.total_entities} |
| Entity tokens | {stats.entity_tokens} |
| Annotation density | {stats.entity_tokens / max(stats.total_tokens, 1) * 100:.1f}% |

## Entity Labels

| Label | Count |
|-------|-------|
"""
    for label, count in sorted(stats.entities_by_label.items()):
        report += f"| {label} | {count} |\n"

    report += f"""
## Biblical Reference Overlap

Of {stats.total_entities} entities found, {stats.precision_at_biblical} ({stats.precision_at_biblical / max(stats.total_entities, 1) * 100:.0f}%) match biblical reference heuristics.

This suggests the legal-citation model {'does' if stats.precision_at_biblical > stats.total_entities * 0.3 else 'does not'} transfer meaningfully to theological citation patterns.

## Most Frequent Entity Texts

| Entity | Frequency |
|--------|-----------|
"""
    for entity, count in entity_counter.most_common(30):
        report += f"| {entity} | {count} |\n"

    report += """
## Interpretation

The GNORM CRF model was trained on medieval Latin legal citations with features
including word shape, context windows, and character n-grams. When applied
zero-shot to 16th-century Latin theological text:

1. **Structural similarity**: Both legal and biblical citations follow
   `abbreviation + number` patterns (e.g., "c. 12" in law vs. "Rom. 5" in theology)
2. **Feature transfer**: Character-level features (periods, digits, titlecase)
   generalise across domains
3. **Domain gap**: The model may over-predict entities (legal references are
   denser in the Glossa Ordinaria than biblical refs in Stöckel) or miss
   theological-specific patterns

## Files

- `zero_shot_entities.tsv` — detailed entity list with context
- `ZERO_SHOT_REPORT.md` — this report
"""

    report_path.write_text(report, encoding="utf-8")
    print(f"\nResults written to: {output_dir}")


def print_summary(stats: ExperimentStats) -> None:
    """Print experiment summary to console."""
    print("\n" + "=" * 60)
    print("ZERO-SHOT CRF EXPERIMENT SUMMARY")
    print("=" * 60)
    print(f"Files processed:        {stats.files_processed}")
    print(f"Total tokens:           {stats.total_tokens}")
    print(f"Entities found:         {stats.total_entities}")
    if stats.total_entities > 0:
        print(f"Biblical ref matches:   {stats.precision_at_biblical} "
              f"({stats.precision_at_biblical / stats.total_entities * 100:.0f}%)")
    print(f"\nEntities by label:")
    for label, count in sorted(stats.entities_by_label.items()):
        print(f"  {label}: {count}")
    if stats.entity_texts:
        counter = Counter(stats.entity_texts)
        print(f"\nTop 10 most frequent entities:")
        for entity, count in counter.most_common(10):
            print(f"  '{entity}' × {count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Zero-shot CRF experiment: GNORM model on Stöckel text"
    )
    parser.add_argument(
        "model_file", nargs="?", type=Path,
        help="Pre-trained CRF model (pickle file)"
    )
    parser.add_argument(
        "--input-dir", type=Path, default=DEFAULT_INPUT_DIR,
        help=f"Directory with normalised text files (default: {DEFAULT_INPUT_DIR})"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for results (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--feature-demo", action="store_true",
        help="Run feature extraction demo (no model needed)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Zero-Shot CRF Experiment")
    print("GNORM Legal-Citation Model → Stöckel Theological Text")
    print("=" * 60)

    if args.feature_demo:
        run_feature_demo(args.input_dir)
        return

    if not args.model_file:
        parser.error("model_file is required (unless using --feature-demo)")

    if not HAS_CRFSUITE:
        print(
            "ERROR: sklearn-crfsuite is required but not installed.\n"
            "Install with: pip install 'itserr-agent[annotation]'",
        )
        return

    if not args.model_file.exists():
        print(f"ERROR: Model file not found: {args.model_file}")
        return

    stats = run_experiment(args.model_file, args.input_dir, args.output_dir)
    print_summary(stats)


if __name__ == "__main__":
    main()
