import uvicorn

from core.factory.builders import build_app
from core.settings import settings

app = build_app()


def main() -> None:
    uvicorn.run(
        app="main:app",
        host=format(settings.server.host, "s"),
        port=settings.server.port,
        reload=settings.server.reload,
        workers=settings.server.workers,
    )


if __name__ == "__main__":
    main()
