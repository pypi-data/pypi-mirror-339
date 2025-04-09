# Project: bigdata_cole_framework
# File Created: 2023-10-01
# Standard Libraries
import os


class ColeAlgorithms:
    @staticmethod
    def get_max_number(numbers: list) -> int:
        """
        Returns the maximum number from a list of numbers.

        :param numbers: List of numbers
        :return: Maximum number in the list
        """
        if not numbers:
            raise ValueError("The list of numbers is empty.")
        return max(numbers)

    @staticmethod
    def get_min_number(numbers: list) -> int:
        """
        Returns the minimum number from a list of numbers.

        :param numbers: List of numbers
        :return: Minimum number in the list
        """
        if not numbers:
            raise ValueError("The list of numbers is empty.")
        return min(numbers)

    @staticmethod
    def get_average(numbers: list) -> int:
        """
        Returns the average of a list of numbers.

        :param numbers: List of numbers
        :return: Average of the numbers in the list
        """
        if not numbers:
            raise ValueError("The list of numbers is empty.")
        return sum(numbers) / len(numbers)
