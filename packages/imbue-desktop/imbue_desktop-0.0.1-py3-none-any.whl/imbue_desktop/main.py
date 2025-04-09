from imbue_core import async_monkey_patches

async_monkey_patches.apply()

import atexit
import signal
import subprocess
import sys
import urllib.parse
from typing import Annotated
from typing import Any
from typing import Optional

import typer

from imbue_desktop.qt import ImbueApplication
from imbue_desktop.utils import get_api_key_from_imbue_toml
from imbue_desktop.utils import get_url_from_imbue_toml

_APP: Any = None


def _main(
    sync_local_repo_path: str,
    server_url: Annotated[Optional[str], typer.Argument()] = None,
    api_key: Optional[str] = None,
) -> None:
    global _APP, _IS_SHUTTING_DOWN_FROM_SIGNAL

    if api_key is None:
        api_key = get_api_key_from_imbue_toml()

    if server_url is None:
        server_url = get_url_from_imbue_toml()

    # Trim the path. E.g. "https://foo.modal.host/dev" -> "https://foo.modal.host".
    parsed = urllib.parse.urlparse(server_url)
    server_url_trimmed = parsed.scheme + "://" + parsed.netloc

    local_sync_process = subprocess.Popen(
        ["uv", "run", "imbue-local-sync", sync_local_repo_path, server_url_trimmed, "--api-key", api_key]
    )
    atexit.register(local_sync_process.terminate)

    _APP = ImbueApplication(sys.argv, server_url=server_url, api_key=api_key)
    _APP.register_signal_handler(signal.SIGINT, _signal_handler)
    result = _APP.exec()
    if _IS_SHUTTING_DOWN_FROM_SIGNAL:
        sys.exit(130)
    else:
        sys.exit(result)


_IS_SHUTTING_DOWN_FROM_SIGNAL = False


def _signal_handler(_signal, _frame) -> None:
    global _IS_SHUTTING_DOWN_FROM_SIGNAL, _APP
    _IS_SHUTTING_DOWN_FROM_SIGNAL = True
    _APP.quit()


# Another level of nesting to make this work as a "pyproject script".
def main() -> None:
    typer.run(_main)


if __name__ == "__main__":
    main()
