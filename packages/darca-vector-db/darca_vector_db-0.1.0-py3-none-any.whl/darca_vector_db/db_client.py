"""
db_client.py
============

A pluggable vector database client system with backend support.
Currently, the only supported backend is Qdrant.

Modules:
    - BaseDBClient (Abstract Base Class)
    - QdrantDBClient (Qdrant implementation of BaseDBClient)
    - DBClient (Unified client interface)
    - Custom Exceptions

Author: Your Name
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from darca_exception.exception import DarcaException
from darca_log_facility.logger import DarcaLogger
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, PointStruct, VectorParams

# === Custom Exceptions ===


class DBClientException(DarcaException):
    """
    Base exception class for all errors related to vector database operations.

    Attributes:
        message (str): Description of the error.
        error_code (str): A unique code representing the error type.
        metadata (dict): Additional information related to the error.
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.metadata = metadata or {}
        super().__init__(message)


class DBConnectionError(DBClientException):
    """Raised when a connection attempt to the vector database fails."""

    pass


class CollectionCreationError(DBClientException):
    """
    Raised when the creation of a collection in the vector database fails.
    """

    pass


class VectorInsertionError(DBClientException):
    """Raised when inserting a vector into a collection fails."""

    pass


class VectorSearchError(DBClientException):
    """Raised when searching for vectors within a collection fails."""

    pass


# === Abstract Base Client ===


class BaseDBClient(ABC):
    """
    Abstract base class for vector database clients.

    This class defines a standardized interface for all vector database
    clients. It enforces implementation of essential methods for connecting
    to a vector database, creating collections, inserting vectors, and
    performing vector searches.

    Methods
    -------
    connect() -> None
        Establishes a connection to the vector database.
    create_collection
        (name: str, vector_size: int, distance_metric: str) -> None
        Creates a new collection in the vector database.
    insert_vector(collection_name: str, vector_id: str, vector: List[float],
        metadata: Optional[Dict[str, Any]]) -> None
        Inserts a vector into a specified collection.
    search_vectors(collection_name: str, query_vector:
        List[float], top_k: int) -> Any
        Searches for similar vectors within a collection.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Establishes a connection to the vector database.

        This method should be implemented by subclasses to establish a
        connection
        to the underlying vector database system.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by the subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def create_collection(
        self, name: str, vector_size: int, distance_metric: str
    ) -> None:
        """
        Creates a new collection in the vector database.

        This method defines the creation of a new collection within the vector
        database. A collection is a logical grouping of vectors with a
        specified size and distance metric.

        Parameters
        ----------
        name : str
            The name of the collection to create. Must be unique within the
            database.
        vector_size : int
            The size (dimensionality) of the vectors to be stored in the
            collection.
        distance_metric : str
            The distance metric to use for vector comparisons. Typical
            values include:

                - 'cosine'
                - 'euclidean'
                - 'dot'

        Raises
        ------
        NotImplementedError
            If the method is not implemented by the subclass.
        ValueError
            If the specified distance metric is not supported by the backend.
            Note: Validation for unsupported distance metrics must be
            implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def insert_vector(
        self,
        collection_name: str,
        vector_id: str,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Inserts a vector into a specified collection.

        This method adds a single vector, identified by a unique ID, to an
        existing collection.
        Optionally, metadata can be associated with the vector for additional
        information.

        Parameters
        ----------
        collection_name : str
            The name of the collection where the vector will be stored.
        vector_id : str
            A unique identifier for the vector. It must be unique within the
            collection.
        vector : List[float]
            The vector data to be inserted. The length of the list should
            match the collection's vector size.
        metadata : dict, optional
            A dictionary of metadata to associate with the vector. Defaults
            to None.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by the subclass.
        ValueError
            If the vector size does not match the expected collection
            vector size.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def search_vectors(
        self, collection_name: str, query_vector: List[float], top_k: int = 10
    ) -> Any:
        """
        Searches for similar vectors within a collection.

        This method performs a similarity search against a specified
        collection,
        returning the most similar vectors to a given query vector.

        Parameters
        ----------
        collection_name : str
            The name of the collection to search within.
        query_vector : List[float]
            The query vector used to perform the search. The length must
            match the collection's vector size.
        top_k : int, optional
            The number of most similar vectors to return. Defaults to 10.

        Returns
        -------
        Any
            The search results as returned by the underlying vector
            database implementation.
            The format of the results may vary depending on the backend.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by the subclass.
        ValueError
            If the query vector size does not match the expected
            collection vector size.
        """
        raise NotImplementedError("Subclasses must implement this method.")


# === Qdrant Implementation ===


class QdrantDBClient(BaseDBClient):
    """
    Implementation of the BaseDBClient for the Qdrant vector database.

    Parameters
    ----------
    host : str
        Host address of the Qdrant server.
    port : int
        Port number for the Qdrant server.
    api_key : str, optional
        API key for authentication.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        api_key: Optional[str] = None,
    ):
        self.logger = DarcaLogger("darca-vector-db.qdrant").get_logger()
        self.host = os.getenv("DARCA_VECTORDB_HOST", host)
        self.port = int(os.getenv("DARCA_VECTORDB_PORT", port))
        self.api_key = api_key
        self.client = None

    def connect(self) -> None:
        """Establishes a connection to the Qdrant server."""
        try:
            self.client = QdrantClient(
                host=self.host, port=self.port, api_key=self.api_key
            )
            self.logger.info(
                f"Successfully connected to Qdrant at {self.host}:{self.port}"
            )
        except Exception:
            self.logger.error("Connection to Qdrant failed", exc_info=True)
            raise DBConnectionError(
                "Failed to connect to Qdrant server", "DB_CONN_ERROR"
            )

    def create_collection(
        self, name: str, vector_size: int, distance_metric: str = "cosine"
    ) -> None:
        """Creates a collection in Qdrant."""
        try:
            distance = getattr(Distance, distance_metric.upper())
            self.client.create_collection(
                name, VectorParams(size=vector_size, distance=distance)
            )
            self.logger.info(f"Collection '{name}' created successfully.")
        except AttributeError:
            raise ValueError(f"Unsupported distance metric: {distance_metric}")
        except UnexpectedResponse:
            self.logger.error("Failed to create collection", exc_info=True)
            raise CollectionCreationError(
                "Failed to create collection", "COLLECTION_CREATION_ERROR"
            )

    def insert_vector(
        self,
        collection_name: str,
        vector_id: int,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Inserts a vector into the Qdrant collection."""
        try:
            point = PointStruct(id=vector_id, vector=vector, payload=metadata)
            self.client.upsert(collection_name=collection_name, points=[point])
            self.logger.info(
                f"Vector with ID '{vector_id}' inserted successfully "
                f"into '{collection_name}'."
            )
        except Exception:
            self.logger.error("Failed to insert vector", exc_info=True)
            raise VectorInsertionError(
                "Failed to insert vector", "VECTOR_INSERTION_ERROR"
            )

    def search_vectors(
        self, collection_name: str, query_vector: List[float], top_k: int = 10
    ) -> Any:
        """Searches for similar vectors within the Qdrant collection."""
        try:
            results = self.client.search(
                collection_name, query_vector, limit=top_k
            )
            self.logger.info(
                f"Search completed successfully in collection "
                f"'{collection_name}'."
            )
            return results
        except Exception:
            self.logger.error("Failed to search vectors", exc_info=True)
            raise VectorSearchError(
                "Failed to search vectors", "VECTOR_SEARCH_ERROR"
            )


# === DBClient Wrapper ===


class DBClient:
    """
    A unified client for interacting with vector databases.

    Parameters
    ----------
    backend : str
        The backend to use (default: 'qdrant').
    kwargs : dict
        Additional parameters for backend initialization.
    """

    def __init__(self, backend: str = "qdrant", **kwargs):
        self.logger = DarcaLogger("darca-vector-db").get_logger()
        if backend == "qdrant":
            self._client = QdrantDBClient(**kwargs)
        else:
            raise DBClientException(
                f"Backend '{backend}' is not supported",
                "DB_UNSUPPORTED_BACKEND",
            )

    def connect(self) -> None:
        """Establishes a connection to the vector database."""
        self._client.connect()
        self.logger.info("Connected to the vector database.")

    def create_collection(
        self, name: str, vector_size: int, distance_metric: str = "cosine"
    ) -> None:
        """
        Creates a new collection in the vector database.

        Parameters
        ----------
        name : str
            The name of the collection to create.
        vector_size : int
            The size of the vectors to be stored in the collection.
        distance_metric : str
            The distance metric to use for vector comparisons
            (default: 'cosine').
        Raises
        -------
        ValueError
            If the distance metric is not supported.
        CollectionCreationError
            If the collection creation fails.
        """
        self._client.create_collection(name, vector_size, distance_metric)
        self.logger.info(f"Collection '{name}' created.")

    def insert_vector(
        self,
        collection_name: str,
        vector_id: str,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Inserts a vector into the specified collection.
        Parameters
        ----------
        collection_name : str
            The name of the collection to insert the vector into.
        vector_id : str
            The unique ID for the vector.
        vector : list[float]
            The vector data to insert.
        metadata : dict, optional
            Additional metadata to associate with the vector.
        Raises
        VectorInsertionError
            If the vector insertion fails.
        """
        self._client.insert_vector(
            collection_name, vector_id, vector, metadata
        )
        self.logger.info(
            f"Vector '{vector_id}' inserted into collection "
            f"'{collection_name}'."
        )

    def search_vectors(
        self, collection_name: str, query_vector: List[float], top_k: int = 10
    ) -> Any:
        """
        Searches for similar vectors in the specified collection.
        Parameters
        ----------
        collection_name : str
            The name of the collection to search.
        query_vector : list[float]
            The vector to search for.
        top_k : int
            The number of similar vectors to return (default: 10).
        Returns
        -------
        Any
            The search results.
        Raises
        VectorSearchError
            If the vector search fails.
        """
        results = self._client.search_vectors(
            collection_name, query_vector, top_k
        )
        self.logger.info(
            f"Search completed in collection '{collection_name}'."
        )
        return results

    def __getattr__(self, name):
        return getattr(self._client, name)
