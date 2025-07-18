"""
Data Access layer for Oracle Forge

This package provides data access classes for managing all types of data
in Oracle Forge, including adventures, lookup data, tables, and rules.
"""

from .base_data import BaseDataAccess, DataAccessError, TemplateNotFoundError, ValidationError
from .adventure_data import AdventureDataAccess
from .lookup_data import LookupDataAccess
from .tables_data import TableDataAccess
from .rules_data import RuleDataAccess

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