# Portfolio Hedging Effectiveness of Rare Earth Elements

## Abstract

Portfolio hedging instruments refer to financial tools that are used to protect against risk, particularly the risk of price fluctiations in e.g. stocks, assets and currencies. Tedeschi (2025) shows that rare earth elements (REEs) used to be effective hedges; however, their effectiveness has been diminished due to market volatility and geopolitical instability. Tedeschi used financial data until early October 2024.

We investigate whether this finding continues to hold using newly available data until the end of June 2025. We find this time period especially relevant due to the announcement of new US tariffs, which has increased market volatility and geopolitical instability. We are particularly interested in REE's hedging effecitveness before and after the first tariff announcement on April 2, 2025.


## Data and Preprocessing

### Data

We extract the highest, lowest, and closing prices of various stocks from August 1, 2023 to June 30, 2025. We use the Polygon API for this extraction. The relevant stocks are:

* Rare Earth and Strategic Metals (REMX): proxy for rare earth prices.
* First Trust Global Wind Energy (FAN): proxy for wind energy market.
* Invesco Solar (TAN): proxy for solar energy market.
* iSHares Global Clean Energy (ICLN): proxy for clean energy market.
* Energy Select Sector SPDR Fund (XLE): proxy for the entire energy sector.

### Preprocessing

For each stock, let $p_t$, $h_t$, and $l_t$ be the closing, highest, and lowest prices in day $t$, respectively. Throughout this document, $t$ is 1-indexed, meaning the index of $t$ starts from 1. 

We calculate the daily returns:

$$r_t = \log \frac{p_t}{p_{t-1}}$$

and the HL volatility:

$$HL_t = \sqrt{\frac{1}{t} \sum_{i=1}^t \frac{1}{4\ln 2} \ln \frac{h_i}{l_i}}$$

## Dynamic Spillover Analysis

### Dynamic Setting

Our goal is to calculate the net spillover of from REMX to each other stock. We also want to calculate this net spillover over a time period; meaning, we will have a net spillover value on each day.

To do this, for each day starting from [TO BE DETERMINED], we take the stock values in the previous 200 days (including the considered day) and feed it into the price movement model as detailed below.

### Modeling Price Movement

Let $y_t$ be the vector of either the returns and votatilities of all 5 stocks in day $t$. Essentially, $y_t$ contains 5 values with are either $r_t$ or $HL_t$ for all 5 stocks.

We use a Vector AutoRegressive (VAR) model, whose generalized form is:

$$y_t = c + \sum_{i=1}^p A_i y_{t-i} + u_i$$

where:
* $c$ is a constant vector.
* $A_i$ are coefficient matrices.
* $u_i \sim WN(0, \Sigma)$ are error terms that reflect random fluctuations of prices.

Tedeschi (2025) adopted a highly simplified version of this VAR model, with $c$ being the zero vector, $p=1$, and $A_1$ being the identity matrix ($I_2$). Hence:

$$y_t = y_{t-1}+u_t$$

Hence, we can now compute the error terms $u_i$. We can also now calculate the covariance matrix $\Sigma$ by calculating the covariance matrix of the error terms $u_i$.

We express this in the Vector Moving Average (VMA) form. The generalized version of VMA is:

$$y_t = c + \sum_{i=0}^\infty \Psi_i u_{t-i}$$

where
* $c$ is the same constant vector.
* $\Psi_i$ are coefficient matrices.

Here, it's easy to see that $c$ is the zero vector and $\Psi_i$ are identity matrices. Thus:

$$y_t = \sum_{i=2}^t u_i$$

### Spillover Calculation

Next, we define the $H$-step ahead Generalized Forecast Error Variance Decomposition (GFEVD), which is a $5 \times 5$ matrix $\Theta(H)$ where the $(i, j)$ element represents the contribution of the $j$-th stock to the forecast error variance of the $i$-th stock. The $(i, j)$ element is:

$$\gamma_{ij}(H) = \frac{1}{\sigma_{ii}} \sum_{h=0}^{H-1} \frac{(\epsilon_i^T \Psi_h \Sigma \epsilon_j)^2}{\epsilon_i^T \Psi_h \Sigma \Psi_h^T \epsilon_j}$$

where:
* $\sigma_{ii}$ is the $i$-th diagonal element of the covariance matrix $\Sigma$.
* $\epsilon_i$ is the $n$-dim selection vector, whose $i$-th element is 1, while all others are zeros.
* $\Psi_i$ are the coefficient matrices in the VMA form.

In our model, we choose $H = 10$, and we note that $\Psi_i$ are identity matrices. Hence:

$$\gamma_{ij} = \frac{1}{\sigma_{ii}} \sum_{h=0}^{9} \frac{(\epsilon_i^T \Sigma \epsilon_j)^2}{\epsilon_i^T \Sigma \epsilon_j} = \frac{10(\epsilon_i^T \Sigma \epsilon_j)^2}{\sigma_{ii} \epsilon_i^T \Sigma \epsilon_j}$$

We normalize our GFEVD matrix by dividing each entry by the row sum:

$$\tilde{\gamma_{ij}} = \frac{\gamma_{ij}}{\sum_j \gamma_{ij}}$$

Finally, the net spillover from the $i$-th stock to the $j$-th stock, we compute:

$$Net_{ij} = \tilde{\gamma_{ji}} - \tilde{\gamma_{ij}}$$



## References

Diebold, Francis X., and Kamil Yilmaz. "Better to give than to receive: Predictive directional measurement of volatility spillovers." International Journal of forecasting 28.1 (2012): 57-66.

Tedeschi, Marco. "Do Rare Earth Elements (REEs) hedge financial risk? A spillover and portfolio analysis in the context of the energy market." Resources Policy (2025): 105612.

