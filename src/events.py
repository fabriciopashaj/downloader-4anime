from typing import Callable, Union

class EventEmitter(object):
    def __init__(self, events: list[str] = []):
        self.__events = dict(((e, []) for e in events))
    def on(self, event, handler: Callable):
        if event not in self:
            self.__events[event] = [handler]
        else:
            self.__events[event].append(handler)
    def emit(self, event: str, *argv, **kwargv) -> bool:
        if event not in self:
            return False
        else:
            for h in self.__events[event]:
                h(*argv, **kwargv);
            return True
    def __contains__(self, event: str) -> bool:
        return event in self.__events
    def __getitem__(self, event: Union[str, tuple[str, int]]) -> Union[Callable, list[Callable], None]:
        if isinstance(event, str):
            return self.__events[event] if event in self else []
        elif isinstance(event, tuple):
            if event[0] not in self:
                return None
            else:
                return self[event[0]][event[1]] if event[1] < len(self) else None
        else:
            return None
    def __len__(self) -> int:
        return len(self.__events)
