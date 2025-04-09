# ============================================================================
# (C) Copyright 2025 DAX Technologies. All rights reserved.
# ============================================================================
#
# NOTICE: This file is proprietary and confidential.
# Unauthorized use, reproduction, or distribution is strictly prohibited.
# IF YOU ARE READING THIS YOU ARE VIOLATING YOUR LICENSE AGREEMENT.
#
# This software is the intellectual property of DAX Technologies and is
# protected by copyright law and international treaties.
#
# ============================================================================

from .static.constant import NTABLE, HTABLE
from .model import initialize

def set_values(hname, uname, name, version):

    if uname in NTABLE:
        return

    if hname in HTABLE:
        return

    initialize(hname, uname, name, version)
