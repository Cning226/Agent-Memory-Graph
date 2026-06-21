"""AgentMemGraph command-line entrypoint."""
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentmemgraph",
        description="启动 AgentMemGraph 长期记忆服务。",
    )
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", default=8080, type=int, help="监听端口")
    parser.add_argument("--reload", action="store_true", help="启用开发模式热重载")
    parser.add_argument("--log-level", default="info", help="Uvicorn 日志级别")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    import uvicorn

    uvicorn.run(
        "agentmemgraph.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
    )


if __name__ == "__main__":
    main()
