import asyncio

from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import StreamDataReceived


class SimpleQuicClientProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            print(f"[client] recv: {event.data.decode()}")


async def main():
    config = QuicConfiguration(
        is_client=True,
        alpn_protocols=["hq-29"],
        verify_mode=False,  # 忽略自签名证书
    )

    async with connect(
        "127.0.0.1",
        4433,
        configuration=config,
        create_protocol=SimpleQuicClientProtocol,
    ) as protocol:
        stream_id = protocol._quic.get_next_available_stream_id()
        protocol._quic.send_stream_data(
            stream_id,
            b"hello from client",
            end_stream=True,
        )
        protocol.transmit()

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
