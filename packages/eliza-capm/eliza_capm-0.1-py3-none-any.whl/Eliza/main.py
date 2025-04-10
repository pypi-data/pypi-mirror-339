import yfinance
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import math
from colorama import init, Fore, Back, Style
from functools import wraps

# Initialize colorama for cross‑platform ANSI
init(autoreset=True)

class eliza:
    def __init__(self):

    #BANNER COZ WHY NOT
        print(Style.BRIGHT + Fore.GREEN + Back.BLACK +
              "\n ███████╗ ██╗      ██████╗  ██████╗  █████╗  \n"
              " ██╔════╝ ██║      ╚══██╔╝  ╚═██╔═╝  ██╔══██╗ \n"
              " █████╗   ██║         ██║      ██║    ███████║\n"
              " ██╔══╝   ██║         ██║     ██║     ██╔══██║\n"
              " ███████╗ ███████╗ ██████╗  ██████╗ ██║  ██║ \n"
              " ╚══════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ \n")
        
    def capm(self, stock_ticker, index_ticker, plot,annualized):
        # ── Data Fetching ───────────────────────────────────
        index = yfinance.download(index_ticker,
                                  start="2024-01-01",
                                  end="2025-04-07",
                                  auto_adjust=True)
        stock = yfinance.download(stock_ticker,
                                  start="2024-01-01",
                                  end="2025-04-07",
                                  auto_adjust=True)

        # ── Return Calculations ─────────────────────────────
        index['R'] = index['Close'].pct_change()
        stock['R'] = stock['Close'].pct_change()
        returns = pd.concat([index['R'], stock['R']],
                            axis=1, join='inner').dropna()
        returns.columns = ['Market', 'Stock']

        # ── CAPM Regression ──────────────────────────────────
        X = sm.add_constant(returns['Market'])
        y = returns['Stock']
        model = sm.OLS(y, X).fit()

        beta       = model.params['Market']
        alpha      = model.params['const']
        resid_mean = model.resid.mean()

        # ── Risk Decomposition ────────────────────────────────
        if annualized:
            # ── Volatility Annualized ──────────────────────────────────────
            vol_m = returns['Market'].std() * (252**0.5)
            vol_s = returns['Stock'].std() * (252**0.5) #This is the total volatility of the stock
            idio_vol = math.sqrt((vol_s**2) - (beta**2 * vol_m**2))

            print(Fore.CYAN + Style.BRIGHT + f"• {index_ticker} Volatility: " +
                Fore.GREEN + f"{vol_m*100:6.2f}%")
            print(Fore.CYAN + Style.BRIGHT + f"• {stock_ticker} Volatility: " +
                Fore.GREEN + f"{vol_s*100:6.2f}%")
            print(Fore.CYAN + Style.BRIGHT + f"• Idiosyncratic Volatility: " +
                Fore.GREEN + f"{idio_vol*100:6.2f}%\n")
        else:
            # ── Volatility Daily ──────────────────────────────────────
            vol_m = returns['Market'].std()
            vol_s = returns['Stock'].std() #This is the total volatility of the stock
            idio_vol = math.sqrt((vol_s**2) - (beta**2 * vol_m**2))

            total_vol = (((vol_m * beta) ** 2) + (vol_s)) ** 0.5
            print(Fore.CYAN + Style.BRIGHT + f"• {index_ticker} Volatility: " +
                Fore.GREEN + f"{vol_m*100:6.2f}%")
            print(Fore.CYAN + Style.BRIGHT + f"• {stock_ticker} Volatility: " +
                Fore.GREEN + f"{vol_s*100:6.2f}%")
            print(Fore.CYAN + Style.BRIGHT + f"• Idiosyncratic Volatility: " +
                Fore.GREEN + f"{idio_vol*100:6.2f}%\n")

        # ── Regression Results ──────────────────────────────
        print(Fore.MAGENTA + Style.BRIGHT + "┌─ Regression Results ──────────────────────")
        print(Fore.MAGENTA + "│ " + Fore.YELLOW + f"Mean Residuals: {resid_mean:.8f}")
        print(Fore.MAGENTA + "│ " + Fore.YELLOW + f"Beta          : {beta:.4f}")
        print(Fore.MAGENTA + "│ " + Fore.YELLOW + f"Alpha         : {alpha:.8f}")
        print(Fore.MAGENTA + "└───────────────────────────────────────────\n")

        # ── Optional Plot ───────────────────────────────────
        if plot:
            plt.figure(figsize=(10, 6))
            plt.xlabel(f'{index_ticker} Returns')
            plt.ylabel(f'{stock_ticker} Returns')
            plt.title(f'{stock_ticker} vs {index_ticker} CAPM')
            plt.grid(True)
            plt.axhline(0, ls='--', lw=0.8)
            plt.scatter(returns['Market'], returns['Stock'], alpha=0.5)
            plt.plot(returns['Market'], beta*returns['Market'] + alpha, lw=2,color='red')
            plt.show()


    def risk_decomposition(self, stock_value, beta, market_vol, idiosyncratic_vol, annualized=False):
        # Convert % to decimal
        market_vol = market_vol / 100
        idiosyncratic_vol = idiosyncratic_vol / 100

        # Risk calculations
        market_risk = beta * market_vol * stock_value
        idiosyncratic_risk = idiosyncratic_vol * stock_value
        total_risk = market_risk + idiosyncratic_risk

        # Styled Printout
        print(Fore.LIGHTBLACK_EX + Style.DIM + "\n┌── Risk Decomposition ───────────────────────────────")
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"│ Stock Value         : " + Fore.CYAN + f"${stock_value:,.2f}")
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"│ Beta                : " + Fore.MAGENTA + f"{beta:.4f}")
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"│ Market Volatility   : " + Fore.GREEN + f"{market_vol*100:.2f}%")
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"│ Idio Volatility     : " + Fore.GREEN + f"{idiosyncratic_vol*100:.2f}%")

        print(Fore.LIGHTBLACK_EX + "├────────────────────────────────────────────────────")
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"│ Market Risk         : " + Fore.YELLOW + f"${market_risk:,.2f}")
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"│ Idiosyncratic Risk  : " + Fore.YELLOW + f"${idiosyncratic_risk:,.2f}")
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"│ Total Risk          : " + Fore.RED + Style.BRIGHT + f"${total_risk:,.2f}")
        print(Fore.LIGHTBLACK_EX + "└────────────────────────────────────────────────────\n")

        return {
            "Market Risk": market_risk,
            "Idiosyncratic Risk": idiosyncratic_risk,
            "Total Risk": total_risk
        }

# Instantiate and run ELIZA
if __name__ == "__main__":
    pass
