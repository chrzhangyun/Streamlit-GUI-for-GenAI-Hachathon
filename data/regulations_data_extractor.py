import json
import requests
import re
import pandas as pd

# API reference: https://www.ecfr.gov/developers/documentation/api/v1#/
# Download the title-17.json file from: https://www.ecfr.gov/api/versioner/v1/structure/2024-11-07/title-17.json
with open("title-17.json", "r", encoding="utf8") as f:
    title17 = json.load(f)

rule_citations = []

for chapter in title17["children"]:
    for part in chapter["children"]:
        if (
            part["identifier"].isdigit()
            and int(part["identifier"]) > 200
            and int(part["identifier"]) < 300
        ):
            for subject_group in part["children"]:
                if "children" in subject_group:
                    for section in subject_group["children"]:
                        citation = {}
                        citation["chapter"] = chapter["identifier"]
                        citation["part"] = part["identifier"]
                        citation["subject_group"] = subject_group["identifier"]
                        citation["section"] = (
                            section["identifier"] if "identifier" in section else ""
                        )

                        rule_citations.append(citation)

print(rule_citations[:1])
print(f"Number of rule citations: {len(rule_citations)}")


rules = {
    "chapter": [],
    "part": [],
    "subject_group": [],
    "section": [],
    "rule_citation": [],
    "rule_text": [],
}
CLEANR = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")

eCFR_endpoint = "https://www.ecfr.gov/api/versioner/v1/full/2024-11-07/title-17.xml?"
for rule_citation in rule_citations[:5]:
    eCFR_URL = (
        eCFR_endpoint
        + f"part={rule_citation['part']}&section={rule_citation['section']}"
    )
    rule_text_xml = requests.get(eCFR_URL).text
    rule_text = re.sub(CLEANR, "", rule_text_xml).strip()[3:]

    print(rule_text)

    rules["chapter"].append(rule_citation["chapter"])
    rules["part"].append(rule_citation["part"])
    rules["subject_group"].append(rule_citation["subject_group"])
    rules["section"].append(rule_citation["section"])
    rules["rule_citation"].append(
        rule_citation["chapter"]
        + "_"
        + rule_citation["part"]
        + "_"
        + rule_citation["subject_group"]
        + "_"
        + rule_citation["section"]
    )
    rules["rule_text"].append(rule_text)

rules_df = pd.DataFrame(rules)
rules_df.to_csv('regulations.csv')