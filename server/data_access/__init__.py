"""
Data Access layer for Oracle Forge

This package provides data access classes for managing all types of data
in Oracle Forge, including adventures, lookup data, tables, and rules.
"""

from .base import BaseDataAccess, DataAccessError, TemplateNotFoundError, ValidationError
from .adventure import AdventureDataAccess
from .lookup import LookupDataAccess
from .tables import TableDataAccess
from .rules import RuleDataAccess

__all__ = [
    'BaseDataAccess',
    'DataAccessError', 
    'TemplateNotFoundError',
    'ValidationError',
    'AdventureDataAccess',
    'LookupDataAccess',
    'TableDataAccess',
    'RuleDataAccess',
] 