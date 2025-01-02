from fastapi import Request

from src.logger import RequestSpan


def span(request: Request) -> RequestSpan:
    return request.state.span


def state(request: Request):
    return request.state.app_state


def leaky_url(request: Request) -> str:
    return request.state.app_state.config.leaky_url
