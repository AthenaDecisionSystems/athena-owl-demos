from ibu.itg.ds.ComplaintHandling_generated_model import Motive, Response, Action


def callDecisionService(config, claim_repo, claim_id: int, client_motive: Motive, intentionToLeave: bool, locale: str = "en"):
    rep = Response()
    rep.actions=[Action(explanationCode="Propose a Vousher for 100$", typeDisc__= "")]
    return rep