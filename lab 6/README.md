# LAB 6: Code and Branch Coverage Analysis

- **Student Name:** Suhas S Iyengar
- **SRN:** PES1UG24AM291
- **Course:** Software Engineering Lab (SE_LAB1)
- **Assigned Topic:** Visa Application (`L6_L7_52_visa_application`)

---

## Overview

Code coverage measures how much of your source code is executed during automated testing. This lab evaluates the difference between **Line Coverage** and **Branch Coverage** using Python's `coverage` and `pytest` tools on `visa_application.py`.

The target functions under test:
1. `visa_fee(visa_type, entries, speed, nationality_group)`: Computes payable visa fee based on category, included allowances, processing speed, and volume surcharges.
2. `documents_complete(forms_filed, photos, is_renewal)`: Validates whether submitted documents meet renewal or standard criteria.
3. `application_status(days_left, is_express, is_peak_season)`: Determines application window status (`open`, `closing`, `closed`) given express and peak season deadlines.

---

## Deliverables in this Directory

| File | Description | Coverage Achieved |
|---|---|---|
| `CodeCoverageTest_visa_application.py` | Targeted test cases for statement coverage | **100% Statement Coverage** |
| `BranchCoverageTest_visa_application.py` | Rigorous test suite for all decision branches | **100% Branch Coverage** |
| `visa_application.py` | Application logic module under test | — |
| `test_visa_application.py` | Complete integrated test suite | **100% Code & Branch** |
| `PES1UG24AM291_Lab6_Report.pdf` | Detailed lab report with screenshots and analysis | Complete |
| `Lab6_Report.pdf` | Clean copy of the lab report | Complete |
| `screenshots/` | Full-resolution terminal output captures | All steps documented |

---

## Coverage Analysis & Results Summary

| Metric | Baseline Starter Suite | Code Coverage Suite | Branch Coverage Suite |
|---|:---:|:---:|:---:|
| **Statements Covered** | 14 / 37 (38%) | 37 / 37 (**100%**) | 37 / 37 (**100%**) |
| **Branches Covered** | 10 / 26 (32%) | 25 / 26 (**98%**) | 26 / 26 (**100%**) |
| **Missing Branches** | Multiple | Line 21->23 | **None (0 missing)** |
| **Test Cases** | 2 | 11 | 20 |
| **Outcome** | Baseline | >90% Target Met | 100% Target Met |

### Key Insight: Line Coverage vs. Branch Coverage
While `CodeCoverageTest_visa_application.py` successfully executed 100% of the lines in `visa_application.py`, branch analysis flagged **Line 21 -> 23**:
- Line 21 is `if speed == "express": rate += 10`, nested inside `if extra > 5:`.
- In the line coverage suite, this was tested with `speed == "express"` (which triggered lines 21 and 22).
- However, when `extra > 5` and `speed == "normal"`, line 21 evaluates to `False`, skipping line 22 and jumping directly to line 23.
- `BranchCoverageTest_visa_application.py` covers both outcomes of this condition, achieving **100% branch coverage**.

---

## Instructions to Run Tests and Coverage Reports

### 1. Run Code Coverage
```bash
coverage run -m pytest CodeCoverageTest_visa_application.py
coverage report -m
```

### 2. Run Branch Coverage
```bash
coverage run --branch -m pytest BranchCoverageTest_visa_application.py
coverage report -m
```

### 3. Run Complete Integrated Test Suite
```bash
coverage run --branch -m pytest test_visa_application.py
coverage report -m
```
