import logging
from collections.abc import Iterator
from typing import Optional

import tableauserverclient as TSC  # type: ignore

from ....utils import SerializedAsset, retry
from ..assets import TableauAsset
from ..constants import DEFAULT_PAGE_SIZE
from .errors import TableauApiError, TableauApiTimeout
from .gql_queries import FIELDS_QUERIES, GQL_QUERIES, QUERY_TEMPLATE

logger = logging.getLogger(__name__)

# increase the value when extraction is too slow
# decrease the value when timeouts arise
_CUSTOM_PAGE_SIZE: dict[TableauAsset, int] = {
    # fields are light but volumes are bigger
    TableauAsset.FIELD: 1000,
    # tables are sometimes heavy
    TableauAsset.TABLE: 50,
}

_TIMEOUT_MESSAGE = (
    "Execution canceled because timeout of 30000 millis was reached"
)

_RETRY_BASE_MS = 10_000
_RETRY_COUNT = 4


def _check_errors(answer: dict) -> None:
    """
    handle errors in graphql response:
    - return None when there's no errors in the answer
    - TableauApiTimeout if any of the errors is a timeout
    - TableauApiError (generic) otherwise
    """
    if "errors" not in answer:
        return

    errors = answer["errors"]

    for error in errors:
        if error.get("message") == _TIMEOUT_MESSAGE:
            # we need specific handling for timeout issues (retry strategy)
            raise TableauApiTimeout(errors)

    raise TableauApiError(answer["errors"])


def gql_query_scroll(
    server,
    resource: str,
    fields: str,
    page_size: int,
) -> Iterator[SerializedAsset]:
    """
    Iterate over GQL query results, handling pagination and cursor

    We have a retry strategy when timeout issues arise.
    It's a known issue on Tableau side, still waiting for their fix:
    https://issues.salesforce.com/issue/a028c00000zKahoAAC/undefined
    """

    @retry(
        exceptions=(TableauApiTimeout,),
        max_retries=_RETRY_COUNT,
        base_ms=_RETRY_BASE_MS,
    )
    def _call(first: int, offset: int) -> dict:
        query = QUERY_TEMPLATE.format(
            resource=resource,
            fields=fields,
            first=first,
            offset=offset,
        )
        answer = server.metadata.query(query)
        _check_errors(answer)
        return answer["data"][f"{resource}Connection"]

    current_offset = 0
    while True:
        payload = _call(first=page_size, offset=current_offset)
        yield payload["nodes"]

        current_offset += len(payload["nodes"])
        total = payload["totalCount"]
        logger.info(f"Extracted {current_offset}/{total} {resource}")

        if not payload["pageInfo"]["hasNextPage"]:
            break


class TableauClientMetadataApi:
    """
    Calls the MetadataAPI, using graphQL
    https://help.tableau.com/current/api/metadata_api/en-us/reference/index.html
    """

    def __init__(
        self,
        server: TSC.Server,
        override_page_size: Optional[int] = None,
    ):
        self._server = server
        self._override_page_size = override_page_size

    def _call(
        self,
        resource: str,
        fields: str,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> SerializedAsset:
        result_pages = gql_query_scroll(
            self._server,
            resource=resource,
            fields=fields,
            page_size=page_size,
        )
        return [asset for page in result_pages for asset in page]

    def _page_size(self, asset: TableauAsset) -> int:
        return (
            self._override_page_size
            or _CUSTOM_PAGE_SIZE.get(asset)
            or DEFAULT_PAGE_SIZE
        )

    def _fetch_fields(self) -> SerializedAsset:
        result: SerializedAsset = []
        page_size = self._page_size(TableauAsset.FIELD)
        for resource, fields in FIELDS_QUERIES:
            current = self._call(resource, fields, page_size)
            result.extend(current)
        return result

    def fetch(
        self,
        asset: TableauAsset,
    ) -> SerializedAsset:
        if asset == TableauAsset.FIELD:
            return self._fetch_fields()

        page_size = self._page_size(asset)
        resource, fields = GQL_QUERIES[asset]
        return self._call(resource, fields, page_size)
