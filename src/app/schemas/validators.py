from typing import Annotated

from pydantic.functional_validators import AfterValidator


def check_amount(amount: int) -> int:
    """Валидация, сумма должна быть больше нуля."""
    assert amount >= 1, f'{amount} не может быть отрицательным числом или нулем.'
    return amount


positiv_int = Annotated[int, AfterValidator(check_amount)]
