import sys
import os
import argparse
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import data_retrieval, visualisation, pdf_generator

# Default backtesting period
DEFAULT_START_DATE = "2015-01-01"
DEFAULT_END_DATE = "2024-12-31"

def run_backtest(start_date: str, end_date: str, daily_investment: float = 30, taker_fee: float = 0.0007):
    """
    Runs the backtest for the Bitcoin Dollar-Cost Averaging (DCA) strategy with daily investments.
    
    - Loads historical data from Binance.
    - Filters data between the specified start and end dates.
    - Resamples hourly data to daily closing prices.
    - Simulates a daily investment strategy including a taker fee.
    - Computes final portfolio value and performance metrics.
    - Generates a performance chart and a PDF report summarizing the results.
    """
    print("Loading Bitcoin data from Binance...")
    df = data_retrieval.get_bitcoin_data()
    
    # Filter data by date range (using index since data_retrieval sets it to datetime)
    df = df[(df.index >= start_date) & (df.index <= end_date)]
    if df.empty:
        print("❌ No data available for the selected period.")
        return
    
    # Resample to daily frequency using the last available price each day
    df_daily = df.resample('D').last().dropna()
    
    total_investment = 0.0
    btc_wallet = 0.0
    purchase_count = 0
    
    # Simulate daily investments over the backtest period
    for _, row in df_daily.iterrows():
        total_investment += daily_investment
        buy_btc = daily_investment / row['close']
        btc_wallet += buy_btc * (1 - taker_fee)
        purchase_count += 1
    
    final_value = btc_wallet * df_daily.iloc[-1]['close']
    performance_pct = (final_value - total_investment) / total_investment * 100
    buy_and_hold_perf = (df_daily.iloc[-1]['close'] - df_daily.iloc[0]['close']) / df_daily.iloc[0]['close'] * 100
    
    print(f"Bought {purchase_count} times, investing ${daily_investment} daily.")
    print(f"Total invested: ${total_investment:.2f}")
    print(f"Final wallet: {btc_wallet:.3f} BTC")
    print(f"Final wallet value: ${final_value:.2f}")
    print(f"Performance: {performance_pct:.2f}%")
    print(f"Buy and Hold Performance: {buy_and_hold_perf:.2f}%")
    
    # For visualization, compile a DataFrame of daily portfolio values
    portfolio_values = []
    cumulative_btc = 0.0
    for _, row in df_daily.iterrows():
        buy_btc = daily_investment / row['close']
        cumulative_btc += buy_btc * (1 - taker_fee)
        portfolio_values.append(cumulative_btc * row['close'])
    
    results_df = pd.DataFrame({
        'date': df_daily.index,
        'portfolio_value': portfolio_values
    })
    
    # Generate performance chart
    plot_path = visualisation.plot_performance(results_df)
    
    # Generate PDF report
    pdf_path = pdf_generator.generate_pdf_report(
        start_date=start_date,
        end_date=end_date,
        investment=daily_investment,
        frequency="daily",
        total_invested=total_investment,
        final_value=final_value,
        profit=final_value - total_investment,
        plot_path=plot_path
    )
    
    print(f"📄 PDF report generated: {pdf_path}")
    return results_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Backtest for the Bitcoin Dollar-Cost Averaging (DCA) strategy with daily investments using Binance data.")
    parser.add_argument('--start_date', type=str, default=DEFAULT_START_DATE, help='Start date in YYYY-MM-DD format (default: 2015-01-01)')
    parser.add_argument('--end_date', type=str, default=DEFAULT_END_DATE, help='End date in YYYY-MM-DD format (default: 2024-12-31)')
    parser.add_argument('--investment', type=float, default=30, help='Amount invested per day in USD (default: 30)')
    parser.add_argument('--taker_fee', type=float, default=0.0007, help='Taker fee (default: 0.0007)')
    
    args = parser.parse_args()
    run_backtest(args.start_date, args.end_date, args.investment, args.taker_fee)




