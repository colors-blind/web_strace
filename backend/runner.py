from __future__ import annotations

import asyncio
import os
import re
import shlex
import signal
from typing import AsyncIterator, Optional

STRACE_BIN = "/usr/bin/strace"

DANGEROUS_CHARS = re.compile(r"[;&|`$(){}]")
REQUIRED_FLAGS = {"-tt", "-T"}


def validate_command(command: str) -> tuple[bool, str]:
    command = command.strip()
    if not command:
        return False, "empty command"
    if len(command) > 2048:
        return False, "command too long"
    if DANGEROUS_CHARS.search(command):
        return False, "shell metacharacters not allowed"
    return True, ""


def build_strace_argv(command: str) -> list[str]:
    parts = shlex.split(command)

    if parts[0] == "strace":
        parts = parts[1:]

    flags: list[str] = []
    program_start = 0
    i = 0
    while i < len(parts):
        p = parts[i]
        if p.startswith("-"):
            flags.append(p)
            if p in ("-e", "-p", "-s", "-o", "-P", "-I"):
                i += 1
                if i < len(parts):
                    flags.append(parts[i])
        else:
            program_start = i
            break
        i += 1

    for f in REQUIRED_FLAGS:
        base = f.lstrip("-")
        if not any(base in fl for fl in flags):
            flags.append(f)

    if "-f" not in flags and "--follow-forks" not in flags:
        flags.append("-f")

    program_args = parts[program_start:]
    return [STRACE_BIN] + flags + ["--"] + program_args


class StraceRunner:
    def __init__(self):
        self._process: Optional[asyncio.subprocess.Process] = None
        self._pid: Optional[int] = None

    @property
    def is_running(self) -> bool:
        return self._process is not None and self._process.returncode is None

    async def start(self, command: str) -> AsyncIterator[str]:
        ok, err = validate_command(command)
        if not ok:
            raise ValueError(f"invalid command: {err}")

        argv = build_strace_argv(command)

        self._process = await asyncio.create_subprocess_exec(
            *argv,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._pid = self._process.pid

        assert self._process.stderr is not None
        async for raw_line in self._process.stderr:
            line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
            if line:
                yield line

    async def stop(self):
        if self._process and self._process.returncode is None:
            try:
                os.kill(self._process.pid, signal.SIGTERM)
                try:
                    await asyncio.wait_for(self._process.wait(), timeout=3.0)
                except asyncio.TimeoutError:
                    self._process.kill()
                    await self._process.wait()
            except ProcessLookupError:
                pass
        self._process = None

    async def wait(self) -> int:
        if self._process:
            return await self._process.wait()
        return -1
