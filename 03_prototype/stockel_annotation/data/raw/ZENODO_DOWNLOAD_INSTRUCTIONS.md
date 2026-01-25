# Zenodo Dataset Download Instructions

**Dataset DOI:** [10.5281/zenodo.14381709](https://doi.org/10.5281/zenodo.14381709)
**Direct URL:** https://zenodo.org/records/14381709

## Manual Download Steps

1. Visit the Zenodo record page above
2. Download all available files (typically a ZIP archive)
3. Place downloaded files in this directory (`data/raw/`)
4. Verify file integrity using provided checksums (if available)

## Expected Contents

Based on the GNORM codebase analysis, the dataset should contain:

- **INCEpTION export files** in UIMA CAS XMI format (ZIP archives)
- **TypeSystem.xml** - Defines the annotation schema
- **XMI files** - Contain text and annotations

## Related Resources

- **GNORM Index (Zenodo 14381710):** https://zenodo.org/records/14381710
  - Contains the automatically generated index of all legal references
  - Lists external norms referenced in the Liber Extra

- **Digital Decretals (source texts):** https://www.digitaldecretals.com/
  - Original digital version of the Ordinary Gloss

## After Download

1. Extract ZIP files if needed
2. Note the username used for annotations (required for pipeline)
3. Test with: `python cas_to_bioes.py <zip_path> <username>`

---

*Download status: Pending manual download*
*Last updated: January 25, 2026*
