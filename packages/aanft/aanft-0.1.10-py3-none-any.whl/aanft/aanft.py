import aiohttp
import asyncio
import aiohttp.client_exceptions
from loguru import logger
from typing_extensions import Self
from typing import List, Coroutine, Dict
import aiofiles

exceptions = aiohttp.client_exceptions
ENDPOINTS_MAINNET = [
    
    #"https://api.wax-aa.bountyblok.io/atomicassets",
    "https://atomic.3dkrender.com/atomicassets",
    "https://wax-aa.eu.eosamsterdam.net/atomicassets",
    "https://atomic-wax.a-dex.xyz/atomicassets",
    "https://atomic-wax-mainnet.wecan.dev/atomicassets",
    "https://wax-atomic.alcor.exchange/atomicassets",
    "http://wax.eosusa.io/atomicassets/atomicassets",  
    #"http://wax.blokcrafters.io/atomicassets", 
    #"http://wax.blacklusion.io/atomicassets"
]
ENDPOINTS_TESTNET = [
    "https://test.wax.api.atomicassets.io",
    "https://wax-test.blokcrafters.io",
    "https://api.waxtest.waxgalaxy.io",
]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


class AANFT:
    def __init__(self, test: bool = False, prefered: int = 0, endpoints=[]) -> None:
        self.network = "testnet" if test else "mainnet"
        self.endpoints = ENDPOINTS_MAINNET if not test else ENDPOINTS_TESTNET
        if endpoints:
            self.endpoints = endpoints
        self.preferred_endpoint = self.endpoints[prefered]  # The default API
        self.selected_endpoint = self.preferred_endpoint
        self.assets = "/v1/assets"
        self.headers = HEADERS
        self.max_tries = 3
        self.limit = 1000
        self.backup_endpoints = self.endpoints[prefered:]  # All other API endpoints

    async def switch_endpoint(self):
        """Switch to the next available endpoint, cycling through the list."""
        if self.backup_endpoints:
            next_endpoint = self.backup_endpoints.pop(0)  # Get the next backup endpoint
            self.backup_endpoints.append(self.selected_endpoint)  # Add current endpoint to the end of the list
            self.selected_endpoint = next_endpoint
            logger.info(f"Switching to backup endpoint: {self.selected_endpoint}")
        else:
            logger.error("No more backup endpoints available.")

    async def get_transfers_deposit(self, sender, recipient, memo, limit):
        payload = {
            "sender": sender,
            "recipient": recipient,
            "memo": memo,
            "limit": limit,
        }
        
        async with aiohttp.ClientSession() as session:
            for attempt in range(self.max_tries):
                try:
                    async with session.get(
                        f"{self.selected_endpoint}/v1/transfers", 
                        params=payload, 
                        headers=self.headers, 
                        timeout=10  # Setting timeout
                    ) as response:
                        #response.raise_for_status()  # Check if status code is 200-299
                        return await response.json()
                
                except (asyncio.TimeoutError, exceptions.ClientResponseError, exceptions.ClientConnectorError) as e:
                    logger.warning(f"Error on {self.selected_endpoint}: {e} (Attempt {attempt + 1}/{self.max_tries})")
                    
                    # Retry if max attempts haven't been reached
                    if attempt + 1 < self.max_tries:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        # Switch to the next API endpoint if current one fails after max tries
                        logger.error(f"Max retries reached for {self.selected_endpoint}. Switching API.")
                        await self.switch_endpoint()  # Switch to another endpoint

            # If all endpoints are tried and none work, return an error message
            return None, "All API endpoints failed after retries."


    async def tx_not_in_file(self, filename, tx_id):
        async with aiofiles.open(filename, mode='r') as file:
            async for line in file:
                if tx_id == line.strip():
                    return False
        return True

    async def fetch_loop(self, account, schema, template, collection, session):
        print(self.preferred_endpoint)
        resultcount = self.limit
        data = []
        page = 1
        reason = "" 
        while resultcount == self.limit:
            params = {"limit": self.limit, "order": "asc", "page": page, "burned": "false"}
            if account:
                params['owner'] = account
            if schema:
                params['schema_name'] = schema
            if template:
                params['template_id'] = template
            if collection:
                params["collection_name"] = collection

            for attempt in range(self.max_tries):
                endpoint = self.selected_endpoint + self.assets  # Update the endpoint dynamically
                try:
                    async with session.get(endpoint, params=params, headers=self.headers, timeout=10) as response:
                        assets = await response.json()
                        
                        if assets:
                            data += assets["data"]
                            resultcount = len(assets['data'])
                            page += 1
                        break  # Exit the retry loop on success
                except (asyncio.TimeoutError, aiohttp.ClientError, KeyError) as e:
                    logger.warning(f"Attempt {attempt + 1} failed on {self.selected_endpoint}: {e}")
                    reason = e
                    # If max retries reached, switch the endpoint
                    if attempt + 1 == self.max_tries:
                        logger.error(f"Max retries reached for {self.selected_endpoint}. Switching to next API endpoint.")
                        await self.switch_endpoint()  # Switch to the next available endpoint
                        break  # Exit retry loop after switching the endpoint
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        return data, reason

    async def fetch_nfts(self, account: str = "", template: str = "", schema: str = "", collection: str = "") -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            for attempt in range(self.max_tries):
                try:
                    return await self.fetch_loop(account, schema, template, collection, session)
                except (asyncio.TimeoutError, aiohttp.ClientConnectorError) as e:
                    logger.warning(f"Error: {e}. Attempt {attempt + 1}/{self.max_tries} on {self.selected_endpoint}")
                    
                    # If max retries reached, switch the endpoint
                    if attempt + 1 == self.max_tries:
                        logger.error(f"Max retries reached for {self.selected_endpoint}. Switching API.")
                        await self.switch_endpoint()  # Switch to another endpoint
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

            return [], "All API endpoints failed after retries."


    async def fetch_templates(
        self: Self,
        collection: str = "",
        schema: str = "",
        has_assets: str = "true"
    ) -> List[Dict]:
        endpoint = self.selected_endpoint + "/v1/templates"
        async with aiohttp.ClientSession() as session:
            resultcount = self.limit
            data = []
            page = 1
            n = 0
            while resultcount == self.limit:
                n += 1
                params = {"limit": self.limit, "order": "asc", "page": page, "burned": "false", "has_assets": has_assets}
                if schema:
                    params['schema_name'] = schema
                if collection:
                    params["collection_name"] = collection
                async with session.get(endpoint, params=params, headers=self.headers) as response:
                    templates = await response.json()
                if templates:
                    data += templates["data"]
                    resultcount = len(templates['data'])
                    page += 1
                else:
                    return data

            return data


    async def fetch_schemas(
        self: Self,
        collection: str = "",
        schema: str = ""
    ) -> List[Dict]:
        limit = 100
        resultcount = limit
        data = []
        page = 1
        n = 0
        endpoint = self.selected_endpoint + "/v1/schemas"
        async with aiohttp.ClientSession() as session:
            while resultcount == limit:
                n += 1
                params = {"limit": limit, "order": "asc", "page": page, "burned": "false"}
                if schema:
                    params['schema_name'] = schema
                if collection:
                    params["collection_name"] = collection
                async with session.get(endpoint, params=params, headers=self.headers) as response:
                    schemas = await response.json()
                    
                if schemas:
                    data = data + schemas["data"]
                    resultcount = len(schemas["data"])
                    page += 1
                else:
                    return data
            return data

    async def fetch_transactions(
        self: Self,
        sender: str = "",
        receiver: str = "",
        memo: str = ""
    ) -> List[Dict]:
        """_summary_

        Args:
            sender (str, optional): _sender account_. Defaults to "".
            receiver (str, optional): _receiver account_. Defaults to "".
            memo (str, optional): _memo_. Defaults to "".

        Returns:
            list: _List of transactions that fit criteria_
        """
        limit = 100
        resultcount = limit
        data = []
        page = 1
        n = 0
        endpoint = self.selected_endpoint + "/v1/transfers"
        async with aiohttp.ClientSession() as session:
            while resultcount == limit:
                n += 1
                params = {"limit": limit, "order": "asc", "page": page} #, "burned": "false"}
                if sender:
                    params['sender'] = sender
                if receiver:
                    params["receiver"] = receiver
                if memo:
                    params["memo"] = memo
                async with session.get(endpoint, params=params, headers=self.headers) as response:
                    transfers = await response.json()
                if transfers:
                    data += transfers["data"]
                    resultcount = len(transfers['data'])
                    page += 1
                else:
                    return data
            return data
                    

        



