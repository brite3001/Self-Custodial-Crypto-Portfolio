import requests
import pprint
import datetime
import yaml
from portfolio.token_template import TokenTemplate

pp = pprint.PrettyPrinter(indent=4)

with open("config.yml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

vane_endpoint = requests.get(f"{config['portfolio_report']['vane_endpoint']}/api/providers")
lmstudio = config['portfolio_report']['lmstudio_endpoint']
model_name = config['portfolio_report']['model_name']

providers = vane_endpoint.json()['providers']

provider_id = providers[1]['id']
provider_name = providers[1]['name']

print(f'Using LLM Provider: {provider_name}')

def portfolio_research(tokens: list[TokenTemplate]):

    research = []

    recommended_websites = """
        site:https://www.reuters.com & 
        site:https://www.bloomberg.com & 
        site:https://www.coindesk.com & 
        site:https://www.theblock.co & 
        site:https://decrypt.co & 
        site:https://beincrypto.com/"""
    
    system_prompt = f"""
        Date: {datetime.datetime.now()}.
        Respond terse. Keep all technical accuracy. Drop filler.

        Rules:
        - Drop: articles (a/an/the), filler words (just/really/basically), pleasantries (sure/happy to), hedging
        - Sentence fragments OK
        - Technical terms stay exact
        - Sometimes Crypto can have quiet periods. If there's little news thats fine, no need to extensively research for crumbs"

        Format: Write in paragraphs. Prioritize density over grammar."""

    vane_request_body = {
        "chatModel": {
        "providerId": provider_id,
        "key": model_name
            },
        "embeddingModel": {
        "providerId": provider_id,
        "key": model_name
            },
        "optimizationMode": "balanced",
        "sources": ["web"],
        "query": "What happened this week in xxx?",
        "systemInstructions": system_prompt,
        "stream": False
    }

    lmstudio_chat_body = {
        "system_prompt": system_prompt,
        "model": model_name,
        "context_length": 25000,
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64
  
    }

    def token_research(token: str):
        vane_request_body['query'] = f'What happened this week in {token}? {recommended_websites}'
        print(vane_request_body['query'])
        query = requests.post(f"{config['portfolio_report']['vane_endpoint']}/api/search", json=vane_request_body)
        query = query.json()['message']

        research.append({'type': 'text', 'content':  vane_request_body['query']})
        research.append({'type': 'text', 'content': query})

    def build_portfolio_report():
        research_text = "\n\n---\n\n".join([item['content'] for item in research])

        lmstudio_chat_body['input'] = [
            {'type': 'text', 'content': research_text},
            {'type': 'text', 'content': 'Summarise the research on individual tokens into a unified portfolio report. Each token was researched in isolation, try make the report cohesive. No need to comment on the makeup of the portfolio itself.  Citations can be dropped.'}
        ]

        report = requests.post(url=f'{lmstudio}/api/v1/chat', 
                    headers={"Authorization": "Bearer eee", "Content-Type": "application/json"},
                    json=lmstudio_chat_body
                )
        return report.json()
    
    def send_weekly_portfolio_report(url: str, api_key: str, report: str) -> None:
        requests.post(
            url + "portfolio",
            data=report.encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}"},
        )

    # for token in tokens:
    #     token_research(token.name)

    for token in ['Solana', 'Ethereum']:
        token_research(token)
    
    aaa = build_portfolio_report()

    # pp.pprint(aaa)

    report = aaa['output'][1]['content']

    print(report)

    send_weekly_portfolio_report(config["ntfy"]["domain"], config["ntfy"]["api_key"], report)