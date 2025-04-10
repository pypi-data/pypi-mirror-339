import httpx
from typing import Iterator, Optional
from ohttpy._generators import make_chunk_generator
from .ohttpy import Client, Response

class ResponseStream(httpx.SyncByteStream):
    """
    Class to convert a OHTTPy response into a SyncByteStream compatible with httpx.Response.
    """
    def __init__(self, response: Response):
        self._chunk_generator = make_chunk_generator(response)

    def __iter__(self) -> Iterator[bytes]:
        yield from self._chunk_generator

    def close(self) -> None:
        self._chunk_generator.close()

class Transport(httpx.BaseTransport):
    """
    Class to serve as a drop-in replacement from httpx.BaseTransport while enabling OHTTP encapsulation for all HTTP communication.
    """
    def __init__(self, key_config: Optional[bytes] = None):
        """
        Constructor.
        @param key_config Optional bytes parameter to provide the OHTTP key configuration as defined by the OHTTP RFC9458 key configuration encoding. This contains the OHTTP public key and set of algorithms for HPKE context. If not provided, the key config will be fetched dynamically from `{url.scheme}://{url.authority}/discover` endpoint for the url specified in an HTTP request.
        """
        super().__init__()
        self.client = Client()
        self.key_config = key_config


    def handle_request(self, request: httpx.Request) -> httpx.Response:
        # call binding to py OHTTPy client
        response = self.client.send_request(
            method=request.method, url=str(request.url),
            headers=dict(request.headers), body=request.content,
            key_config=self.key_config)

        # translate response into httpx compatible format
        status_code = response.status_code()
        headers = response.headers()
        stream = ResponseStream(response)

        # construct httpx response
        httpx_response = httpx.Response(
            status_code=status_code, headers=headers,
            request=request, stream=stream)

        return httpx_response
