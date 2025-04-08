from typing import Type, TypeVar, Generic
from sqlalchemy import select
from sqlalchemy.sql import Select

T = TypeVar('T')

class QueryBuilder(Generic[T]):
    """
    Query builder for constructing SQLAlchemy queries with a fluent API.
    """
    
    def __init__(self, model_class: Type[T]):
        """
        Initialize with the model class to query.
        
        Args:
            model_class: The SQLAlchemy model class
        """
        self.model_class = model_class
        self.query = select(model_class)
        self._filters = []
        self._sort = []
        self._limit = None
        self._offset = None
        self._group_by = []
        
    def filter(self, *conditions) -> 'QueryBuilder[T]':
        """
        Add filter conditions to the query.
        
        Args:
            *conditions: SQLAlchemy filter conditions
            
        Returns:
            Self for method chaining
        """
        self._filters.extend(conditions)
        return self
    
    def filter_by(self, **kwargs) -> 'QueryBuilder[T]':
        """
        Add filter conditions using keyword arguments.
        
        Args:
            **kwargs: Field name and value pairs
            
        Returns:
            Self for method chaining
        """
        for field_name, value in kwargs.items():
            field = getattr(self.model_class, field_name)
            self._filters.append(field == value)
        return self
        
    def order_by(self, *order_criteria) -> 'QueryBuilder[T]':
        """
        Add ordering criteria to the query.
        
        Args:
            *order_criteria: SQLAlchemy order by expressions
            
        Returns:
            Self for method chaining
        """
        self._sort.extend(order_criteria)
        return self
        
    def limit(self, count: int) -> 'QueryBuilder[T]':
        """
        Set the limit for the query.
        
        Args:
            count: Maximum number of records to return
            
        Returns:
            Self for method chaining
        """
        self._limit = count
        return self
        
    def offset(self, count: int) -> 'QueryBuilder[T]':
        """
        Set the offset for the query.
        
        Args:
            count: Number of records to skip
            
        Returns:
            Self for method chaining
        """
        self._offset = count
        return self
        
    def group_by(self, *group_criteria) -> 'QueryBuilder[T]':
        """
        Add group by criteria to the query.
        
        Args:
            *group_criteria: SQLAlchemy group by expressions
            
        Returns:
            Self for method chaining
        """
        self._group_by.extend(group_criteria)
        return self
        
    def build(self) -> Select:
        """
        Build and return the SQLAlchemy query object.
        
        Returns:
            SQLAlchemy Select object
        """
        query = self.query
        
        if self._filters:
            query = query.filter(*self._filters)
            
        if self._sort:
            query = query.order_by(*self._sort)
            
        if self._group_by:
            query = query.group_by(*self._group_by)
            
        if self._offset is not None:
            query = query.offset(self._offset)
            
        if self._limit is not None:
            query = query.limit(self._limit)
            
        return query
        
    @staticmethod
    def for_model(model_class: Type[T]) -> 'QueryBuilder[T]':
        """
        Create a new query builder for the given model class.
        
        Args:
            model_class: The SQLAlchemy model class
            
        Returns:
            New QueryBuilder instance
        """
        return QueryBuilder(model_class) 