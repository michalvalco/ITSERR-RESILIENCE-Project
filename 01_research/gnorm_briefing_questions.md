# GNORM Technical Briefing Questions

**Briefing Dates:** February 11-12, 2026
**Purpose:** Understand GNORM capabilities for integration with ethically-grounded AI agent prototype
**Prepared by:** [Your Name]
**Contact:** Andrea Esuli, Alessio Ferrante (WP5 Hosts)

---

## Context

This question list is prepared for the GNORM technical briefing during the first week of the ITSERR fellowship. The goal is to gather sufficient technical understanding to implement a working integration between the AI research assistant prototype and GNORM's annotation capabilities.

**Integration Goal:** Enable the AI agent to request and display GNORM annotations for religious and theological texts, with appropriate epistemic indicators (FACTUAL/INTERPRETIVE/DEFERRED) based on annotation confidence levels.

---

## 1. Architecture & Overview

### 1.1 System Architecture
- [ ] What is the overall architecture of GNORM? (monolithic, microservices, etc.)
- [ ] What components make up the GNORM system?
- [ ] Is there a system architecture diagram available?

### 1.2 CRF Model Details
- [ ] What CRF (Conditional Random Field) implementation is used?
- [ ] What training data was the model trained on?
- [ ] What is the model's domain coverage for religious/theological texts?
- [ ] Are there multiple models for different text types or languages?

### 1.3 Current Status
- [ ] What is the current development status of GNORM?
- [ ] Is there a stable API available for external integration?
- [ ] What environments exist? (dev, staging, production)
- [ ] Are there known limitations or active development areas?

---

## 2. API & Integration

### 2.1 API Fundamentals
- [ ] What is the API format? (REST, GraphQL, gRPC, other)
- [ ] What is the base URL structure?
- [ ] What authentication model is used? (API key, OAuth, JWT, none)
- [ ] Are there rate limits? If so, what are they?
- [ ] Is there API documentation available?

### 2.2 Request Format
- [ ] What is the request payload structure for annotation requests?
- [ ] How should text be submitted? (plain text, specific encoding, document format)
- [ ] What parameters are available? (entity types, confidence threshold, etc.)
- [ ] Is there a maximum text length per request?
- [ ] Can requests specify which entity types to extract?

### 2.3 Response Format
- [ ] What is the response payload structure?
- [ ] How are annotations represented? (inline, offset-based, standoff, etc.)
- [ ] What metadata is included with each annotation?
- [ ] Are confidence scores included? How are they scaled (0-1, 0-100, etc.)?
- [ ] How are relations between entities represented?

### 2.4 Example Request/Response
- [ ] Can you provide a sample request?
- [ ] Can you provide a sample response?
- [ ] Are there example scripts or code snippets available?

---

## 3. Entity Types & Annotations

### 3.1 Available Entity Types
- [ ] What entity types does GNORM recognize?
- [ ] Are there entity types specific to religious/theological content?
  - Persons (biblical figures, saints, theologians)?
  - Places (sacred locations, historical sites)?
  - Concepts (theological terms, doctrines)?
  - Temporal expressions (liturgical calendar, historical periods)?
  - Textual references (scripture citations, patristic references)?
  - Organizations (religious orders, councils, churches)?

### 3.2 Entity Attributes
- [ ] What attributes are provided for each entity?
- [ ] Is there normalization/linking to external databases? (Wikidata, VIAF, etc.)
- [ ] Are variant forms/aliases handled?

### 3.3 Relations
- [ ] What relation types are extracted between entities?
- [ ] How are relations represented in the output?
- [ ] What is the confidence scoring for relations?

### 3.4 Customization
- [ ] Can custom entity types be defined for specific projects?
- [ ] Is there a way to provide domain-specific training data?
- [ ] Can entity extraction be scoped to specific types per request?

---

## 4. Confidence Scores & Interpretation

### 4.1 Confidence Model
- [ ] How are confidence scores calculated?
- [ ] What do different confidence levels indicate about reliability?
- [ ] What is considered high/medium/low confidence?

### 4.2 Threshold Recommendations
- [ ] What confidence threshold is recommended for production use?
- [ ] How should low-confidence annotations be handled?
- [ ] Are there guidelines for human review triggers?

### 4.3 Mapping to Epistemic Indicators
For my prototype, I plan to map GNORM confidence to epistemic indicators:
- High confidence → `[FACTUAL]`
- Medium confidence → `[INTERPRETIVE]`
- Low confidence → `[INTERPRETIVE]` with flag for verification

- [ ] Does this mapping align with your understanding of GNORM's confidence semantics?
- [ ] Are there additional factors beyond confidence that should influence this mapping?
- [ ] Are there annotation types that should always be flagged for human review regardless of confidence?

---

## 5. Processing Modes

### 5.1 Real-time vs. Batch
- [ ] Is real-time (synchronous) processing available?
- [ ] What is the typical latency for a single text annotation?
- [ ] Is batch processing available for larger documents?
- [ ] How is batch processing status tracked?

### 5.2 Performance Characteristics
- [ ] What is the processing time per character/word/document?
- [ ] Are there performance differences by entity type?
- [ ] What resources are required for self-hosting (if applicable)?

### 5.3 Caching
- [ ] Are annotation results cached?
- [ ] How should clients handle caching for repeated texts?

---

## 6. Text Types & Languages

### 6.1 Supported Languages
- [ ] What languages are supported?
- [ ] Is multilingual text handled within a single document?
- [ ] Are there language-specific models?

### 6.2 Text Types
- [ ] What text types work best with GNORM?
- [ ] How does it perform on:
  - Modern theological/academic texts?
  - Historical texts (patristic, medieval)?
  - Scripture and scriptural commentary?
  - Liturgical texts?
- [ ] Are there text types that are known to perform poorly?

### 6.3 Pre-processing
- [ ] What text pre-processing is recommended?
- [ ] How should special characters, Unicode, etc. be handled?
- [ ] Are there encoding requirements?

---

## 7. Integration with T-ReS

### 7.1 T-ReS Overview
- [ ] What is T-ReS's primary function?
- [ ] How does T-ReS complement GNORM?
- [ ] What text analysis capabilities does T-ReS provide?

### 7.2 GNORM + T-ReS Workflow
- [ ] What is the recommended workflow for using both tools?
- [ ] Do they share data formats or can outputs be chained?
- [ ] Are there integration examples available?

### 7.3 Annotation Sharing
- [ ] How can annotations be shared between systems?
- [ ] Is there a common annotation format (TEI, Web Annotation, custom)?
- [ ] Can T-ReS consume GNORM annotations and vice versa?

---

## 8. Deployment & Access

### 8.1 Access During Fellowship
- [ ] How will I access GNORM during the fellowship?
- [ ] Are there test credentials or a sandbox environment?
- [ ] Is there a development/staging endpoint for testing?

### 8.2 Post-Fellowship Access
- [ ] Can the prototype continue using GNORM after the fellowship?
- [ ] What are the terms for research use?
- [ ] Is there a process for requesting continued access?

### 8.3 Self-Hosting
- [ ] Is it possible to run GNORM locally?
- [ ] What are the system requirements?
- [ ] Is there a Docker image or installation guide?

---

## 9. Future Integrations (ITSERR WPs)

### 9.1 WP4 - DaMSym
- [ ] Are there plans for GNORM-DaMSym integration?
- [ ] How might symbolic reasoning complement CRF annotations?

### 9.2 WP6 - YASMINE
- [ ] How might ethical guidelines from YASMINE apply to annotation display?
- [ ] Are there coordination plans between WP3 and WP6?

### 9.3 WP7 - REVER
- [ ] How does GNORM relate to hermeneutical tradition analysis in REVER?
- [ ] Are there shared annotation schemas?

---

## 10. Technical Support & Resources

### 10.1 Documentation
- [ ] Is there API documentation available?
- [ ] Are there tutorials or getting-started guides?
- [ ] Is there a technical paper describing GNORM?

### 10.2 Support Channels
- [ ] Who should I contact for technical questions during development?
- [ ] Is there a Slack, Teams, or other communication channel?
- [ ] Is there a bug tracker or issue system?

### 10.3 Code Examples
- [ ] Are there Python client examples available?
- [ ] Are there example projects using GNORM?
- [ ] Is there a reference implementation?

---

## Notes During Briefing

*Use this section to capture notes during the Feb 11-12 briefing*

### Day 1 Notes (Feb 11)




### Day 2 Notes (Feb 12)




---

## Action Items Post-Briefing

- [ ] Update system_design.md with GNORM integration details
- [ ] Create GNORM client module in prototype
- [ ] Define confidence-to-indicator mapping rules
- [ ] Request API credentials/access
- [ ] Schedule follow-up questions meeting if needed

---

## Quick Reference Card

*Fill in during briefing for quick reference during development*

| Item | Value |
|------|-------|
| API Base URL | |
| Auth Type | |
| Auth Header | |
| Request Format | |
| Response Format | |
| Confidence Scale | |
| High Confidence Threshold | |
| Rate Limit | |
| Support Contact | |

