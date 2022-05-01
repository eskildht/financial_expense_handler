import sys
from typing import Type
from food_receipt import FoodReceipt
from electricity_bill import ElectricityBill
from other_expense import OtherExpense
from financial_expense import FinancialExpense
from financial_expense_handler import FinancialExpenseHandler
from simple_term_menu import TerminalMenu
from pathlib import Path
from time import strftime


class Main:

    def __init__(self, name_of_participants: list | None = None) -> None:
        if name_of_participants is not None:
            self.num_participants = len(name_of_participants)
            self.name_of_participants = name_of_participants
        else:
            self.num_participants = self.get_int_input(
                "Enter number of participants: ")
            self.name_of_participants = []

            participants_count = 0
            while participants_count != self.num_participants:
                self.name_of_participants.append(
                        input(f"Name {participants_count + 1}: "))
                participants_count += 1

        self.expense_handler = FinancialExpenseHandler(self.num_participants)

        self.main_menu = self.create_main_menu()
        self.add_expense_main_menu = self.create_add_expense_main_menu()
        self.add_expense_owner_menu = self.create_add_expense_owner_menu(
                self.name_of_participants)
        self.adjust_split_main_menu = self.create_adjust_split_main_menu()

    def get_int_input(self, input_msg: str) -> int:
        ret: int
        try:
            ret = int(input(input_msg))
        except ValueError as e:
            print(f"ValueError occurred: {e}. Please try again.\n")
            return self.get_int_input(input_msg)
        return ret

    def run(self):
        self.main_menu_handler()

    def main_menu_handler(self):
        main_menu_sel = self.main_menu.show()
        while True:
            if main_menu_sel == 0:
                self.add_expense_main_menu_handler()
            elif main_menu_sel == 1:
                self.remove_expense_main_menu_handler()
            elif main_menu_sel == 2:
                self.adjust_split_main_menu_handler()
            elif main_menu_sel == 3:
                self.calculate_results()
            elif main_menu_sel == 4:
                self.save()
            elif main_menu_sel == 5 or main_menu_sel is None:
                break
            main_menu_sel = self.main_menu.show()

    def add_expense_main_menu_handler(self):
        add_expense_main_menu_sel = self.add_expense_main_menu.show()
        expense_type = None
        if add_expense_main_menu_sel == 0:
            expense_type = "Food receipt"
        elif add_expense_main_menu_sel == 1:
            expense_type = "Electricity bill"
        elif add_expense_main_menu_sel == 2:
            expense_type = "Other expense"
        if expense_type is not None:
            expense_owner = self.add_expense_owner_menu_handler(expense_type)
            if isinstance(expense_owner, int) and expense_owner != self.num_participants:
                expense_amount = self.add_expense_amount_menu_handler(
                        expense_type, self.name_of_participants[expense_owner])
                self.expense_handler.add_expense(
                        expense_amount, expense_owner, expense_type)
            else:
                self.add_expense_main_menu_handler()

    def remove_expense_main_menu_handler(self):
        menu_entries = [
                str(expense) + " " + self.name_of_participants[expense.get_owner()] for expense in self.expense_handler.get_expenses()]
        remove_expense_main_menu = self.create_remove_expense_main_menu(
                menu_entries)
        remove_expense_main_menu_sel = remove_expense_main_menu.show(
                )
        if remove_expense_main_menu_sel is not None:
            for index in remove_expense_main_menu_sel:  # type: ignore
                self.expense_handler.remove_expense(index)

    def add_expense_owner_menu_handler(self, expense_type: str) -> int | tuple[int, ...] | None:
        return self.update_and_show(self.add_expense_owner_menu, f"  Main menu / Add expense / {expense_type} / Select owner\n")

    def add_expense_amount_menu_handler(self, expense_type: str, expense_owner: str) -> float:
        print(
                f"  Main menu / Add expense / {expense_type} / {expense_owner} / Amount\n")
        return self.get_float_input("  Enter amount: ")

    def get_float_input(self, input_msg: str) -> float:
        ret: float
        try:
            ret = float(input(input_msg))
        except ValueError as e:
            print(f"  ValueError occurred: {e}. Please try again.\n")
            return self.get_float_input(input_msg)
        return ret

    def adjust_split_main_menu_handler(self):
        adjust_split_main_menu_sel = self.adjust_split_main_menu.show()
        expense_type = None
        expense_type_print_name = None
        if adjust_split_main_menu_sel == 0:
            expense_type = FoodReceipt
            expense_type_print_name = "Food receipt"
        elif adjust_split_main_menu_sel == 1:
            expense_type = ElectricityBill
            expense_type_print_name = "Electricity bill"
        elif adjust_split_main_menu_sel == 2:
            expense_type = OtherExpense
            expense_type_print_name = "Other expense"
        if expense_type is not None:
            self.adjust_split_values_menu_handler(
                    expense_type, expense_type_print_name)

    def adjust_split_values_menu_handler(self, expense_type: Type[FinancialExpense], expense_type_print_name):
        print(
                f"  Main menu / Adjust split / {expense_type_print_name} \n")
        all_expense_splits = self.expense_handler.get_expense_splits()
        current_splits = all_expense_splits[expense_type] if expense_type in all_expense_splits else tuple(
            1 / self.num_participants for _ in range(self.num_participants))
        current_splits_print = ", ".join(
                [str(int(x*100)) + "%" for x in current_splits])
        print_names = ", ".join(self.name_of_participants)
        print(
                f"  {expense_type_print_name} has the current split:\n  {print_names} = {current_splits_print}\n")
        if expense_type in all_expense_splits:
            self.get_and_set_split_values(expense_type)
        else:
            print(f"  {expense_type_print_name} has not been added yet. Add at least one before adjusting split.")
            input("\n  Press enter to continue")


    def get_and_set_split_values(self, expense_type: Type[FinancialExpense]) -> None:
        try:
            split_values=tuple(
                    float(x)/100 for x in input("  Enter new split (%-values only): ").split(", "))
            self.expense_handler.set_expense_split(split_values, expense_type)
        except ValueError as e:
            print(f"  ValueError occurred: {e}. Please try again.\n")
            self.get_and_set_split_values(expense_type)


    def update_and_show(self, menu: TerminalMenu, menu_title: str | None = None) -> int | tuple[int, ...] | None:
        if menu_title is not None:
            menu._title_lines=tuple(menu_title.split("\n"))
        return menu.show()

    def create_menu(self, menu_title: str, menu_entries: list, menu_cursor: str = "> ", menu_cursor_style: tuple = ("fg_red", "bold"), menu_style: tuple = ("bg_red", "fg_yellow"), multi_select: bool = False,  show_search_hint: bool = False, multi_select_empty_ok: bool = False) -> TerminalMenu:
        menu=TerminalMenu(
                title=menu_title,
                menu_entries=menu_entries,
                menu_cursor=menu_cursor,
                menu_cursor_style=menu_cursor_style,
                menu_highlight_style=menu_style,
                cycle_cursor=True,
                clear_screen=True,
                multi_select=multi_select,
                multi_select_select_on_accept=False,
                multi_select_empty_ok=multi_select_empty_ok,
                show_search_hint=show_search_hint
                )
        return menu

    def create_main_menu(self) -> TerminalMenu:
        menu_title = "  Main menu\n"
        menu_entries = ["Add expense", "Remove expense(s)", "Adjust split",
                "Calculate results", "Save", "Quit"]
        return self.create_menu(menu_title, menu_entries)

    def create_add_expense_main_menu(self) -> TerminalMenu:
        menu_title = "  Main menu / Add expense\n"
        menu_entries = ["Food receipt",
                "Electricity bill", "Other expense", "Back"]
        return self.create_menu(menu_title, menu_entries)

    def create_add_expense_owner_menu(self, name_of_participants: list) -> TerminalMenu:
        menu_title = "  Main menu / Add expense / {expense_type} / Select owner\n"
        menu_entries = [name for name in name_of_participants]
        menu_entries.append("Back")
        return self.create_menu(menu_title, menu_entries)

    def create_remove_expense_main_menu(self, menu_entries: list) -> TerminalMenu:
        menu_title = "  Main menu / Remove expense(s)\n"
        return self.create_menu(menu_title, menu_entries, multi_select=True, show_search_hint=True, multi_select_empty_ok=True)

    def create_adjust_split_main_menu(self) -> TerminalMenu:
        menu_title = "  Main menu / Adjust split \n"
        menu_entries = ["Food receipt",
                "Electricity bill", "Other expense", "Back"]
        return self.create_menu(menu_title, menu_entries)

    def calculate_results(self, save_call: bool = False) -> None:
        column_separation = " "*4

        expenses_by_owner, totals_by_owner = self.present_current_expenses(
                column_separation)
        should_have_been_totals_by_owner = self.present_splits(
                expenses_by_owner, column_separation*2)
        self.present_transfer_summary(
                totals_by_owner, should_have_been_totals_by_owner)

        if not save_call:
            input("\nPress enter to continue")

    def present_current_expenses(self, column_separation: str) -> tuple[list[list[FinancialExpense]], list[float]]:
        header = self.get_header("Current expenses")
        print(header)

        for i in range(self.num_participants - 1):
            print(self.name_of_participants[i].ljust(
                26), end=column_separation)
        print(self.name_of_participants[-1].ljust(26), end="\n\n")

        expenses_by_owner = []
        for x in range(self.num_participants):
            owner_expenses_sorted_by_type = []
            for y in FinancialExpenseHandler.VALID_EXPENSE_TYPES:
                owner_expenses_sorted_by_type.extend(
                        self.expense_handler.get_expenses_by_owner_and_type(x, y))
            expenses_by_owner.append(owner_expenses_sorted_by_type)

        longest_list = max(expenses_by_owner, key=len)
        totals = [0.0 for _ in range(self.num_participants)]
        for i in range(len(longest_list)):
            for j in range(self.num_participants):
                if i <= len(expenses_by_owner[j]) - 1:
                    print(expenses_by_owner[j][i], end=column_separation)
                    totals[j] += expenses_by_owner[j][i].get_amount()
                else:
                    print("".ljust(26), end=column_separation)
            print()

        total_line = "-"*(self.num_participants*26 +
                len(column_separation)*(self.num_participants - 1))
        print(total_line)
        for i in range(self.num_participants - 1):
            print(str(totals[i]).ljust(26), end=column_separation)
        print(str(totals[-1]).ljust(26), end="\n\n")

        return (expenses_by_owner, totals)

    def present_splits(self, expenses_by_owner: list[list[FinancialExpense]], column_separation: str) -> list[float]:
        splits = self.expense_handler.get_expense_splits()

        header = self.get_header("Split")
        print(header)

        print("Split percentages:\n")

        for i in range(self.num_participants - 1):
            print(self.name_of_participants[i], end=column_separation)
        print(self.name_of_participants[-1], end="\n\n")

        for expense_type in splits:
            split_values = splits[expense_type]
            for i in range(self.num_participants - 1):
                print((str(int(round(split_values[i]*100, 1))) + "%").ljust(
                    len(self.name_of_participants[i])), end=column_separation)
            print((str(int(round(split_values[-1]*100, 1))) + "%").ljust(
                len(self.name_of_participants[-1])), end=(column_separation + expense_type.PRINT_NAME + "\n"))
        print()

        print("By split percentages, amounts should have been:\n")

        for i in range(self.num_participants - 1):
            print(self.name_of_participants[i], end=column_separation)
        print(self.name_of_participants[-1], end="\n\n")

        totals_by_expense_type = {
                x: 0.0 for x in FinancialExpenseHandler.VALID_EXPENSE_TYPES}
        lists_of_tuple_pairs = list(
                map(lambda x: list(map(lambda y: (y.get_amount(), type(y)), x)), expenses_by_owner))
        for list_of_tuple_pairs in lists_of_tuple_pairs:
            for tuple_pair in list_of_tuple_pairs:
                totals_by_expense_type[tuple_pair[1]  # type: ignore
                        ] += tuple_pair[0]

        totals_by_owner = [0.0 for _ in range(self.num_participants)]
        for expense_type in splits:
            split_values = splits[expense_type]
            for i in range(self.num_participants - 1):
                print(str(round(split_values[i]*totals_by_expense_type[expense_type], 2)).ljust(  # type: ignore
                    len(self.name_of_participants[i]) + len(column_separation)), end="")
                totals_by_owner[i] += split_values[i] * \
                        totals_by_expense_type[expense_type]  # type: ignore
            print(str(round(split_values[-1]*totals_by_expense_type[expense_type], 2)).ljust(  # type: ignore
                len(self.name_of_participants[-1]) + len(column_separation)), end=(expense_type.PRINT_NAME + "\n"))
            totals_by_owner[-1] += split_values[-1] * \
                    totals_by_expense_type[expense_type]  # type: ignore

        total_line = "-"*(self.num_participants*26 +
                (len(column_separation) // 2)*(self.num_participants - 1))
        print(total_line)

        for i in range(self.num_participants - 1):
            print(str(round(totals_by_owner[i], 2)).ljust(
                len(self.name_of_participants[i]) + len(column_separation)), end="")
        print(round(totals_by_owner[-1], 2), end="\n\n")

        return totals_by_owner

    def present_transfer_summary(self, totals_by_owner: list[float], should_have_been_totals_by_owner: list[float]) -> None:
        header = self.get_header("Transfer summary")
        print(header)

        standings = [totals_by_owner[i] - should_have_been_totals_by_owner[i]
                for i in range(self.num_participants)]

        transfer_history = []
        longest_name_payer_len = 0
        for i in range(self.num_participants):
            if standings[i] < 0:
                for j in range(self.num_participants):
                    if standings[j] > 0:
                        amount_to_pay = None
                        if abs(standings[i]) <= standings[j]:
                            amount_to_pay = abs(standings[i])
                        else:
                            amount_to_pay = standings[j]
                        standings[i] += amount_to_pay
                        standings[j] -= amount_to_pay
                        transfer_history.append(
                                (self.name_of_participants[i], self.name_of_participants[j], amount_to_pay))
                        if longest_name_payer_len < len(self.name_of_participants[i]):
                            longest_name_payer_len = len(
                                    self.name_of_participants[i])

        if len(transfer_history) > 0:
            for transfer in transfer_history:
                print((transfer[0]).ljust(longest_name_payer_len) + " --> " + str(
                    round(transfer[2], 2)).ljust(7) + " --> " + transfer[1])
        else:
            print("No transfer needs to occur")

    def get_header(self, title: str, column_separation_len: int = 4) -> str:
        header_char = "*"
        header_tot_len = self.num_participants*26 + \
                (self.num_participants - 1)*column_separation_len
        title_self_len = len(title)
        padding_len = header_tot_len - title_self_len
        left_padding_len = padding_len // 2
        header = header_char*header_tot_len + "\n" + \
                title.rjust(left_padding_len + title_self_len,
                        " ").ljust(header_tot_len, " ") + "\n" + header_char*header_tot_len + "\n"
        return header

    def save(self):
        Path("./saves").mkdir(exist_ok=True)
        timestamp = strftime("%Y-%m-%d-%H:%M:%S")
        sys.stdout = open(f"./saves/{timestamp}.txt", "w")
        self.calculate_results(save_call=True)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        print(f"Results successfully saved to file ./saves/{timestamp}.txt")
        input("\nPress enter to continue")

    def debug(self) -> None:
        if self.num_participants >= 3:
            self.expense_handler.add_expense(120, 0, "Food receipt")
            self.expense_handler.add_expense(12, 1, "Food receipt")
            self.expense_handler.add_expense(765.33, 0, "Electricity bill")
            self.expense_handler.add_expense(7651.22, 1, "Electricity bill")
            self.expense_handler.add_expense(928.56, 0, "Food receipt")
            self.expense_handler.add_expense(872.4, 0, "Other expense")
            self.expense_handler.add_expense(1200.12, 0, "Food receipt")
            self.expense_handler.add_expense(122.22, 2, "Electricity bill")
            self.expense_handler.add_expense(312.45, 1, "Food receipt")
            self.expense_handler.add_expense(57.2, 1, "Food receipt")
            self.expense_handler.add_expense(1111.2, 2, "Food receipt")
            self.expense_handler.set_expense_split(
                    (0.12, 0.47, 0.41), FoodReceipt)
        self.run()


if __name__ == "__main__":
    # Main(["Laurenz", "Andrew", "Karl"]).debug()
    Main().run()
