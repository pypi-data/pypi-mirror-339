from asyncio import current_task
from typing import override

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from archipy.adapters.orm.sqlalchemy.session_manager_ports import AsyncSessionManagerPort, SessionManagerPort
from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import SqlAlchemyConfig
from archipy.helpers.metaclasses.singleton import Singleton


class SessionManagerAdapter(SessionManagerPort, metaclass=Singleton):
    """Manages SQLAlchemy database sessions for synchronous operations.

    This adapter creates and manages database sessions using SQLAlchemy's
    session management system. It implements the Singleton pattern to ensure
    a single instance exists throughout the application lifecycle.

    Args:
        orm_config (SqlAlchemyConfig, optional): Configuration for the ORM.
            If None, retrieves from global config. Defaults to None.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter
        >>> from archipy.configs.config_template import SqlAlchemyConfig
        >>>
        >>> # Using default global configuration
        >>> manager = SessionManagerAdapter()
        >>> session = manager.get_session()
        >>>
        >>> # Using custom configuration
        >>> custom_config = SqlAlchemyConfig(DATABASE="custom_db", HOST="localhost")
        >>> custom_manager = SessionManagerAdapter(custom_config)
    """

    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        configs: SqlAlchemyConfig = orm_config or BaseConfig().global_config().SQLALCHEMY
        self.engine = self._create_engine(configs)
        self._session_generator = self._get_session_generator(configs)

    @override
    def get_session(self) -> Session:
        """Retrieves a SQLAlchemy session from the session factory.

        The session is scoped to the current context to ensure thread safety.

        Returns:
            Session: A SQLAlchemy session instance that can be used for
                database operations.

        Examples:
            >>> session = session_manager.get_session()
            >>> user = session.query(User).filter_by(id=1).first()
        """
        return self._session_generator()

    @override
    def remove_session(self) -> None:
        """Removes the current session from the registry.

        This should be called when you're done with a session to prevent
        resource leaks, particularly at the end of web requests.

        Examples:
            >>> session = session_manager.get_session()
            >>> # Use session for operations
            >>> session_manager.remove_session()
        """
        self._session_generator.remove()

    def _get_session_generator(self, configs: SqlAlchemyConfig) -> scoped_session:
        session_maker = sessionmaker(self.engine)
        return scoped_session(session_maker)

    @staticmethod
    def _create_engine(configs: SqlAlchemyConfig) -> Engine:
        url = URL.create(
            drivername=configs.DRIVER_NAME,
            username=configs.USERNAME,
            password=configs.PASSWORD,
            host=configs.HOST,
            port=configs.PORT,
            database=configs.DATABASE,
        )
        return create_engine(
            url,
            isolation_level=configs.ISOLATION_LEVEL,
            echo=configs.ECHO,
            echo_pool=configs.ECHO_POOL,
            enable_from_linting=configs.ENABLE_FROM_LINTING,
            hide_parameters=configs.HIDE_PARAMETERS,
            pool_pre_ping=configs.POOL_PRE_PING,
            pool_size=configs.POOL_SIZE,
            pool_recycle=configs.POOL_RECYCLE_SECONDS,
            pool_reset_on_return=configs.POOL_RESET_ON_RETURN,
            pool_timeout=configs.POOL_TIMEOUT,
            pool_use_lifo=configs.POOL_USE_LIFO,
            query_cache_size=configs.QUERY_CACHE_SIZE,
            max_overflow=configs.POOL_MAX_OVERFLOW,
        )


class AsyncSessionManagerAdapter(AsyncSessionManagerPort, metaclass=Singleton):
    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        configs: SqlAlchemyConfig = orm_config or BaseConfig().global_config().SQLALCHEMY
        self.engine = self._create_async_engine(configs)
        self._session_generator = self._get_session_generator(configs)

    @override
    def get_session(self) -> AsyncSession:
        return self._session_generator()

    @override
    async def remove_session(self) -> None:
        await self._session_generator.remove()

    def _get_session_generator(self, configs: SqlAlchemyConfig) -> async_scoped_session:
        session_maker: async_sessionmaker = async_sessionmaker(self.engine)
        return async_scoped_session(session_maker, current_task)

    @staticmethod
    def _create_async_engine(configs: SqlAlchemyConfig) -> AsyncEngine:
        url = URL.create(
            drivername=configs.DRIVER_NAME,
            username=configs.USERNAME,
            password=configs.PASSWORD,
            host=configs.HOST,
            port=configs.PORT,
            database=configs.DATABASE,
        )
        return create_async_engine(
            url,
            isolation_level=configs.ISOLATION_LEVEL,
            echo=configs.ECHO,
            echo_pool=configs.ECHO_POOL,
            enable_from_linting=configs.ENABLE_FROM_LINTING,
            hide_parameters=configs.HIDE_PARAMETERS,
            pool_pre_ping=configs.POOL_PRE_PING,
            pool_size=configs.POOL_SIZE,
            pool_recycle=configs.POOL_RECYCLE_SECONDS,
            pool_reset_on_return=configs.POOL_RESET_ON_RETURN,
            pool_timeout=configs.POOL_TIMEOUT,
            pool_use_lifo=configs.POOL_USE_LIFO,
            query_cache_size=configs.QUERY_CACHE_SIZE,
            max_overflow=configs.POOL_MAX_OVERFLOW,
        )
