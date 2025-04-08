from enum import Enum
from sgb.collections import Host


class HOSTS(Enum):

    @property
    def NAME(self) -> str:
        return self.value.name

    @property
    def IP(self) -> str | None:
        return self.value.ip

    @property
    def ALIAS(self) -> str:
        return self.value.alias

    DC1 = Host("vld-np-dc1.sgb.lan", "dc1", "192.168.2.2")
    AD = DC1

    DC2 = Host("vld-np-dc2.sgb.lan", "dc2", "192.168.2.3")

    DEVELOPER = Host("vld-np-sgb-46.sgb.lan", "192.168.3.167")

    SKYPE = Host("vld-np-skype.sgb.lan", "192.168.2.25")

    DAME_WARE = DEVELOPER

    EXECUTOR = Host("vld-al-pk-165.sgb.lan", "192.168.10.198")

    ROUTER = DEVELOPER
