import grpc
from proto.py import slug_service_pb2, slug_service_pb2_grpc
from services.slug import SlugService


class SlugGrpcController(slug_service_pb2_grpc.SlugServiceServicer):
    _service: SlugService

    def __init__(self, service: SlugService) -> None:
        super().__init__()
        self._service = service

    async def GetUniqueSlug(
        self,
        request: slug_service_pb2.Void,
        context: grpc.aio.ServicerContext,
    ):
        slug = await self._service.get_unique_slug()
        return slug_service_pb2.Slug(slug=slug)

    async def ReleaseSlug(
        self,
        request: slug_service_pb2.Slug,
        context: grpc.aio.ServicerContext,
    ):
        await self._service.release_slug(slug=request.slug)
        return slug_service_pb2.Void()
