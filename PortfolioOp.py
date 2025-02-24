import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Input
#-----------------------------------------------------------------------------------
risk_penalty = int(input("Podaj liczbę ryzka od 1-10, gdzie 1 to największe ryzko, a 10 najmniejsze: "))
#csv_file = input("Podaj lozkalizacje pliku CSV aktywów:  ")
csv_file = r"C:\Users\PC\Downloads\letstryagain.csv.csv"  
df = pd.read_csv(csv_file, delimiter=",", thousands=",")
#-----------------------------------------------------------------------------------



#Kalkulacje
#-----------------------------------------------------------------------------------
asset_names = df.columns[1:]
num_assets = len(asset_names)
returns = df[asset_names].pct_change().dropna()



def calculate_balanced_sharpe(returns, weights, risk_free_rate=0.02, risk_penalty=5):
    portfolio_return = np.sum(returns.mean().values * weights) * 252

    portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

    adjusted_sharpe_ratio = (portfolio_return - risk_free_rate) / (portfolio_stddev ** risk_penalty) if portfolio_stddev != 0 else 0
    
    return [adjusted_sharpe_ratio, portfolio_return, portfolio_stddev]



num_portfolios = 5000

weights_list = []
sharpe_list = []
returns_list = []
volatility_list = []

best_sharpe = -np.inf  
best_weights = None
best_return = None
best_volatility = None

for _ in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)  

    sharpe_ratio, portfolio_return, portfolio_stddev = calculate_balanced_sharpe(returns, weights, risk_penalty=risk_penalty)

    weights_list.append(weights)
    sharpe_list.append(sharpe_ratio)
    returns_list.append(portfolio_return)
    volatility_list.append(portfolio_stddev)

    if sharpe_ratio > best_sharpe:
        best_sharpe = sharpe_ratio
        best_weights = weights
        best_return = portfolio_return
        best_volatility = portfolio_stddev
#-----------------------------------------------------------------------------------



#Plot
#-----------------------------------------------------------------------------------
plt.figure(figsize=(12, 8))
plt.scatter(volatility_list, returns_list, c=sharpe_list, cmap="viridis", alpha=0.5, label="Random Portfolios")



plt.scatter(best_volatility, best_return, color="red", marker="X", s=200, label="Optimized Portfolio")



plt.colorbar(label="Adjusted Sharpe Ratio")



plt.xlabel("Volatility (Risk) - Annualized")
plt.ylabel("Expected Return - Annualized")
plt.title(f"Efficient Frontier & Balanced Sharpe Optimal Portfolio (Adjusted Sharpe: {best_sharpe:.2f})")



column_labels = ["Asset", "Percentage"]
table_data = [[asset_names[i], f"{best_weights[i] * 100:.1f}%"] for i in range(num_assets)]
table = plt.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='bottom', bbox=[0, -0.3, 1, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)



plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#-----------------------------------------------------------------------------------