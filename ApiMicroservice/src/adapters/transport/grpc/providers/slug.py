import grpc
from domain.ports.slug import ISlugProvider, Slug
from adapters.transport.grpc.proto.py import slug_service_pb2, slug_service_pb2_grpc


class SlugGrpcProvider(ISlugProvider):
    _stub: slug_service_pb2_grpc.SlugServiceStub

    def __init__(self, channel: grpc.aio.Channel) -> None:
        self._stub = slug_service_pb2_grpc.SlugServiceStub(channel)

    async def get_unique_slug(self) -> Slug:
        response = await self._stub.GetUniqueSlug(slug_service_pb2.Void())
        return response.slug

    async def release_slug(self, slug: Slug) -> None:
        await self._stub.ReleaseSlug(slug_service_pb2.Slug(slug=slug))
