from abc import abstractmethod


class BaseInAgentClient:
    def __init__(self): ...

    @abstractmethod
    async def start_listen(self) -> bool: ...

    # 3N: [T] - Уведомление об одобрении запроса на сделку
    @abstractmethod
    async def request_accepted_notify(self) -> int: ...  # id
