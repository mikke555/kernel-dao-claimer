from web3.exceptions import ContractCustomError

from data.const import KERNEL_DISTRIBUTER, KERNEL_DISTRIBUTER_ABI
from models.responses.proof_response import Data, ProofResponse
from modules.http import HttpClient
from modules.logger import logger
from modules.wallet import Wallet


class Kernel(Wallet):
    base_url = "https://common.kerneldao.com/merkle/proofs/kernel_eth"
    message = "Sign message to view your Season 1 points"
    index = 8

    def __init__(self, id: str, private_key: str, chain_name: str, proxy: str = ""):
        super().__init__(id, private_key, chain_name, proxy)
        self.http = HttpClient(self.proxy)
        self.label += "KERNEL DAO |"
        self.contract = self.get_contract(KERNEL_DISTRIBUTER, KERNEL_DISTRIBUTER_ABI)

    def check_allocation(self) -> Data | None:
        signature = self.sign_message(self.message)
        params = {"address": self.address, "signature": signature}

        resp = self.http.get(self.base_url, params=params)
        data = ProofResponse(**resp.json())

        if data.data is None:
            logger.warning(f"{self.label} Not eligible")
            return

        logger.debug(f"{self.label} {int(data.data.balance) / 10**18} KERNEL")
        return data.data

    def claim_airdrop(self):
        """claim(uint256 index,address account,uint256 cumulativeAmount,bytes32[] merkleProof)"""
        data = self.check_allocation()

        if data is None:
            return

        try:
            contract_tx = self.contract.functions.claim(
                self.index, self.address, int(data.balance), data.proof
            ).build_transaction(self.get_tx_params())

        except ContractCustomError:
            logger.error(f"{self.label} Contract error, most likely already claimed")
            return

        self.send_tx(contract_tx, tx_label=f"{self.label} Claim airdrop")
