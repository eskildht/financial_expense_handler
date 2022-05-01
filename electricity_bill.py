from financial_expense import FinancialExpense


class ElectricityBill(FinancialExpense):

    PRINT_NAME = "(electricity bill)"

    def __init__(self, amount: float, owner: int, num_participants: int) -> None:
        super().__init__(amount, owner, num_participants)

    def __str__(self) -> str:
        s = str(self._amount).ljust(8) + "(electricity bill)"
        return s.ljust(26)
