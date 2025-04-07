from typing import NamedTuple
from urllib.parse import parse_qs, urlparse


class TaskRoute(NamedTuple):
    """Task decoded route

    Args:
        NamedTuple (_type_): _description_
    """

    scheme: str  # task / lambda / etc.
    module: str  # module or lambda arn (as host)
    function: str  # function path or callable name
    query: dict  # parsed query params if any

    @classmethod
    def from_url(cls, url: str) -> "TaskRoute":
        """Create a TaskRoute from a url

        Args:
            url (str): Url to create route from

        Returns:
            TaskRoute: TaskRoute instance
        """

        parsed = urlparse(url)

        scheme = parsed.scheme  # 'task' or 'lambda'
        module = parsed.netloc  # module path or ARN
        function = parsed.path.lstrip("/")  # remove leading slash
        query = parse_qs(parsed.query)

        return TaskRoute(scheme, module, function, query)
