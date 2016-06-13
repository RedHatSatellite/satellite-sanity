#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import sat6_hw_reqs

CPUINFO_CORRECT = """processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 63
model name	: Intel(R) Xeon(R) CPU E5-2640 v3 @ 2.60GHz
stepping	: 2
microcode	: 45
cpu MHz		: 2600.004
cache size	: 20480 KB
physical id	: 0
siblings	: 16
core id		: 0
cpu cores	: 8
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 15
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm ida arat epb xsaveopt pln pts dts tpr_shadow vnmi flexpriority ept vpid fsgsbase bmi1 avx2 smep bmi2 erms invpcid
bogomips	: 5200.00
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:

processor	: 1
vendor_id	: GenuineIntel
cpu family	: 6
model		: 63
model name	: Intel(R) Xeon(R) CPU E5-2640 v3 @ 2.60GHz
stepping	: 2
microcode	: 45
cpu MHz		: 2600.004
cache size	: 20480 KB
physical id	: 0
siblings	: 16
core id		: 1
cpu cores	: 8
apicid		: 2
initial apicid	: 2
fpu		: yes
fpu_exception	: yes
cpuid level	: 15
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm ida arat epb xsaveopt pln pts dts tpr_shadow vnmi flexpriority ept vpid fsgsbase bmi1 avx2 smep bmi2 erms invpcid
bogomips	: 5200.00
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:

processor	: 2
vendor_id	: GenuineIntel
cpu family	: 6
model		: 63
model name	: Intel(R) Xeon(R) CPU E5-2640 v3 @ 2.60GHz
stepping	: 2
microcode	: 45
cpu MHz		: 2600.004
cache size	: 20480 KB
physical id	: 0
siblings	: 16
core id		: 2
cpu cores	: 8
apicid		: 4
initial apicid	: 4
fpu		: yes
fpu_exception	: yes
cpuid level	: 15
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm ida arat epb xsaveopt pln pts dts tpr_shadow vnmi flexpriority ept vpid fsgsbase bmi1 avx2 smep bmi2 erms invpcid
bogomips	: 5200.00
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:

processor	: 3
vendor_id	: GenuineIntel
cpu family	: 6
model		: 63
model name	: Intel(R) Xeon(R) CPU E5-2640 v3 @ 2.60GHz
stepping	: 2
microcode	: 45
cpu MHz		: 2600.004
cache size	: 20480 KB
physical id	: 0
siblings	: 16
core id		: 3
cpu cores	: 8
apicid		: 6
initial apicid	: 6
fpu		: yes
fpu_exception	: yes
cpuid level	: 15
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm ida arat epb xsaveopt pln pts dts tpr_shadow vnmi flexpriority ept vpid fsgsbase bmi1 avx2 smep bmi2 erms invpcid
bogomips	: 5200.00
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:""".split("\n")
CPUINFO_WRONG = """processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 13
model name	: Intel(R) Pentium(R) M processor 1.60GHz
stepping	: 6
cpu MHz		: 1594.879
cache size	: 2048 KB
fdiv_bug	: no
hlt_bug		: no
f00f_bug	: no
coma_bug	: no
fpu		: yes
fpu_exception	: yes
cpuid level	: 2
wp		: yes
flags		: fpu vme de pse tsc msr mce cx8 apic mtrr pge mca cmov pat clflush dts acpi mmx fxsr sse sse2 ss tm pbe up est tm2
bogomips	: 3189.75""".split("\n")

MEMINFO_CORRECT = """MemTotal:       32765636 kB
MemFree:        20927108 kB
Buffers:          468912 kB
Cached:          6015312 kB
SwapCached:            0 kB
Active:          7388452 kB
Inactive:        3262356 kB
Active(anon):    4168592 kB
Inactive(anon):      260 kB
Active(file):    3219860 kB
Inactive(file):  3262096 kB
Unevictable:        1804 kB
Mlocked:               0 kB
SwapTotal:      16457724 kB
SwapFree:       16457724 kB
Dirty:               148 kB
Writeback:             0 kB
AnonPages:       4168424 kB
Mapped:            48456 kB
Shmem:               460 kB
Slab:             872564 kB
SReclaimable:     743312 kB
SUnreclaim:       129252 kB
KernelStack:       10928 kB
PageTables:        25704 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    32840540 kB
Committed_AS:    4348320 kB
VmallocTotal:   34359738367 kB
VmallocUsed:      382156 kB
VmallocChunk:   34359339696 kB
HardwareCorrupted:     0 kB
AnonHugePages:   3688448 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:        7168 kB
DirectMap2M:     2015232 kB
DirectMap1G:    31457280 kB""".split("\n")
MEMINFO_WRONG = """MemTotal:      2075004 kB
MemFree:        573152 kB
Buffers:        238388 kB
Cached:         908372 kB
SwapCached:          0 kB
Active:         899384 kB
Inactive:       531556 kB
HighTotal:     1179584 kB
HighFree:       127448 kB
LowTotal:       895420 kB
LowFree:        445704 kB
SwapTotal:     1020116 kB
SwapFree:      1020116 kB
Dirty:              20 kB
Writeback:           0 kB
AnonPages:      284208 kB
Mapped:          59524 kB
Slab:            58980 kB
PageTables:       5080 kB
NFS_Unstable:        0 kB
Bounce:              0 kB
CommitLimit:   2057616 kB
Committed_AS:   931932 kB
VmallocTotal:   114680 kB
VmallocUsed:      4404 kB
VmallocChunk:   110068 kB
HugePages_Total:     0
HugePages_Free:      0
HugePages_Rsvd:      0
Hugepagesize:     4096 kB""".split("\n")


class TestSat6HWReqs(unittest.TestCase):

    def test_cpu_cores(self):
        input_data = {'proc_cpuinfo': CPUINFO_CORRECT}
        self.assertEquals(4, sat6_hw_reqs.cpu_cores(input_data))
        input_data = {'proc_cpuinfo': CPUINFO_WRONG}
        self.assertEquals(1, sat6_hw_reqs.cpu_cores(input_data))

    def test_ram_size(self):
        input_data = {'proc_meminfo': MEMINFO_CORRECT}
        self.assertEquals(32765636, sat6_hw_reqs.ram_size(input_data))
        input_data = {'proc_meminfo': MEMINFO_WRONG}
        self.assertEquals(2075004, sat6_hw_reqs.ram_size(input_data))

    def test_swap_size(self):
        input_data = {'proc_meminfo': MEMINFO_CORRECT}
        self.assertEquals(16457724, sat6_hw_reqs.swap_size(input_data))
        input_data = {'proc_meminfo': MEMINFO_WRONG}
        self.assertEquals(1020116, sat6_hw_reqs.swap_size(input_data))

    def test_main_nomatch(self):
        input_data = {}
        input_data['proc_cpuinfo'] = CPUINFO_CORRECT
        input_data['proc_meminfo'] = MEMINFO_CORRECT
        self.assertEquals(None, sat6_hw_reqs.main(input_data))

    def test_main_match_cpu(self):
        input_data = {}
        input_data['proc_cpuinfo'] = CPUINFO_WRONG
        input_data['proc_meminfo'] = MEMINFO_CORRECT
        expected = {'errors': [
            '1 CPU cores is below minimal requirement of 2',
        ]}
        self.assertEquals(expected, sat6_hw_reqs.main(input_data))

    def test_main_match_ram_swap(self):
        input_data = {}
        input_data['proc_cpuinfo'] = CPUINFO_CORRECT
        input_data['proc_meminfo'] = MEMINFO_WRONG
        expected = {'errors': [
            'RAM size 2075004 kB is below minimal requirement of 12582912 kB',
            'Swap size 1020116 kB is below minimal requirement of 4194304 kB',
        ]}
        self.assertEquals(expected, sat6_hw_reqs.main(input_data))

    def test_main_match_all(self):
        input_data = {}
        input_data['proc_cpuinfo'] = CPUINFO_WRONG
        input_data['proc_meminfo'] = MEMINFO_WRONG
        expected = {'errors': [
            '1 CPU cores is below minimal requirement of 2',
            'RAM size 2075004 kB is below minimal requirement of 12582912 kB',
            'Swap size 1020116 kB is below minimal requirement of 4194304 kB',
        ]}
        self.assertEquals(expected, sat6_hw_reqs.main(input_data))
