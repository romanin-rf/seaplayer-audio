import logging
import datetime
from rich.console import Console
from typing_extensions import Literal, Optional

# ! Main Class
class Logger:
    __level_colors__ = {
        'NOTSET': '#767676',
        'DEBUG' : 'magenta',
        'INFO': 'green',
        'WARN': 'orange1',
        'WARNING': 'italic orange1',
        'ERROR': 'red',
        'FATAL': 'italic red',
        'CRITICAL': 'italic bold red'
    }
    
    def __init__(
        self,
        level: Literal['NOTSET', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL']='NOTSET',
        format_time: str="\\[ {hour:02}:{minute:02}:{second:02} ]",
        format_log: str="{time}{level} {msg}",
        console: Optional[Console]=None
    ) -> None:
        assert level in {'NOTSET', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL'}
        self.levelname: str = level
        self.level: int = getattr(logging, self.levelname)
        self.format_time = format_time
        self.format_log = format_log
        self.console = console or Console()
    
    def __log(self, levelname: str, msg: str, with_new_line: bool):
        level = logging.getLevelNamesMapping()[levelname]
        if logging.root.manager.disable <= level:
            levelcolor = self.__level_colors__[levelname]
            dt = datetime.datetime.now()
            tt = self.format_time.format(
                year=dt.year, month=dt.month, day=dt.day,
                hour=dt.hour, minute=dt.minute, second=dt.second
            )
            if with_new_line:
                self.console.print()
            return self.console.print(
                self.format_log.format(time=tt, level=f"\\[[{levelcolor}]{levelname:^12}[/{levelcolor}]]", msg=msg)
            )
    
    def debug(self, msg: str, *, with_new_line: bool=False) -> None:
        return self.__log('DEBUG', msg, with_new_line)
    
    def info(self, msg: str, *, with_new_line: bool=False) -> None:
        return self.__log('INFO', msg, with_new_line)
    
    def warn(self, msg: str, *, with_new_line: bool=False) -> None:
        return self.__log('WARN', msg, with_new_line)
    
    def warning(self, msg: str, *, with_new_line: bool=False) -> None:
        return self.__log('WARNING', msg, with_new_line)
    
    def error(self, msg: str, *, with_new_line: bool=False) -> None:
        return self.__log('ERROR', msg, with_new_line)
    
    def fatal(self, msg: str, *, with_new_line: bool=False) -> None:
        return self.__log('FATAL', msg, with_new_line)
    
    def critical(self, msg: str, *, with_new_line: bool=False) -> None:
        return self.__log('CRITICAL', msg, with_new_line)
    
    def rule(self, title: str) -> None:
        self.console.print()
        self.console.rule(title)