from brownie import (
    Box,
    network,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})
    # print(box.retrieveValue())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    initializer = box.changeValue, 1
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    print(f"Proxy deployed to {proxy}, you can now upgrade to V2.")

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.changeValue(2, {"from": account})
    print("The value above was changed from the proxy.")
    print(proxy_box.retrieveValue())
    print(box.retrieveValue())
    print("the value changed in both the Box and the proxy.")
    box_v2 = BoxV2.deploy({"from": account})

    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )

    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print("We are incrementing the value by one of the intial value in the proxy box.")
    proxy_box.increment({"from": account})
    print(proxy_box.retrieveValue())
