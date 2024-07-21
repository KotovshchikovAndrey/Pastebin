from adapters.transport.grpc.client import GrpcAsyncClient
from adapters.transport.grpc.proto.py import slug_service_pb2, slug_service_pb2_grpc
from domain.ports.slug import ISlugProvider, Slug


class SlugGrpcProvider(ISlugProvider):
    _stub: slug_service_pb2_grpc.SlugServiceStub

    def __init__(self, client: GrpcAsyncClient) -> None:
        self._stub = slug_service_pb2_grpc.SlugServiceStub(client.get_channel())

    async def get_unique_slug(self) -> Slug:
        response = await self._stub.GetUniqueSlug(slug_service_pb2.Void())
        return response.slug

    async def release_slug(self, slug: Slug) -> None:
        await self._stub.ReleaseSlug(slug_service_pb2.Slug(slug=slug))
