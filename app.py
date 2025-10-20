"""
MT5 Sentiment Analysis Bot - Main Streamlit Application
Professional trading bot with Smart Money Concepts and ML-powered sentiment analysis
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import AppConfig, DataConfig
from src.mt5.connection import MT5Connection, get_mt5_connection
from src.mt5.data_fetcher import MT5DataFetcher
from src.analysis.sentiment_engine import SentimentEngine
from src.analysis.multi_timeframe import MultiTimeframeAnalyzer
from src.health.monitor import HealthMonitor
from src.database.repository import get_repository
from src.utils.logger import setup_logging, get_logger
from src.reporting.pdf_generator import PDFReportGenerator

# GUI Components
from gui.components.sentiment_card import render_sentiment_card, render_confidence_bar, render_factors_table
from gui.components.chart_panel import render_price_chart, render_indicator_charts, render_smc_analysis, render_mtf_chart
from gui.components.health_dashboard import render_health_dashboard, render_system_metrics, render_issues_list
from gui.components.metrics_panel import (
    render_metrics_panel, render_performance_chart, render_data_metrics,
    render_model_metrics, render_live_metrics_ticker
)
from gui.components.settings_panel import (
    render_mt5_settings, render_analysis_settings, render_model_settings,
    render_alert_settings, render_display_settings, render_data_management
)

# Initialize logging
setup_logging()
logger = get_logger()

# Page configuration
st.set_page_config(
    page_title=AppConfig.PAGE_TITLE,
    page_icon=AppConfig.PAGE_ICON,
    layout=AppConfig.LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E40AF;
        text-align: center;
        padding: 1rem 0;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .status-healthy {
        background-color: #10B981;
        color: white;
    }
    .status-warning {
        background-color: #F59E0B;
        color: white;
    }
    .status-critical {
        background-color: #EF4444;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_components():
    """Initialize bot components (cached)"""
    try:
        logger.info("Initializing bot components", category="general")
        
        components = {
            'sentiment_engine': SentimentEngine(),
            'mtf_analyzer': MultiTimeframeAnalyzer(),
            'health_monitor': HealthMonitor(),
            'repository': get_repository(),
            'pdf_generator': PDFReportGenerator()
        }
        
        logger.info("Components initialized successfully", category="general")
        return components
    except Exception as e:
        logger.error(f"Error initializing components: {str(e)}", category="general")
        st.error(f"Failed to initialize components: {str(e)}")
        return None


def get_mt5_data(symbol: str, timeframes: list, connection, data_fetcher):
    """Fetch MT5 data for multiple timeframes"""
    data_dict = {}
    
    for tf in timeframes:
        with st.spinner(f"Fetching {symbol} {tf} data..."):
            df = data_fetcher.get_ohlcv(symbol, tf, count=1000)
            if df is not None and not df.empty:
                data_dict[tf] = df
    
    return data_dict


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🎯 MT5 Sentiment Analysis Bot</h1>', unsafe_allow_html=True)
    
    # Live metrics ticker at the top
    render_live_metrics_ticker()
    
    # Live metrics ticker at the top
    render_live_metrics_ticker()
    
    # Initialize components
    components = initialize_components()
    
    if components is None:
        st.error("Failed to initialize. Please check configuration and try again.")
        return
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Symbol selection
        symbol = st.selectbox(
            "Symbol",
            ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSD"],
            index=0
        )
        
        # Timeframe selection
        primary_tf = st.selectbox(
            "Primary Timeframe",
            ["M15", "H1", "H4", "D1"],
            index=1
        )
        
        # Multi-timeframe analysis
        enable_mtf = st.checkbox("Multi-Timeframe Analysis", value=True)
        
        if enable_mtf:
            mtf_timeframes = st.multiselect(
                "Additional Timeframes",
                ["M15", "H1", "H4", "D1"],
                default=["M15", "H4", "D1"]
            )
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-Refresh", value=False)
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval (sec)", 30, 300, 60)
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            analyze_button = st.button("🔄 Analyze", use_container_width=True, type="primary")
        with col2:
            health_check_button = st.button("🏥 Health Check", use_container_width=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Analysis",
        "📈 Indicators",
        "📊 Metrics",
        "🧠 SMC",
        "🏥 Health",
        "⚙️ Settings"
    ])
    
    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'health_results' not in st.session_state:
        st.session_state.health_results = None
    
    # Analysis Tab
    with tab1:
        st.header("Sentiment Analysis")
        
        if analyze_button or (auto_refresh and st.session_state.analysis_results is None):
            try:
                # MT5 Connection
                with st.spinner("Connecting to MT5..."):
                    connection = get_mt5_connection()
                    if not connection.is_connected():
                        connection.connect()
                    data_fetcher = MT5DataFetcher(connection)
                
                # Fetch data
                if enable_mtf and mtf_timeframes:
                    all_timeframes = list(set([primary_tf] + mtf_timeframes))
                else:
                    all_timeframes = [primary_tf]
                
                data_dict = get_mt5_data(symbol, all_timeframes, connection, data_fetcher)
                
                if not data_dict:
                    st.error("Failed to fetch data. Please check MT5 connection.")
                    return
                
                # Perform analysis
                if enable_mtf and len(data_dict) > 1:
                    with st.spinner("Performing multi-timeframe analysis..."):
                        results = components['mtf_analyzer'].analyze_multiple_timeframes(
                            data_dict, symbol
                        )
                        st.session_state.analysis_results = results
                else:
                    with st.spinner("Analyzing sentiment..."):
                        df = data_dict[primary_tf]
                        results = components['sentiment_engine'].analyze_sentiment(
                            df, symbol, primary_tf
                        )
                        st.session_state.analysis_results = results
                
                st.success("✓ Analysis complete!")
                
            except Exception as e:
                logger.error(f"Error during analysis: {str(e)}", category="general")
                st.error(f"Analysis failed: {str(e)}")
                return
        
        # Display results
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            if enable_mtf and 'dominant_sentiment' in results:
                # Multi-timeframe results
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    sentiment_data = {
                        'sentiment': results['dominant_sentiment']['sentiment'],
                        'confidence': results['overall_confidence'],
                        'risk_level': 'MEDIUM'  # Could be calculated
                    }
                    render_sentiment_card(sentiment_data)
                
                with col2:
                    st.subheader("Timeframe Alignment")
                    alignment = results.get('alignment', {})
                    
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Alignment Score", f"{alignment.get('score', 0):.0%}")
                    col_b.metric("Aligned", "Yes" if alignment.get('aligned') else "No")
                    col_c.metric("Timeframes", alignment.get('total_timeframes', 0))
                    
                    # MTF Chart
                    if 'timeframe_results' in results:
                        render_mtf_chart(results['timeframe_results'])
                
                # Suggestions
                if 'suggestions' in results:
                    st.subheader("💡 Trading Suggestions")
                    for suggestion in results['suggestions']:
                        st.info(suggestion)
                
            else:
                # Single timeframe results
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    render_sentiment_card(results)
                    render_confidence_bar(results.get('confidence', 0.0))
                
                with col2:
                    st.subheader("Analysis Details")
                    st.write(f"**Symbol:** {results.get('symbol', 'N/A')}")
                    st.write(f"**Timeframe:** {results.get('timeframe', 'N/A')}")
                    st.write(f"**Price:** {results.get('price', 0):.5f}")
                    st.write(f"**Timestamp:** {results.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Contributing factors
                if 'factors' in results:
                    render_factors_table(results['factors'])
                
                # Insights
                if 'insights' in results:
                    st.subheader("💡 Key Insights")
                    for insight in results['insights']:
                        st.info(insight)
        
        else:
            st.info("👆 Click 'Analyze' to start sentiment analysis")
    
    # Indicators Tab
    with tab2:
        st.header("Technical Indicators")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            if enable_mtf and 'timeframe_results' in results:
                # Show indicators for selected timeframe
                selected_tf = st.selectbox("Select Timeframe", list(results['timeframe_results'].keys()))
                tf_result = results['timeframe_results'][selected_tf]
                
                if 'technical_signals' in tf_result:
                    render_indicator_charts(tf_result['technical_signals'])
            elif 'technical_signals' in results:
                render_indicator_charts(results['technical_signals'])
            else:
                st.info("No indicator data available")
        else:
            st.info("Run analysis first to see indicators")
    
    # Metrics Tab
    with tab3:
        st.header("📊 Performance Metrics")
        
        # Store last update time in session state
        if 'last_update' not in st.session_state:
            st.session_state.last_update = datetime.now()
        
        # Update timestamp after analysis
        if analyze_button:
            st.session_state.last_update = datetime.now()
        
        # Main metrics panel
        render_metrics_panel(
            repository=components['repository'],
            last_update=st.session_state.last_update,
            update_frequency=DataConfig.UPDATE_FREQUENCY,
            symbol=symbol,
            timeframe=primary_tf
        )
        
        st.markdown("---")
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            render_performance_chart(components['repository'])
        
        with col2:
            render_model_metrics(components['repository'])
        
        st.markdown("---")
        
        # Data metrics
        render_data_metrics(components['repository'], symbol, primary_tf)
    
    # SMC Tab
    with tab4:
        st.header("Smart Money Concepts")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            if enable_mtf and 'timeframe_results' in results:
                selected_tf = st.selectbox("Timeframe", list(results['timeframe_results'].keys()), key="smc_tf")
                tf_result = results['timeframe_results'][selected_tf]
                
                if 'smc_signals' in tf_result:
                    render_smc_analysis(tf_result['smc_signals'])
            elif 'smc_signals' in results:
                render_smc_analysis(results['smc_signals'])
            else:
                st.info("No SMC data available")
        else:
            st.info("Run analysis first to see SMC analysis")
    
    # Health Tab
    with tab5:
        st.header("System Health")
        
        if health_check_button or st.session_state.health_results is None:
            with st.spinner("Running health check..."):
                try:
                    health_results = components['health_monitor'].perform_health_check()
                    st.session_state.health_results = health_results
                    st.success("✓ Health check complete")
                except Exception as e:
                    st.error(f"Health check failed: {str(e)}")
        
        if st.session_state.health_results:
            health_results = st.session_state.health_results
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                render_health_dashboard(health_results)
            
            with col2:
                render_system_metrics(health_results)
            
            st.divider()
            render_issues_list(health_results)
        else:
            st.info("👆 Click 'Health Check' to view system status")
    
    # Settings Tab
    with tab6:
        st.header("Configuration")
        
        settings_tab1, settings_tab2, settings_tab3, settings_tab4 = st.tabs([
            "MT5", "Analysis", "Alerts", "Data"
        ])
        
        with settings_tab1:
            render_mt5_settings()
        
        with settings_tab2:
            render_analysis_settings()
            render_model_settings()
        
        with settings_tab3:
            render_alert_settings()
        
        with settings_tab4:
            render_display_settings()
            render_data_management()
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Generate Report"):
            st.info("Report generation coming soon...")
    with col2:
        if st.button("📥 Export Data"):
            st.info("Data export coming soon...")
    with col3:
        if st.button("📋 View Logs"):
            st.info("Log viewer coming soon...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {str(e)}", category="general")
        st.error(f"Application error: {str(e)}")
