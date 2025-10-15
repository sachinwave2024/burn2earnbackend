# import pandas as pd
# from web3 import Web3
# from eth_account import Account
# import time

# # Enable HD wallet features
# Account.enable_unaudited_hdwallet_features()    

# BSC_RPC_URL = "https://bsc-dataseed.binance.org/"  # Binance Smart Chain RPC
# USDT_CONTRACT_ADDRESS = Web3.toChecksumAddress("0x55d398326f99059fF775485246999027B3197955")
# ADMIN_WALLET = Web3.toChecksumAddress("0x5F9aD24f35A17f1fE2BaD256a1fb56C3f04cD969")
# ADMIN_PRIVATE_KEY = "3ddf925deee093c1fd65d9854c927abb3819faff971666a0b38cc1ae89adb117"
# MIN_BNB_FOR_GAS = 0.0005  # Minimum BNB required for transaction fees
# BNB_TOPUP_AMOUNT = 0.0006 

# # Connect to Web3
# w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# # Load USDT contract
# USDT_ABI = [
#                 {"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Approval", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
#                 ], "name": "OwnershipTransferred", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Transfer", "type": "event"},
#                 {"constant": True, "inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "sender", "type": "address"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}
#             ]


# usdt_contract = w3.eth.contract(address=USDT_CONTRACT_ADDRESS, abi=USDT_ABI)

# # Read backup phrases from Excel
# df = pd.read_excel("/home/wave/Desktop/backup.xlsx", engine="openpyxl")



# ########################
# ########## fro backup 




# # Process each wallet
# # for index, row in df.iterrows():
# #     try:
# #         phrase = row['backup_phrase']
# #         acct = Account.from_mnemonic(phrase)
# #         wallet_address = Web3.toChecksumAddress(acct.address)  # Convert to checksum format
# #         private_key = acct.key.hex()

# #         # Check BNB balance
# #         bnb_balance = w3.eth.get_balance(wallet_address) / 10**18
# #         if bnb_balance < MIN_BNB_FOR_GAS:
# #             print(f"Skipping {wallet_address} (Insufficient BNB: {bnb_balance} BNB)")
# #             continue

# #         # Check USDT balance
# #         usdt_balance = usdt_contract.functions.balanceOf(wallet_address).call() / 10**6
# #         if usdt_balance <= 0:
# #             print(f"Skipping {wallet_address} (No USDT)")
# #             continue

# #         # Get gas details
# #         nonce = w3.eth.get_transaction_count(wallet_address)
# #         gas_price = w3.eth.gas_price
# #         gas_limit = 100000  # Adjusted gas limit for USDT transfer

# #         # Manually encode transaction data
# #         tx_data = usdt_contract.encodeABI(fn_name="transfer", args=[ADMIN_WALLET, int(usdt_balance * 10**6)])

# #         # Build transaction manually
# #         tx = {
# #             'to': USDT_CONTRACT_ADDRESS,
# #             'value': 0,
# #             'gas': gas_limit,
# #             'gasPrice': gas_price,
# #             'nonce': nonce,
# #             'data': tx_data,
# #         }

# #         # Sign and send transaction
# #         signed_tx = w3.eth.account.sign_transaction(tx, private_key)
# #         tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
# #         print(f"✅ Transferred {usdt_balance} USDT from {wallet_address} (Tx: {Web3.toHex(tx_hash)})")

# #         # print(f"✅ Transferred {usdt_balance} USDT from {wallet_address} (Tx: {w3.to_hex(tx_hash)})")
# #         # time.sleep(1.5)  # Avoid rate limits
# #         time.sleep(5)  # Avoid rate limits

# #     except Exception as e:
# #         print(f"❌ Error processing {wallet_address if wallet_address else 'Unknown'}: {str(e)}")

# # print("🚀 Transfer process completed.")



# #################################################################
# ############## for privat key 

# for index, row in df.iterrows():
#     try:
#         private_key = row['backup_phrase'].strip()  # Ensure no extra spaces
#         acct = Account.from_key(private_key)  # Use private key directly
#         wallet_address = Web3.toChecksumAddress(acct.address)  # Convert to checksum format

#         print(f"Processing wallet: {wallet_address}")

#         # Check BNB balance
#         bnb_balance = w3.eth.get_balance(wallet_address) / 10**18
#         if bnb_balance < MIN_BNB_FOR_GAS:
#             print(f"Skipping {wallet_address} (Insufficient BNB: {bnb_balance} BNB)")
#             continue

#         # Check USDT balance
#         usdt_balance = usdt_contract.functions.balanceOf(wallet_address).call() / 10**6
#         if usdt_balance <= 0:
#             print(f"Skipping {wallet_address} (No USDT)")
#             continue

#         # Get gas details
#         nonce = w3.eth.get_transaction_count(wallet_address)
#         gas_price = w3.eth.gas_price
#         gas_limit = 100000  # Adjust gas limit for USDT transfer

#         # Encode transaction data
#         tx_data = usdt_contract.encodeABI(fn_name="transfer", args=[ADMIN_WALLET, int(usdt_balance * 10**6)])

#         # Build transaction manually
#         tx = {
#             'to': USDT_CONTRACT_ADDRESS,
#             'value': 0,
#             'gas': gas_limit,
#             'gasPrice': gas_price,
#             'nonce': nonce,
#             'data': tx_data,
#         }

#         # Sign and send transaction
#         signed_tx = w3.eth.account.sign_transaction(tx, private_key)
#         tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

#         print(f"✅ Transferred {usdt_balance} USDT from {wallet_address} (Tx: {Web3.toHex(tx_hash)})")
#         time.sleep(5)  # Avoid rate limits

#     except Exception as e:
#         print(f"❌ Error processing {wallet_address if 'wallet_address' in locals() else 'Unknown'}: {str(e)}")

# print("🚀 Transfer process completed.")



# import pandas as pd
# from web3 import Web3
# from eth_account import Account
# import time

# # Enable HD wallet features
# Account.enable_unaudited_hdwallet_features()    

# BSC_RPC_URL = "https://bsc-dataseed.binance.org/"  # Binance Smart Chain RPC
# USDT_CONTRACT_ADDRESS = Web3.toChecksumAddress("0x55d398326f99059fF775485246999027B3197955")
# ADMIN_WALLET = Web3.toChecksumAddress("0xd2dF2b3e5f066cc34C331d32C20D35669dAb9202")
# ADMIN_PRIVATE_KEY = "9431d3ed6d99b498519186333bfd3641117801d77fe20511ce0f587a999afd53"

# w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))  # Ensure correct provider


# account = w3.eth.account.from_key(ADMIN_PRIVATE_KEY)
# print(f"Admin Wallet Address: {account.address}")
# MIN_BNB_FOR_GAS = 0.0005  # Minimum BNB required for transaction fees
# BNB_TOPUP_AMOUNT = 0.0006 

# # Connect to Web3
# w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# # Load USDT contract
# USDT_ABI = [
#                 {"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Approval", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
#                 ], "name": "OwnershipTransferred", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Transfer", "type": "event"},
#                 {"constant": True, "inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "sender", "type": "address"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}
#             ]


# usdt_contract = w3.eth.contract(address=USDT_CONTRACT_ADDRESS, abi=USDT_ABI)

# # Read backup phrases from Excel
# df = pd.read_excel("/home/wave/Desktop/backup.xlsx", engine="openpyxl") 


# def send_bnb(admin_wallet, admin_key, to_wallet, amount):
#     """Send BNB from admin wallet to a user wallet."""
    
#     # Ensure the 'from' wallet matches the private key
#     if w3.eth.account.from_key(admin_key).address.lower() != admin_wallet.lower():
#         print(f"❌ ERROR: Private key does not match the admin wallet address!")
#         return None

#     # Get Admin's BNB balance
#     admin_balance = w3.eth.get_balance(admin_wallet) / 10**18  
#     if admin_balance < amount:
#         print(f"❌ Admin has insufficient BNB ({admin_balance} BNB), cannot send {amount} BNB.")
#         return None  # Skip if admin has no funds

#     nonce = w3.eth.get_transaction_count(admin_wallet)  # Get nonce from admin wallet
#     gas_price = w3.eth.gas_price

#     tx = {
#         'from': admin_wallet,  # ✅ Ensure the transaction is sent from Admin
#         'to': to_wallet,  
#         'value': Web3.toWei(amount, "ether"), # ✅ Correct function name,  # ✅ Corrected here
#         'gas': 21000,
#         'gasPrice': gas_price,
#         'nonce': nonce,
#     }

#     signed_tx = w3.eth.account.sign_transaction(tx, admin_key)  # ✅ Sign with admin key
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

#     print(f"✅ Sent {amount} BNB from Admin ({admin_wallet}) to {to_wallet} (Tx: {w3.to_hex(tx_hash)})")
#     return tx_hash


# # ✅ Process wallets
# for index, row in df.iterrows():
#     try:
#         private_key = row['backup_phrase'].strip()
#         acct = Account.from_key(private_key)
#         # wallet_address = w3.to_checksum_address(acct.address)  # ✅ Ensure checksum address
#         wallet_address = Web3.toChecksumAddress(acct.address)  # ✅ Correct function name


#         print(f"🚀 Processing wallet: {wallet_address}")

#         # ✅ Check BNB and USDT balances
#         bnb_balance = w3.eth.get_balance(wallet_address) / 10**18
#         usdt_balance = usdt_contract.functions.balanceOf(wallet_address).call() / 10**6  

#         if usdt_balance <= 1:
#             print(f"⏩ Skipping {wallet_address} (No USDT)")
#             continue

#         # ✅ If no BNB, send gas fee from admin
#         if bnb_balance < MIN_BNB_FOR_GAS:
#             print(f"⏳ {wallet_address} has insufficient BNB, sending {BNB_TOPUP_AMOUNT} BNB from admin...")
#             tx_hash = send_bnb(ADMIN_WALLET, ADMIN_PRIVATE_KEY, wallet_address, BNB_TOPUP_AMOUNT)
#             if tx_hash:
#                 w3.eth.wait_for_transaction_receipt(tx_hash)  # Ensure BNB is received before sending USDT
#             else:
#                 print(f"❌ Skipping {wallet_address}, admin could not send BNB.")
#                 continue  # Skip to next wallet if BNB couldn't be sent

#         # ✅ Prepare USDT transfer
#         nonce = w3.eth.get_transaction_count(wallet_address)
#         gas_price = w3.eth.gas_price
#         gas_limit = 200000  

#         tx_data = usdt_contract.encodeABI(fn_name="transfer", args=[ADMIN_WALLET, int(usdt_balance * 10**6)])

#         tx = {
#             'to': USDT_CONTRACT_ADDRESS,
#             'value': 0,
#             'gas': gas_limit,
#             'gasPrice': gas_price,
#             'nonce': nonce,
#             'data': tx_data,
#         }

#         # ✅ Sign and send USDT transfer
#         signed_tx = w3.eth.account.sign_transaction(tx, acct.key)
#         tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

#         print(f"✅ Sent {amount} BNB from Admin ({admin_wallet}) to {to_wallet} (Tx: {w3.toHex(tx_hash)})")  # ✅ Fixed function name
#         time.sleep(1.5)  

#     except Exception as e:
#         print(f"❌ Error processing {wallet_address if 'wallet_address' in locals() else 'Unknown'}: {str(e)}")

# print("🚀 Transfer process completed.")
























import pandas as pd
from web3 import Web3
from eth_account import Account

# ✅ Load the Excel file (update file name & sheet name if needed)
df = pd.read_excel("/home/wave/Desktop/backuppp.xlsx", engine="openpyxl") 

# ✅ Connect to Binance Smart Chain (BSC) RPC
BSC_RPC = "https://bsc-dataseed.binance.org/"  # Update if needed
w3 = Web3(Web3.HTTPProvider(BSC_RPC))

# ✅ USDT Contract Details (Update if different for your case)
USDT_CONTRACT_ADDRESS = "0x55d398326f99059fF775485246999027B3197955"  # BSC USDT
USDT_ABI = [
                {"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
                {"anonymous": False, "inputs": [
                    {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
                    {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
                ], "name": "Approval", "type": "event"},
                {"anonymous": False, "inputs": [
                    {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
                ], "name": "OwnershipTransferred", "type": "event"},
                {"anonymous": False, "inputs": [
                    {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
                    {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
                    {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
                ], "name": "Transfer", "type": "event"},
                {"constant": True, "inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": True, "inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": True, "inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": True, "inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": True, "inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "address", "name": "sender", "type": "address"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
                {"constant": False, "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}
            ]
usdt_contract = w3.eth.contract(address=USDT_CONTRACT_ADDRESS, abi=USDT_ABI)

# ✅ Process each wallet
print("\n📋 Wallets with USDT >= 1")
print("----------------------------------------------")
print("Private Key | Wallet Address | USDT Balance")
print("----------------------------------------------")

for index, row in df.iterrows():
    try:
        private_key = row['backup_phrase'].strip()
        acct = Account.from_key(private_key)
        wallet_address = w3.toChecksumAddress(acct.address)

        # ✅ Get USDT Balance
        usdt_balance = usdt_contract.functions.balanceOf(wallet_address).call() / 10**18  # USDT has 6 decimals
        
        if usdt_balance >= 1:
            print(f"{private_key} | {wallet_address} | {usdt_balance:.2f} USDT")
    
    except Exception as e:
        print(f"❌ Error processing {row['backup_phrase']}: {str(e)}")

print("----------------------------------------------")
print("✅ Process completed.")































# from eth_account import Account
# from mnemonic import Mnemonic
# from bip32utils import BIP32Key, BIP32_HARDEN
# import binascii

# # Replace this with your actual 12/24-word mnemonic phrase
# mnemonic_phrase = "actual address hello all engine utility expose farm inside rate divert garment"

# # Generate seed from mnemonic
# mnemo = Mnemonic("english")
# seed = mnemo.to_seed(mnemonic_phrase)  # This returns bytes, which is correct

# # Ensure seed is in correct format (hex)
# seed_hex = binascii.hexlify(seed).decode()
# print("Seed (hex):", seed_hex)  # Debugging: Ensure it's a valid hex string

# # Generate master key from binary seed (corrected)
# master_key = BIP32Key.fromEntropy(seed)  # Ensure seed is passed as bytes

# # Generate sub-wallets using Ethereum's BIP-44 derivation path
# num_wallets = 550  # Number of sub-wallets to derive
# wallets = []

# for i in range(num_wallets):
#     child_key = master_key.ChildKey(44 + BIP32_HARDEN) \
#                           .ChildKey(60 + BIP32_HARDEN) \
#                           .ChildKey(0 + BIP32_HARDEN) \
#                           .ChildKey(0) \
#                           .ChildKey(i)

#     private_key = child_key.WalletImportFormat()  # Might be causing the issue
#     private_key_hex = child_key.PrivateKey().hex()  # Ensure it's a valid hex key
#     account = Account.from_key(private_key_hex)  # Use the corrected hex key

#     wallets.append({"index": i, "address": account.address, "private_key": private_key_hex})

# # Print sub-wallet addresses
# for wallet in wallets:
#     print(f"Sub-Wallet {wallet['index']}: {wallet['address']}")



# from mnemonic import Mnemonic
# from bip32utils import BIP32Key, BIP32_HARDEN
# from eth_account import Account

# # Replace with your actual 12/24-word mnemonic phrase
# mnemonic_phrase = "actual address hello all engine utility expose farm inside rate divert garment"

# # Generate seed from mnemonic
# mnemo = Mnemonic("english")
# seed = mnemo.to_seed(mnemonic_phrase)

# # Generate master key
# master_key = BIP32Key.fromEntropy(seed)

# # Derive the parent wallet (Ethereum BIP-44: m/44'/60'/0')
# parent_key = master_key.ChildKey(44 + BIP32_HARDEN) \
#                        .ChildKey(60 + BIP32_HARDEN) \
#                        .ChildKey(0 + BIP32_HARDEN)

# # Generate parent wallet address
# parent_address = Account.from_key(parent_key.PrivateKey().hex()).address
# print("🔹 Parent Wallet Address:", parent_address)

# # Target wallet to find
# target_address = "0x80916B3d99AA47205b05926875263e0E1999eC4d".lower()

# # Set the number of child wallets to derive
# num_addresses = 1000  # You can increase this if needed

# # Track found matches
# found_matches = []

# # Loop through all child addresses
# for i in range(num_addresses):
#     child_key = parent_key.ChildKey(0).ChildKey(i)
#     child_address = Account.from_key(child_key.PrivateKey().hex()).address
    
#     # Print each child address with its index
#     print(f"🔸 Child {i} Address: {child_address}")

#     # Check if this child matches the target address
#     if child_address.lower() == target_address:
#         found_matches.append(i)

# # Display results
# if found_matches:
#     print("\n🎯 ✅ Target Address Found at Indices:", found_matches)
# else:
#     print("\n🚨 Target address not found in the first", num_addresses, "derivations.")








# import pandas as pd
# import firebase_admin
# from firebase_admin import credentials, firestore
# import time

# # === Step 1: Initialize Firebase App ===
# cred = credentials.Certificate("/home/wave/Downloads/houzer-1bdaf-firebase-adminsdk-fbsvc-d2e326f9aa.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # === Step 2: Load Excel Data ===
# excel_path = "/home/wave/Downloads/Properties.xlsx"
# try:
#     df = pd.read_excel(excel_path, engine='openpyxl')  # Use openpyxl for .xlsx
# except Exception as e:
#     print(f"❌ Error reading Excel file: {e}")
#     exit()

# # === Step 3: Upload Each Row to Firestore using Batches (recommended) ===
# collection_name = "Dealers"
# batch = db.batch()
# count = 0
# batch_size = 500  # Firestore max is 500 writes per batch

# try:
#     for index, row in df.iterrows():
#         doc_ref = db.collection(collection_name).document()  # Auto-generate document ID
#         batch.set(doc_ref, row.to_dict())
#         count += 1

#         if count % batch_size == 0:
#             batch.commit()
#             print(f"✅ Uploaded {count} records so far...")
#             batch = db.batch()
#             time.sleep(1)  # Small delay to avoid quota errors

#     # Commit remaining records
#     if count % batch_size != 0:
#         batch.commit()
#         print(f"✅ Final commit: Uploaded {count} total records.")

#     print("🎉 All data uploaded successfully to Firestore!")

# except Exception as e:
#     print(f"❌ Error uploading to Firestore: {e}")


# import firebase_admin
# from firebase_admin import credentials, firestore
# import time

# # === Step 1: Initialize Firebase App ===
# cred = credentials.Certificate("/home/wave/Downloads/houzer-1bdaf-firebase-adminsdk-fbsvc-d2e326f9aa.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # === Step 2: Set Collection Name to Delete ===
# collection_name = "properties"
# batch_size = 500

# def delete_collection(coll_ref, batch_size):
#     docs = coll_ref.limit(batch_size).stream()
#     deleted = 0

#     for doc in docs:
#         print(f"🗑️ Deleting document: {doc.id}")
#         doc.reference.delete()
#         deleted += 1

#     return deleted

# # === Step 3: Delete in Batches ===
# try:
#     while True:
#         deleted = delete_collection(db.collection(collection_name), batch_size)
#         if deleted == 0:
#             break
#         time.sleep(1)  # Optional delay to respect Firestore limits

#     print(f"✅ Collection '{collection_name}' deleted successfully.")

# except Exception as e:
#     print(f"❌ Error deleting collection: {e}")



# import pandas as pd
# import firebase_admin
# from firebase_admin import credentials, firestore

# # === Step 1: Initialize Firebase App ===
# cred = credentials.Certificate("/home/wave/Downloads/houzer-1bdaf-firebase-adminsdk-fbsvc-d2e326f9aa.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # === Step 2: Load Excel Data ===
# excel_path = "/home/wave/Downloads/Properties.xlsx"
# df = pd.read_excel(excel_path, engine='openpyxl')  # ✅ Set correct engine

# # === Step 3: Upload Each Row to Firestore ===
# collection_name = "properties"

# for index, row in df.iterrows():
#     data = row.to_dict()
#     db.collection(collection_name).add(data)

# print("✅ Data uploaded successfully to Firestore.")

# import time
# from web3 import Web3

# # ========== CONFIG ==========
# INFURA_URL = "https://bsc-dataseed.binance.org/"  # BSC RPC URL
# USDT_CONTRACT_ADDRESS = Web3.toChecksumAddress("0x55d398326f99059fF775485246999027B3197955")  # USDT on BSC

# ADMIN_WALLET = Web3.toChecksumAddress("0xaee20d609bDA8824114A26050c2F52966C40d356")  # Replace
# ADMIN_PRIVATE_KEY = "27870e56923adf34adab3b992c17e9552a26bc7038c7879bcf5566f5f9e4773f" # Replace securely
# WITHDRAW_WALLET = Web3.toChecksumAddress("0xaee20d609bDA8824114A26050c2F52966C40d356")  # Replace

# REQUIRED_BALANCE = 10       # Minimum USDT required to trigger transfer
# WITHDRAW_AMOUNT = 10        # Amount to send to withdraw wallet

# # ========== INIT ==========
# w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# # ✅ USDT Contract Details (Update if different for your case)
# USDT_CONTRACT_ADDRESS = "0x55d398326f99059fF775485246999027B3197955"  # BSC USDT
# USDT_ABI = [
#                 {"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Approval", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
#                 ], "name": "OwnershipTransferred", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Transfer", "type": "event"},
#                 {"constant": True, "inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "sender", "type": "address"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}
#             ]
# usdt_contract = w3.eth.contract(address=USDT_CONTRACT_ADDRESS, abi=USDT_ABI)

# # ========== FUNCTIONS ==========
# def get_usdt_balance(address):
#     decimals = usdt_contract.functions.decimals().call()
#     raw_balance = usdt_contract.functions.balanceOf(address).call()
#     return raw_balance / (10 ** decimals)


# def send_usdt(from_wallet, from_key, to_wallet, amount):
#     if amount <= 0:
#         print("⚠️ Amount is zero or negative — transaction skipped.")
#         return

#     nonce = w3.eth.get_transaction_count(from_wallet)
#     gas_price = w3.eth.gas_price
#     gas_limit = 100000

#     tx_data = usdt_contract.encodeABI(fn_name="transfer", args=[to_wallet, int(amount * 10**18)])

#     tx = {
#         'to': USDT_CONTRACT_ADDRESS,
#         'value': 0,
#         'gas': gas_limit,
#         'gasPrice': gas_price,
#         'nonce': nonce,
#         'data': tx_data,
#     }

#     signed_tx = w3.eth.account.sign_transaction(tx, from_key)
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#     print(f"✅ Transaction sent! {amount} USDT from {from_wallet} to {to_wallet} (Tx: {w3.toHex(tx_hash)})")
#     return tx_hash

# # ========== MAIN LOOP ==========
# while True:
#     try:
#         admin_usdt = get_usdt_balance(ADMIN_WALLET)
#         print(f"💼 Admin USDT Balance: {admin_usdt:.6f}")

#         if admin_usdt >= REQUIRED_BALANCE:
#             print(f"✅ Balance sufficient (≥ {REQUIRED_BALANCE} USDT). Proceeding to transfer {WITHDRAW_AMOUNT} USDT...")
#             send_usdt(ADMIN_WALLET, ADMIN_PRIVATE_KEY, WITHDRAW_WALLET, WITHDRAW_AMOUNT)
#         else:
#             print(f"⛔ Balance insufficient ({admin_usdt:.6f} < {REQUIRED_BALANCE}). No transaction sent.")
#     except Exception as e:
#         print(f"❌ Error occurred: {e}")

#     print("⏳ Waiting 5 seconds before next check...\n")
#     time.sleep(10)





# import requests

# bscscan_api_key = "H2MN7QS9RTXE7IQF267U1KBS1W37MKTEUG"
# contract_address = "0x723b28cE69c5cA2a2226c22e023b299c11E69da8"

# def get_total_supply():
#     url = f"https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress={contract_address}&apikey={bscscan_api_key}"
#     res = requests.get(url).json()
#     if res['status'] == '1':
#         return int(res['result'])
#     return None

# def get_holders_count():
#     url = f"https://api.bscscan.com/api?module=token&action=tokenholderchart&contractaddress={contract_address}&apikey={bscscan_api_key}"
#     res = requests.get(url).json()
#     if res['status'] == '1':
#         return len(res['result'])  # Number of holders in the chart (usually top 1000)
#     return None

# def get_token_info_from_contract():
#     url = f"https://api.bscscan.com/api?module=contract&action=getsourcecode&address={contract_address}&apikey={bscscan_api_key}"
#     res = requests.get(url).json()
#     if res['status'] == '1' and res['result']:
#         contract_data = res['result'][0]
#         return {
#             "Token Name": contract_data.get("ContractName"),
#             "Symbol": None,  # Can't fetch from here
#             "Decimals": None  # Not available here either
#         }
#     return {}

# # --- RUN THE FUNCTIONS ---
# total_supply = get_total_supply()
# holders = get_holders_count()
# token_info = get_token_info_from_contract()

# # --- DISPLAY RESULTS ---
# print("Token Name:", token_info.get('Token Name'))
# print("Symbol:", token_info.get('Symbol', 'N/A'))
# print("Decimals:", token_info.get('Decimals', 'N/A'))
# print("Contract Address:", contract_address)
# print("Max Total Supply:", total_supply)
# print("Holders (Top 1000 only):", holders)












# import pandas as pd

# # Load the Excel file
# df = pd.read_excel("/home/wave/Downloads/Weekly_Emissions_CH4_2010_2024.xlsx", header=None)

# # Step 1: Set the first row as column headers
# df.columns = df.iloc[0]
# df = df.drop(index=0)

# # Step 2: Transpose so that dates become the index
# df = df.transpose()

# # Step 3: Rename columns (Row_1, Row_2, ...)
# df.columns = [f"Row_{i}" for i in range(1, len(df.columns) + 1)]

# # Step 4: Parse the index as datetime
# df.index = pd.to_datetime(df.index, format="%m/%d/%Y", errors='coerce')

# # Step 5: Drop rows with invalid dates
# df = df[~df.index.isna()]

# # Step 6: Convert all values to float
# df = df.astype(float)

# # Step 7: Add a 'Year' column based on the index
# df['Year'] = df.index.year

# # Step 8: Calculate the average of all rows per year
# yearly_avg = df.groupby('Year').mean().mean(axis=1)

# # Step 9: Compute cumulative average year-by-year
# cumulative_avg = yearly_avg.expanding().mean()

# # Step 10: Save results to Excel
# result = pd.DataFrame({
#     'Year': cumulative_avg.index,
#     'Cumulative_Average': cumulative_avg.values
# })
# result.to_excel("/home/wave/Downloads/output_cumulative_yearly_averages.xlsx", index=False)

# print("✅ Done: output_cumulative_yearly_averages.xlsx created.")



# import pandas as pd

# # Load your Excel file
# input_file = "/home/wave/Downloads/dummy.xlsx"  # Replace with your actual file path
# # Load the Excel file and print all sheet names
# xls = pd.ExcelFile(input_file)
# print("Available sheet names:", xls.sheet_names)

# sheet_name = "processed_unique_locations"  # Sheet with the data

# # Read the Excel file
# df = pd.read_excel(input_file, sheet_name=sheet_name)

# # Identify static (non-date) columns
# static_columns = ['Name', 'Type', 'Province', 'Latitude', 'Longitude']

# # Reshape the data: convert wide date columns to rows
# df_melted = df.melt(id_vars=static_columns, var_name='Date', value_name='Value')

# # Convert the 'Date' column to proper datetime format
# df_melted['Date'] = pd.to_datetime(df_melted['Date'], errors='coerce')

# # Save the reshaped data to a new Excel file
# output_file = "processed_long_format.xlsx"
# df_melted.to_excel(output_file, index=False)

# print(f"Saved reshaped data to {output_file}")







# import multiprocessing
# from web3 import Web3
# from eth_account import Account
# import os

# # Enable HD wallet derivation
# Account.enable_unaudited_hdwallet_features()

# # Admin wallet seed phrase or private key
# ADMIN_PRIVATE_KEY = "9431d3ed6d99b498519186333bfd3641117801d77fe20511ce0f587a999afd53"
# ADMIN_WALLET = Web3.toChecksumAddress("0xd2dF2b3e5f066cc34C331d32C20D35669dAb9202")
# RPC_URL = "https://bsc-dataseed.binance.org/"

# # USDT contract
# USDT_CONTRACT = Web3.toChecksumAddress("0x55d398326f99059fF775485246999027B3197955")

# # Web3 instance
# w3 = Web3(Web3.HTTPProvider(RPC_URL))

# # USDT ABI (minimal)
# USDT_ABI = [
#                 {"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Approval", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
#                 ], "name": "OwnershipTransferred", "type": "event"},
#                 {"anonymous": False, "inputs": [
#                     {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
#                     {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
#                     {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
#                 ], "name": "Transfer", "type": "event"},
#                 {"constant": True, "inputs": [], "name": "_decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "_symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mint", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [], "name": "renounceOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "sender", "type": "address"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
#                 {"constant": False, "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}
#             ]


# # Load USDT contract
# usdt_contract = w3.eth.contract(address=USDT_CONTRACT, abi=USDT_ABI)

# # Get USDT decimals once
# USDT_DECIMALS = usdt_contract.functions.decimals().call()

# # Get master account from private key
# master_account = Account.from_key(ADMIN_PRIVATE_KEY)

# # Derive wallet address using HD path
# def derive_wallet(index):
#     path = f"m/44'/60'/0'/0/{index}"
#     account = Account.from_mnemonic(master_account.key.hex(), account_path=path)
#     return account

# # Check wallet balance
# def check_wallet(index):
#     try:
#         account = derive_wallet(index)
#         address = Web3.toChecksumAddress(account.address)
#         balance_raw = usdt_contract.functions.balanceOf(address).call()
#         balance = balance_raw / (10 ** USDT_DECIMALS)

#         if balance >= 1:
#             print(f"[FOUND] Index: {index} | Address: {address} | USDT: {balance}")
#             return (index, address, balance)

#     except Exception as e:
#         print(f"[ERROR] Index {index}: {str(e)}")

#     return None

# # Worker function for a range of indices
# def process_range(start, end):
#     result = []
#     for idx in range(start, end):
#         res = check_wallet(idx)
#         if res:
#             result.append(res)
#     return result

# # Split index range for multiprocessing
# def chunk_indices(start, end, chunks):
#     step = (end - start) // chunks
#     return [(start + i * step, start + (i + 1) * step if i < chunks - 1 else end) for i in range(chunks)]

# # Main execution
# if __name__ == "__main__":
#     start_index = 0
#     end_index = 1000  # Adjust range as needed
#     num_processes = multiprocessing.cpu_count()

#     chunks = chunk_indices(start_index, end_index, num_processes)

#     print(f"Starting scan using {num_processes} processes from index {start_index} to {end_index}...")

#     with multiprocessing.Pool(processes=num_processes) as pool:
#         results = pool.starmap(process_range, chunks)

#     # Flatten results
#     all_found = [item for sublist in results for item in sublist]

#     print("\n=== Summary ===")
#     for idx, address, balance in all_found:
#         print(f"Index: {idx} | Wallet: {address} | USDT: {balance}")

#     print(f"\nTotal wallets with >= 1 USDT: {len(all_found)}")



# import requests
# import pandas as pd

# API_KEY = "H2MN7QS9RTXE7IQF267U1KBS1W37MKTEUG"
# ADDRESS = "0xA5021FF959F4833a1F7160dE51E2E7401AB1A0bB"
# BASE_URL = "https://api.bscscan.com/api"

# params = {
#     "module": "account",
#     "action": "tokentx",
#     "address": ADDRESS,
#     "startblock": 0,
#     "endblock": 99999999,
#     "sort": "asc",
#     "apikey": API_KEY
# }

# response = requests.get(BASE_URL, params=params)
# data = response.json()

# if data["status"] == "1":
#     txs = data["result"]
#     df = pd.DataFrame(txs)
#     df.to_csv("bep20_transactions.csv", index=False)
#     print(f"Fetched {len(df)} token transfers. Saved to bep20_transactions.csv.")
# else:
#     print(f"Error fetching data: {data['message']}")
