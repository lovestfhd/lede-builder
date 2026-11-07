#!/usr/bin/env python3
"""Fail closed unless the generated LEDE config selects only the custom board."""
import pathlib
import re
import sys

config = pathlib.Path(sys.argv[1]).read_text()
expected = "CONFIG_TARGET_DEVICE_qualcommax_ipq807x_DEVICE_tplink_tl-er2260t"
required = {
    "CONFIG_TARGET_qualcommax",
    "CONFIG_TARGET_qualcommax_ipq807x",
    "CONFIG_TARGET_MULTI_PROFILE",
    expected,
}
enabled = set(re.findall(r"^(CONFIG_[^=\s]+)=y$", config, re.M))
profiles = {symbol for symbol in enabled if symbol.startswith("CONFIG_TARGET_DEVICE_")}
missing = required - enabled
if missing or profiles != {expected} or "CONFIG_TARGET_ALL_PROFILES" in enabled:
    sys.exit(f"Unsafe target configuration: missing={sorted(missing)}, profiles={sorted(profiles)}")
print("Verified: exactly one custom board profile enabled.")
