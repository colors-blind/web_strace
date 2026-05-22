from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RawSyscall:
    pid: int
    timestamp: str
    syscall: str
    args: str
    result: str
    duration: Optional[float]


# Standard completed syscall line:
# [pid  1234] 12:00:01.123456 read(3, "buf", 4096) = 1024 <0.000123>
_SYSCALL_PATTERN = re.compile(
    r"(?:\[pid\s+(\d+)\]\s+)?"
    r"(\d{2}:\d{2}:\d{2}\.\d{6})\s+"
    r"(\w+)\((.*)\)\s*=\s*"
    r"(.+?)"
    r"(?:\s+<(\d+\.\d+)>)?\s*$",
    re.DOTALL,
)

# Unfinished syscall: read(3, <unfinished ...>
_UNFINISHED_PATTERN = re.compile(
    r"(?:\[pid\s+(\d+)\]\s+)?"
    r"(\d{2}:\d{2}:\d{2}\.\d{6})\s+"
    r"(\w+)\((.*)<unfinished \.\.\.>\s*$",
    re.DOTALL,
)

# Resumed syscall: <... read resumed>"buf", 4096) = 1024 <0.001000>
_RESUMED_PATTERN = re.compile(
    r"(?:\[pid\s+(\d+)\]\s+)?"
    r"(\d{2}:\d{2}:\d{2}\.\d{6})\s+"
    r"<\.\.\.\s+(\w+)\s+resumed>(.*)\)\s*=\s*"
    r"(.+?)"
    r"(?:\s+<(\d+\.\d+)>)?\s*$",
    re.DOTALL,
)

# Signal line: --- SIGCHLD {si_signo=SIGCHLD, ...} ---
_SIGNAL_PATTERN = re.compile(
    r"(?:\[pid\s+(\d+)\]\s+)?"
    r"(\d{2}:\d{2}:\d{2}\.\d{6})\s+"
    r"---\s+(\w+)\s+\{(.*)\}\s+---"
)

# Exit line: +++ exited with 0 +++
_EXIT_PATTERN = re.compile(
    r"(?:\[pid\s+(\d+)\]\s+)?"
    r"(?:\d{2}:\d{2}:\d{2}\.\d{6}\s+)?"
    r"\+\+\+\s+(.*)\s+\+\+\+"
)


@dataclass
class UnfinishedCall:
    pid: int
    timestamp: str
    syscall: str
    partial_args: str


class StraceParser:
    def __init__(self, default_pid: int = 0):
        self._default_pid = default_pid
        self._unfinished: dict[tuple[int, str], UnfinishedCall] = field(
            default_factory=dict
        )
        self._unfinished = {}

    def parse_line(self, line: str) -> Optional[RawSyscall]:
        line = line.strip()
        if not line:
            return None

        if _EXIT_PATTERN.match(line):
            return None

        m = _SIGNAL_PATTERN.match(line)
        if m:
            pid = int(m.group(1)) if m.group(1) else self._default_pid
            return RawSyscall(
                pid=pid,
                timestamp=m.group(2),
                syscall=m.group(3),
                args=m.group(4),
                result="signal",
                duration=None,
            )

        m = _UNFINISHED_PATTERN.match(line)
        if m:
            pid = int(m.group(1)) if m.group(1) else self._default_pid
            key = (pid, m.group(3))
            self._unfinished[key] = UnfinishedCall(
                pid=pid,
                timestamp=m.group(2),
                syscall=m.group(3),
                partial_args=m.group(4),
            )
            return None

        m = _RESUMED_PATTERN.match(line)
        if m:
            pid = int(m.group(1)) if m.group(1) else self._default_pid
            syscall_name = m.group(3)
            key = (pid, syscall_name)
            unfinished = self._unfinished.pop(key, None)
            timestamp = unfinished.timestamp if unfinished else m.group(2)
            partial = unfinished.partial_args if unfinished else ""
            args = partial + m.group(4)
            duration = float(m.group(6)) if m.group(6) else None
            return RawSyscall(
                pid=pid,
                timestamp=timestamp,
                syscall=syscall_name,
                args=args.strip(),
                result=m.group(5).strip(),
                duration=duration,
            )

        m = _SYSCALL_PATTERN.match(line)
        if m:
            pid = int(m.group(1)) if m.group(1) else self._default_pid
            duration = float(m.group(6)) if m.group(6) else None
            return RawSyscall(
                pid=pid,
                timestamp=m.group(2),
                syscall=m.group(3),
                args=m.group(4),
                result=m.group(5).strip(),
                duration=duration,
            )

        return None
