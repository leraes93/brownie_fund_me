from http.client import FOUND
from eth_account import Account
from brownie import network, accounts, exceptions
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me, LOCAL_BLOCKCHAIN_ENVIROMENTS
import pytest

def test_can_fund_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx  = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

def test_fund_does_not_exist():
    account = get_account()
    fund_me = deploy_fund_me()
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("only for local testing...")
    fund_me = deploy_fund_me()
    bad_account = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_account})