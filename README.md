# Buy vs Rent Calculator for Kiwis 🥝

This Python script provides a detailed comparison between buying and renting a house in New Zealand, taking into account various costs and economic factors over a specified period. It aims to help users make an informed decision based on their financial situation and housing market trends.

This tool can provide a helpful financial perspective to help guide your decision-making process when considering buying versus renting a house in New Zealand.

## Dependencies

This script requires Python 3 and the following packages:

```bash
pip install numpy numpy-financial argparse
```

## Usage

To run the script, you need to provide several arguments detailing your current savings, house purchase price, and weekly rental price. There are also numerous optional arguments to better tailor the calculations to your specific situation.

### Required Arguments

```bash
--current-savings: Your current savings in NZD.
--house-purchase-price: The purchase price of the house in NZD.
--rental-price: The weekly rental price in NZD.
```

### Optional Arguments

```bash
--minimum-deposit: The minimum deposit percentage required to buy a house (default: 20%).
--transfer-cost: Costs associated with transferring the house, such as legal fees (default: 1500 NZD).
--house-insurance: Annual house insurance cost in NZD (default: 1000).
--house-maintenance: Annual house maintenance cost in NZD (default: 1000).
--house-rates: Annual house rates in NZD (default: 2000).
--rental-increase: Annual percentage increase in rental price (default: 4%).
--mortgage-interest-rate: Annual mortgage interest rate (default: 4.79%).
--savings-interest-rate: Annual savings interest rate (default: 6%).
--savings-interest-tax: Tax rate for savings interest (default: 33%).
--capital-gains-rate: Annual capital gains rate on the value of the house (default: 2%).
--capital-gains-tax: Tax rate for capital gains (default: 0%).
--boarders-contributions: Weekly contributions from boarders in NZD (default: 0).
--boarders-contributions-tax: Tax rate for boarders' contributions (default: 0%).
--period-years: Number of years to compare in the scenario (default: 30).
```

### Example Command

```bash
python3 buy_vs_rent.py --current-savings 160000 --house-purchase-price 800000 --rental-price 400
```

## Key Assumptions

- The script assumes you will live in the house you buy, hence the mortgage repayment replaces rent.
- The comparison between buying and renting scenarios is based on minimizing the two cash flows required to service each living situation.
- Surplus funds under the cheaper living scenario are invested.
- The house is not sold during the comparison period.
