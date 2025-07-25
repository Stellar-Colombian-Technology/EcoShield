from dataclasses import dataclass
from math import ceil
from typing import Generic, List, TypeVar, Callable, Dict

T = TypeVar("T")

@dataclass(frozen=True)
class Pager(Generic[T]):
    registers: List[T]
    total: int
    page_index: int
    page_size: int
    search: str

    @property
    def total_pages(self) -> int:
        return ceil(self.total / self.page_size) if self.page_size else 1

    @property
    def has_previous_page(self) -> bool:
        return self.page_index > 1

    @property
    def has_next_page(self) -> bool:
        return self.page_index < self.total_pages

    def map_registers(self, mapper_fn: Callable[[T], T]) -> 'Pager':
        return Pager(
            registers=list(map(mapper_fn, self.registers)),
            total=self.total,
            page_index=self.page_index,
            page_size=self.page_size,
            search=self.search
        )

    def filter_registers(self, predicate_fn: Callable[[T], bool]) -> 'Pager':
        filtered = list(filter(predicate_fn, self.registers))
        return Pager(
            registers=filtered,
            total=len(filtered),
            page_index=self.page_index,
            page_size=self.page_size,
            search=self.search
        )

    def get_pagination_info(self) -> Dict:
        return {
            "currentPage": self.page_index,
            "pageSize": self.page_size,
            "totalCount": self.total,
            "totalPages": self.total_pages,
            "hasPrevious": self.has_previous_page,
            "hasNext": self.has_next_page,
            "search": self.search
        }