from __future__ import annotations

from .models import Severity, SyscallCategory

CATEGORY_MAP: dict[str, SyscallCategory] = {
    # File
    "open": SyscallCategory.FILE,
    "openat": SyscallCategory.FILE,
    "close": SyscallCategory.FILE,
    "stat": SyscallCategory.FILE,
    "fstat": SyscallCategory.FILE,
    "lstat": SyscallCategory.FILE,
    "newfstatat": SyscallCategory.FILE,
    "statx": SyscallCategory.FILE,
    "access": SyscallCategory.FILE,
    "faccessat": SyscallCategory.FILE,
    "faccessat2": SyscallCategory.FILE,
    "rename": SyscallCategory.FILE,
    "renameat": SyscallCategory.FILE,
    "renameat2": SyscallCategory.FILE,
    "unlink": SyscallCategory.FILE,
    "unlinkat": SyscallCategory.FILE,
    "chmod": SyscallCategory.FILE,
    "fchmod": SyscallCategory.FILE,
    "chown": SyscallCategory.FILE,
    "mkdir": SyscallCategory.FILE,
    "mkdirat": SyscallCategory.FILE,
    "rmdir": SyscallCategory.FILE,
    "getcwd": SyscallCategory.FILE,
    "chdir": SyscallCategory.FILE,
    "readlink": SyscallCategory.FILE,
    "readlinkat": SyscallCategory.FILE,
    "getdents": SyscallCategory.FILE,
    "getdents64": SyscallCategory.FILE,
    "fcntl": SyscallCategory.FILE,
    "dup": SyscallCategory.FILE,
    "dup2": SyscallCategory.FILE,
    "dup3": SyscallCategory.FILE,
    "pipe": SyscallCategory.FILE,
    "pipe2": SyscallCategory.FILE,
    # IO
    "read": SyscallCategory.IO,
    "write": SyscallCategory.IO,
    "pread64": SyscallCategory.IO,
    "pwrite64": SyscallCategory.IO,
    "readv": SyscallCategory.IO,
    "writev": SyscallCategory.IO,
    "sendfile": SyscallCategory.IO,
    "lseek": SyscallCategory.IO,
    "ioctl": SyscallCategory.IO,
    # Network
    "socket": SyscallCategory.NETWORK,
    "connect": SyscallCategory.NETWORK,
    "bind": SyscallCategory.NETWORK,
    "listen": SyscallCategory.NETWORK,
    "accept": SyscallCategory.NETWORK,
    "accept4": SyscallCategory.NETWORK,
    "send": SyscallCategory.NETWORK,
    "sendto": SyscallCategory.NETWORK,
    "sendmsg": SyscallCategory.NETWORK,
    "recv": SyscallCategory.NETWORK,
    "recvfrom": SyscallCategory.NETWORK,
    "recvmsg": SyscallCategory.NETWORK,
    "shutdown": SyscallCategory.NETWORK,
    "getsockname": SyscallCategory.NETWORK,
    "getpeername": SyscallCategory.NETWORK,
    "setsockopt": SyscallCategory.NETWORK,
    "getsockopt": SyscallCategory.NETWORK,
    # Process
    "fork": SyscallCategory.PROCESS,
    "vfork": SyscallCategory.PROCESS,
    "clone": SyscallCategory.PROCESS,
    "clone3": SyscallCategory.PROCESS,
    "execve": SyscallCategory.PROCESS,
    "execveat": SyscallCategory.PROCESS,
    "wait4": SyscallCategory.PROCESS,
    "waitid": SyscallCategory.PROCESS,
    "exit_group": SyscallCategory.PROCESS,
    "exit": SyscallCategory.PROCESS,
    "getpid": SyscallCategory.PROCESS,
    "getppid": SyscallCategory.PROCESS,
    "gettid": SyscallCategory.PROCESS,
    "set_tid_address": SyscallCategory.PROCESS,
    "prctl": SyscallCategory.PROCESS,
    "arch_prctl": SyscallCategory.PROCESS,
    "set_robust_list": SyscallCategory.PROCESS,
    "sched_getaffinity": SyscallCategory.PROCESS,
    "sched_yield": SyscallCategory.PROCESS,
    # Memory
    "mmap": SyscallCategory.MEMORY,
    "munmap": SyscallCategory.MEMORY,
    "mprotect": SyscallCategory.MEMORY,
    "brk": SyscallCategory.MEMORY,
    "mremap": SyscallCategory.MEMORY,
    "madvise": SyscallCategory.MEMORY,
    "msync": SyscallCategory.MEMORY,
    "mincore": SyscallCategory.MEMORY,
    # Sync / Blocking
    "futex": SyscallCategory.SYNC,
    "epoll_wait": SyscallCategory.SYNC,
    "epoll_pwait": SyscallCategory.SYNC,
    "epoll_create": SyscallCategory.SYNC,
    "epoll_create1": SyscallCategory.SYNC,
    "epoll_ctl": SyscallCategory.SYNC,
    "poll": SyscallCategory.SYNC,
    "ppoll": SyscallCategory.SYNC,
    "select": SyscallCategory.SYNC,
    "pselect6": SyscallCategory.SYNC,
    "nanosleep": SyscallCategory.SYNC,
    "clock_nanosleep": SyscallCategory.SYNC,
    "eventfd": SyscallCategory.SYNC,
    "eventfd2": SyscallCategory.SYNC,
    # Signal
    "rt_sigaction": SyscallCategory.SIGNAL,
    "rt_sigprocmask": SyscallCategory.SIGNAL,
    "rt_sigreturn": SyscallCategory.SIGNAL,
    "sigaltstack": SyscallCategory.SIGNAL,
    "kill": SyscallCategory.SIGNAL,
    "tgkill": SyscallCategory.SIGNAL,
    "tkill": SyscallCategory.SIGNAL,
}

SEVERITY_THRESHOLDS = [
    (1.0, Severity.BLOCKED),
    (0.1, Severity.SLOW),
    (0.01, Severity.WARNING),
]


def classify_syscall(name: str) -> SyscallCategory:
    return CATEGORY_MAP.get(name, SyscallCategory.OTHER)


def assess_severity(duration: float | None) -> Severity:
    if duration is None:
        return Severity.NORMAL
    for threshold, severity in SEVERITY_THRESHOLDS:
        if duration >= threshold:
            return severity
    return Severity.NORMAL
