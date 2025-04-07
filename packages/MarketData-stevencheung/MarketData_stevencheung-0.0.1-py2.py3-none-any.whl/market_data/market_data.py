import yfinance as yf

def csv_individual_market_data(ticker: str, v_start: str, v_end: str, v_period: str, v_interval: str):
    """Fetches market data for a given stock ticker within a specified time range and saves it as a CSV file.

    Args:
        ticker (str): The stock ticker symbol.
        v_start (str): The start date for the data retrieval in 'YYYY-MM-DD' format.
        v_end (str): The end date for the data retrieval in 'YYYY-MM-DD' format.
        v_period (str): The data period (e.g., "1d", "5d", "1mo", "3mo", "1y").
        v_interval (str): The interval between data points (e.g., "1m", "5m", "1d", "1wk").

    Returns:
        _type_: A DataFrame containing the fetched market data.
    """
    data = yf.download(ticker, start=v_start, end=v_end, period=v_period, interval=v_interval)
    with open(f'{v_start}_{v_end}_{ticker}.csv', "w") as f:
        for i in data.to_csv():
            f.write(i)

def get_x_year_intervals(ticker: str, start_year: int, end_year: int, interval: int):
    for i in range(start_year, end_year+1):
        csv_individual_market_data(ticker, f'{i}-01-01', f'{i+interval}-01-01', "1d", "1d")
