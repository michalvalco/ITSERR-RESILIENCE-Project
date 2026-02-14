# PROMPT: Apply Surgical Additions from Deep Read Analysis

**Date:** February 14, 2026
**Context:** The deep read analysis of GEM and CHAT reports (`deep_read_GEM_CHAT_analysis.md`, now in PKB) identified 8 action items — specific text additions to be inserted into two live reference documents. No edits have been applied yet.

## Task

Apply all 8 additions from `deep_read_GEM_CHAT_analysis.md` (PKB) to the two target files on the filesystem. Use Filesystem tools to edit files in place. Work through all items in one pass.

### Target Files (on filesystem)

1. **`pipeline_technical_reference.md`**
   - Path: `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\docs\resources\pipeline_technical_reference.md`
   - Also in PKB as static snapshot — the PKB copy will NOT be updated (it's read-only context). The filesystem copy is the live document.

2. **`workflow_diagram.md`**
   - Path: `C:\Users\valco\OneDrive\Documents\GitHub\ITSERR-RESILIENCE-Project\01_research\workflow_diagram.md`
   - Also in PKB — same situation, filesystem is the live copy.

### Edits to Apply

Read `deep_read_GEM_CHAT_analysis.md` from PKB for the full suggested text. Here is the action item summary with insertion points:

#### For `pipeline_technical_reference.md` (6 edits):

| # | Finding | Where to Insert | Priority |
|---|---------|----------------|----------|
| 2.1 | `all_possible_states`/`transitions` CRF note | §4 (Feature Engineering), after the Hyperparameter Search table — add as new subsection "Note on Sparse Training Data" | MEDIUM |
| 2.2 | Tokenization alignment warning | §2 (Data Formats), inside "Zero-Shot Test Strategy" — append to Path B description | MEDIUM |
| 2.3 | Network scale (1,795 nodes / 41,784 edges) | §1 (Pipeline Architecture Overview), after the existing "41,784 legal references" mention in the performance line | LOW |
| 2.4 | ATON Framework identification | §7 (Adaptation Gaps), replace the "3D visualization" row; ALSO add new bullet to §8 "Still TBD" list | HIGH |
| 2.5 | Pavone & Imperia Talmud paper (cross-domain precedent) | §1 (Pipeline Architecture Overview), after the performance/codebase lines — add as new note | MEDIUM |
| — | Update "Last updated" date | Header — change to "February 14, 2026 (deep read additions applied)" | — |

#### For `workflow_diagram.md` (2 edits):

| # | Finding | Where to Insert | Priority |
|---|---------|----------------|----------|
| 3.1 | Omeka S / W3C Web Annotation integration | Stage 7 (INTERACT), after the existing "Integration with Slovak infrastructure" block — add as new subsection "Technical Integration Path" | HIGH |
| 3.2 | `digitaldecretals.com` reference | Stage 5 (REPRESENT), after "Arianna demonstrated the GNORM prototype web interface at ariannapavone.com/gnorm/" | LOW |

### Items NOT applied to filesystem (PKB-only documents):

- Finding 4.1 (Pavone & Imperia for literature synthesis) — targets `Ethically-Grounded_AI_Agents...md` which is PKB-only and read-only. Note it as a TODO for when the integrated synthesis is drafted.
- Finding 4.2 (full citation) — bibliography item, will be captured during synthesis drafting.

### Process

1. Load Filesystem tools (`tool_search` for "read file from user computer filesystem")
2. Read each target file
3. Apply edits using `Filesystem:edit_file` — use the suggested text from the deep read analysis (in PKB), inserting at the locations specified above
4. Read back edited files to verify insertions look correct
5. Update the HUB file: change Current Status date to Feb 14, note edits applied, update Next steps

### Quality Check

After all edits:
- Confirm no broken markdown tables
- Confirm section numbering still works
- Confirm "Last updated" dates reflect the changes
- Report what was done

---

*Handoff prompt for fresh context window. All source material is in PKB or on filesystem — no additional uploads needed.*
