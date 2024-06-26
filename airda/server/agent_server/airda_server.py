import fastapi
from overrides import overrides

from airda.server import WebFrameworkServer
from airda.server.api.api import APIImpl
from airda.server.protocol import AddDatasourceRequest, ChatCompletionRequest


class AirdaServer(WebFrameworkServer):
    def __init__(self, host="0.0.0.0", port=8888):
        super().__init__(host, port)
        self.router = None

    def init_api(self):
        return APIImpl()

    @overrides
    def create_app(self):
        return fastapi.FastAPI(debug=True)

    @overrides
    def run_server(self):
        import uvicorn

        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    @overrides
    def add_routes(self):
        self.router = fastapi.APIRouter()
        self.router.add_api_route(
            "/v1/chat/completions",
            self.create_completion,
            methods=["POST"],
            tags=["chat completions"],
        )
        self.router.add_api_route(
            "/v1/datasource/add",
            self.create_completion,
            methods=["POST"],
            tags=["datasource add"],
        )
        self.app.include_router(self.router)

    async def create_completion(self, request: ChatCompletionRequest):
        return await self._api.create_completion(request)

    def add_datasource(self, request: AddDatasourceRequest):
        return self._api.add_datasource(request)
