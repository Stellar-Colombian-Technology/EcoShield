from dataclasses import dataclass

@dataclass(frozen=True)
class Params:
    page_size: int = 10
    page_index: int = 1
    search: str = ''
    max_page_size: int = 50

    @property
    def effective_page_size(self) -> int:
        return min(self.page_size, self.max_page_size)

    @property
    def effective_page_index(self) -> int:
        return max(self.page_index, 1)

    @property
    def normalized_search(self) -> str:
        return self.search.lower()

    def with_page_size(self, new_size: int):
        return Params(
            page_size=new_size,
            page_index=self.page_index,
            search=self.search,
            max_page_size=self.max_page_size
        )

    def with_page_index(self, new_index: int):
        return Params(
            page_size=self.page_size,
            page_index=new_index,
            search=self.search,
            max_page_size=self.max_page_size
        )

    def with_search(self, new_search: str):
        return Params(
            page_size=self.page_size,
            page_index=self.page_index,
            search=new_search,
            max_page_size=self.max_page_size
        )