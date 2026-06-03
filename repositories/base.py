"""
Generic Repository Interface — Assignment 11
Defines the contract all storage backends must fulfil.
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    """
    Generic repository interface.
    All CRUD operations are defined here; implementations provide the storage.
    """

    @abstractmethod
    def save(self, entity: T) -> T:
        """Create or update an entity. Returns the saved entity."""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Return entity by ID, or None if not found."""
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """Return all stored entities."""
        pass

    @abstractmethod
    def delete(self, entity_id: ID) -> bool:
        """Delete entity by ID. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def exists(self, entity_id: ID) -> bool:
        """Return True if an entity with this ID exists."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Return total number of stored entities."""
        pass
