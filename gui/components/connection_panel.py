"""
MT5 Connection Panel
Dedicated UI for connecting/disconnecting from MT5
"""
import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mt5_connector import get_connector, MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_PATH


def render_connection_panel():
    """Render MT5 connection control panel"""
    
    st.markdown("### 🔌 MT5 Connection Manager")
    
    # Initialize session state
    if 'mt5_connector' not in st.session_state:
        st.session_state.mt5_connector = get_connector()
    
    connector = st.session_state.mt5_connector
    
    # Get current status
    status = connector.get_status()
    is_connected = status['connected']
    
    # Connection status display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if is_connected:
            st.success("🟢 **CONNECTED**")
            
            # Show account info
            account_info = connector.get_account_info()
            if account_info:
                st.markdown(f"""
                **Account:** {account_info['login']}  
                **Server:** {account_info['server']}  
                **Balance:** {account_info['balance']} {account_info['currency']}  
                **Company:** {account_info['company']}
                """)
                
                if connector.connection_time:
                    elapsed = datetime.now() - connector.connection_time
                    hours = int(elapsed.total_seconds() // 3600)
                    minutes = int((elapsed.total_seconds() % 3600) // 60)
                    st.caption(f"Connected for: {hours}h {minutes}m")
        else:
            st.error("🔴 **DISCONNECTED**")
            
            if status['last_error']:
                st.warning(f"⚠️ Last error: {status['last_error']}")
    
    with col2:
        # Connection time indicator
        if is_connected and connector.connection_time:
            st.metric(
                "Uptime",
                f"{int((datetime.now() - connector.connection_time).total_seconds() // 60)}m"
            )
    
    st.markdown("---")
    
    # Credentials display
    st.markdown("#### 📋 Connection Details")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"""
        **Login:** `{MT5_LOGIN}`  
        **Server:** `{MT5_SERVER}`
        """)
    
    with col_b:
        st.markdown(f"""
        **Password:** `{'*' * len(MT5_PASSWORD)}`  
        **Path:** `{MT5_PATH[:40]}...`
        """)
    
    st.markdown("---")
    
    # Control buttons
    st.markdown("#### 🎮 Controls")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button(
            "🔌 CONNECT" if not is_connected else "🔌 RECONNECT",
            type="primary",
            use_container_width=True,
            disabled=is_connected
        ):
            with st.spinner("Connecting to MT5..."):
                success, message = connector.connect()
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    with col2:
        if st.button(
            "⛔ DISCONNECT",
            type="secondary",
            use_container_width=True,
            disabled=not is_connected
        ):
            with st.spinner("Disconnecting..."):
                success, message = connector.disconnect()
                
                if success:
                    st.info(f"ℹ️ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    with col3:
        if st.button(
            "🔄 Check Status",
            use_container_width=True
        ):
            st.rerun()
    
    # Connection instructions
    if not is_connected:
        st.markdown("---")
        st.markdown("#### 💡 Connection Instructions")
        
        st.info("""
        **To connect:**
        1. Click the **🔌 CONNECT** button
        2. Wait for connection to establish (5-10 seconds)
        3. Check the green status indicator
        
        **If connection fails:**
        - Check that MT5 is installed
        - Verify internet connection
        - Check firewall settings
        - See console output for detailed errors
        """)


def render_connection_widget():
    """Render minimal connection status widget for other pages"""
    
    # Initialize connector if not exists
    if 'mt5_connector' not in st.session_state:
        st.session_state.mt5_connector = get_connector()
    
    connector = st.session_state.mt5_connector
    status = connector.get_status()
    
    if status['connected']:
        account_info = connector.get_account_info()
        if account_info:
            st.success(f"🟢 MT5 Connected: {account_info['login']} @ {account_info['server']}")
        else:
            st.success("🟢 MT5 Connected")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.error("🔴 MT5 Disconnected - Go to Settings → Connection")
        with col2:
            if st.button("Connect"):
                st.switch_page("Settings")


def get_connection_status() -> dict:
    """Get current MT5 connection status (for use in other components)"""
    
    if 'mt5_connector' not in st.session_state:
        st.session_state.mt5_connector = get_connector()
    
    connector = st.session_state.mt5_connector
    return connector.get_status()


def get_mt5_connector():
    """Get MT5 connector instance (for use in other components)"""
    
    if 'mt5_connector' not in st.session_state:
        st.session_state.mt5_connector = get_connector()
    
    return st.session_state.mt5_connector
