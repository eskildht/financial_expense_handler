from financial_expense import FinancialExpense


class OtherExpense(FinancialExpense):

    PRINT_NAME = "(other expense)"

    def __init__(self, amount: float, owner: int, num_participants: int) -> None:
        super().__init__(amount, owner, num_participants)

    def __str__(self) -> str:
        s = str(self._amount).ljust(8) + "(other expense)"
        return s.ljust(26)
