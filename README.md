# Self Custodial Crypto Portfolio

## What does this do?
I wanted the portfolio auto rebalancing functionality of [3commas](https://help.3commas.io/en/articles/3109000-creating-a-portfolio) or [shrimpy](https://www.shrimpy.io/), but wanted to hold all the coins on my hardware wallet.
This python script reads the balances of all the different coins in your portfolio on chain, checks if the coin allocations have moved above or below what you've set, then suggests what to buy or sell.

## How do I use it?
1. I create a portfolio in the yaml file included with the project, I set all the target allocations for my coins
2. The app grabs the balances of all the coins on-chain
3. Coin allocations on-chain are compared to the allocations I set in the yaml file
4. The App spits out buy or sell orders for each coin. The coins which require the largest allocation to be bought or sold are listed first. This allows me to make a smaller number of trades, that have a bigger impact on balaning my portfolio
5. I use my favourite exchange to buy/sell the coins (mostly non-custodial exchanges from [kycnot.me](https://kycnot.me))
6. Re-run the app as desired 
