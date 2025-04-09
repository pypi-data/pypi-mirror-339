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

from ._version import __name__
from ._version import __version__
from dax_client.internal import schema

schema.init(__name__, __version__)
