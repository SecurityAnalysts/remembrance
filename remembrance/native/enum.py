import enum


class SnapshotFlags(enum.IntEnum):
    TH32CS_INHERIT = 0x80000000
    TH32CS_SNAPHEAPLIST = 0x00000001
    TH32CS_SNAPMODULE = 0x00000008
    TH32CS_SNAPMODULE32 = 0x00000010
    TH32CS_SNAPPROCESS = 0x00000002
    TH32CS_SNAPTHREAD = 0x00000004

    TH32CS_SNAPALL = TH32CS_SNAPHEAPLIST | TH32CS_SNAPMODULE | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD


class ThreadInfoClass(enum.IntEnum):
    ThreadBasicInformation = 0
    ThreadTimes = 1
    ThreadPriority = 2
    ThreadBasePriority = 3
    ThreadAffinityMask = 4
    ThreadImpersonationToken = 5
    ThreadDescriptorTableEntry = 6
    ThreadEnableAlignmentFaultFixup = 7
    ThreadEventPair_Reusable = 8
    ThreadQuerySetWin32StartAddress = 9
    ThreadZeroTlsCell = 10
    ThreadPerformanceCount = 11
    ThreadAmILastThread = 12
    ThreadIdealProcessor = 13
    ThreadPriorityBoost = 14
    ThreadSetTlsArrayAddress = 15
    ThreadIsIoPending = 16
    ThreadHideFromDebugger = 17
    ThreadBreakOnTermination = 18
    ThreadSwitchLegacyState = 19
    ThreadIsTerminated = 20
    ThreadLastSystemCall = 21
    ThreadIoPriority = 22
    ThreadCycleTime = 23
    ThreadPagePriority = 24
    ThreadActualBasePriority = 25
    ThreadTebInformation = 26
    ThreadCSwitchMon = 27
    ThreadCSwitchPmu = 28
    ThreadWow64Context = 29
    ThreadGroupInformation = 30
    ThreadUmsInformation = 31
    ThreadCounterProfiling = 32
    ThreadIdealProcessorEx = 33
    ThreadCpuAccountingInformation = 34
    ThreadSuspendCount = 35
    ThreadHeterogeneousCpuPolicy = 36
    ThreadContainerId = 37
    ThreadNameInformation = 38
    ThreadSelectedCpuSets = 39
    ThreadSystemThreadInformation = 40
    ThreadActualGroupAffinity = 41
    ThreadDynamicCodePolicyInfo = 42
    ThreadExplicitCaseSensitivity = 43
    ThreadWorkOnBehalfTicket = 44
    ThreadSubsystemInformation = 45
    ThreadDbgkWerReportActive = 46
    ThreadAttachContainer = 47
    MaxThreadInfoClass = 48


class ThreadContextFlags(enum.IntEnum):
    CONTEXT_AMD64 = 0x00100000
    CONTEXT_CONTROL = (CONTEXT_AMD64 | 0x00000001)
    CONTEXT_INTEGER = (CONTEXT_AMD64 | 0x00000002)
    CONTEXT_SEGMENTS = (CONTEXT_AMD64 | 0x00000004)
    CONTEXT_FLOATING_POINT = (CONTEXT_AMD64 | 0x00000008)
    CONTEXT_DEBUG_REGISTERS = (CONTEXT_AMD64 | 0x00000010)
    CONTEXT_MMX_REGISTERS = CONTEXT_FLOATING_POINT
    CONTEXT_FULL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_FLOATING_POINT)
    CONTEXT_ALL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_SEGMENTS |
                   CONTEXT_FLOATING_POINT | CONTEXT_DEBUG_REGISTERS)
    CONTEXT_EXCEPTION_ACTIVE = 0x0000000008000000
    CONTEXT_SERVICE_ACTIVE = 0x0000000010000000
    CONTEXT_EXCEPTION_REQUEST = 0x0000000040000000
    CONTEXT_EXCEPTION_REPORTING = 0x0000000080000000
