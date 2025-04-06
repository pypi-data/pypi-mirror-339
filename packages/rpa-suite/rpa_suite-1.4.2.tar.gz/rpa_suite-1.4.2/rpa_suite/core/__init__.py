# rpa_suite/core/__init__.py

"""
The Core module is where we can import all Sub-Objects used by the rpa_suite module separately, categorized by their respective classes based on functionality. However, we can also use them through the main rpa object using the following syntax:
>>> from rpa_suite import rpa
>>> rpa.clock.wait_for_exec()
>>> rpa.file.screen_shot() ...
among others.

pt-br
----------
O módulo Core é de onde podemos importar todos os Sub-Objetos usados pelo módulo rpa_suite de forma separada, categorizados por suas respectivas classes com base na funcionalidade. No entanto, também podemos usá-los através do objeto principal rpa usando a seguinte sintaxe:
>>> from rpa_suite import rpa
>>> rpa.clock.wait_for_exec()
>>> rpa.file.screen_shot() ...
entre outros.

"""
from .clock import Clock
from .date import Date
from .dir import Directory
from .email import Email
from .file import File
from .log import Log
from .print import Print
from .regex import Regex
from .validate import Validate
