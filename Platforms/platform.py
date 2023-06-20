from abc import ABC, abstractmethod

class Platform (ABC):
    name: str

    @abstractmethod
    def is_valid_problem_url(self, url):
        pass

    @abstractmethod
    def get_test_cases(self, url):
        pass

    @abstractmethod
    def get_problem_id(self, url):
        pass