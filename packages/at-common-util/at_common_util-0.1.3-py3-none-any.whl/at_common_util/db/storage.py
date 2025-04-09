from typing import List, Type, Optional, TypeVar, Any, Dict, Generic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
import logging
from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
import threading
import asyncio

T = TypeVar('T')
FilterType = List[Any]
SortType = List[Any]

class Storage(Generic[T]):
    """
    Database connection management for SQLAlchemy async sessions.
    
    This class follows the singleton pattern and should be initialized with
    a connection URL before use.
    """
    _instance = None
    _is_initialized = False
    _thread_lock = threading.Lock()
    _async_lock = None  # Will be initialized in __new__

    def __new__(cls, *args, **kwargs):
        with cls._thread_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.engine = None
                cls._instance.AsyncSessionLocal = None
                cls._instance.DB_CONNECTION_URL = None
                cls._instance._async_lock = asyncio.Lock()
        return cls._instance

    def init(self, connection_url: str) -> None:
        """Initialize the Storage with async database connection
        
        Args:
            connection_url: The database connection URL
            
        Raises:
            RuntimeError: If initialization fails
        """
        with self._thread_lock:
            # Store cleanup task if created during this initialization
            cleanup_task = None
            
            # Check if already initialized with same connection URL
            if self._is_initialized and self.DB_CONNECTION_URL == connection_url:
                logging.debug("Storage already initialized with the same connection URL")
                return

            # Clean up existing engine if reinitializing
            if self._is_initialized:
                logging.info("Reinitializing Storage with new connection URL")
                # Create cleanup task but don't wait for it to complete inside the lock
                cleanup_task = asyncio.create_task(self._cleanup_engine())
            
            try:
                # Store the connection URL for potential override in tests
                self.DB_CONNECTION_URL = connection_url
                
                # Base engine arguments
                engine_args = {
                    "pool_pre_ping": True,  # Add connection health check
                    "pool_recycle": 3600,   # Recycle connections after 1 hour
                    "echo": False,          # Set to True for SQL logging during development
                }
                
                # For non-SQLite connections, add connection pooling parameters
                if not connection_url.startswith('sqlite'):
                    engine_args.update({
                        "pool_size": 10,        # Connection pool size
                        "max_overflow": 20      # Max additional connections
                    })
                
                self.engine = create_async_engine(
                    self.DB_CONNECTION_URL,
                    **engine_args
                )
                self.AsyncSessionLocal = async_sessionmaker(
                    bind=self.engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                    autoflush=False
                )
                self._is_initialized = True
                logging.info("Storage initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Storage: {str(e)}")
                raise RuntimeError(f"Storage initialization failed: {str(e)}")
        
        # If we created a cleanup task, wait for it to complete outside the lock
        if cleanup_task:
            try:
                # Use asyncio.run to handle the case when called from a synchronous context
                asyncio.run(cleanup_task)
            except RuntimeError:
                # If we're already in an async context, we can't use asyncio.run
                # The task will run in the background
                pass

    async def init_async(self, connection_url: str) -> None:
        """Asynchronous version of init for use in async contexts
        
        Args:
            connection_url: The database connection URL
            
        Raises:
            RuntimeError: If initialization fails
        """
        async with self._async_lock:
            # Check if already initialized with same connection URL
            if self._is_initialized and self.DB_CONNECTION_URL == connection_url:
                logging.debug("Storage already initialized with the same connection URL")
                return

            # Clean up existing engine if reinitializing
            if self._is_initialized:
                logging.info("Reinitializing Storage with new connection URL")
                await self._cleanup_engine()
            
            try:
                # Store the connection URL for potential override in tests
                self.DB_CONNECTION_URL = connection_url
                
                # Base engine arguments
                engine_args = {
                    "pool_pre_ping": True,  # Add connection health check
                    "pool_recycle": 3600,   # Recycle connections after 1 hour
                    "echo": False,          # Set to True for SQL logging during development
                }
                
                # For non-SQLite connections, add connection pooling parameters
                if not connection_url.startswith('sqlite'):
                    engine_args.update({
                        "pool_size": 10,        # Connection pool size
                        "max_overflow": 20      # Max additional connections
                    })
                
                self.engine = create_async_engine(
                    self.DB_CONNECTION_URL,
                    **engine_args
                )
                self.AsyncSessionLocal = async_sessionmaker(
                    bind=self.engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                    autoflush=False
                )
                self._is_initialized = True
                logging.info("Storage initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Storage: {str(e)}")
                raise RuntimeError(f"Storage initialization failed: {str(e)}")

    async def _cleanup_engine(self):
        """Clean up the existing engine and connection pools"""
        async with self._async_lock:
            if self.engine:
                logging.info("Disposing existing database engine")
                await self.engine.dispose()
                self.engine = None
                self.AsyncSessionLocal = None
                self._is_initialized = False

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """Get a database session as an async context manager
        
        Yields:
            AsyncSession: A SQLAlchemy async session
            
        Raises:
            RuntimeError: If storage is not initialized
            Exception: Any database errors that occur during session use
        """
        if not self._is_initialized:
            raise RuntimeError("Storage must be initialized with database settings first. Call storage.init() before using.")
            
        session = self.AsyncSessionLocal()
        try:
            yield session
        except SQLAlchemyError as e:
            logging.error(f"Database error: {str(e)}")
            await session.rollback()
            raise
        except Exception as e:
            logging.error(f"Session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()
            
    @asynccontextmanager
    async def transaction(self) -> AsyncSession:
        """
        Provides a transaction context manager for explicit transaction control
        
        Yields:
            AsyncSession: A SQLAlchemy async session with active transaction
            
        Example:
            async with storage.transaction() as session:
                # Multiple operations in a single transaction
                session.add(model1)
                session.add(model2)
        """
        async with self.get_session() as session:
            async with session.begin():
                yield session

    async def query(
        self, 
        model_class: Type[T], 
        filters: Optional[FilterType] = None,
        sort: Optional[SortType] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[T]:
        """
        Query database for records with optional filtering, sorting, and pagination
        
        Args:
            model_class: The SQLAlchemy model class
            filters: List of SQLAlchemy filter conditions
            sort: List of SQLAlchemy order_by expressions
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of model objects
        """
        async with self.get_session() as session:
            query = select(model_class)
            if filters:
                query = query.filter(*filters)
            if sort:
                query = query.order_by(*sort)
            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            
            result = await session.execute(query)
            return result.scalars().all()
    
    async def find_one(
        self,
        model_class: Type[T],
        filters: Optional[FilterType] = None,
    ) -> Optional[T]:
        """
        Find a single record matching the filters
        
        Args:
            model_class: The SQLAlchemy model class
            filters: List of SQLAlchemy filter conditions
            
        Returns:
            Single model object or None if not found
        """
        async with self.get_session() as session:
            query = select(model_class)
            if filters:
                query = query.filter(*filters)
            query = query.limit(1)
            
            result = await session.execute(query)
            return result.scalars().first()
            
    async def create(self, model_obj: T) -> T:
        """
        Create a new record in the database
        
        Args:
            model_obj: The model object to create
            
        Returns:
            The created model object with ID populated
        """
        async with self.get_session() as session:
            session.add(model_obj)
            await session.commit()
            await session.refresh(model_obj)
            return model_obj
    
    async def create_many(self, model_objects: List[T]) -> List[T]:
        """
        Create multiple records efficiently using bulk operations
        
        Args:
            model_objects: List of model objects to create
            
        Returns:
            List of created model objects with IDs populated
        """
        if not model_objects:
            return []
            
        async with self.transaction() as session:
            # Add all objects to session in one go
            session.add_all(model_objects)
            
            # Flush once instead of refreshing individually
            await session.flush()
            return model_objects
            
    async def update_by_field(
        self, 
        model_class: Type[T], 
        field_name: str, 
        field_value: Any, 
        update_data: Dict[str, Any]
    ) -> Optional[T]:
        """
        Update a record by a specific field value with the provided data
        
        Args:
            model_class: The SQLAlchemy model class
            field_name: The field name to use for identifying the record
            field_value: The value of the field to match
            update_data: Dictionary of field names and values to update
            
        Returns:
            Updated model object or None if not found
        """
        if not update_data:
            return await self.get_by_field(model_class, field_name, field_value)
            
        async with self.get_session() as session:
            field = getattr(model_class, field_name)
            query = update(model_class).where(field == field_value).values(**update_data)
            await session.execute(query)
            await session.commit()
            
            # Return the updated record
            return await self.get_by_field(model_class, field_name, field_value)
    
    async def get_by_field(self, model_class: Type[T], field_name: str, field_value: Any) -> Optional[T]:
        """
        Get a record by a specific field value
        
        Args:
            model_class: The SQLAlchemy model class
            field_name: The field name to use for identifying the record
            field_value: The value of the field to match
            
        Returns:
            Model object or None if not found
        """
        field = getattr(model_class, field_name)
        return await self.find_one(model_class, filters=[field == field_value])
            
    async def delete_by_field(self, model_class: Type[T], field_name: str, field_value: Any) -> bool:
        """
        Delete a record by a specific field value
        
        Args:
            model_class: The SQLAlchemy model class
            field_name: The field name to use for identifying the record
            field_value: The value of the field to match
            
        Returns:
            True if deleted successfully, False otherwise
        """
        async with self.get_session() as session:
            field = getattr(model_class, field_name)
            query = delete(model_class).where(field == field_value)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0
    
    async def delete_many_by_field(self, model_class: Type[T], field_name: str, values: List[Any]) -> int:
        """
        Delete multiple records by field values in a single transaction
        
        Args:
            model_class: The SQLAlchemy model class
            field_name: The field name to use for identifying the records
            values: List of values to match against the field
            
        Returns:
            Number of records deleted
        """
        if not values:
            return 0
            
        async with self.get_session() as session:
            field = getattr(model_class, field_name)
            filter_condition = field.in_(values)
            
            # Execute delete query
            stmt = delete(model_class).where(filter_condition)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount
            
    async def count(self, model_class: Type[T], filters: Optional[FilterType] = None) -> int:
        """
        Count the number of records
        
        Args:
            model_class: The SQLAlchemy model class
            filters: Optional list of filter conditions
            
        Returns:
            Number of records matching the filters
        """
        async with self.get_session() as session:
            query = select(func.count()).select_from(model_class)
            if filters:
                query = query.filter(*filters)
            result = await session.execute(query)
            return result.scalar_one()

    async def dispose(self) -> None:
        """
        Cleanup database connections
        
        This should be called when shutting down the application
        """
        if hasattr(self, 'engine') and self.engine:
            logging.info("Disposing database engine connections")
            await self.engine.dispose()
            self._is_initialized = False

    async def shutdown(self):
        """Shutdown the Storage and clean up all connections"""
        async with self._async_lock:
            if self._is_initialized:
                await self._cleanup_engine()
                logging.info("Storage shutdown complete")

class StorageManager:
    """
    A registry for managing multiple storage instances.
    Supports both synchronous and asynchronous access patterns.
    """
    _pools = {}
    _thread_lock = threading.Lock()
    _async_lock = asyncio.Lock()
    
    @classmethod
    def get_storage(cls, name: str = "default", connection_url: Optional[str] = None) -> Storage:
        """
        Synchronous access for threading environments
        
        Args:
            name: Storage name/identifier
            connection_url: Database connection URL (required for new storage instances)
            
        Returns:
            Storage instance
            
        Raises:
            ValueError: If connection_url is not provided for a new storage instance
        """
        with cls._thread_lock:
            if name not in cls._pools:
                if not connection_url:
                    raise ValueError("Must provide connection_url for new storage")
                store = Storage()
                store.init(connection_url)
                cls._pools[name] = store
            return cls._pools[name]
            
    @classmethod
    async def get_storage_async(cls, name: str = "default", connection_url: Optional[str] = None) -> Storage:
        """
        Asynchronous access for coroutine environments
        
        Args:
            name: Storage name/identifier
            connection_url: Database connection URL (required for new storage instances)
            
        Returns:
            Storage instance
            
        Raises:
            ValueError: If connection_url is not provided for a new storage instance
        """
        async with cls._async_lock:
            if name not in cls._pools:
                if not connection_url:
                    raise ValueError("Must provide connection_url for new storage")
                store = Storage()
                # Use the async initialization method
                await store.init_async(connection_url)
                cls._pools[name] = store
            return cls._pools[name]