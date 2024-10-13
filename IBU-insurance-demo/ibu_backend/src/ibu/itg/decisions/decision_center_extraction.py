# Call update_forward_refs()
# Branch
# Rule at top level package


from typing import Optional, Callable

from abc import ABC, abstractmethod
from pydantic import BaseModel, json

# Explore the REST API: http://localhost:9060/decisioncenter-api/swagger-ui/index.html

from ibu.itg.decisions.call_api import Connection


# MODEL


class DecisionCenterExtract(BaseModel):
    decision_service: 'DecisionService'

    def save_to_file(self, path):
        string = self.model_dump_json(indent=4)
        print(string[9400:9500])
        with open(path, 'w', encoding='utf-8') as file:
            file.write(self.model_dump_json(indent=4))

    @staticmethod
    def read_from_file(path) -> 'DecisionCenterExtract':
        extract: DecisionCenterExtract = DecisionCenterExtract.parse_file(path, encoding='utf-8')
        return extract

    @staticmethod
    def create(decision_service_name: str, dc_api_connection: Connection) -> 'DecisionCenterExtract':
        params = {'q': f'name:{decision_service_name}'}
        response_json = dc_api_connection.call_request(method='GET', endpoint='decisionservices', params=params)

        if len(response_json["elements"]) == 0:
            raise Exception(f"Decision service \"{decision_service_name}\" was not found")

        decision_service = DecisionService(
            id=response_json["elements"][0]["id"],
            name=decision_service_name,
            fully_qualified_name=decision_service_name,
            projects=[])

        decision_service.extract_projects(dc_api_connection)

        print("extract_projects done")

        return DecisionCenterExtract(decision_service=decision_service)

    def print(self):
        self.decision_service.print(0)

    def find_rule_or_dt_by_fully_qualified_name(self, fqn: str) -> Optional['RuleOrDT']:
        decision_service = self.decision_service
        for project in decision_service.projects:
            for folder in project.folders:
                for rule_or_dt in folder.rules_and_dts:
                    if rule_or_dt.fully_qualified_name == fqn:
                        return rule_or_dt


class Artefact(ABC, BaseModel):
    id: str
    name: str
    fully_qualified_name: str

    @abstractmethod
    def get_direct_children(self) -> list['Artefact']:
        pass

    def print(self, indent_level: int):
        print('    ' * indent_level, self.fully_qualified_name)
        for child in self.get_direct_children():
            child.print(indent_level + 1)


class DecisionService(Artefact):
    projects: list['Project'] = []

    # @override
    def get_direct_children(self) -> list[Artefact]:
        children = self.projects[:]  # Shallow copy
        return children

    def extract_projects(self, dc_api_connection: Connection) -> None:
        endpoint = f'decisionservices/{self.id}/projects'

        response_json = dc_api_connection.call_request(method='GET', endpoint=endpoint)
        projects: list[dict] = response_json["elements"]
        self.projects = [Project(id=p["id"], name=p["name"], fully_qualified_name=p["name"],
                                 internal_id=p["internalId"], folders=[]) for p in projects]

        for project in self.projects:
            project.extract_children(dc_api_connection)


class Project(Artefact):
    internal_id: str
    folders: list['Folder']  # all the folders not just the root folders

    # @override
    def get_direct_children(self) -> list[Artefact]:  # The root folders
        return [f for f in self.folders if not f.parent_id]

    # @override
    def extract_children(self, dc_api_connection: Connection) -> None:
        print("extract_children")
        self.extract_folders(dc_api_connection)
        self.extract_rules_and_dts(dc_api_connection)
        self.compute_fully_qualified_names()
        print("after compute_fully_qualified_names")

    def extract_folders(self, dc_api_connection: Connection) -> None:
        print("extract_folders")
        endpoint = f'projects/{self.id}/folders'
        response_json = dc_api_connection.call_request(method='GET', endpoint=endpoint)
        folders: list[dict] = response_json["elements"]
        self.folders = [Folder(id=f["id"], name=f["name"], fully_qualified_name=f["name"], internal_id=f["internalId"],
                               parent_id=f["parentId"],
                               sub_folders=[], rules_and_dts=[]) for f in folders]

        for folder in self.folders:
            if folder.parent_id:
                for f in self.folders:
                    if f.internal_id == folder.parent_id:
                        f.sub_folders.append(folder)

    def extract_rules_and_dts(self, dc_api_connection: Connection) -> None:
        print("Enter extract_rules_and_dts")
        endpoint = f'projects/{self.id}/rules'
        params = {'withContent': 'true'}
        response_json = dc_api_connection.call_request(method='GET', endpoint=endpoint, params=params)
        rules_and_dts: list[dict] = response_json["elements"]

        def ensure_not_none(s: str):
            return "" if s is None else s

        all_rules_and_dts: list[RuleOrDT] = [
            RuleOrDT(id=r["id"], name=r["name"], fully_qualified_name=r["name"], rule_package=r["rulePackage"],
                     html=r["html"], documentation=ensure_not_none(r["documentation"])) for r in rules_and_dts]

        for rule_or_dt in all_rules_and_dts:
            for folder in self.folders:
                if folder.internal_id == rule_or_dt.rule_package:
                    folder.rules_and_dts.append(rule_or_dt)

        print("Quit extract_rules_and_dts")

    def compute_fully_qualified_names(self):
        for f in self.get_direct_children():  # Root folders
            f.fully_qualified_name = f.name
            f.propagate_down_fully_qualified_name()


class Folder(Artefact):
    internal_id: str
    parent_id: Optional[str]
    sub_folders: list['Folder']
    rules_and_dts: list['RuleOrDT']

    # @override
    def get_direct_children(self) -> list[Artefact]:
        sub_folders = self.sub_folders[:]  # Shallow copy
        rules_and_dts = self.rules_and_dts[:]
        return sub_folders + rules_and_dts

    def propagate_down_fully_qualified_name(self):
        for sub_folder in self.sub_folders:
            sub_folder.fully_qualified_name = self.fully_qualified_name + "." + sub_folder.name
            sub_folder.propagate_down_fully_qualified_name()
        for rule_or_dt in self.rules_and_dts:
            rule_or_dt.fully_qualified_name = self.fully_qualified_name + "." + rule_or_dt.name


class RuleOrDT(Artefact):
    rule_package: str
    html: str
    documentation: str

    # @override
    def get_direct_children(self) -> list[Artefact]:
        return []


def test1():
    connection = Connection(
        base_url='http://localhost:9060/decisioncenter-api/v1',
        username='odmAdmin',
        password='odmAdmin',
        verbose=True
    )

    try:
        decision_service_name = 'ds-insurance-pc-claims-nba'
        decision_center_extract0 = DecisionCenterExtract.create(decision_service_name, connection)

        path = f'json/{decision_service_name}.json'
        print("a")
        decision_center_extract0.save_to_file(path)
        print("b")
        decision_center_extract = DecisionCenterExtract.read_from_file(path)
        print("c")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Quitting gently")
        return

    decision_center_extract.print()

    for fully_qualified_name in [
        "Complaint Handling.Reimbursed amount.Targeted.RA-DED-UP - Upgrade policy with no deductible",
        "Complaint Handling.Applied coverages.Targeted.Auto.AC-AUTO-SUBV-DISC - Discount on substitution vehicle"
    ]:
        print(f"{fully_qualified_name}:")
        rule_or_dt = decision_center_extract.find_rule_or_dt_by_fully_qualified_name(fully_qualified_name)
        if rule_or_dt:
            print(f"FOUND {rule_or_dt.name:}")
            print(" HTML ->", rule_or_dt.html)
            print(" documentation ->", rule_or_dt.documentation)
        else:
            print("-> NOT FOUND")


if __name__ == "__main__":
    test1()

DecisionCenterExtract.update_forward_refs()
Artefact.update_forward_refs()
DecisionService.update_forward_refs()
Project.update_forward_refs()
Folder.update_forward_refs()
RuleOrDT.update_forward_refs()
