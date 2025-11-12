from portfolio.portfolio import Portfolio
import yaml
import schedule
import time


def main():
    print("Running portfolio job")
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

    p.pie_chart(False)

    with open("cold_config.yml", "r") as yaml_file:
        cold_config = yaml.safe_load(yaml_file)
        p_cold = Portfolio(config=cold_config)

    p_cold.get_token_balances()
    p_cold.get_token_prices()
    p_cold.calculate_portfolio_value()

    if config["ntfy"]["enabled"]:
        print("Sending portfolio notification")
        p.send_portfolio_notification(
            config["ntfy"]["domain"],
            config["ntfy"]["api_key"],
            p.portfolio_value + p_cold.portfolio_value,
            config["ntfy"]["sell_target"],
        )

        print("Sending price alerts (if any)")
        p.send_price_alerts(
            config["ntfy"]["domain"],
            config["ntfy"]["api_key"],
            config["ntfy"]["alert_threshold"],
        )

        p.send_balance_advice(
            config["ntfy"]["domain"],
            config["ntfy"]["api_key"],
            config["ntfy"]["balance_threshold"],
        )

    print(
        f"TOTAL PORTFOLIO VALUE: {p.portfolio_value + p_cold.portfolio_value} HOT ({p.portfolio_value}) COLD ({p_cold.portfolio_value})"
    )


schedule.every().day.at("09:00", "Australia/Victoria").do(main)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
