# Subatomic Agents API 

**Subatomic Agents** is a modular, enterprise-grade AI framework by [Subatomic](https://www.getsubatomic.ai) for automating and scaling business intelligence workflows using agent-based architectures.

*This package provides the **Sales Proposal Agent**, which transforms meeting transcripts and summaries into structured, client-ready sales proposals.*

---

## *🚀 Features*

- *Includes the Sales Proposal Agent for generating structured, client-ready proposals from meeting inputs*

---

## *📆 Installation*

*Install via *[*PyPI*](https://pypi.org/project/subatomic-agents/)*:*

```bash
pip install subatomic-agents
```

---

## *🧠 Usage*

```python
from subatomic_agents.sales_proposal.services.agentic_generator import sales_proposal_agentic_generator

result = sales_proposal_agentic_generator(
    query = """
    Please, create a Sales Proposal with these guidelines:
    Meeting Summary URLs (and file types): https://example.com (pdf)
    Meeting Transcript URL (and file type): https://example2.com (pdf)
    """
)

print(f"FINAL RESULT => {result}")
```

---

## *📂 Output*

*Returns a structured JSON dictionary representing the sales proposal (excluding internal vector data).*\
*The result is also saved to **`sales_proposal_{id}.pdf`** and **`sales_proposal_{id}.docx`**.*

---

## *➕ Extending the Framework*

*This framework is modular and designed for easy extension:*

- *Add new agents in **`agents/`***
- *Define prompt strategies in **`factories/`***
- *Extend the generation flow via **`SalesProposalGeneratorService`***

---

## *🧪 Requirements*

- *Python 3.9+*
- *Compatible with **`uv`**, **`pip`**, or **`poetry`**-based environments*

---

## *👥 Authors*

*Built by *[*Subatomic*](https://www.getsubatomic.ai)*

- *Karl Simon · *[*karl@getsubatomic.ai*](mailto:karl@getsubatomic.ai)*
- *Aaron Sosa · *[*wilfredo@getsubatomic.ai*](mailto:wilfredo@getsubatomic.ai)*

---