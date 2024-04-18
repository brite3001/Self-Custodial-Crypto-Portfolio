from attrs import define, validators, field


@define
class TokenTemplate:
    name: str = field(validator=[validators.instance_of(str)])
    coingecko_name: str = field(
        validator=[validators.instance_of(str)]
    )  # some tokens have slightly different names in the coingecko API

    token_address: str = field(validator=[validators.instance_of(str)])
    contract_address: str = field(validator=[validators.instance_of(str)])
    decimals: int = field(validator=[validators.instance_of(int)])
    api_key: str = field(validator=[validators.instance_of(str)])

    allocation: float = field(
        validator=[validators.instance_of(float)]
    )  # allocation % in portfolio

    price: float = field(init=False)  # current price of token according to coingecko
    balance: float = field(init=False)  # balance in token_address

    actual_allocation: float = field(
        init=False
    )  # calc allocation according to (price * balance / portfolio_value) * 100

    allocation_delta: float = field(
        init=False
    )  # delta between allocation and actual allocation
