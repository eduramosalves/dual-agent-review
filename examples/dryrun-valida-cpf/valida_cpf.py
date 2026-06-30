"""Brazilian CPF validation — executor's (Claude) deliverable for the cross-review example.

NOTE: this file intentionally contains the bugs the reviewer found (see 20-review.md). It is kept
as-is to show what the reviewer was auditing — it is NOT a corrected reference implementation.
"""


def valida_cpf(cpf: str) -> bool:
    """Validate a CPF by its two check digits.

    Accepts masked ("529.982.247-25") or unmasked ("52998224725").
    """
    # strip mask: keep digits only
    digitos = [c for c in cpf if c.isdigit()]
    if len(digitos) != 11:
        return False
    nums = [int(c) for c in digitos]

    # first check digit
    soma = sum(nums[i] * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    dv1 = 0 if resto == 10 else resto
    if dv1 != nums[9]:
        return False

    # second check digit
    soma = sum(nums[i] * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    dv2 = 0 if resto == 10 else resto
    if dv2 != nums[10]:
        return False

    return True
