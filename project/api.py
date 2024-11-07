from ninja.pagination import RouterPaginated
from ninja import NinjaAPI
from common.utils.auth import AuthBearer
from common.utils.import_api_routes import import_api_routes


api = NinjaAPI(
    auth=AuthBearer(),
    title="API Docs",
    urls_namespace="api",
    default_router=RouterPaginated()
)


api = import_api_routes(api)
