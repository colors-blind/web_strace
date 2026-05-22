from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SyscallCategory(str, Enum):
    FILE = "file"
    IO = "io"
    NETWORK = "network"
    PROCESS = "process"
    MEMORY = "memory"
    SYNC = "sync"
    SIGNAL = "signal"
    OTHER = "other"


class Severity(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    SLOW = "slow"
    BLOCKED = "blocked"


class SyscallEvent(BaseModel):
    id: int
    pid: int
    timestamp: str
    syscall: str
    args: str
    result: str
    duration: Optional[float] = None
    category: SyscallCategory = SyscallCategory.OTHER
    severity: Severity = Severity.NORMAL


class SessionStats(BaseModel):
    total_count: int = 0
    category_counts: dict[str, int] = {}
    syscall_counts: dict[str, int] = {}
    top_slow: list[SyscallEvent] = []


class StartRequest(BaseModel):
    command: str


class SessionInfo(BaseModel):
    id: str
    command: str
    start_time: str
    end_time: Optional[str] = None
    total_syscalls: int = 0
    status: str = "running"
