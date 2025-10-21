"""
MT5 Data Fetcher
Retrieves OHLCV and tick data from MetaTrader 5 with validation and error handling
"""
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum

from .connection import MT5Connection, ensure_connection, MT5ConnectionError
from .validator import DataValidator
from config.settings import DataConfig


class Timeframe(Enum):
    """MT5 Timeframe enumeration"""
    M1 = mt5.TIMEFRAME_M1
    M2 = mt5.TIMEFRAME_M2
    M3 = mt5.TIMEFRAME_M3
    M4 = mt5.TIMEFRAME_M4
    M5 = mt5.TIMEFRAME_M5
    M6 = mt5.TIMEFRAME_M6
    M10 = mt5.TIMEFRAME_M10
    M12 = mt5.TIMEFRAME_M12
    M15 = mt5.TIMEFRAME_M15
    M20 = mt5.TIMEFRAME_M20
    M30 = mt5.TIMEFRAME_M30
    H1 = mt5.TIMEFRAME_H1
    H2 = mt5.TIMEFRAME_H2
    H3 = mt5.TIMEFRAME_H3
    H4 = mt5.TIMEFRAME_H4
    H6 = mt5.TIMEFRAME_H6
    H8 = mt5.TIMEFRAME_H8
    H12 = mt5.TIMEFRAME_H12
    D1 = mt5.TIMEFRAME_D1
    W1 = mt5.TIMEFRAME_W1
    MN1 = mt5.TIMEFRAME_MN1
    
    @classmethod
    def from_string(cls, timeframe_str: str) -> 'Timeframe':
        """Convert string to Timeframe enum"""
        return cls[timeframe_str.upper()]
    
    @classmethod
    def to_minutes(cls, timeframe: 'Timeframe') -> int:
        """Convert timeframe to minutes"""
        mapping = {
            cls.M1: 1, cls.M2: 2, cls.M3: 3, cls.M4: 4, cls.M5: 5,
            cls.M6: 6, cls.M10: 10, cls.M12: 12, cls.M15: 15,
            cls.M20: 20, cls.M30: 30,
            cls.H1: 60, cls.H2: 120, cls.H3: 180, cls.H4: 240,
            cls.H6: 360, cls.H8: 480, cls.H12: 720,
            cls.D1: 1440, cls.W1: 10080, cls.MN1: 43200
        }
        return mapping.get(timeframe, 0)


class MT5DataFetcher:
    """
    Fetches and manages market data from MetaTrader 5
    
    Features:
    - OHLCV data retrieval
    - Tick data retrieval
    - Symbol information
    - Data validation
    - Error handling and retries
    - Rate limiting compliance
    """
    
    def __init__(self, connection: Optional[MT5Connection] = None):
        """
        Initialize data fetcher
        
        Args:
            connection: MT5Connection instance (optional, uses global MT5 if None)
        """
        print(f"[DEBUG] MT5DataFetcher.__init__() called")
        print(f"[DEBUG]   connection parameter = {connection}")
        print(f"[DEBUG]   Will use: {'Old MT5Connection object' if connection else 'Global MT5 API'}")
        
        self.connection = connection  # None means use global MT5 API
        self.validator = DataValidator()
        
        # Check if MT5 is initialized
        if connection is None:
            terminal_info = mt5.terminal_info()
            print(f"[DEBUG]   Global MT5 terminal_info = {terminal_info}")
            if terminal_info:
                print(f"[DEBUG]   ✓ MT5 globally initialized")
                print(f"[DEBUG]   Terminal: {terminal_info.name}")
                print(f"[DEBUG]   Company: {terminal_info.company}")
            else:
                print(f"[DEBUG]   ✗ MT5 NOT globally initialized!")
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_bars_fetched": 0,
            "total_ticks_fetched": 0,
        }
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get symbol information
        
        Args:
            symbol: Trading symbol (e.g., "EURUSD")
            
        Returns:
            Optional[Dict]: Symbol information or None if failed
        """
        try:
            info = mt5.symbol_info(symbol)
            if info is None:
                return None
            
            return {
                "name": info.name,
                "description": info.description,
                "point": info.point,
                "digits": info.digits,
                "spread": info.spread,
                "trade_contract_size": info.trade_contract_size,
                "trade_tick_value": info.trade_tick_value,
                "trade_tick_size": info.trade_tick_size,
                "bid": info.bid,
                "ask": info.ask,
                "last": info.last,
                "volume_min": info.volume_min,
                "volume_max": info.volume_max,
                "volume_step": info.volume_step,
                "currency_base": info.currency_base,
                "currency_profit": info.currency_profit,
                "currency_margin": info.currency_margin,
                "visible": info.visible,
                "select": info.select,
            }
        except Exception as e:
            print(f"Error getting symbol info for {symbol}: {str(e)}")
            return None
    
    @ensure_connection
    def get_symbol_tick(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get latest tick for symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Optional[Dict]: Latest tick data or None
        """
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return None
            
            return {
                "time": datetime.fromtimestamp(tick.time),
                "bid": tick.bid,
                "ask": tick.ask,
                "last": tick.last,
                "volume": tick.volume,
                "spread": tick.ask - tick.bid,
            }
        except Exception as e:
            print(f"Error getting tick for {symbol}: {str(e)}")
            return None
    
    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "H1",
        count: int = 1000,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        validate: bool = True
    ) -> Optional[pd.DataFrame]:
        """
        Get OHLCV data for a symbol
        
        Args:
            symbol: Trading symbol (e.g., "EURUSD")
            timeframe: Timeframe string (e.g., "H1", "M15")
            count: Number of bars to retrieve
            start_date: Start date for data (optional)
            end_date: End date for data (optional)
            validate: Whether to validate data
            
        Returns:
            Optional[pd.DataFrame]: OHLCV data or None if failed
        """
        self.stats["total_requests"] += 1
        
        try:
            # Convert timeframe string to MT5 constant
            tf = Timeframe.from_string(timeframe)
            
            # Get data
            if start_date and end_date:
                rates = mt5.copy_rates_range(symbol, tf.value, start_date, end_date)
            elif start_date:
                rates = mt5.copy_rates_from(symbol, tf.value, start_date, count)
            else:
                rates = mt5.copy_rates_from_pos(symbol, tf.value, 0, count)
            
            if rates is None or len(rates) == 0:
                self.stats["failed_requests"] += 1
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            # Rename columns for consistency
            df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'tick_volume': 'Volume',
                'spread': 'Spread',
                'real_volume': 'RealVolume'
            }, inplace=True)
            
            # Select relevant columns
            columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if 'Spread' in df.columns:
                columns.append('Spread')
            if 'RealVolume' in df.columns:
                columns.append('RealVolume')
            
            df = df[columns]
            
            # Validate data if requested
            if validate:
                is_valid, issues = self.validator.validate_ohlcv(df, symbol, timeframe)
                if not is_valid:
                    print(f"⚠️  Data validation issues for {symbol} {timeframe}: {issues}")
                    # Attempt to clean data
                    df = self.validator.clean_ohlcv(df)
            
            # Update statistics
            self.stats["successful_requests"] += 1
            self.stats["total_bars_fetched"] += len(df)
            
            return df
            
        except Exception as e:
            self.stats["failed_requests"] += 1
            print(f"Error fetching OHLCV for {symbol} {timeframe}: {str(e)}")
            return None
    
    def get_ticks(
        self,
        symbol: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        count: int = 10000,
        flags: int = mt5.COPY_TICKS_ALL
    ) -> Optional[pd.DataFrame]:
        """
        Get tick data for a symbol
        
        Args:
            symbol: Trading symbol
            start_date: Start date for ticks
            end_date: End date for ticks (optional)
            count: Maximum number of ticks
            flags: Tick flags (ALL, INFO, TRADE)
            
        Returns:
            Optional[pd.DataFrame]: Tick data or None
        """
        self.stats["total_requests"] += 1
        
        try:
            if end_date:
                ticks = mt5.copy_ticks_range(symbol, start_date, end_date, flags)
            else:
                ticks = mt5.copy_ticks_from(symbol, start_date, count, flags)
            
            if ticks is None or len(ticks) == 0:
                self.stats["failed_requests"] += 1
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(ticks)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            self.stats["successful_requests"] += 1
            self.stats["total_ticks_fetched"] += len(df)
            
            return df
            
        except Exception as e:
            self.stats["failed_requests"] += 1
            print(f"Error fetching ticks for {symbol}: {str(e)}")
            return None
    
    def get_multi_timeframe_data(
        self,
        symbol: str,
        timeframes: List[str],
        count: int = 1000,
        validate: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Get data for multiple timeframes
        
        Args:
            symbol: Trading symbol
            timeframes: List of timeframe strings
            count: Number of bars per timeframe
            validate: Whether to validate data
            
        Returns:
            Dict[str, pd.DataFrame]: Data for each timeframe
        """
        result = {}
        
        for tf in timeframes:
            df = self.get_ohlcv(symbol, tf, count, validate=validate)
            if df is not None:
                result[tf] = df
        
        return result
    
    def get_available_symbols(self, group: str = "*") -> List[str]:
        """
        Get list of available symbols
        
        Args:
            group: Symbol group filter (default: all)
            
        Returns:
            List[str]: List of symbol names
        """
        try:
            symbols = mt5.symbols_get(group)
            if symbols is None:
                return []
            return [s.name for s in symbols if s.visible]
        except Exception as e:
            print(f"Error getting symbols: {str(e)}")
            return []
    
    def calculate_pip_value(self, symbol: str) -> Optional[float]:
        """
        Calculate pip value for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Optional[float]: Pip value or None
        """
        info = self.get_symbol_info(symbol)
        if info is None:
            return None
        
        point = info['point']
        digits = info['digits']
        
        # Most forex pairs have 5 digits (0.00001), pip is 0.0001
        if digits == 5 or digits == 3:
            pip_value = point * 10
        else:
            pip_value = point
        
        return pip_value
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get data fetcher statistics
        
        Returns:
            Dict: Statistics
        """
        success_rate = 0
        if self.stats["total_requests"] > 0:
            success_rate = (
                self.stats["successful_requests"] / self.stats["total_requests"] * 100
            )
        
        return {
            **self.stats,
            "success_rate": f"{success_rate:.2f}%",
        }
    
    def __repr__(self) -> str:
        return f"<MT5DataFetcher requests={self.stats['total_requests']} bars={self.stats['total_bars_fetched']}>"


if __name__ == "__main__":
    # Test data fetcher
    print("📊 Testing MT5 Data Fetcher...")
    
    try:
        from .connection import MT5Connection
        
        conn = MT5Connection()
        conn.connect()
        
        fetcher = MT5DataFetcher(conn)
        
        # Test symbol info
        info = fetcher.get_symbol_info("EURUSD")
        print(f"✓ Symbol Info: {info['name']} - Spread: {info['spread']}")
        
        # Test tick
        tick = fetcher.get_symbol_tick("EURUSD")
        print(f"✓ Latest Tick: Bid={tick['bid']}, Ask={tick['ask']}")
        
        # Test OHLCV
        df = fetcher.get_ohlcv("EURUSD", "H1", count=100)
        print(f"✓ OHLCV Data: {len(df)} bars retrieved")
        print(df.tail())
        
        # Test multi-timeframe
        mtf_data = fetcher.get_multi_timeframe_data(
            "EURUSD",
            ["M15", "H1", "H4"],
            count=50
        )
        print(f"✓ Multi-Timeframe: {list(mtf_data.keys())}")
        
        # Statistics
        stats = fetcher.get_statistics()
        print(f"✓ Statistics: {stats}")
        
        conn.disconnect()
        print("✓ Test completed successfully")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
