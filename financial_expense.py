from abc import ABC, abstractmethod


class FinancialExpense(ABC):

    PRINT_NAME = "(financial expense)"

    def __init__(self, amount: float, owner: int, num_participants: int) -> None:
        self.set_amount(amount)
        self.set_num_participants(num_participants)
        self.set_owner(owner)
        self._expense_split = tuple(
            1 / self._num_participants for _ in range(self._num_participants))

    def get_amount(self) -> float:
        return self._amount

    def get_num_participants(self) -> int:
        return self._num_participants

    def get_owner(self) -> int:
        return self._owner

    def get_expense_split(self) -> tuple[float, ...]:
        return self._expense_split

    def get_expense_split_amounts(self) -> tuple[float, ...]:
        return tuple(x * self._amount for x in self._expense_split)

    def set_amount(self, amount: float) -> None:
        self.__validate_amount(amount)
        self._amount = amount

    def set_num_participants(self, num_participants: int) -> None:
        self.__validate_num_participants(num_participants)
        self._num_participants = num_participants

    def set_owner(self, owner: int) -> None:
        self.__validate_owner(owner)
        self._owner = owner

    def set_expense_split(self, expense_split: tuple[float, ...]) -> None:
        self.__validate_expense_split(expense_split)
        self._expense_split = expense_split

    def __validate_amount(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("amount cannot be negative")

    def __validate_num_participants(self, num_participants: int) -> None:
        if num_participants < 1:
            raise ValueError(
                "num_participants cannot be less than 1")

    def __validate_owner(self, owner: int) -> None:
        if self._num_participants - 1 < owner < 0:
            raise ValueError(
                "owner must be a valid index constrained by num_participants")

    def __validate_expense_split(self, expense_split: tuple[float, ...]) -> None:
        if not sum(expense_split) == 1:
            raise ValueError("expense_split must sum to 1")
        for val in expense_split:
            if 1 < val < 0:
                raise ValueError(
                    "all values in expense_split must be in range [0, 1]")

    @abstractmethod
    def __str__(self) -> str:
        pass
