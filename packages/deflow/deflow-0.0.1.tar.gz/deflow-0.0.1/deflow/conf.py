# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

PREFIX: str = "DEFLOW"


def env(
    var: str, default: Optional[str] = None
) -> Optional[str]:  # pragma: no cov
    return os.getenv(f"{PREFIX}_{var.upper().replace(' ', '_')}", default)


class Config:

    @property
    def root_path(self) -> Path:
        return Path(env("CORE_ROOT_PATH", "."))

    @property
    def conf_path(self) -> Path:
        return self.root_path / env("CORE_CONF_PATH", "conf")


config = Config()
