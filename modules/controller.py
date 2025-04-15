from models.account import Account
from modules.kernel import Kernel


class Controller:
    def __init__(self, account: Account, action: str):
        self.action = action
        self.account = account.model_dump()

    def execute(self) -> None:
        handler = getattr(self, self.action)
        handler()

    def check_allocation(self) -> None:
        kernel = Kernel(**self.account, chain_name="ethereum")
        kernel.check_allocation()

    def claim_airdrop(self) -> None:
        kernel = Kernel(**self.account, chain_name="ethereum")
        kernel.claim_airdrop()
