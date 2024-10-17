import yfinance as yf
import numpy as np
from scipy.stats import norm
from datetime import datetime, timedelta

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    if T <= 0 or sigma <= 0:
        print(f"Invalid time to expiration (T={T}) or implied volatility (sigma={sigma})")
        return {'Delta': 'N/A', 'Gamma': 'N/A', 'Theta': 'N/A', 'Vega': 'N/A', 'Rho': 'N/A'}
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        delta = norm.cdf(d1) - 1
        theta = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    
    return {
        'Delta': delta,
        'Gamma': gamma,
        'Theta': theta,
        'Vega': vega,
        'Rho': rho
    }

def fetch_greeks(ticker):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")['Close'].iloc[0]
        print(f"Current price for {ticker}: {current_price}")
        
        expiration_dates = stock.options
        if expiration_dates:
            future_dates = [date for date in expiration_dates if datetime.strptime(date, "%Y-%m-%d") > datetime.now()]
            if not future_dates:
                print(f"No valid future options available for {ticker}")
                return {'Delta': 'N/A', 'Gamma': 'N/A', 'Theta': 'N/A', 'Vega': 'N/A', 'Rho': 'N/A'}
            expiration_date = None
            for date in future_dates:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                time_to_expiration = (date_obj - datetime.now()).days / 365
                if time_to_expiration > 0:  # Ensure there's a positive time to expiration
                    expiration_date = date
                    break
            if expiration_date is None:
                print(f"No valid future options with a positive time to expiration for {ticker}")
                return {'Delta': 'N/A', 'Gamma': 'N/A', 'Theta': 'N/A', 'Vega': 'N/A', 'Rho': 'N/A'}
        else:
            print(f"No options available for {ticker}")
            return {'Delta': 'N/A', 'Gamma': 'N/A', 'Theta': 'N/A', 'Vega': 'N/A', 'Rho': 'N/A'}

        print(f"Using expiration date: {expiration_date}")
        
        options_chain = stock.option_chain(expiration_date)
        if not options_chain.calls.empty:
            call_option = options_chain.calls.iloc[0]
            strike_price = call_option['strike']
            implied_volatility = call_option['impliedVolatility']
            
            if implied_volatility <= 0:
                print(f"Invalid or missing implied volatility for {ticker}. Using fallback value of 20%.")
                implied_volatility = 0.2
            
            option_type = 'call'
            expiration_date_obj = datetime.strptime(expiration_date, "%Y-%m-%d")
            today = datetime.now()
            time_to_expiration = (expiration_date_obj - today).days / 365
            print(f"Strike price: {strike_price}, Implied Volatility: {implied_volatility}, Time to Expiration: {time_to_expiration}")
            
            risk_free_rate = 0.05
            
            greeks = calculate_greeks(current_price, strike_price, time_to_expiration, risk_free_rate, implied_volatility, option_type)
            return greeks
        else:
            print(f"No call options available for {ticker} at {expiration_date}")
            return {'Delta': 'N/A', 'Gamma': 'N/A', 'Theta': 'N/A', 'Vega': 'N/A', 'Rho': 'N/A'}

    except Exception as e:
        print(f"Failed to fetch Greeks for {ticker}: {e}")
        return {'Delta': 'N/A', 'Gamma': 'N/A', 'Theta': 'N/A', 'Vega': 'N/A', 'Rho': 'N/A'}

# Example usage
ticker = 'AAPL'
greeks = fetch_greeks(ticker)
if greeks:
    print(f"Greeks for {ticker}: {greeks}")
else:
    print("No Greeks data available.")
