"""
Standalone MT5 Connector
Simple, direct connection to MetaTrader 5 with hardcoded test credentials
"""
import os
import MetaTrader5 as mt5
from datetime import datetime
from pathlib import Path


# Hardcoded test credentials - can be overridden by environment variables
MT5_LOGIN = int(os.getenv("MT5_LOGIN", "211744072") or 211744072)
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "dFbKaNLWQ53@9@Z")
MT5_SERVER = os.getenv("MT5_SERVER", "ExnessKE-MT5Trial9")
MT5_PATH = os.getenv("MT5_PATH", r"C:\Program Files\MetaTrader 5\terminal64.exe")
MT5_TIMEOUT = int(os.getenv("MT5_TIMEOUT", "60000"))


class MT5Connector:
    """Simple MT5 connection manager"""
    
    def __init__(self):
        self.login = MT5_LOGIN
        self.password = MT5_PASSWORD
        self.server = MT5_SERVER
        self.path = MT5_PATH
        self.timeout = MT5_TIMEOUT
        self.connected = False
        self.last_error = None
        self.connection_time = None
        
        # Debug logging
        print(f"[DEBUG] MT5Connector.__init__() - Created new connector instance")
        print(f"[DEBUG]   Login: {self.login}")
        print(f"[DEBUG]   Server: {self.server}")
        print(f"[DEBUG]   Path: {self.path}")
        
    def connect(self) -> tuple[bool, str]:
        """
        Connect to MT5
        
        Returns:
            tuple: (success: bool, message: str)
        """
        print("\n" + "="*60)
        print("MT5 CONNECTION ATTEMPT")
        print("="*60)
        
        # Step 1: Validate credentials
        print(f"\n[1/4] Validating credentials...")
        print(f"   Login: {self.login}")
        print(f"   Server: {self.server}")
        print(f"   Path: {self.path}")
        
        if not self.login or self.login == 0:
            msg = "❌ Invalid login"
            print(f"   {msg}")
            self.last_error = msg
            return False, msg
            
        if not self.password:
            msg = "❌ Invalid password"
            print(f"   {msg}")
            self.last_error = msg
            return False, msg
            
        if not self.server:
            msg = "❌ Invalid server"
            print(f"   {msg}")
            self.last_error = msg
            return False, msg
        
        print(f"   ✓ Credentials validated")
        
        # Step 2: Check MT5 package
        print(f"\n[2/4] Checking MetaTrader5 package...")
        try:
            version_info = mt5.version()
            if version_info:
                print(f"   ✓ MT5 package available (Build {version_info[0]})")
            else:
                print(f"   ✓ MT5 package available")
        except Exception as e:
            msg = f"❌ MetaTrader5 package error: {e}"
            print(f"   {msg}")
            self.last_error = msg
            return False, msg
        
        # Step 3: Initialize MT5
        print(f"\n[3/4] Initializing MT5 terminal...")
        
        # Try with path first
        if self.path and Path(self.path).exists():
            print(f"   Trying path: {self.path}")
            success = mt5.initialize(
                path=self.path,
                login=self.login,
                password=self.password,
                server=self.server,
                timeout=self.timeout
            )
        else:
            # Try common paths
            print(f"   Configured path not found, searching...")
            common_paths = [
                r"C:\Program Files\MetaTrader 5\terminal64.exe",
                r"C:\Program Files (x86)\MetaTrader 5\terminal.exe",
            ]
            
            found = False
            for path in common_paths:
                if Path(path).exists():
                    print(f"   Found MT5 at: {path}")
                    success = mt5.initialize(
                        path=path,
                        login=self.login,
                        password=self.password,
                        server=self.server,
                        timeout=self.timeout
                    )
                    found = True
                    break
            
            if not found:
                print(f"   No MT5 found in common locations, trying default...")
                success = mt5.initialize()
        
        if not success:
            error = mt5.last_error()
            error_code = error[0] if error else -1
            error_text = error[1] if error and len(error) > 1 else "Unknown error"
            msg = f"❌ Initialization failed - Code {error_code}: {error_text}"
            print(f"   {msg}")
            
            # Provide helpful tips
            if error_code == 1:
                print(f"   💡 MT5 not installed or wrong path")
            elif error_code == 5:
                print(f"   💡 Old MT5 version - please update")
            
            self.last_error = msg
            return False, msg
        
        print(f"   ✓ MT5 initialized successfully")
        
        # Step 4: Login
        print(f"\n[4/4] Logging in to {self.server}...")
        
        login_success = mt5.login(self.login, password=self.password, server=self.server)
        
        if not login_success:
            error = mt5.last_error()
            error_code = error[0] if error else -1
            error_text = error[1] if error and len(error) > 1 else "Unknown error"
            msg = f"❌ Login failed - Code {error_code}: {error_text}"
            print(f"   {msg}")
            
            # Provide helpful tips
            if error_code == 10004:
                print(f"   💡 No connection to server - check internet/firewall")
            elif error_code == 10013:
                print(f"   💡 Invalid credentials or account expired")
            elif error_code == 10014:
                print(f"   💡 Server '{self.server}' not found")
            
            mt5.shutdown()
            self.last_error = msg
            return False, msg
        
        # Verify account info
        account = mt5.account_info()
        if account is None:
            msg = "❌ Failed to get account info"
            print(f"   {msg}")
            mt5.shutdown()
            self.last_error = msg
            return False, msg
        
        # Success!
        self.connected = True
        self.connection_time = datetime.now()
        self.last_error = None
        
        print(f"   ✓ Login successful!")
        print(f"\n" + "="*60)
        print("CONNECTION SUCCESSFUL")
        print("="*60)
        print(f"Account: {account.login}")
        print(f"Server: {account.server}")
        print(f"Name: {account.name}")
        print(f"Balance: {account.balance} {account.currency}")
        print(f"Leverage: 1:{account.leverage}")
        print(f"Company: {account.company}")
        print("="*60 + "\n")
        
        return True, f"Connected as {account.login} on {account.server}"
    
    def disconnect(self) -> tuple[bool, str]:
        """
        Disconnect from MT5
        
        Returns:
            tuple: (success: bool, message: str)
        """
        print("\n" + "="*60)
        print("MT5 DISCONNECTION")
        print("="*60)
        
        try:
            mt5.shutdown()
            self.connected = False
            self.connection_time = None
            msg = "✓ Disconnected successfully"
            print(msg)
            print("="*60 + "\n")
            return True, msg
        except Exception as e:
            msg = f"❌ Disconnect error: {str(e)}"
            print(msg)
            print("="*60 + "\n")
            self.last_error = msg
            return False, msg
    
    def is_connected(self) -> bool:
        """
        Check if connected to MT5
        
        Returns:
            bool: Connection status
        """
        if not self.connected:
            return False
        
        try:
            account = mt5.account_info()
            if account is None:
                self.connected = False
                return False
            return True
        except:
            self.connected = False
            return False
    
    def get_account_info(self) -> dict:
        """
        Get account information
        
        Returns:
            dict: Account information or None
        """
        if not self.is_connected():
            return None
        
        try:
            account = mt5.account_info()
            if account is None:
                return None
            
            return {
                'login': account.login,
                'server': account.server,
                'name': account.name,
                'balance': account.balance,
                'equity': account.equity,
                'margin': account.margin,
                'margin_free': account.margin_free,
                'currency': account.currency,
                'leverage': account.leverage,
                'company': account.company,
            }
        except Exception as e:
            print(f"Error getting account info: {e}")
            return None
    
    def get_status(self) -> dict:
        """
        Get connection status
        
        Returns:
            dict: Connection status information
        """
        return {
            'connected': self.is_connected(),
            'login': self.login,
            'server': self.server,
            'connection_time': self.connection_time,
            'last_error': self.last_error,
        }


# Global connector instance
_connector = None


def get_connector() -> MT5Connector:
    """Get global MT5 connector instance"""
    global _connector
    if _connector is None:
        _connector = MT5Connector()
    return _connector


# Test function
if __name__ == "__main__":
    print("Testing MT5 Connector...")
    print()
    
    connector = MT5Connector()
    
    # Test connection
    success, message = connector.connect()
    
    if success:
        print("\n✓ Connection test passed!")
        
        # Show account info
        info = connector.get_account_info()
        if info:
            print(f"\nAccount Details:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        
        # Disconnect
        connector.disconnect()
    else:
        print(f"\n✗ Connection test failed: {message}")
