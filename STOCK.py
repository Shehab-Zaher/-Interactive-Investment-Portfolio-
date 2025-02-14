import streamlit as st
import pandas as pd
import yfinance as yf

# Title of the app
st.title("📊 Interactive Investment Portfolio Analysis")

# Input for stock symbols
symbols = st.text_input("Enter stock symbols (comma separated)", "NVDA, GOOG, AMZN")

# Convert input symbols to a list
symbols_list = [symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()]

# Date range for fetching stock data
start_date = st.date_input("Start date", pd.to_datetime("2022-01-01").date())
end_date = st.date_input("End date", pd.to_datetime("today").date())

# Button to fetch and display data
if st.button("Fetch Data"):
    if not symbols_list:
        st.error("⚠️ Please enter at least one stock symbol.")
    else:
        try:
            # Fetch stock data
            data = yf.download(symbols_list, start=str(start_date), end=str(end_date))

            if data.empty:
                st.warning("⚠️ No data found. Check the stock symbols or date range.")
            else:
                st.write("✅ **Stock Data:**")
                st.write(data)

                # Ensure 'Close' exists (works for both single and multiple stocks)
                if "Close" in data:
                    # Display closing prices
                    st.subheader("📈 Closing Prices")
                    st.line_chart(data["Close"])

                    # Calculate and display daily returns
                    st.subheader("📊 Daily Returns")
                    daily_returns = data["Close"].pct_change().dropna()
                    st.line_chart(daily_returns)

                    # Calculate and display cumulative returns
                    st.subheader("📈 Cumulative Returns")
                    cumulative_returns = (1 + daily_returns).cumprod() - 1
                    st.line_chart(cumulative_returns)

                    # Show correlation matrix if multiple stocks exist
                    if len(symbols_list) > 1:
                        st.subheader("🔗 Correlation Matrix")
                        st.write(daily_returns.corr())

                    # Calculate and display Sharpe Ratio
                    st.subheader("📊 Sharpe Ratio")
                    risk_free_rate = 0.01  # Assumed risk-free rate
                    sharpe_ratios = (daily_returns.mean() - risk_free_rate) / daily_returns.std()
                    st.write(sharpe_ratios)
                else:
                    st.error("⚠️ No 'Close' price data available for the selected stocks.")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
