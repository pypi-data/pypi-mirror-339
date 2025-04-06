from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.client import LedgerClient, NetworkConfig
import aiohttp
import mnemonic
from typing import Optional, Dict, Any, Callable, List
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import logging
from urllib.parse import urlparse
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# No default RPC nodes - users must provide their own
DEFAULT_RPC_NODES = []

# Wallet Class
class SeiWallet:
    """
    🔥 SeiWallet: A lit wallet manager for the Sei blockchain 🔥

    Features:
    - Import wallets using mnemonic phrases (wallet creation not supported)
    """
    def import_wallet(self, mnemonic_phrase: str) -> Dict[str, str]:
        """
        Import a Sei wallet from a mnemonic phrase.

        Args:
            mnemonic_phrase (str): The mnemonic phrase to import the wallet.

        Returns:
            Dict[str, str]: Wallet details (private key, public key, address).
        """
        try:
            wallet = LocalWallet.from_mnemonic(mnemonic_phrase, prefix="sei")
            logger.info(f"Wallet imported successfully for address: {wallet.address()} 🤑")
            return {
                "private_key": wallet._key.private_key.hex(),
                "public_key": wallet._key.public_key.hex(),
                "bech32_address": str(wallet.address())
            }
        except Exception as e:
            logger.error(f"Failed to import wallet: {e} 💥")
            raise ValueError(f"Invalid mnemonic: {e}")

    def _import_wallet_instance(self, mnemonic_phrase: str) -> LocalWallet:
        """
        Import a wallet instance for internal use.

        Args:
            mnemonic_phrase (str): The mnemonic phrase to import the wallet.

        Returns:
            LocalWallet: The imported wallet instance.
        """
        try:
            return LocalWallet.from_mnemonic(mnemonic_phrase, prefix="sei")
        except Exception as e:
            logger.error(f"Failed to import wallet instance: {e} 💥")
            raise ValueError(f"Invalid mnemonic: {e}")

# Transaction Class
class SeiTransaction:
    """
    🔥 SeiTransaction: A lit transaction handler for the Sei blockchain 🔥

    Features:
    - Build, sign, and broadcast token transfer transactions
    - Check transaction status
    - Automatic RPC node failover
    """
    def __init__(self, rpc_nodes: List[str], chain_id: str, wallet: LocalWallet):
        self.rpc_nodes = rpc_nodes
        self.current_rpc_index = 0
        self.current_rpc_url = self.rpc_nodes[self.current_rpc_index]
        self.chain_id = chain_id
        self.network_config = NetworkConfig(
            url=self.current_rpc_url,
            chain_id=chain_id,
            fee_minimum_gas_price=0.1,
            fee_denomination="usei",
            staking_denomination="usei"
        )
        self.client = LedgerClient(self.network_config)
        self.wallet = wallet

    async def _validate_rpc(self, rpc_url: str) -> bool:
        """Validate the RPC URL and check if the node is reachable."""
        try:
            parsed = urlparse(rpc_url)
            if not any(parsed.scheme.startswith(prefix) for prefix in ['rest+https', 'rest+http', 'grpc+https', 'grpc+http']):
                logger.error(f"Invalid RPC URL format: {rpc_url} - URL must start with rest+https://, rest+http://, grpc+https://, or grpc+http:// ❌")
                return False

            # Remove the prefix for the health check
            clean_url = rpc_url.replace('rest+', '').replace('grpc+', '')
            
            # Remove trailing slash if present
            clean_url = clean_url.rstrip('/')
            
            # Try different health check endpoints
            health_endpoints = ['/health', '/status', '/abci_info']
            
            async with aiohttp.ClientSession() as session:
                for endpoint in health_endpoints:
                    try:
                        async with session.get(f"{clean_url}{endpoint}", timeout=5) as resp:
                            if resp.status == 200:
                                return True
                    except:
                        continue
                        
                # If none of the health endpoints work, try a basic connection test
                async with session.get(clean_url, timeout=5) as resp:
                    return resp.status == 200
                    
            return False
        except Exception as e:
            logger.warning(f"RPC node {rpc_url} is not reachable: {e} 📡")
            return False
            return False

    async def _switch_to_next_rpc(self):
        """Switch to the next RPC node in the list if the current one fails."""
        self.current_rpc_index = (self.current_rpc_index + 1) % len(self.rpc_nodes)
        self.current_rpc_url = self.rpc_nodes[self.current_rpc_index]
        logger.info(f"Switching to RPC node: {self.current_rpc_url} 🔄")
        self.network_config = NetworkConfig(rpc_url=self.current_rpc_url, chain_id=self.chain_id)
        self.client = LedgerClient(self.network_config)

    async def build_and_sign_tx(self, to_address: str, amount: float, denom: str = "usei") -> Dict[str, Any]:
        """
        Build and sign a transaction for token transfer.

        Args:
            to_address (str): The recipient's address.
            amount (float): The amount of tokens to send.
            denom (str): The denomination of the tokens (default: "usei").

        Returns:
            Dict[str, Any]: The signed transaction.
        """
        for _ in range(len(self.rpc_nodes)):
            try:
                amount_wei = int(amount * 1e6)  # Convert to wei (Sei uses 6 decimals)
                tx = self.client.send_tokens(to_address, amount_wei, denom, self.wallet)
                logger.info(f"Transaction built and signed for {amount} {denom} to {to_address} ✍️")
                return tx
            except Exception as e:
                logger.error(f"Failed to build/sign transaction with {self.current_rpc_url}: {e} 💥")
                if "connection" in str(e).lower():
                    await self._switch_to_next_rpc()
                else:
                    raise
        raise ValueError("All RPC nodes failed to build/sign the transaction. 🚫")

    async def broadcast_tx(self, signed_tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Broadcast a signed transaction to the Sei network.

        Args:
            signed_tx (Dict[str, Any]): The signed transaction.

        Returns:
            Dict[str, Any]: The broadcast result.
        """
        for _ in range(len(self.rpc_nodes)):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"{self.current_rpc_url}/broadcast", json=signed_tx, timeout=10) as resp:
                        result = await resp.json()
                        logger.info(f"Transaction broadcasted successfully: {result} 📡")
                        return result
            except Exception as e:
                logger.error(f"Failed to broadcast transaction with {self.current_rpc_url}: {e} 💥")
                if "connection" in str(e).lower():
                    await self._switch_to_next_rpc()
                else:
                    raise
        raise ValueError("All RPC nodes failed to broadcast the transaction. 🚫")

    async def check_tx_status(self, tx_hash: str) -> Dict[str, Any]:
        """
        Check the status of a transaction by its hash.

        Args:
            tx_hash (str): The transaction hash.

        Returns:
            Dict[str, Any]: The transaction status.
        """
        for _ in range(len(self.rpc_nodes)):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.current_rpc_url}/tx/{tx_hash}", timeout=10) as resp:
                        status = await resp.json()
                        logger.info(f"Transaction status checked: {status} 🔍")
                        return status
            except Exception as e:
                logger.error(f"Failed to check transaction status with {self.current_rpc_url}: {e} 💥")
                if "connection" in str(e).lower():
                    await self._switch_to_next_rpc()
                else:
                    raise
        raise ValueError("All RPC nodes failed to check transaction status. 🚫")

# DeFi Data Class
class DeFiData:
    """
    🔥 DeFiData: A lit DeFi data fetcher for the Sei blockchain 🔥

    Features:
    - Fetch real-time token prices (DexScreener, CoinGecko)
    - Fetch trading pair data (liquidity, volume)
    """
    async def get_token_price(self, token_address: str, source: str = "dexscreener") -> Dict[str, Any]:
        """
        Fetch the real-time price and trading data of a token.

        Args:
            token_address (str): The token contract address.
            source (str): The price source ("dexscreener" or "coingecko").

        Returns:
            Dict[str, Any]: Token price and trading data.
        """
        try:
            if source.lower() == "dexscreener":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://api.dexscreener.com/latest/dex/tokens/{token_address}",
                        timeout=10
                    ) as resp:
                        if resp.status != 200:
                            logger.error(f"DexScreener API error: {resp.status} ❌")
                            raise ValueError(f"API returned status {resp.status}")
                        data = await resp.json()
                        pairs = data.get("pairs", [])
                        if not pairs:
                            return {
                                "price": 0.0,
                                "volume24h": 0.0,
                                "liquidity": 0.0,
                                "priceChange24h": "0.00",
                                "marketCap": 0.0,
                                "fdv": 0.0
                            }
                        
                        pair = pairs[0]
                        result = {
                            "price": float(pair.get("priceUsd", 0.0)),
                            "volume24h": float(pair.get("volume", {}).get("h24", 0.0)),
                            "liquidity": float(pair.get("liquidity", {}).get("usd", 0.0)),
                            "priceChange24h": pair.get("priceChange", {}).get("h24", "0.00"),
                            "marketCap": float(pair.get("marketCap", 0.0)),
                            "fdv": float(pair.get("fdv", 0.0))
                        }
                        logger.info(f"Fetched token data from DexScreener: {result} 💰")
                        return result
            elif source.lower() == "coingecko":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://api.coingecko.com/api/v3/simple/price?ids=sei&vs_currencies=usd",
                        timeout=10
                    ) as resp:
                        if resp.status != 200:
                            logger.error(f"CoinGecko API error: {resp.status} ❌")
                            raise ValueError(f"API returned status {resp.status}")
                        data = await resp.json()
                        price = data.get("sei", {}).get("usd", 0.0)
                        logger.info(f"Fetched {token_symbol} price from CoinGecko: ${price} 💰")
                        return float(price) if price else 0.0
            else:
                raise ValueError(f"Unsupported price source: {source} 🚫")
        except Exception as e:
            logger.error(f"Failed to fetch token price from {source}: {e} 💥")
            return 0.0

    async def get_dex_trading_data(self, pair_address: str) -> Dict[str, float]:
        """
        Fetch liquidity and volume data for a trading pair.

        Args:
            pair_address (str): The address of the trading pair.

        Returns:
            Dict[str, float]: Trading data (liquidity, volume, pair).
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.dexscreener.com/latest/dex/pairs/{pair_address}",
                    timeout=10
                ) as resp:
                    if resp.status != 200:
                        logger.error(f"DexScreener API error: {resp.status} ❌")
                        raise ValueError(f"API returned status {resp.status}")
                    data = await resp.json()
                    pair = data.get("pair", {})
                    result = {
                        "liquidity": float(pair.get("liquidity", {}).get("usd", 0.0)),
                        "volume": float(pair.get("volume", {}).get("h24", 0.0)),
                        "pair": pair.get("baseToken", {}).get("symbol", "") + "/" + pair.get("quoteToken", {}).get("symbol", "")
                    }
                    logger.info(f"Fetched trading data for pair {pair_address}: {result} 📊")
                    return result
        except Exception as e:
            logger.warning(f"Failed to fetch trading data for {pair_address}: {e} 💥")
            return {"liquidity": 0.0, "volume": 0.0, "pair": "N/A"}

# AI Engine Class
class AIEngine:
    """
    🔥 AIEngine: A lit AI engine for market analysis, trading signals, and chatbots 🔥

    Features:
    - Market analysis with real-time price data
    - Trading signals based on historical data
    - Interactive chatbot with DeFi data integration
    - Supports OpenAI, Anthropic, Google Gemini, and Groq
    """
    def __init__(self, model_name: str, api_key: str, system_prompt: str, max_tokens: int, temperature: float, feature_type: str, memory: Optional[ConversationBufferMemory] = None):
        self.model_name = model_name
        self.feature_type = feature_type
        self.system_prompt = system_prompt or self.get_default_prompt()
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.memory = memory or ConversationBufferMemory(return_messages=True)

        try:
            if model_name == "openai":
                self.llm = ChatOpenAI(model="gpt-4o", api_key=api_key, max_tokens=max_tokens, temperature=temperature)
            elif model_name == "claude":
                self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=api_key, max_tokens=max_tokens, temperature=temperature)
            elif model_name == "gemini":
                self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=api_key, max_tokens=max_tokens, temperature=temperature)
            elif model_name == "groq":
                self.llm = ChatGroq(model="mixtral-8x7b-32768", api_key=api_key, max_tokens=max_tokens, temperature=temperature)
            else:
                raise ValueError(f"Unsupported model: {model_name}. Supported models are: 'openai', 'claude', 'gemini', 'groq'. 🚫")
        except Exception as e:
            logger.error(f"Failed to initialize AI model {model_name}: {e} 💥")
            raise

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.chain = ConversationChain(llm=self.llm, memory=self.memory, prompt=self.prompt)
        logger.info(f"AI engine initialized with model {model_name} for {feature_type} 🤖")

    def get_default_prompt(self) -> str:
        """Get the default system prompt based on the feature type."""
        prompts = {
            "market_analysis": "You are a crypto market analyst. Analyze the provided real-time price data and historical trends to identify market movements. Be concise and data-driven. 📈",
            "trading_signals": "You are a trading signal generator for Sei blockchain. Based on historical price data and trends, generate buy/sell signals with confidence levels. Be precise. 📉",
            "chatbot": "You are a helpful crypto assistant on the Sei blockchain. Answer user queries about tokens, NFTs, market trends, wallets, and DeFi using real-time data. Be friendly, informative, and concise. 💬"
        }
        return prompts.get(self.feature_type, "You are a helpful assistant.")

    async def run(self, input_data: str, defi_data: Optional[float] = None) -> str:
        """
        Run the AI model with optional DeFi data integration.

        Args:
            input_data (str): The input data for the AI model.
            defi_data (float, optional): Real-time DeFi data (e.g., token price).

        Returns:
            str: The AI model's response.
        """
        try:
            if defi_data and self.feature_type == "chatbot":
                input_data = f"{input_data} (Current SEI price: ${defi_data} USD)"
            response = await self.chain.arun(input=input_data)
            logger.info(f"AI response generated: {response} ✨")
            return response.strip()
        except Exception as e:
            logger.error(f"AI engine error for {self.model_name}: {e} 💥")
            return f"Sorry, I encountered an error processing your request with {self.model_name}."

# Custom Chatbot Class
class CustomChatbot:
    """
    🔥 CustomChatbot: A lit custom chatbot builder for the Sei blockchain 🔥

    Features:
    - Build custom chatbots with user-defined intents
    - Integrate real-time DeFi data
    - Add intents dynamically
    """
    def __init__(self, model_name: str, api_key: str, intents: Optional[Dict[str, Callable]] = None, system_prompt: Optional[str] = None, max_tokens: int = 300, temperature: float = 0.7, defi_data_fetcher: Optional[DeFiData] = None):
        self.engine = AIEngine(
            model_name=model_name,
            api_key=api_key,
            system_prompt=system_prompt or "You are a custom Sei chatbot. Follow the intents provided. 💬",
            max_tokens=max_tokens,
            temperature=temperature,
            feature_type="chatbot"
        )
        self.intents = intents or {}
        self.defi_data_fetcher = defi_data_fetcher or DeFiData()
        logger.info(f"Custom chatbot initialized with model {model_name} 🤖")

    async def process_message(self, message: str) -> str:
        """
        Process a user message based on defined intents.

        Args:
            message (str): The user's message.

        Returns:
            str: The chatbot's response.
        """
        try:
            for intent, handler in self.intents.items():
                if intent.lower() in message.lower():
                    defi_data = await self.defi_data_fetcher.get_token_price("SEI") if "price" in intent.lower() else None
                    handler_response = await handler(message, defi_data)
                    if handler_response:
                        return handler_response
                    return await self.engine.run(message, defi_data)
            defi_data = await self.defi_data_fetcher.get_token_price("SEI")
            return await self.engine.run(message, defi_data)
        except Exception as e:
            logger.error(f"Chatbot processing error: {e} 💥")
            return "Sorry, I couldn’t process your message. 😓"

    def add_intent(self, intent_name: str, handler: Callable):
        """
        Add a custom intent with a handler function.

        Args:
            intent_name (str): The name of the intent.
            handler (Callable): The handler function for the intent.
        """
        self.intents[intent_name.lower()] = handler
        logger.info(f"Added intent: {intent_name} to chatbot 🎯")

# Main SDK Class
class SeiAISDK:
    """
    🔥 SeiAISDK: A lit AI-powered SDK for the Sei blockchain 🔥

    Features:
    - Import wallets using mnemonic phrases (wallet creation not supported)
    - Send tokens and perform P2P token swaps
    - Fetch real-time DeFi data (token prices, trading pairs)
    - AI-powered market analysis, trading signals, and chatbots
    - Custom chatbot development with real-time data integration
    - Flexible RPC node support with automatic fallback
    - Flexible AI agent selection (OpenAI, Anthropic, Gemini, Groq)
    """
    def __init__(self, rpc_nodes: Optional[List[str]] = None, chain_id: str = "atlantic-2", mnemonic: str = None, ai_config: Optional[Dict[str, Any]] = None, ai_agents_config: Optional[Dict[str, Dict[str, Any]]] = None):
        """
        Initialize the SDK with user-provided RPC nodes and AI configuration.

        Args:
            rpc_nodes (List[str], optional): List of RPC node URLs for Sei blockchain. Defaults to public Sei testnet nodes.
            chain_id (str): The chain ID for the Sei network (e.g., 'atlantic-2' for testnet, 'pacific-1' for mainnet).
            mnemonic (str): The mnemonic phrase for wallet import (required for transaction operations).
            ai_config (dict, optional): Configuration for a single AI agent.
            ai_agents_config (dict, optional): Configuration for multiple AI agents for different tasks.
        """
        self.rpc_nodes = rpc_nodes or DEFAULT_RPC_NODES
        if not self.rpc_nodes:
            raise ValueError("At least one RPC node must be provided. 🚫")
        self.chain_id = chain_id

        # Validate RPC nodes
        async def validate_and_set_rpc():
            valid_nodes = []
            for node in self.rpc_nodes:
                try:
                    if await SeiTransaction(self.rpc_nodes, self.chain_id, None)._validate_rpc(node):
                        valid_nodes.append(node)
                    else:
                        logger.warning(f"RPC node {node} is not reachable. 📡")
                except Exception as e:
                    logger.warning(f"RPC node {node} validation failed: {e} 💥")

            if not valid_nodes:
                raise ValueError("No reachable RPC nodes provided. Please provide a valid RPC node URL. 🚫")

            self.rpc_nodes = valid_nodes

        loop = asyncio.get_event_loop()
        loop.run_until_complete(validate_and_set_rpc())

        # Initialize wallet and transaction handler
        self.wallet = SeiWallet()
        if mnemonic is None:
            logger.warning("Mnemonic not provided. Transaction operations (e.g., sending tokens, P2P swaps) will not be available. ⚠️")
            self.wallet_instance = None
            self.tx_handler = None
        else:
            self.wallet_instance = self.wallet._import_wallet_instance(mnemonic)
            self.tx_handler = SeiTransaction(self.rpc_nodes, self.chain_id, self.wallet_instance)

        # Initialize DeFi data fetcher
        self.defi_data = DeFiData()

        # Initialize AI configurations
        self.ai_config = ai_config or {
            "model": "groq",
            "api_key": None,
            "system_prompt": None,
            "max_tokens": 300,
            "temperature": 0.7
        }

        self.ai_agents_config = ai_agents_config or {
            "market_analysis": self.ai_config,
            "trading_signals": self.ai_config,
            "chatbot": self.ai_config
        }
        logger.info("SeiAISDK initialized successfully! 🚀")

    def _get_ai_config(self, feature_type: str) -> Dict[str, Any]:
        """Get the AI configuration for a specific feature type."""
        return self.ai_agents_config.get(feature_type, self.ai_config)

    async def import_wallet(self, mnemonic_phrase: str) -> Dict[str, str]:
        """
        Import a Sei wallet from a mnemonic phrase.

        Args:
            mnemonic_phrase (str): The mnemonic phrase to import the wallet.

        Returns:
            Dict[str, str]: Wallet details (private key, public key, address).
        """
        wallet_info = self.wallet.import_wallet(mnemonic_phrase)
        self.wallet_instance = self.wallet._import_wallet_instance(mnemonic_phrase)
        self.tx_handler = SeiTransaction(self.rpc_nodes, self.chain_id, self.wallet_instance)
        return wallet_info

    async def send_tokens(self, to_address: str, amount: float, denom: str = "usei") -> Dict[str, Any]:
        """
        Send tokens to another address on the Sei blockchain.

        Args:
            to_address (str): The recipient's Sei address.
            amount (float): The amount of tokens to send.
            denom (str): The denomination of the tokens (default: "usei").

        Returns:
            Dict[str, Any]: Transaction result.
        """
        if not self.tx_handler:
            raise ValueError("Wallet not imported. Provide a mnemonic during initialization or use import_wallet. 🚫")
        signed_tx = await self.tx_handler.build_and_sign_tx(to_address, amount, denom)
        return await self.tx_handler.broadcast_tx(signed_tx)

    async def check_tx_status(self, tx_hash: str) -> Dict[str, Any]:
        """
        Check the status of a transaction by its hash.

        Args:
            tx_hash (str): The transaction hash.

        Returns:
            Dict[str, Any]: Transaction status.
        """
        if not self.tx_handler:
            raise ValueError("Wallet not imported. Provide a mnemonic during initialization or use import_wallet. 🚫")
        return await self.tx_handler.check_tx_status(tx_hash)

    async def swap_tokens_p2p(self, counterparty_address: str, token_to_send: str, amount_to_send: float, token_to_receive: str, amount_to_receive: float, denom_to_send: str = "usei", denom_to_receive: str = "tokenx") -> Dict[str, Any]:
        """
        Perform a P2P token swap with another user (trust-based).

        Args:
            counterparty_address (str): The address of the counterparty.
            token_to_send (str): The token to send.
            amount_to_send (float): The amount of tokens to send.
            token_to_receive (str): The token to receive.
            amount_to_receive (float): The amount of tokens to receive.
            denom_to_send (str): The denomination of the token to send (default: "usei").
            denom_to_receive (str): The denomination of the token to receive (default: "tokenx").

        Returns:
            Dict[str, Any]: Swap result.
        """
        if not self.tx_handler:
            raise ValueError("Wallet not imported. Provide a mnemonic during initialization or use import_wallet. 🚫")

        try:
            logger.info(f"Sending {amount_to_send} {denom_to_send} to {counterparty_address}... 💸")
            tx_hash_send = await self.send_tokens(counterparty_address, amount_to_send, denom_to_send)
            logger.info(f"Sent tokens. Tx Hash: {tx_hash_send} 🚀")

            tx_status = await self.check_tx_status(tx_hash_send)
            if tx_status.get("code") == 0:  # Success code in Cosmos
                logger.info(f"Transaction confirmed. Status: {tx_status} ✅")
            else:
                raise ValueError(f"Initial transfer failed. Status: {tx_status} ❌")

            logger.info(f"Waiting for {counterparty_address} to send {amount_to_receive} {denom_to_receive} to {self.wallet_instance.address()}... ⏳")
            print(f"Waiting for {counterparty_address} to send {amount_to_receive} {denom_to_receive} to {self.wallet_instance.address()}...")
            print("Counterparty must complete their transfer manually. This swap is not trustless. 🤝")

            return {
                "tx_hash_send": tx_hash_send,
                "status": "pending_counterparty_transfer",
                "message": f"Waiting for {counterparty_address} to send {amount_to_receive} {denom_to_receive}"
            }
        except Exception as e:
            logger.error(f"P2P swap failed: {e} 💥")
            raise

    async def get_token_price(self, token_symbol: str, source: str = "dexscreener") -> float:
        """
        Fetch the real-time price of a token.

        Args:
            token_symbol (str): The token symbol (e.g., "SEI").
            source (str): The price source ("dexscreener" or "coingecko").

        Returns:
            float: The token price in USD.
        """
        return await self.defi_data.get_token_price(token_symbol, source)

    async def get_dex_trading_data(self, pair_address: str) -> Dict[str, float]:
        """
        Fetch liquidity and volume data for a trading pair.

        Args:
            pair_address (str): The address of the trading pair.

        Returns:
            Dict[str, float]: Trading data (liquidity, volume, pair).
        """
        return await self.defi_data.get_dex_trading_data(pair_address)

    async def analyze_market(self, price_data: Dict[str, Any]) -> str:
        """
        Analyze market trends using AI.

        Args:
            price_data (Dict[str, Any]): Price data for analysis.

        Returns:
            str: Market analysis result.
        """
        config = self._get_ai_config("market_analysis")
        engine = AIEngine(
            model_name=config["model"],
            api_key=config["api_key"],
            system_prompt=config.get("system_prompt"),
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            feature_type="market_analysis"
        )
        return await engine.run(str(price_data))

    async def generate_trading_signals(self, historical_data: list) -> str:
        """
        Generate trading signals using AI.

        Args:
            historical_data (list): Historical price data.

        Returns:
            str: Trading signals.
        """
        config = self._get_ai_config("trading_signals")
        engine = AIEngine(
            model_name=config["model"],
            api_key=config["api_key"],
            system_prompt=config.get("system_prompt"),
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            feature_type="trading_signals"
        )
        return await engine.run(str(historical_data))

    async def chat_with_ai(self, message: str) -> str:
        """
        Interact with the default AI chatbot.

        Args:
            message (str): User message.

        Returns:
            str: Chatbot response.
        """
        config = self._get_ai_config("chatbot")
        engine = AIEngine(
            model_name=config["model"],
            api_key=config["api_key"],
            system_prompt=config.get("system_prompt"),
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            feature_type="chatbot"
        )
        return await engine.run(message, defi_data=await self.defi_data.get_token_price("SEI"))

    def create_custom_chatbot(self, model_name: Optional[str] = None, api_key: Optional[str] = None, intents: Optional[Dict[str, Callable]] = None, system_prompt: Optional[str] = None, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> CustomChatbot:
        """
        Create a custom chatbot instance for users to build their own bots.

        Args:
            model_name (str, optional): AI model name.
            api_key (str, optional): API key for the AI model.
            intents (Dict[str, Callable], optional): Custom intents for the chatbot.
            system_prompt (str, optional): Custom system prompt.
            max_tokens (int, optional): Maximum tokens for AI responses.
            temperature (float, optional): Temperature for AI responses.

        Returns:
            CustomChatbot: A custom chatbot instance.
        """
        config = self._get_ai_config("chatbot")
        return CustomChatbot(
            model_name=model_name or config["model"],
            api_key=api_key or config["api_key"],
            intents=intents,
            system_prompt=system_prompt or config.get("system_prompt"),
            max_tokens=max_tokens or config["max_tokens"],
            temperature=temperature or config["temperature"],
            defi_data_fetcher=self.defi_data
        )


seiai = SeiAISDK
__all__ = ['seiai']