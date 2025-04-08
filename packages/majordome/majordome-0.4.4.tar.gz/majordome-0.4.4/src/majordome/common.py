# -*- coding: utf-8 -*-
from textwrap import dedent

T_REFERENCE = 298.15
""" Thermodynamic reference temperature [K]. """

T_NORMAL = 273.15
""" Normal state reference temperature [K]. """

P_NORMAL = 101325.0
""" Normal state reference temperature [K]. """

CompositionType = str | dict[str, float]
""" Input type for Cantera composition dictionaries. """


def report_title(title: str, report: str) -> str:
    """ Generate a text report with a underscored title. """
    return dedent(f"""\n{title}\n{len(title) * "-"}\n""") + report
