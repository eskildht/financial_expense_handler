from typing import Type
from financial_expense import FinancialExpense
from electricity_bill import ElectricityBill
from food_receipt import FoodReceipt
from other_expense import OtherExpense


class FinancialExpenseHandler:

    VALID_EXPENSE_TYPES = (FoodReceipt, ElectricityBill, OtherExpense)

    def __init__(self, num_participants: int) -> None:
        self._expenses = []
        self._num_participants = num_participants

    def add_expense(self, amount: float, owner: int, expense_type: str) -> None:
        if expense_type == "Food receipt":
            self._expenses.append(FoodReceipt(
                amount, owner, self._num_participants))
        elif expense_type == "Electricity bill":
            self._expenses.append(ElectricityBill(
                amount, owner, self._num_participants))
        elif expense_type == "Other expense":
            self._expenses.append(OtherExpense(
                amount, owner, self._num_participants))

    def remove_expense(self, index: int) -> None:
        del self._expenses[index]

    def get_expenses(self) -> list[FinancialExpense]:
        return self._expenses

    def get_expenses_by_owner(self, owner: int) -> list:
        return [x for x in self._expenses if x.get_owner() == owner]

    def get_expenses_by_type(self, expense_type: Type[FinancialExpense]) -> list:
        return [x for x in self._expenses if isinstance(x, expense_type)]

    def get_expenses_by_owner_and_type(self, owner: int, expense_type: Type[FinancialExpense]):
        return list(filter(lambda x: isinstance(x, expense_type), self.get_expenses_by_owner(owner)))

    def set_expense_split(self, expense_split: tuple[float, ...], expense_type: Type[FinancialExpense]) -> None:
        for expense in self._expenses:
            if isinstance(expense, expense_type):
                expense.set_expense_split(expense_split)

    def get_expense_splits(self) -> dict[Type[FinancialExpense], tuple[float, ...]]:
        res = {}
        for expense_type in FinancialExpenseHandler.VALID_EXPENSE_TYPES:
            candidate = next(
                (x for x in self._expenses if isinstance(x, expense_type)), None)
            if candidate is not None:
                res[expense_type] = candidate.get_expense_split()
        return res
