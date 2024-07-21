import grpc


class GrpcAsyncClient:
    _channel: grpc.aio.Channel

    def __init__(self, grpc_channel_address: str) -> None:
        self._channel = grpc.aio.insecure_channel(
            target=grpc_channel_address,
            options=[
                ("grpc.enable_retries", 3),
            ],
        )

    async def close(self) -> None:
        await self._channel.close()

    def get_channel(self):
        return self._channel
