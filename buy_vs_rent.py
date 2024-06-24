#
# A Buy vs Rent calculator for the New Zealanders
#
# Key Assumptions:
# - You intend to live in the house you're buying, so the mortgage repayment supplants rent
# - The comparison between buying & renting scenarios is based on the minimum of the two cash flows to service each living situation,
#   and the difference is added & invested under the cheaper of the two scenarios
# - You don't sell the house you own
#

import argparse
import numpy as np
import numpy_financial as npf

def invest_savings(savings, interest_rate, tax_rate):
    savings_yield = savings * interest_rate
    savings_yield -= savings_yield * tax_rate
    return savings + savings_yield

def main():
    parser = argparse.ArgumentParser(description='Compare renting vs buying a house in New Zealand 🥝', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    required = parser.add_argument_group('required arguments')
    required.add_argument('--current-savings', type=float, required=True, help='Current savings in NZD')
    required.add_argument('--house-purchase-price', type=float, required=True, help='House purchase price in NZD')
    required.add_argument('--rental-price', type=float, required=True, help='Weekly rental price in NZD')

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--minimum-deposit', type=float, default=0.2, help="Minimum deposit required to buy a house is 20%%")
    optional.add_argument('--transfer-cost', type=float, default=1500, help='Cost of house transfer in NZD, such as legal fees')
    optional.add_argument('--house-insurance', type=float, default=1000, help='Annual house insurance in NZD')
    optional.add_argument('--house-maintenance', type=float, default=1000, help='Annual house maintenance in NZD')
    optional.add_argument('--house-rates', type=float, default=2000, help='Annual house rates in NZD')
    optional.add_argument('--rental-increase', type=float, default=0.04, help='Annual rental price increase')
    optional.add_argument('--mortgage-interest-rate', type=float, default=0.0479, help='Annual mortgage interest rate')
    optional.add_argument('--savings-interest-rate', type=float, default=0.06, help='Annual savings interest rate')
    optional.add_argument('--savings-interest-tax', type=float, default=0.33, help='Tax rate for savings interest')
    optional.add_argument('--capital-gains-rate', type=float, default=0.02, help='Annual capital gains rate')
    optional.add_argument('--capital-gains-tax', type=float, default=0.0, help='Tax rate for capital gains')
    optional.add_argument('--boarders-contributions', type=float, default=0.0, help='Weekly contributions from boarders in NZD')
    optional.add_argument('--boarders-contributions-tax', type=float, default=0.0, help='Tax rate for boarders contributions')
    optional.add_argument('--period-years', type=int, default=30, help='Period to compare in years')
    args = parser.parse_args()

    # Check if savings are 20% of the house purchase price
    if args.current_savings < 0.2 * args.house_purchase_price:
        print("You need at least 20% of the house purchase price as savings to buy a house (${} NZD)".format(0.2 * args.house_purchase_price))
        return

    # Initial calculations
    loan_amount = args.house_purchase_price + args.transfer_cost - args.current_savings
    monthly_mortgage_payment = -npf.pmt(args.mortgage_interest_rate / 12, args.period_years * 12, loan_amount)

    print(f"Loan amount: ${loan_amount:,.2f}, monthly payments: ${monthly_mortgage_payment:,.2f}")

    # Define variables that will change over time
    weekly_rental_price = args.rental_price
    weekly_boarders_contributions = args.boarders_contributions
    house_value = args.house_purchase_price
    house_rates = args.house_rates

    rent_savings = args.current_savings
    buy_savings = 0 # Assume all of the savings are used in the house deposit

    # Iterate through the years and play out the two scenarios
    for year in range(args.period_years):
        for month in range(12):
            # Determine cost for each living scenario & assume these costs are directly serviced by the renters/homeowner's income
            rent_cost = weekly_rental_price * 52 / 12
            buy_cost = monthly_mortgage_payment + (args.house_insurance + args.house_maintenance + house_rates) / 12

            # Invest savings for the month
            rent_savings = invest_savings(rent_savings, args.savings_interest_rate / 12, args.savings_interest_tax)
            buy_savings = invest_savings(buy_savings, args.savings_interest_rate / 12, args.savings_interest_tax)

            # Add leftover cash (i.e. the difference between the two scenarios) to the savings
            leftover_cash = abs(rent_cost - buy_cost)
            if (rent_cost < buy_cost):
                rent_savings += leftover_cash
            else:
                buy_savings += leftover_cash

            # Add cash from boarders
            boarders_contributions = weekly_boarders_contributions * 52 / 12
            boarders_contributions -= boarders_contributions * args.boarders_contributions_tax
            buy_savings += boarders_contributions

        print(f"year {year + 1}: rent savings ${rent_savings:,.2f}, buy savings ${buy_savings:,.2f}, house value: ${house_value:,.2f}")

        # Make updates based on annual rate increases
        weekly_rental_price *= (1 + args.rental_increase)
        weekly_boarders_contributions *= (1 + args.rental_increase) # increase weekyl boarder contributions in line with rental market

        house_value *= (1 + args.capital_gains_rate)
        house_rates *= (1 + args.capital_gains_rate) # Adjust annual rates in line with house value


    # Display results
    print("-" * 100)
    print(f"Net worth for renting scenario: ${rent_savings:,.2f}")
    print(f"Net worth for buying scenario: ${buy_savings:,.2f} + house value ${house_value:,.2f}, which is now owned outright with a CGT of ${house_value * args.capital_gains_tax:,.2f}")

    total_buy_savings = buy_savings + house_value - house_value * args.capital_gains_tax

    if rent_savings > total_buy_savings:
        print("Including house value in net worth, you'll be ${:,.2f} better off renting over a {} year period".format(rent_savings - total_buy_savings, args.period_years))
    else:
        print("Including house value in net worth, you'll be ${:,.2f} better off buying over a {} year period".format(total_buy_savings - rent_savings, args.period_years))

if __name__ == '__main__':
    main()