import asyncio

from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import StreamDataReceived


class SimpleQuicServerProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            data = event.data.decode()
            print(f"[server] recv: {data}")
            print(f"stream_id:{event.stream_id}")

            # 回一个响应
            self._quic.send_stream_data(
                event.stream_id,
                b"hello from server",
                end_stream=True,
            )
            self.transmit()


async def main():
    config = QuicConfiguration(
        is_client=False,
        alpn_protocols=["hq-29"],
    )
    config.load_cert_chain("certs/cert.pem", "certs/key.pem")

    await serve(
        host="0.0.0.0",
        port=4433,
        configuration=config,
        create_protocol=SimpleQuicServerProtocol,
    )

    print("[server] QUIC server listening on 4433")
    await asyncio.Future()  # 永远不退出


if __name__ == "__main__":
    asyncio.run(main())
