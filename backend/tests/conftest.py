import pytest
import asyncio
from typing import Generator

# Scope must matched the asyncio_default_fixture_loop_scope in pyproject.toml
@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
