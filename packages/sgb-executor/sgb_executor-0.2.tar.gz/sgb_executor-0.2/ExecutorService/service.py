import isgb

from sgb import A, Result
from sgb.consts.names import LINK
from sgb.collections import strlist
from sgb.tools import ParameterList
from ExecutorService.const import SD

from typing import Any
from subprocess import CompletedProcess

ISOLATED = False

SC = A.CT_SC


def start(as_standalone: bool = False) -> None:

    if A.U.for_service(SD, as_standalone=as_standalone):

        def service_call_handler(sc: SC | str, pl: ParameterList) -> Any:
            if sc == "execute":
                command: str | strlist = pl.values[0]

                def login_and_password_fill(value: str) -> str:
                    for item in (LINK.ADMINISTRATOR_LOGIN, LINK.ADMINISTRATOR_PASSWORD):
                        value = value.replace(
                            A.D_F.link(item),
                            A.D_V_E.value(item, False),
                        )
                    return value

                if isinstance(command, str):
                    pl.values[0] = login_and_password_fill(command)
                if isinstance(command, list):
                    pl.values[0] = A.D.map(login_and_password_fill, command)
                result: CompletedProcess = A.EXC.execute(*pl.values)
                return Result(
                    None,
                    {
                        index: item
                        for index, item in enumerate(
                            (
                                result.args,
                                result.returncode,
                                result.stdout,
                                result.stderr,
                            )
                        )
                    },
                )

        def service_starts_handler() -> None:
            pass

        A.SRV.serve(
            SD,
            service_call_handler,
            service_starts_handler,  # type: ignore
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
