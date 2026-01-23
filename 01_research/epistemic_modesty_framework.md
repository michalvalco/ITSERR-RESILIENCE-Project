# Epistemic Modesty Framework for AI-Assisted Theological Research

## Version 0.1 — Pre-Fellowship Draft

**Author:** Prof. Michal Valčo
**Date:** [Date]
**Status:** Working draft—to be refined during GNORM technical briefing and fellowship discussions

---

## Abstract

This document articulates a framework for "epistemic modesty" in AI systems designed to assist theological and religious studies scholarship. Drawing on personalist anthropology and hermeneutical theory, it argues that AI tools must explicitly differentiate between factual recall, interpretive synthesis, and matters requiring human judgment. The framework proposes a tripartite indicator system (`[FACTUAL]`, `[INTERPRETIVE]`, `[DEFERRED]`) operationalizing this distinction in human-AI interaction.

---

## 1. The Problem: Hermeneutical Flattening

### 1.1 Definition

**Hermeneutical flattening** occurs when AI systems treat all textual content as equally processable, collapsing the interpretive complexity of religious and theological texts into uniform computational representations.

This manifests as:

- **False equivalence**: Treating verifiable facts and contested interpretations as having equal epistemic status
- **Confidence miscalibration**: Presenting interpretive claims with the same certainty as factual ones
- **Agency displacement**: Implicitly positioning the AI as interpreter rather than the human researcher
- **Contextual blindness**: Ignoring the situatedness of interpretation within traditions, communities, and personal formation

### 1.2 Why This Matters for Religious Studies

Religious and theological texts operate on multiple registers simultaneously:

| Register | Example | Appropriate AI Role |
|----------|---------|---------------------|
| **Historical-factual** | "Luther posted the 95 Theses in 1517" | Verification, citation |
| **Textual-linguistic** | "The Hebrew term *hesed* appears 248 times in the OT" | Counting, pattern identification |
| **Interpretive-synthetic** | "This passage echoes Wisdom literature themes" | Suggesting connections (flagged as interpretation) |
| **Theological-normative** | "This text teaches that God is love" | Deferral to human judgment |
| **Existential-transformative** | "What does this mean for my faith?" | Beyond AI competence |

AI systems that fail to distinguish these registers risk:

1. Undermining scholarly rigor by blurring fact and interpretation
2. Eroding researcher agency by positioning AI as authority
3. Flattening theological claims to mere information
4. Missing the formative dimension of theological engagement

### 1.3 The Stakes

For the humanities scholar, an AI that presents theological interpretations with factual confidence is worse than useless—it is actively misleading. It imports a positivist epistemology inappropriate to the subject matter. The goal is not to eliminate AI assistance but to design it with appropriate epistemic humility.

---

## 2. Philosophical Foundations

### 2.1 Personalist Anthropology

The framework draws on personalist philosophy (Mounier, Buber, Wojtyla) to ground three key claims:

**Claim 1: The person as irreducible interpreter**

> "The human person is not merely a processor of information but a situated interpreter whose understanding is shaped by formation, tradition, and encounter." (cf. Mounier)

AI cannot replicate the existential situatedness that grounds theological interpretation. It can assist but not replace the person-as-interpreter.

**Claim 2: Dialogue over instrumentalism**

> "Authentic knowledge emerges through I-Thou encounter, not I-It manipulation." (cf. Buber)

The AI-researcher relationship should approach dialogue—mutual responsiveness, transparency, respect for the other's contribution—rather than pure instrumentalism where AI is merely a tool.

**Claim 3: Agency preservation**

> "The researcher must remain the 'acting person' who takes responsibility for interpretive judgments." (cf. Wojtyla)

AI designs that subtly shift interpretive agency to the machine undermine the researcher's self-determination. The framework insists on explicit markers that preserve human agency.

### 2.2 Hermeneutical Theory

From Gadamer and Ricoeur, the framework draws:

**The hermeneutical circle**: Understanding proceeds through iterative engagement between part and whole, text and interpreter. AI can support this process but cannot stand outside it.

**Effective-historical consciousness**: Every interpreter brings a "horizon" shaped by history, tradition, and prejudgment. AI lacks such a horizon; it simulates pattern recognition without genuine historical consciousness.

**Surplus of meaning**: Texts, especially sacred texts, carry more meaning than any single interpretation can exhaust. AI systems should signal this inexhaustibility rather than implying closure.

**Distanciation and appropriation**: Ricoeur distinguishes the text's autonomy from the reader's act of making it one's own. AI can assist with distanciation (objective analysis) but appropriation remains irreducibly personal.

### 2.3 Synthesis: Epistemic Modesty as Design Principle

Epistemic modesty is the deliberate design choice to:

1. **Acknowledge limitations**: The AI explicitly marks the boundaries of its competence
2. **Differentiate epistemic status**: Different types of claims receive different treatment
3. **Preserve agency**: The human researcher remains the primary interpreter
4. **Signal uncertainty**: Where genuine uncertainty exists, it is communicated rather than masked

This is not merely a safety feature but a positive design value emerging from the nature of the subject matter.

---

## 3. The Indicator Framework

### 3.1 Tripartite Classification

The framework proposes three epistemic indicators for AI responses:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│    [FACTUAL]        [INTERPRETIVE]        [DEFERRED]            │
│                                                                  │
│    Verifiable       AI-assisted           Requires human        │
│    information      synthesis             judgment              │
│                                                                  │
│    ───────────      ─────────────         ─────────────         │
│                                                                  │
│    High confidence  Medium confidence     Beyond AI             │
│    Source-backed    Pattern-based         competence            │
│    Checkable        Should be verified    Researcher decides    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 [FACTUAL] — Verifiable Information

**Definition**: Claims that can be verified against authoritative sources and are not subject to significant scholarly dispute.

**Characteristics**:
- Citation-backed or citation-backable
- Consensus among relevant scholars
- Empirically or documentarily verifiable
- Not dependent on interpretive frameworks

**Examples**:
- Bibliographic data: "Gadamer published *Truth and Method* in 1960"
- Direct quotations with citations
- Historical dates with scholarly consensus
- Statistical data from texts: "The term appears 47 times"
- Definitions from specified sources

**Signal to researcher**: This information can be trusted as accurate within normal scholarly standards. Verification is possible and encouraged.

### 3.3 [INTERPRETIVE] — AI-Assisted Synthesis

**Definition**: Claims involving pattern recognition, connection-making, or synthetic analysis where the AI contributes beyond mere retrieval.

**Characteristics**:
- Based on patterns the AI identifies
- Involves inference or synthesis
- May be useful but should be verified
- Represents AI's contribution to interpretation

**Examples**:
- Thematic connections: "This passage shares vocabulary with X"
- Structural observations: "The argument follows a chiastic pattern"
- Comparative analysis: "Unlike Author A, Author B emphasizes..."
- Literature mapping: "This concept relates to discussions in..."
- Suggested implications: "This might suggest that..."

**Signal to researcher**: This is the AI's analysis. It may be valuable but reflects the AI's pattern recognition, not authoritative interpretation. The researcher should evaluate critically.

### 3.4 [DEFERRED] — Human Judgment Required

**Definition**: Matters where the AI explicitly declines to render judgment because they require human interpretive authority, value judgment, or theological discernment.

**Characteristics**:
- Normative or evaluative claims
- Theological truth assertions
- Matters of contested interpretation
- Questions requiring existential engagement
- Value judgments about religious practices

**Examples**:
- "What does this text really mean?" → [DEFERRED]
- "Is this interpretation correct?" → [DEFERRED]
- "What should I believe about X?" → [DEFERRED]
- "Is this practice spiritually beneficial?" → [DEFERRED]
- "How should the church respond to Y?" → [DEFERRED]

**Signal to researcher**: The AI cannot and should not determine this. The researcher, in their situatedness and responsibility, must make this judgment.

### 3.5 Edge Cases and Hybrid Responses

Many responses will combine indicator types:

```
User: "What do scholars say about Paul's view of justification?"

Response:
[FACTUAL] The term δικαιοσύνη (dikaiosyne) appears 58 times in
Paul's letters, with the highest concentration in Romans (34x)
and Galatians (11x).

[INTERPRETIVE] There appear to be two major scholarly camps:
the traditional Protestant reading emphasizing forensic
justification, and the "New Perspective" associated with Sanders,
Dunn, and Wright emphasizing covenant membership. Your sources
seem to engage more with the latter.

[DEFERRED] Which reading more faithfully represents Paul's
intention, and what this means for contemporary theology,
are questions that require your own engagement with the texts
and tradition.
```

---

## 4. Implementation Considerations

### 4.1 Classification Mechanisms

The framework can be implemented through:

**Prompt Engineering**:
- System prompts that define indicators and provide examples
- Instructions to classify each claim before presenting

**Post-Processing**:
- Heuristic checks ensuring indicators are present
- Pattern matching for normative language (triggers [DEFERRED])
- Citation detection (supports [FACTUAL])

**Model Fine-Tuning** (future):
- Training on examples of appropriate classification
- Reward modeling for epistemic humility

### 4.2 Failure Modes

| Failure | Description | Mitigation |
|---------|-------------|------------|
| Under-deferral | AI makes normative claims without [DEFERRED] | Strong prompting, post-processing checks |
| Over-deferral | AI defers on factual matters unnecessarily | Clear examples, confidence thresholds |
| Inconsistency | Same claim type gets different indicators | Standardized classification rules |
| Indicator fatigue | Users ignore indicators | Minimal use, only when genuinely informative |

### 4.3 User Experience

Indicators should be:
- **Non-intrusive**: Integrated naturally into response flow
- **Scannable**: Visually distinct without dominating
- **Informative**: Actually guiding researcher attention
- **Consistent**: Same situations get same treatment

---

## 5. Relation to Levels of AI Engagement

The epistemic indicators intersect with the four levels of AI engagement proposed in the working paper:

| Engagement Level | Primary Indicators | Deferral Frequency |
|------------------|-------------------|-------------------|
| **Level 1: Information Retrieval** | [FACTUAL] dominant | Rare |
| **Level 2: Structured Synthesis** | [FACTUAL] + [INTERPRETIVE] | Occasional |
| **Level 3: Interpretive Assistance** | [INTERPRETIVE] dominant | Moderate |
| **Level 4: Collaborative Reasoning** | All three balanced | High |

As engagement deepens, the proportion of [INTERPRETIVE] and [DEFERRED] content increases, reflecting the AI's appropriate humility about interpretive matters.

---

## 6. Objections and Responses

### 6.1 "All AI output is interpretive"

**Objection**: Even "factual" retrieval involves interpretation—query understanding, source selection, relevance ranking.

**Response**: Granted. The framework distinguishes *degrees* of interpretive involvement, not binary categories. [FACTUAL] marks claims where AI interpretation is minimal and verification is straightforward, not where interpretation is absent entirely.

### 6.2 "This slows down the interaction"

**Objection**: Indicators add cognitive load and slow research.

**Response**: The framework targets scholarly research where accuracy matters more than speed. Moreover, clear indicators may actually *reduce* cognitive load by letting researchers quickly identify what needs verification versus what can be trusted.

### 6.3 "Users will ignore the indicators"

**Objection**: Like EULA agreements, users will learn to ignore the indicators.

**Response**: Possible, but this is true of all epistemic hygiene practices. The framework creates the *possibility* of appropriate calibration; whether researchers use it is their responsibility. The alternative—false confidence—is worse.

### 6.4 "The AI cannot accurately self-assess"

**Objection**: LLMs are notoriously bad at knowing what they don't know.

**Response**: The framework doesn't require perfect self-assessment. It uses heuristics (normative language → [DEFERRED]) and defaults to humility ([INTERPRETIVE] or [DEFERRED] when uncertain). Imperfect implementation is better than none.

---

## 7. Integration with GNORM/ITSERR Tools

### 7.1 GNORM Annotation Confidence

GNORM's CRF-based annotations include confidence scores. These can inform indicators:

| GNORM Confidence | Indicator Mapping |
|------------------|-------------------|
| High (>0.9) | [FACTUAL]: "GNORM identifies X as a named entity" |
| Medium (0.7-0.9) | [INTERPRETIVE]: "GNORM suggests X may be..." |
| Low (<0.7) | [DEFERRED] or omit: "The classification is uncertain" |

### 7.2 T-ReS Integration

Text analysis results from T-ReS can be presented with indicators:
- Quantitative patterns → [FACTUAL]
- Structural analysis → [INTERPRETIVE]
- Significance claims → [DEFERRED]

### 7.3 YASMINE Ethical Guidelines (WP6)

YASMINE's guidelines for handling religious content align with epistemic modesty—both emphasize appropriate caution with sensitive material. The indicator framework operationalizes these guidelines at the response level.

---

## 8. Future Directions

### 8.1 Empirical Validation

The framework's effectiveness should be tested:
- Do indicators actually change researcher behavior?
- What indicator frequency is optimal?
- How do different user groups respond?

### 8.2 Community Standards

Long-term, disciplinary communities (theology, religious studies, DH) could develop standards for epistemic indicators, similar to citation conventions.

### 8.3 Tool Ecosystem

The indicator framework could become a component in larger tool ecosystems, with standard APIs for communicating epistemic status between tools.

---

## 9. Conclusion

Epistemic modesty is not a limitation but a feature—an affirmation that AI tools for theological research should respect the irreducible complexity of their subject matter and the interpretive agency of human researchers. The tripartite indicator framework (`[FACTUAL]`, `[INTERPRETIVE]`, `[DEFERRED]`) provides a concrete implementation of this principle.

The framework emerges from personalist anthropology's insistence on human dignity and agency, hermeneutical theory's recognition of interpretive complexity, and practical concern for scholarly rigor. It represents not humility as weakness but humility as appropriate calibration of AI's role in the research process.

---

## References

*To be expanded in final version*

- Buber, Martin. *I and Thou*. Scribner, 1958.
- Gadamer, Hans-Georg. *Truth and Method*. 2nd rev. ed. Continuum, 2004.
- Mounier, Emmanuel. *Personalism*. University of Notre Dame Press, 1952.
- Ricoeur, Paul. *Interpretation Theory*. Texas Christian University Press, 1976.
- Wojtyla, Karol. *The Acting Person*. Reidel, 1979.

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | [Date] | Initial draft |

---

*This framework will be refined based on GNORM technical briefing insights and fellowship discussions.*
