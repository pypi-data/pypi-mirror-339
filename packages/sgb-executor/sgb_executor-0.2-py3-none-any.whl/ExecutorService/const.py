import isgb

from sgb.collections import strtuple
from sgb.collections.service import ServiceDescription

from sgb import A

NAME: str = "Executor"

VERSION: str = "0.02"

HOST = A.CT_H.EXECUTOR

PACKAGES: strtuple = None

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Executor",
    host_changeable=True,
    packages=PACKAGES,
    commands=(),
    version=VERSION,
    use_standalone=True,
    standalone_name="executor",
)
