import matplotlib.pyplot as plt

def plot_performance(results_df):
    """
    Generates a performance chart showing the evolution of portfolio value.
    Expects results_df to have columns 'date' and 'portfolio_value'.
    Saves the chart as performance.png.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['date'], results_df['portfolio_value'], marker='o', linestyle='-')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.grid(True)
    
    plot_path = 'performance.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

if __name__ == '__main__':
    import pandas as pd
    # Example test data
    data = {
        'date': pd.date_range(start='2020-01-01', periods=10, freq='D'),
        'portfolio_value': [100 + i * 10 for i in range(10)]
    }
    df = pd.DataFrame(data)
    path = plot_performance(df)
    print("Chart saved to", path)

