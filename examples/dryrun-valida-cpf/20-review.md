# Quality audit (reviewer: gemini)

> This is the actual review the Gemini CLI ("Agy") produced for this deliverable, translated to
> English. It followed the review contract on its own, from reading the global `GEMINI.md` — no
> format hand-holding. It caught the planted bug (#1) *and* a second genuine bug nobody planted (#2).

**Verdict:** `REQUEST-CHANGES`

---

## Findings

### 1. CPFs with all-identical digits are treated as valid
- **Severity:** Blocker
- **Pointer:** `valida_cpf.py:14-16`
- **Description:** The current code accepts CPFs made of repeated digits (e.g. `"111.111.111-11"`
  or `"000.000.000-00"`), because they mathematically satisfy the check-digit equations. However,
  the Brazilian tax authority explicitly classifies them as invalid. This is the most common and
  well-known CPF edge case, and the code fails the acceptance criterion *"Handles known CPF edge
  cases"*.
- **Suggested fix:**
  ```python
  if len(set(digitos)) == 1:
      return False
  ```

### 2. Inputs with arbitrary non-numeric characters are incorrectly accepted
- **Severity:** Major
- **Pointer:** `valida_cpf.py:14`
- **Description:** The generic character cleanup `digitos = [c for c in cpf if c.isdigit()]` makes
  invalid strings with suffixes or random characters (e.g. `"529.982.247-25abc"` or
  `"529a982b247-25"`) validate successfully if the underlying digit sequence is valid. The
  acceptance criterion requires *"Rejects invalid input (wrong length, non-numeric)"*, which implies
  rejecting formats that aren't strictly numeric (11 digits) or the classic mask (14 chars,
  `###.###.###-##`).
- **Suggested fix:** Validate the overall input format before extracting the digits. A simple, clean
  way is an exact regex:
  ```python
  import re

  # allow only the clean format (11 digits) or the exact mask (14 chars: ddd.ddd.ddd-dd)
  if not re.match(r"^\d{11}$|^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf):
      return False
  ```
