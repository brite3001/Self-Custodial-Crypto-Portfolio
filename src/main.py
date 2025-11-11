from portfolio.portfolio import Portfolio
import yaml


def main():
    with open("config.yml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
        p = Portfolio(config=config)

    p.get_token_balances()
    p.get_token_prices()

    # for token in p.tokens:
    #     print(f"{token.name} | {token.balance} | {token.price}")

    p.calculate_missing_allocations()

    # for token in p.tokens:
    #     print(f"{token.name} | {token.allocation}%")

    p.calculate_portfolio_value()

    p.calculate_actual_token_allocation()

    p.calculate_allocation_delta()

    p.generate_balancing_advice()

    chart_buffer = p.pie_chart()

    with open("cold_config.yml", "r") as yaml_file:
        cold_config = yaml.safe_load(yaml_file)
        p_cold = Portfolio(config=cold_config)

    p_cold.get_token_balances()
    p_cold.get_token_prices()
    p_cold.calculate_portfolio_value()

    p.send_portfolio_notification(
        config["ntfy"]["domain"],
        config["ntfy"]["api_key"],
        p.portfolio_value + p_cold.portfolio_value,
        config["ntfy"]["sell_target"],
    )

    # p.send_portfolio_charts(
    #     config["ntfy"]["domain"], config["ntfy"]["api_key"], chart_buffer
    # )

    p.token_price_alerts(
        config["ntfy"]["domain"],
        config["ntfy"]["api_key"],
        config["ntfy"]["sell_target"],
    )

    print(
        f"TOTAL PORTFOLIO VALUE: {p.portfolio_value + p_cold.portfolio_value} HOT ({p.portfolio_value}) COLD ({p_cold.portfolio_value})"
    )


if __name__ == "__main__":
    main()
