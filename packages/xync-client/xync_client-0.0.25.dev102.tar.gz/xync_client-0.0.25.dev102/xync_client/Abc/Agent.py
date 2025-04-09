from abc import abstractmethod

from pydantic import BaseModel
from xync_schema import models
from xync_schema.models import OrderStatus, Coin, Cur, Ad, AdStatus, Agent, Cred, PmexBank
from xync_schema.types import BaseAd, AdSaleIn, AdBuyIn, BaseOrder

from xync_client.Abc.Ex import BaseExClient
from xync_client.Abc.Base import BaseClient


class BaseAgentClient(BaseClient):
    def __init__(self, agent: Agent):
        self.agent: Agent = agent
        super().__init__(self.agent.actor.ex)  # , "host_p2p"
        self.ex_client: BaseExClient = self.ex.client()

    # 0: Получшение ордеров в статусе status, по монете coin, в валюте coin, в направлении is_sell: bool
    @abstractmethod
    async def get_orders(
        self, status: OrderStatus = OrderStatus.created, coin: Coin = None, cur: Cur = None, is_sell: bool = None
    ) -> list: ...

    # 1: [T] Запрос на старт сделки
    @abstractmethod
    async def order_request(self, order: BaseOrder) -> dict: ...

    # async def start_order(self, order: Order) -> OrderOutClient:
    #     return OrderOutClient(self, order)

    # 1N: [M] - Запрос мейкеру на сделку
    @abstractmethod
    async def order_request_ask(self) -> dict: ...  # , ad: Ad, amount: float, pm: Pm, taker: Agent

    # 2N: [M] - Уведомление об отмене запроса на сделку
    @abstractmethod
    async def request_canceled_notify(self) -> int: ...  # id

    # # # Cred
    @property
    @abstractmethod
    def fiat_pyd(self) -> BaseModel.__class__: ...

    @abstractmethod
    def fiat_args2pyd(
        self, exid: int | str, cur: str, detail: str, name: str, fid: int, typ: str, extra=None
    ) -> fiat_pyd: ...

    # 25: Список реквизитов моих платежных методов
    @abstractmethod
    async def creds(self) -> list: ...  # {fiat.exid: {fiat}}

    # Создание реквизита на бирже
    async def fiat_new(self, cred: models.Cred) -> models.Cred:
        await models.Actor.get_or_create({"name": cred.exid}, ex=self.ex_client.ex, exid=self.agent.actor.exid)
        CredIn()
        fiat_db: Cred = (await self.fiat_pyd2db(fiat, self.agent.user_id))[0]
        if not (fiatex := models.CredEx.get_or_none(fiat=fiat_db, ex=self.agent.ex)):
            fiatex, _ = models.CredEx.update_or_create({}, fiat=fiat_db, ex=self.agent.ex)
        return fiatex

    # 27: Редактирование реквизита моего платежного метода
    @abstractmethod
    async def fiat_upd(self, fiat_id: int, detail: str, name: str = None) -> Cred: ...

    # 28: Удаление реквизита моего платежного метода
    @abstractmethod
    async def fiat_del(self, fiat_id: int) -> bool: ...

    # # # Ad
    # 29: Список моих объявлений
    @abstractmethod
    async def my_ads(self, status: AdStatus = None) -> list[BaseAd]: ...

    # 30: Создание объявления
    @abstractmethod
    async def ad_new(self, ad: BaseAd) -> Ad: ...

    # 31: Редактирование объявления
    @abstractmethod
    async def ad_upd(
        self,
        offer_id: int,
        amount: int,
        fiats: list[Cred] = None,
        price: float = None,
        is_float: bool = None,
        min_fiat: int = None,
        details: str = None,
        autoreply: str = None,
        status: AdStatus = None,
    ) -> Ad: ...

    # 32: Удаление
    @abstractmethod
    async def ad_del(self, ad_id: int) -> bool: ...

    # 33: Вкл/выкл объявления
    @abstractmethod
    async def ad_switch(self, offer_id: int, active: bool) -> bool: ...

    # 34: Вкл/выкл всех объявлений
    @abstractmethod
    async def ads_switch(self, active: bool) -> bool: ...

    # # # User
    # 35: Получить объект юзера по его ид
    @abstractmethod
    async def get_user(self, user_id) -> dict: ...

    # 36: Отправка сообщения юзеру с приложенным файлом
    @abstractmethod
    async def send_user_msg(self, msg: str, file=None) -> bool: ...

    # 37: (Раз)Блокировать юзера
    @abstractmethod
    async def block_user(self, is_blocked: bool = True) -> bool: ...

    # 38: Поставить отзыв юзеру
    @abstractmethod
    async def rate_user(self, positive: bool) -> bool: ...

    # 39: Балансы моих монет
    @abstractmethod
    async def my_assets(self) -> dict: ...

    # Сохранение объявления (с Pm/Cred-ами) в бд
    async def ad_pydin2db(self, ad_pydin: AdSaleIn | AdBuyIn) -> Ad:
        ad_db = await self.ex_client.ad_pydin2db(ad_pydin)
        await ad_db.creds.add(*getattr(ad_pydin, "creds_", []))
        return ad_db

    @staticmethod
    async def cred_pydin2db(cred: CredIn) -> Cred:
        df, unq = cred.args()
        cred_db, _ = await Cred.update_or_create(df, **unq)
        if cred.banks:
            await cred_db.banks.add(*[await PmexBank.get(exid=b) for b in cred.banks])
        return cred_db

    @staticmethod
    async def fiat_cred2db(cred: Cred) -> Cred:
        fiat, _ = await Cred.get_or_create(cred=cred)
        return fiat
