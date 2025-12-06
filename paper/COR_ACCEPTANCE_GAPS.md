# COR Acceptance Gap Analysis

## ✅ FIXED: Required Sections Added to `cor_paper.tex`

| Section | Status | Notes |
|---------|--------|-------|
| Highlights (3-5 bullets) | ✅ Added | 5 bullets, all ≤85 chars |
| Funding Statement | ✅ Added | "No specific grant" |
| Declaration of Competing Interests | ✅ Added | Standard declaration |
| CRediT Author Statement | ✅ Added | Template - fill in names |
| Data Availability Statement | ✅ Added | GitHub + Zenodo placeholder |
| Declaration of Generative AI Use | ✅ Added | GitHub Copilot disclosed |

---

## 🚨 CRITICAL REMAINING GAPS

### 1. **SCOPE MISMATCH** (Highest Risk of Desk Rejection)

**Problem**: COR is an Operations Research journal. Your paper is a **software/tooling paper**.

COR requires papers in these areas:
- Transportation, Logistics, Supply Chains
- Production and Scheduling  
- Optimization — Exact methods
- Optimization — Approximate methods/Metaheuristics
- Machine Learning and Data Science

**Your paper**: Focuses on software engineering (code reduction, API design) rather than OR algorithms.

**Fixes (choose one or more)**:

1. **Add Optimization Content**: Add a section on "Scheduling Optimization Using Discovered Process Models"
   - Example: Use discovered DFG to optimize resource allocation in P2P
   - Formulate as MILP or constraint programming problem

2. **Reframe as ML/Data Science**: Emphasize preprocessing as feature engineering for predictive process mining
   - Add prediction experiments using discovered patterns

3. **Consider Alternative Venues**:
   - **Information Systems** (Elsevier) - Better fit for software papers
   - **Software and Systems Modeling** (Springer)
   - **Decision Support Systems** (Elsevier)
   - **Journal of Systems and Software** (Elsevier)

---

### 2. **WEAK EXPERIMENTAL VALIDATION** (High Risk)

**COR Requirements**:
> "All full-length research papers must demonstrate constructive algorithmic complexity"
> "Numerical illustrations (examples) are not sufficient: the numerical experiments must have a scientific value of their own"
> "Real-world data is also valued"

**Current Issues**:
| Issue | Impact | Fix |
|-------|--------|-----|
| Synthetic data only | ❌ Major | Use BPI Challenge 2019 (P2P process) |
| Lower quality than pm4py | ⚠️ Moderate | Justify trade-off (speed vs quality) |
| No statistical tests | ❌ Major | Add Wilcoxon signed-rank tests |
| Limited benchmarks | ⚠️ Moderate | Add ProM comparison |

**Recommended Actions**:

```python
# Download and use real-world BPI Challenge data
# BPI Challenge 2019: Purchase Order Process (Exact P2P use case!)
# URL: https://data.4tu.nl/articles/dataset/BPI_Challenge_2019/12715853

# BPI Challenge 2017: Loan Application (O2C parallel)
# URL: https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884
```

---

### 3. **REPRODUCIBILITY PACKAGE** (Medium Risk)

**COR Requirement**:
> "Fully reproducible results are core...authors should grant full access to the data and codes"

**Actions Needed**:
1. Create Zenodo archive before submission
2. Replace `XXXXXXX` in paper with actual DOI
3. Include:
   - All source code (✅ exists)
   - `comparative_study.py` (✅ exists)
   - Generated data files (✅ exists)
   - `requirements.txt` with versions

---

### 4. **GRAPHICAL ABSTRACT** (Low Risk, but Recommended)

COR encourages graphical abstracts. Create one showing:

```
[ERP Tables] → [JSON Config] → [ERP-ProcessMiner] → [Event Log] → [Process Model] → [Insights]
```

---

## 📋 SUBMISSION CHECKLIST

### Before Submission:
- [ ] Replace `[Author 1]`, `[Author 2]` in CRediT statement with real names
- [ ] Create Zenodo deposit, get DOI, update paper
- [ ] Add graphical abstract
- [ ] Run BPI Challenge 2019 experiments
- [ ] Add statistical significance tests
- [ ] Verify Harvard citation style compliance
- [ ] Ensure all figures are high-resolution (300 DPI)

### Structural Requirements:
- [x] Title (descriptive, <20 words recommended)
- [x] Abstract (describes problem, contribution, insights)
- [x] Keywords (1-7 terms)
- [x] Highlights (3-5 bullets, ≤85 chars)
- [x] Funding statement
- [x] Competing interests declaration
- [x] CRediT author statement
- [x] Data availability statement
- [x] AI declaration
- [ ] Graphical abstract (recommended)

### Technical Requirements:
- [ ] Real-world dataset experiments (BPI Challenge)
- [ ] Statistical significance testing
- [ ] Comparison with >1 baseline (add ProM)
- [ ] Algorithmic complexity proof (not just O(n) claim)

---

## 🎯 ALTERNATIVE VENUES (If COR Scope Mismatch Too Large)

| Journal | Focus | IF | Fit |
|---------|-------|-----|-----|
| **Information Systems** | IS/BPM/Data Mgmt | 3.7 | ⭐⭐⭐⭐⭐ |
| **Decision Support Systems** | Decision/Analytics | 7.5 | ⭐⭐⭐⭐ |
| **Journal of Systems and Software** | Software Engineering | 3.5 | ⭐⭐⭐⭐⭐ |
| **Software and Systems Modeling** | Model-Driven | 2.0 | ⭐⭐⭐⭐ |
| **IEEE Trans. Software Engineering** | Software/Tools | 7.4 | ⭐⭐⭐⭐ |
| **JOSS** | Open Source Software | N/A | ⭐⭐⭐⭐⭐ |

---

## SUMMARY: Probability of COR Acceptance

| Factor | Score | Notes |
|--------|-------|-------|
| Formatting/Structure | 95% | All required sections present |
| Experimental Rigor | 60% | Synthetic data, no real-world |
| Scope Alignment | 40% | Software paper, not OR |
| Novelty | 70% | Good preprocessing contribution |

**Overall Assessment**: ~50% chance unless OR content added or alternative venue chosen.

**Recommendation**: Consider **Information Systems** (Elsevier) or **Journal of Systems and Software** as primary targets, or add substantial OR content (optimization problem formulation) for COR.
