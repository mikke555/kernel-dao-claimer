import json

import questionary

from models.network import Network

style = questionary.Style(
    [
        ("qmark", "fg:#47A6F9 bold"),
        ("pointer", "fg:#47A6F9 bold"),
        ("highlighted", "fg:#808080"),
        ("answer", "fg:#808080"),
        ("instruction", "fg:#808080 italic"),
    ]
)

ethereum = Network(
    name="ethereum",
    explorer="https://etherscan.io",
    eip_1559=True,
    native_token="ETH",
    chain_id=1868,
)


network_mapping = {
    "ethereum": ethereum,
}

KERNEL_DISTRIBUTER = "0x68B55c20A2634B25a50a219b632F22854D810bf5"

with open("data/abi/kernel.json") as f:
    KERNEL_DISTRIBUTER_ABI = json.load(f)

with open("data/abi/ERC20.json") as f:
    ERC20_ABI = json.load(f)
