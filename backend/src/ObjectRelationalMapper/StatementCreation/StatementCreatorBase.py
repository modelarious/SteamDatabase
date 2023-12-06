from typing import Type
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase
from abc import ABC, abstractmethod


class StatementCreatorBase(ABC):
    @abstractmethod
    def create(ORMObjectClass: Type[ORMAbstractBase]) -> str:
        pass
