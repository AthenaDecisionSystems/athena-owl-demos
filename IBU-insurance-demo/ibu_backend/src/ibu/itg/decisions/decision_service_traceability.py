"""
Filename: decision_service_traceability.py

Description:
    Set traceability on ODM decision invocation
"""


def set_trace(request_payload: dict, trace: bool):
    if not trace:
        request_payload["__TraceFilter__"] = None
    else:
        request_payload["__TraceFilter__"] = {
            "infoRulesetProperties": False,
            "infoOutputString": False,
            "infoInputParameters": False,
            "infoOutputParameters": False,
            "none": False,
            "infoExecutionEventsAsked": False,
            "workingMemoryFilter": "string",
            "infoBoundObjectByRule": False,
            "infoExecutionDuration": False,
            "infoExecutionDate": False,
            "infoExecutionEvents": False,
            "infoInetAddress": False,
            "infoRules": False,
            "infoRulesNotFired": False,
            "infoSystemProperties": False,
            "infoTasks": False,
            "infoTasksNotExecuted": False,
            "infoTotalRulesFired": False,
            "infoTotalRulesNotFired": False,
            "infoTotalTasksExecuted": False,
            "infoTotalTasksNotExecuted": False,
            "infoWorkingMemory": False,
            "infoRulesFired": True,
            "infoTasksExecuted": False,
            "infoBoundObjectSerializationType": "ClassName"
        }


class TraceArtefact:
    name: str
    type_: str

    def __init__(self, name: str, type_: str):
        self.name = name
        self.type_ = type_  # "RULE" or "DT"

    def __str__(self):
        return f"DecisionTraceArtefact({self.name}, {self.type_})"

    @staticmethod
    def get_trace_artefact(artefact_payload: dict) -> 'TraceArtefact':
        properties: list[dict] = artefact_payload["properties"]["property"]

        for prop in properties:
            if prop["name"] == "ilog.rules.dt" and prop["value"]:
                return TraceArtefact(prop["value"], "DT")

        return TraceArtefact(artefact_payload["businessName"], "RULE")

    @staticmethod
    def get_fired_trace_artefacts(response_payload: dict) -> list['TraceArtefact']:
        fired_trace_artefacts: list['TraceArtefact'] = []

        try:
            decision_trace = response_payload['__decisionTrace__']
        except KeyError:
            raise Exception("Decision trace not found. Make sure __TraceFilter__ is set on the request")

        rule_information: list[dict] = decision_trace['rulesFired']['ruleInformation']
        for artefact_payload in rule_information:
            fired_trace_artefacts.append(TraceArtefact.get_trace_artefact(artefact_payload))
        return fired_trace_artefacts


if __name__ == "__main__":
    try:
        mode = "DEV"
        from call_api import Connection
    except ImportError:
        mode = "PACK"
        from ibu.itg.decisions.call_api import Connection


    def call_decision_service(connection: Connection, rule_app: str, ruleset: str, request_payload: dict) -> dict:
        return connection.call_request(method='POST', endpoint=f"{rule_app}/{ruleset}", json=request_payload,
                                       headers={"Content-Type": "application/json"})


    def test():
        from scenarios import scenario_passengers_1, scenario_ibu_1
        scenario = scenario_ibu_1
        set_trace(scenario.request_payload, True)
        response_json: dict = call_decision_service(connection=Connection(
            base_url='http://localhost:9060/DecisionService/rest',
            username='odmAdmin',
            password='odmAdmin',
            verbose=True),
            rule_app=scenario.rule_app,
            ruleset=scenario.ruleset,
            request_payload=scenario.request_payload)
        for fired_artefact in TraceArtefact.get_fired_trace_artefacts(response_json):
            print("*", fired_artefact)


    test()
