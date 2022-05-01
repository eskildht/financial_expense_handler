from financial_expense import FinancialExpense


class FoodReceipt(FinancialExpense):

    PRINT_NAME = "(food receipt)"

    def __init__(self, amount: float, owner: int, num_participants: int) -> None:
        super().__init__(amount, owner, num_participants)

    def __str__(self) -> str:
        s = str(self._amount).ljust(8) + "(food receipt)"
        return s.ljust(26)
