from abc import ABC, abstractmethod

class Platform (ABC):
    name: str
    url_patterns: list[str]

    @abstractmethod
    def is_valid_problem_url(self, url: str):
        pass

    @abstractmethod
    def get_test_cases(self, url: str):
        pass

    @abstractmethod
    def get_problem_id(self, url: str):
        pass

    @abstractmethod
    def get_time_memory_limits(self, url: str):
        pass

    