from typing import Annotated

from pydantic.functional_validators import AfterValidator


def check_amount(amount: int) -> int:
    """Валидация, сумма должна быть больше нуля."""
    no_valid_answer = f'{amount} не может быть отрицательным числом или нулем.'
    assert amount >= 1, no_valid_answer  # noqa: S101
    return amount


positiv_int = Annotated[int, AfterValidator(check_amount)]
