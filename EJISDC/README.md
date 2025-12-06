# ERP-ProcessMiner: EJISDC Submission - README

## Submission Package Contents

This folder contains all materials for submission to the **Electronic Journal of Information Systems in Developing Countries (EJISDC)**.

### 📄 Primary Manuscript
- `paper/ejisdc_paper.tex` - Main manuscript (LaTeX format, ~8,500 words)
- `paper/references.bib` - Complete bibliography (60+ references including ICT4D literature)

### 📊 Figures (All 300 DPI)
Located in `paper/`:
1. `architecture_diagram.png/pdf` - System architecture (Figure 1)
2. `rq1_usability.png/pdf` - Code complexity comparison (Figure 2)  
3. `rq2_quality_statistical.png/pdf` - Discovery quality with error bars (Figure 3)
4. `rq3_efficiency.png/pdf` - Resource efficiency (4 subplots) (Figure 4)
5. `rq4_accessibility.png/pdf` - Educational accessibility radar chart (Figure 5)

### 📈 Experimental Data
Located in `experiments/ejisdc/`:
- `rq1_usability.csv` - Lines of code measurements
- `rq2_quality_statistical.csv` - Fitness scores (10 iterations)
- `rq3_efficiency.csv` - Time and memory measurements  
- `rq4_accessibility.csv` - Accessibility assessment data
- `ejisdc_tables.tex` - LaTeX-formatted tables for all results

### 🔬 Reproducibility
Located in `experiments/`:
- `ejisdc_experiments.py` - Complete experimental script (803 lines)
- `generate_architecture_diagram.py` - Architecture diagram generator

### 📋 Supporting Documents
- `COVER_LETTER.txt` - Cover letter for editors
- `EJISDC_SUBMISSION_CHECKLIST.md` - Submission requirements checklist
- `README.md` - This file

---

## Manuscript Highlights

**Title:** ERP-ProcessMiner: An Accessible Open-Source Toolkit for Process Mining in Resource-Constrained Educational and Organizational Contexts

**Authors:**
- Almas Ospanov (Corresponding) - Astana IT University & L.N. Gumilyov Eurasian National University
- P. Alonso-Jordá - Universitat Politècnica de València  
- Ainur Zhumadillayeva - L.N. Gumilyov Eurasian National University

**Key Results:**
- 57.1% reduction in preprocessing code complexity
- 35% lower memory usage vs. pm4py
- Statistically validated (n=10, Wilcoxon tests, p<0.05)
- Fitness: 0.76 (ERP-PM) vs. 1.00 (pm4py) - trade-off for accessibility

**Keywords:** Process mining; ERP systems; Open-source software; Developing countries; ICT for development; Educational technology

---

## Submission Instructions

### Pre-Submission Tasks
- [x] Manuscript prepared (LaTeX)
- [x] All figures generated (300 DPI, PDF + PNG)
- [x] Experimental data collected and validated
- [x] Cover letter written
- [x] Author information prepared
- [ ] **Create Zenodo replication package** (add DOI to paper)
- [ ] **Upload to submission portal**

### Submission Portal
**URL:** https://mc.manuscriptcentral.com/ejisdc

### Files to Upload
1. `paper/ejisdc_paper.tex` (or compiled PDF)
2. `paper/references.bib`
3. All figure files from `paper/` (10 files)
4. `COVER_LETTER.txt`
5. Supplementary: Experimental scripts (optional)

---

## Wiley Free Format Submission

EJISDC accepts **Free Format** submissions, meaning:
- ✅ You can submit in your preferred format (Word, PDF, LaTeX)
- ✅ Reference style can be any consistent format
- ✅ No need to reformat before submission
- ✅ Wiley will format if accepted

**However, our manuscript already follows standard academic conventions:**
- Double-spaced, 12pt font, 2.5cm margins
- Structured sections (Intro, Methods, Results, Discussion, Conclusion)
- Consistent APA-style references
- Professional LaTeX formatting

---

## Quality Assurance Checklist

### Manuscript Structure ✅
- [x] Title page with all author affiliations
- [x] Abstract (250 words, structured)
- [x] Keywords (6 terms relevant to ICT4D)
- [x] Introduction with clear problem statement
- [x] Literature review (Related Work)
- [x] Methodology (clear, reproducible)
- [x] Results (4 research questions answered)
- [x] Discussion (implications for developing countries)
- [x] Conclusion (future work identified)

### Ethical Requirements ✅
- [x] Data availability statement
- [x] Competing interests declaration (none)
- [x] Funding statement (no specific grant)
- [x] Author contributions (CRediT taxonomy)
- [x] Ethical approval (not applicable - software study)

### Technical Requirements ✅
- [x] All citations properly formatted
- [x] All figures referenced in text
- [x] All tables referenced in text
- [x] Figure captions complete
- [x] Table captions complete
- [x] Equations numbered (if applicable)
- [x] Consistent terminology throughout

### Figures Quality ✅
- [x] Resolution: 300 DPI minimum
- [x] File formats: PDF (vector) + PNG (raster)
- [x] Readable text in figures
- [x] Color-blind friendly (green/blue palette)
- [x] Professional appearance

### Statistical Rigor ✅
- [x] Sample size justified (n=10 iterations)
- [x] Statistical tests applied (Wilcoxon signed-rank)
- [x] P-values reported (p<0.05)
- [x] Effect sizes clear (57.1% LOC reduction, 35% memory savings)
- [x] Error bars shown in figures

---

## Alignment with EJISDC Scope

### Primary Fit Areas:
1. **ICT for Development (ICT4D)** ⭐⭐⭐⭐⭐
   - Addresses technology adoption barriers in developing countries
   - Focuses on resource constraints and accessibility

2. **Educational Technology** ⭐⭐⭐⭐⭐
   - Designed for classroom use
   - Reduces learning curve for process mining

3. **Open Source Software** ⭐⭐⭐⭐⭐
   - MIT license eliminates cost barriers
   - Emphasizes reproducibility and transparency

4. **Information Systems in Organizations** ⭐⭐⭐⭐
   - ERP data transformation for process mining
   - Practical tool for small/medium enterprises

### Citation to Key ICT4D Literature:
- Walsham (2017) - ICT4D reflections
- Heeks (2018) - ICT4D frameworks
- Soja (2006) - ERP implementation in developing countries
- Avgerou (2008) - IS in developing countries
- Zheng et al. (2018) - Conceptualizing ICT4D

---

## Expected Review Process

**EJISDC Timeline (Typical):**
- Initial screening: 1-2 weeks
- Peer review: 6-12 weeks  
- Revision cycle: 4-8 weeks (if minor/major revisions)
- Final decision: 8-16 weeks total

**Open Access:**
- EJISDC is Gold OA with **NO Article Processing Charges (APC)**
- Freely accessible upon publication
- Indexed in Scopus, Web of Science (ESCI)

---

## Post-Submission Actions

### Upon Submission:
1. Save submission confirmation email
2. Note manuscript ID number
3. Monitor email for editor communications

### If Revisions Requested:
1. Respond within deadline (typically 2-3 months)
2. Prepare point-by-point response document
3. Highlight changes in revised manuscript
4. Update experimental results if needed

### Upon Acceptance:
1. Create Zenodo deposit for replication package
2. Add DOI to final manuscript
3. Promote on social media / academic networks
4. Update GitHub repository README with publication link

---

## Contact Information

**Corresponding Author:**  
Almas Ospanov  
Email: 222134@astanait.edu.kz  
Affiliation: Astana IT University & L.N. Gumilyov Eurasian National University

**GitHub Repository:**  
https://github.com/TerexSpace/erp-process-mining-tkit

**Questions about submission?**  
EJISDC Editorial Office: ejisdc@wiley.com  
Wiley Author Support: https://authorsupport.wiley.com/

---

## Version History

- **v1.0** (December 6, 2025) - Initial submission package prepared
- All experiments completed with statistical validation
- Manuscript finalized with ICT4D framing
- Cover letter and supporting documents created

---

**✅ READY FOR SUBMISSION TO EJISDC**
