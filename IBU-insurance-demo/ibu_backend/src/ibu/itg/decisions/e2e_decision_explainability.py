import json
from typing import Optional

from pydantic import BaseModel

import re

try:
    mode = "DEV"
    from decision_center_extraction import DecisionCenterExtract, RuleOrDT, \
        Documentation
    from decision_service_traceability import TraceArtefact, set_trace
except ImportError:
    mode = "PACK"
    from ibu.itg.decisions.decision_center_extraction import DecisionCenterExtract, RuleOrDT, Documentation
    from ibu.itg.decisions.decision_service_traceability import TraceArtefact, set_trace


def extract_explanation(documentation: str) -> str:
    # Extract the explanation from the documentation
    pattern = re.compile(r"EXPLANATION(.*?)END OF EXPLANATION", re.DOTALL)
    result = pattern.search(documentation)

    if result:
        explanation = result.group(1).strip()
    else:
        explanation = ""
    return explanation

class ExplanationArtefact(BaseModel):
    name: str
    type_: str  # "RULE" or "DT"
    html: str
    documentation: Documentation
    explanation: str

    # def __init__(self, name: str, type_: str, html: str, documentation: str, explanation: str):
    #     self.name = name
    #     self.type_ = type_  # "RULE" or "DT"
    #     self.html = html
    #     self.documentation = documentation
    #     self.explanation = explanation
    
class ExplanationArtefactList(BaseModel):       
    errors_and_warnings: list[str]
    explanation_artefacts: list[ExplanationArtefact]

    @staticmethod
    def build(decision_center_extract: DecisionCenterExtract, response_payload: dict) -> "ExplanationArtefactList":
        errors_and_warnings = []
        explanation_artefacts = []

        for trace_artefact in TraceArtefact.get_fired_trace_artefacts(response_payload):
            rule: Optional[RuleOrDT] = decision_center_extract.find_rule_or_dt_by_fully_qualified_name(
                trace_artefact.name)
            if rule:
                print ("type(rule.documentation)",type(rule.documentation))
                html_artefact = ExplanationArtefact(name=trace_artefact.name, type_=trace_artefact.type_,
                                                    html=rule.html,
                                                    documentation=rule.documentation,
                                                    explanation=extract_explanation(rule.documentation))
                explanation_artefacts.append(html_artefact)
            else:
                errors_and_warnings.append(f"Could not find {trace_artefact.name} in Decision Center extract")

        return ExplanationArtefactList(errors_and_warnings=errors_and_warnings,
                                       explanation_artefacts=explanation_artefacts)


def test():
    # from scenarios import scenario_passengers_1 as scenario
    from scenarios import scenario_ibu_1 as scenario
    request_payload = scenario.request_payload
    decision_service_name = scenario.decision_service_name
    rule_app = scenario.rule_app
    ruleset = scenario.ruleset

    # STEP 1 - Instantiate DecisionCenterExtract either by exploring DecisionCenter or by loading a serialized extract

    decision_center_extract: Optional[DecisionCenterExtract]
    option = "Load"  # "Explore" or "Load"

    try:
        if option == "Explore":
            from call_api import Connection
            connection_dc = Connection(
                base_url='http://localhost:9060/decisioncenter-api/v1',
                username='odmAdmin',
                password='odmAdmin',
                verbose=True
            )
            decision_center_extract = DecisionCenterExtract.create(decision_service_name, connection_dc)
            decision_center_extract.print()
        else:
            if mode == "DEV":
                path = f'../../../../../decisions/{decision_service_name}.json'
            else:
                path = f'{decision_service_name}.json'
            decision_center_extract = DecisionCenterExtract.read_from_file(path)

    except Exception as e:
        # STEP 2 - If any error, print it
        print(f"An error occurred: {e}")
        print(f"Rule traceability is disabled")
        decision_center_extract = None

    # STEP 3 - Build your request payload your own way

    request_payload = scenario.request_payload  # Done above

    # STEP 4 - Set traces on the payload

    if decision_center_extract:
        set_trace(request_payload, True)

    try:
        # STEP 5 - Invoke the decision service your own way
        from call_api import Connection
        connection_res = Connection(
            base_url='http://localhost:9060/DecisionService/rest',
            username='odmAdmin',
            password='odmAdmin',
            verbose=True)

        response_payload: dict = connection_res.call_request(method='POST', endpoint=f"{rule_app}/{ruleset}",
                                                             json=request_payload,
                                                             headers={"Content-Type": "application/json"})

        # STEP 6 - Build the artefact list

        print("*****")
        explanation_artefact_list = ExplanationArtefactList.build(decision_center_extract, response_payload)

        # STEP 7 - Add it to the response payload (optional)

        response_payload['explanation'] = explanation_artefact_list.dict()

        json_str: str = json.dumps(response_payload, indent=4)

        print(json_str)

        # STEP 8 - Print the result (optional)

        if explanation_artefact_list.errors_and_warnings:
            for e in explanation_artefact_list.errors_and_warnings:
                print(e)
        for html_artefact in explanation_artefact_list.explanation_artefacts:
            print(f"******")
            print(f"{html_artefact.name}")
            print(f"html           {html_artefact.html}")
            print(f"documentation  {html_artefact.documentation}")
            print(f"explanation  {html_artefact.explanation}")

        print("*****")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Quitting gently")


if __name__ == "__main__":
    test()
