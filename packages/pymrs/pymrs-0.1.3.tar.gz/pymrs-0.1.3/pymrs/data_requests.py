import httpx
import logging
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)
from abc import abstractmethod
from json import dumps, loads
from math import ceil
from .asyncclient import AsyncMRSClient


class _QueryPartOfJSON(BaseModel):
    """This class validates 'query' part of data request JSON."""

    classname: str | None = Field(default=None)
    queryString: str | None = Field(default=None)
    eq: list[dict[str, str]] | None = Field(default=None)
    le: list[dict[str, float]] | None = Field(default=None)
    lt: list[dict[str, float]] | None = Field(default=None)
    ge: list[dict[str, float]] | None = Field(default=None)
    gt: list[dict[str, float]] | None = Field(default=None)
    like: list[dict[str, str]] | None = Field(default=None)
    andd: list[dict[dict[str, str], dict[str, str]]] | None = Field(
        default=None, alias="and"
    )
    orr: list[dict[dict[str, str], dict[str, str]]] | None = Field(
        default=None, alias="or"
    )
    nott: list[dict[dict[str, str], dict[str, str]]] | None = Field(
        default=None, alias="not"
    )
    wktPolygon: str | None = Field(default=None)
    advQS: bool | None = Field(default=None)


# part that would have worked according to data requests segment of API documentation
# class _ScrollPartOfJSON(BaseModel):
#     scroll: bool | None = Field(default=None)
#     scrollId: str | None = Field(default=None)
#     slice: int | None = Field(default=None)
#     sliceCount: int | None = Field(default=None)


class _PaginationPartOfJSON(BaseModel):
    """
    This class should validate 'pagination' part of data request JSON according to
    "Data requests" segment in API documentation but the behavior is not fully tested yet.
    """

    start: int | None = Field(default=None)
    count: int | None = Field(default=None)
    sort: int | None = Field(default=None)
    dir: str | None = Field(default=None)

    @field_validator("dir")
    @classmethod
    def check_function_name(cls, dir: str):
        if dir not in ["ASC", "DESC", None]:
            raise ValueError(f"Sorting direction {dir} is not supported.")
        return dir


class _GroupPartOfJSON(BaseModel):
    """
    This class should validate 'group' part of data request JSON according to
    "Data requests" segment in API documentation but the behavior is not fully tested yet.
    """

    fields: list[str] | None = Field(default=None)
    func: str | None = Field(default=None)
    aggr: str | None = Field(default=None)

    @field_validator("func")
    @classmethod
    def check_function_name(cls, func: str):
        if func not in ["COUNT", "SUM", "AVG", "MIN", "MAX", "PERCENTILE", None]:
            raise ValueError(f"Function {func} is not supported.")
        return func


class QueryValidation(BaseModel):
    """
    This class validates JSON used for data request and is used for JSON generation in Query.assemble_query
    """

    query: _QueryPartOfJSON | None = Field(default=None)
    # scroll: _ScrollPartOfJSON | None = Field(default=None)
    scroll: bool | None = Field(default=None)
    scrollId: str | None = Field(default=None)
    count: int | None = Field(default=None)
    pagination: _PaginationPartOfJSON | None = Field(default=None)
    highlighted: bool | None = Field(default=None)
    showFragment: bool | None = Field(default=None)
    group: _GroupPartOfJSON | None = Field(default=None)
    showGeom: bool | None = Field(default=None)
    loadProperties: list[str] | None = Field(default=None)
    uniquetermsPropName: str | None = Field(default=None)


class BaseQuery(object):
    def __init__(
        self, client: AsyncMRSClient, namespace: str, http_method: str = "GET"
    ):
        """
        Initializes the BaseQuery with the necessary parameters.

        Args:
            client (AsyncMRSClient): The asynchronous client used for making requests.
            namespace (str): The target namespace for the query.
            http_method (str): The HTTP method to use for the request (default is "GET").
        """
        self.client: AsyncMRSClient = client
        self.url_prefix: str = "/data/"
        self.namespace: str = namespace
        self.http_method: str = http_method  # GET/POST/PUT
        self.metaclass: str = ""

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Abstract property that should return the full URL for the query.

        Returns:
            str: The URL for the request.
        """
        pass

    @property
    @abstractmethod
    def data(self) -> str | bytes:
        """
        Abstract property that should return the query data to send with the request.

        Returns:
            str | bytes: The data to be sent in the HTTP request.
        """
        pass

    async def request(self):
        """
        Sends an asynchronous HTTP request using the AsyncMRSClient session stored in client attribute.

        Returns:
            Response: The response from the server.
        """
        return await self.client.request(
            method=self.http_method, endpoint=self.url, data=self.data
        )


class Query(BaseQuery):
    def __init__(self, client: AsyncMRSClient, namespace):
        """
        Initializes the Query with the client and namespace, and sets up various query parameters.

        Args:
            client (AsyncMRSClient): The asynchronous client used for making requests.
            namespace (str): The target namespace for the query.
        """
        super().__init__(client, namespace)
        self.query_queryString: str | None = None
        self.query_eq: list[dict[str, str]] | None = None
        self.query_le: list[dict[str, float]] | None = None
        self.query_lt: list[dict[str, float]] | None = None
        self.query_ge: list[dict[str, float]] | None = None
        self.query_gt: list[dict[str, float]] | None = None
        self.query_like: list[dict[str, str]] | None = None
        self.query_and: list[dict[dict[str, str], dict[str, str]]] | None = None
        self.query_or: list[dict[dict[str, str], dict[str, str]]] | None = None
        self.query_not: list[dict[dict[str, str], dict[str, str]]] | None = None
        self.query_wktPolygon: str | None = None
        self.query_advQS: bool | None = None
        self.scroll: bool | None = None
        self.scrollId: str | None = None
        # self.scroll_slice: int | None = None
        self.scroll_count: int | None = None
        self.pagination_start: int | None = None
        self.pagination_count: int | None = None
        self.pagination_sort: str | None = None
        self.pagination_dir: str | None = None
        self.highlighted: bool | None = None
        self.showFragment: bool | None = None
        self.group_fields: list[str] | None = None
        self.group_func: str | None = None
        self.group_aggr: str | None = None
        self.showGeom: bool | None = None
        self.loadProperties: list[str] | None = None
        self.uniqueTermsPropName: str | None = None
        self.raw_url: str | None = None
        self.raw_data: str | None = None

    def _get_nsp(self, classname: str) -> tuple[str, ...]:
        if classname is None:
            raise ValueError("The class name has to be specified!")
        if ":" not in classname:
            raise ValueError('The class name must be in a form "kmeta:Name"')
        return tuple(classname.split(":"))

    def assemble_query(self, url=False, data=False):
        """
        Assembles the query into a dictionary and optionally returns it as a URL string or bytes.

        Args:
            url (bool): If True, returns the query as a URL-encoded string.
            data (bool): If True, returns the query data in bytes format.

        Returns:
            str: JSON formatted string

        Raises:
            ValueError: If the namespace is missing from the query.
        """
        query_dict = {}
        if self.raw_url:
            if url:
                return f'{self.raw_url.replace("[", "%5B").replace("]", "%5D")}'
            elif data:
                return self.raw_url
        if not self.namespace:
            raise ValueError("ERROR: Query missing namespace.")
        query_dict["query"] = {
            "classname": None,
            "queryString": self.query_queryString,
            "eq": self.query_eq,
            "le": self.query_le,
            "lt": self.query_lt,
            "ge": self.query_ge,
            "gt": self.query_gt,
            "like": self.query_like,
            "and": self.query_and,
            "or": self.query_or,
            "not": self.query_not,
            "wktPolygon": self.query_wktPolygon,
            "advQS": self.query_advQS,
        }
        if self.metaclass:
            query_dict["query"]["classname"] = self.namespace + ":" + self.metaclass
        # else:
        #     query_dict["query"] = {"classname": self.namespace}
        # part that would have worked according to data requests segment of API documentation
        # query_dict["scroll"] = {
        #     "scroll": self.scroll,
        #     "scrollId": self.scrollId,
        #     "slice": self.scroll_slice,
        #     "sliceCount": self.scroll_sliceCount,
        # }
        query_dict["scroll"] = self.scroll
        query_dict["scrollId"] = self.scrollId
        query_dict["count"] = self.scroll_count
        query_dict["pagination"] = {
            "start": self.pagination_start,
            "count": self.pagination_count,
            "sort": self.pagination_sort,
            "dir": self.pagination_dir,
        }
        query_dict["highlighted"] = self.highlighted
        query_dict["showFragment"] = self.showFragment
        query_dict["group"] = {
            "fields": self.group_fields,
            "func": self.group_func,
            "aggr": self.group_aggr,
        }
        query_dict["showGeom"] = self.showGeom
        query_dict["loadProperties"] = self.loadProperties
        query_dict["uniqueTermsPropName"] = self.uniqueTermsPropName
        final_query = loads(
            QueryValidation.model_validate_json(dumps(query_dict)).model_dump_json(
                exclude_none=True
            )
        )
        final_query = dumps({k: final_query[k] for k in final_query if final_query[k]})
        if url:
            formatted_url = f"{self.url_prefix}{self.namespace}.json?q={final_query}"
            formatted_url = formatted_url.replace("[", "%5B").replace("]", "%5D")
            return formatted_url
        elif data:
            return str.encode(final_query)
        return final_query

    @property
    def url(self):
        """
        Returns the complete URL for the query.

        Returns:
            str: The full URL for the query.
        """
        return f"{self.url_prefix}{self.namespace}.json"

    @property
    def data(self):
        """
        Returns the query data to send with the request.

        Returns:
            str | bytes: The data for the request.
        """
        return self.assemble_query(data=True)

    async def close_scroll(self):
        """
        Sends a request to close the scroll context on the server.

        Returns:
            Response: The response from the client if scrollId is set, otherwise None.
        """

        url = f"{self.url_prefix}{self.namespace}/{self.scrollId}/closeScroll.json"
        if self.scrollId:
            return await self.client.request(method="POST", endpoint=url)
        return None

    async def get_entities(self, classname: str, json=None) -> list:
        """Specify a WRS class to query for entities.
        Args:
            classname (str): the name of the class in "kmeta:Name" form.
        Returns:
            list: of entities that found or the empty list.
        """
        nsp = self._get_nsp(classname)[0]
        endpoint: str = "/".join(("", "data", nsp, classname)) + ".json"
        logging.debug(f"get_entities endpoint: {endpoint}, json: {json}")
        response = await self.client.request(method="GET", endpoint=endpoint, json=json)
        if response:
            return response["entities"]
        return []

    async def get_records(self, return_iterator=True):
        """
        Retrieves records from the server with support for pagination and scrolling.

        Args:
            return_iterator (bool): If True, returns an iterator for retrieving records in batches.

        Returns:
            DataIterator | dict: The data iterator or the full response data.

        Raises:
            RequestError: If there is an error with the data request.
        """
        resp_dict = await super().request()
        if resp_dict is None:
            logging.error(f"Error connecting Memoza")
            return None

        try:
            total_length = resp_dict["totalLength"]
            if len(resp_dict.get("entities", [])) == 0:
                logging.info(f"No records found for the query")
                if return_iterator:
                    return DataIterator(self, [], total_length)
                else:
                    return []
            total_batches = ceil(total_length / len(resp_dict["entities"]))
            logging.info(
                f"Retrieving {total_length:,d} records in {total_batches} batches..."
            )
            if self.scroll == True:
                self.scrollId = resp_dict["scrollId"]
        except httpx.RequestError as e:
            logging.error(e)
            return None
        if return_iterator:
            return DataIterator(self, resp_dict["entities"], total_length)
        else:
            return resp_dict["entities"]

    async def get_content(self, classname: str, uri: str):
        """Specify a WRS class to query for a content of an entity.
        Args:
            classname (str): the name of the class in "kmeta:Name" form.
            uri (str): URI of the entity that needs to be accessed
        Returns:
            str: the content of an entity.
        """
        nsp = self._get_nsp(classname)[0]
        endpoint: str = "/".join((nsp, classname, uri, "content.json"))
        url: str = f"{self.url_prefix}{endpoint}"
        response = await self.client.request("GET", url)
        if response is not None:
            return response
        return ""

    async def __aenter__(self):
        """
        Enters the runtime context related to this object.
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exits the runtime context related to this object, ensuring the session is closed.
        """
        await self.client.client.aclose()


class DataIterator:
    def __init__(self, query: Query, entities, length):
        """
        Initializes the DataIterator with the Query and the first batch of data.

        Args:
            query (Query): The query object that generates the data.
            data_json (dict): The initial batch of data received from the server.
        """
        self.entities = entities
        self.current_entity_index = 0
        self.total_length = length
        self.total_batches = ceil(self.total_length / len(entities))
        self.current_batch = 1
        self.query = query

    def __iter__(self):
        """
        Returns the iterator object itself.

        Returns:
            DataIterator: The iterator instance.
        """
        return self

    async def __next__(self):
        """
        Retrieves the next entity in the data. If the current batch is exhausted,
        it requests the next batch from the server.

        Returns:
            dict: The next entity in the dataset.

        Raises:
            StopIteration: If there are no more entities to retrieve.
        """
        if not self.entities:
            if self.total_batches > self.current_batch:
                try:
                    r = await self.query.client.request(
                        "GET", self.query.url, self.query.data
                    )
                    if r:
                        self.entities = r["entities"]
                        self.current_batch += 1
                        self.current_entity_index = 0
                    if (
                        self.current_batch % 10 == 0
                    ):  # print every n subsequent requests
                        logging.info(
                            f"{self.current_batch}/{self.total_batches} {self.query.namespace}:{self.query.data}"
                        )
                except Exception as e:
                    logging.error(f"Failed to fetch next batch: {e}")
                    await self.query.close_scroll()
                    raise StopIteration
            else:
                logging.info(f"Retrieved {self.total_length:,d} records.")
                await self.query.close_scroll()
                raise StopIteration
        self.current_entity_index += 1
        return self.entities.pop(0)

    def __len__(self):
        return len(self.entities)

    def __aenter__(self):
        """
        Enter method for context management.

        Returns:
            DataIterator: The iterator instance.
        """
        return self

    def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit method for context management.

        Returns:
            None
        """
        return
