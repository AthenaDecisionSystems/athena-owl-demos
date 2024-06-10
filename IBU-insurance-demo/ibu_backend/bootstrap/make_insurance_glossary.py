import sys,os
module_path = "../../owl-agent-backend/src"
sys.path.append(os.path.abspath(module_path))
from athena.glossary.glossary_mgr import build_get_glossary

"""
"""

def init_phrases(glossary: build_get_glossary):
    glossary.add_phrases("Actions", {"fr": "Actions", "en": "Actions"})
    glossary.add_phrases(
        "NoClaims",
        {"fr": "Pas de sinistre pour ce client", "en": "No claims for this client"},
    )
    glossary.add_phrases(
        "ClaimNotFound",
        {
            "fr": "Sinistre $claim_id non trouvé pour le client $client_id",
            "en": "Claim $claim_id not found for client $client_id",
        },
    )
    glossary.add_phrases(
        "ClientNotFound",
        {"fr": "Client $clientid non trouvé", "en": "Client $clientid not found"},
    )
    glossary.add_phrases(
        "Proposal", {"fr": "une proposition commerciale", "en": "a commercial proposal"}
    )
    glossary.add_phrases(
        "AcknowledgmentOfReceipt",
        {
            "fr": "un accusé de réception",
            "en": "an acknowledgement of receipt",
        },
    )
    glossary.add_phrases(
        "ClaimsExpert", {"fr": "un conseiller sinistre", "en": "a claims expert"}
    )
    glossary.add_phrases(
        "ClientRepresentative",
        {
            "fr": "un gestionnaire de compte",
            "en": "a client representative",
        },
    )
    glossary.add_phrases(
        "SorryAboutPerceptionButFair",
        {
            "fr": "une note qui explique que nous sommes désolés de sa perception mais c'est le juste prix",
            "en": "a note that explains that we are sorry about the perception but it is the fair price",
        },
    )
    glossary.add_phrases("Letter", {"fr": "lettre", "en": "letter"})
    glossary.add_phrases(
        "CommercialProposal",
        {
            "fr": "une proposition commerciale",
            "en": "a commercial proposal",
        },
    )
    glossary.add_phrases("SMS", {"fr": "SMS", "en": "SMS"})
    glossary.add_phrases("Phone", {"fr": "téléphone", "en": "phone"})
    glossary.add_phrases(
        "analysis_gives",
        {
            "fr": "L'analyse du cas du client donne :\n",
            "en": "The analysis of the client case gives:\n",
        },
    )
    glossary.add_phrases(
        "NoAction",
        {
            "fr": "Pas d'action pour ce client",
            "en": "No action for this client",
        },
    )
    glossary.add_phrases(
        "CommunicateWithClient",
        {
            "fr": "Communiquer avec le client par $channel $messageType",
            "en": "Communicate with the client by $channel $messageType",
        },
    )
    glossary.add_phrases(
        "PrepareProposal",
        {
            "fr": "Préparer une proposition commerciale pour le client.",
            "en": "Prepare a commercial proposal for the client.",
        },
    )
    glossary.add_phrases(
        "ResendTo",
        {
            "fr": "Renvoyer à $recipient",
            "en": "Resend to $recipient",
        },
    )
    glossary.add_phrases(
        "CommercialEffort",
        {
            "fr": "Envisager un effort commercial",
            "en": "Consider a commercial effort",
        },
    )
    glossary.add_phrases(
        "UpsellProposal",
        {
            "fr": "Proposer une offre commerciale pour le produit $policyUpgrade pour le prix $price avec un offre supplémentaire $offer.  Le benefice pour le client est '$benefit'.",
            "en": "Propose a commercial offer for the product $policyUpgrade for the price $price with an additional offer $offer.  The benefit for the client is '$benefit'.",
        },
    )
    glossary.add_phrases(
        "UnknownAction",
        {
            "fr": "Action inconnue: $actionType",
            "en": "Unknown action: $actionType",
        },
    )
    glossary.add_phrases(
        "Explanation",
        {"fr": "    Explication: $expl\n", "en": "    Explanation: $expl\n"},
    )
    glossary.add_phrases(
        "PolicyReference",
        {
            "fr": "    Référence de la règle: $ref",
            "en": "    Policy reference: $ref",
        },
    )
    initialize_explanations(glossary)


def initialize_explanations(glossary: build_get_glossary):
    # id: ret_qos_37, runtimeval = ret-qos-37, ODM val = Retention QoS #37
    glossary.add_phrase(
        "ret-qos-37-expl",
        "en",
        "Large delay: $actualDuration days vs $targetDuration days",
    )
    glossary.add_phrase(
        "ret-qos-37-expl",
        "fr",
        "Sérieux retard: $actualDuration jours au lieu de $targetDuration jours",
    )
    glossary.add_phrase(
        "ret-qos-37-expl",
        "es",
        "Retraso importante: $actualDuration días vs $targetDuration días",
    )
    glossary.add_phrase("ret-qos-37-policy", "en", "Retention QoS #37")
    glossary.add_phrase("ret-qos-37-policy", "fr", "Retention QoS #37")
    glossary.add_phrase("ret-qos-37-policy", "es", "Retention QoS #37")
    # id: ret_qos_38, runtimeval = ret-qos-38, ODM val = Retention QoS #38
    glossary.add_phrase(
        "ret-qos-38-expl",
        "en",
        "Good client and small delay: $actualDuration days vs $targetDuration days",
    )
    glossary.add_phrase(
        "ret-qos-38-expl",
        "fr",
        "Bon client et léger retard: $actualDuration jours au lieu de $targetDuration jours",
    )
    glossary.add_phrase(
        "ret-qos-38-expl",
        "es",
        "Buen cliente y retraso pequeño: $actualDuration días vs $targetDuration días",
    )
    glossary.add_phrase("ret-qos-38-policy", "en", "Retention QoS #38")
    glossary.add_phrase("ret-qos-38-policy", "fr", "Retention QoS #38")
    glossary.add_phrase("ret-qos-38-policy", "es", "Retention QoS #38")
    # id: ret_qos_39, runtimeval = ret-qos-39, ODM val = Retention QoS #39
    glossary.add_phrase(
        "ret-qos-39-expl",
        "en",
        "Small delay: $actualDuration days vs $targetDuration days",
    )
    glossary.add_phrase(
        "ret-qos-39-expl",
        "fr",
        "Léger retard: $actualDuration jours au lieu de $targetDuration jours",
    )
    glossary.add_phrase(
        "ret-qos-39-expl",
        "es",
        "Retraso pequeño: $actualDuration días vs $targetDuration días",
    )
    glossary.add_phrase("ret-qos-39-policy", "en", "Retention QoS #39")
    glossary.add_phrase("ret-qos-39-policy", "fr", "Retention QoS #39")
    glossary.add_phrase("ret-qos-39-policy", "es", "Retention QoS #39")
    # id: ret_qos_40, runtimeval = ret-qos-40, ODM val = Retention QoS #40
    glossary.add_phrase(
        "ret-qos-40-expl",
        "en",
        "No delay: $actualDuration days vs $targetDuration days",
    )
    glossary.add_phrase(
        "ret-qos-40-expl",
        "fr",
        "Pas de retard: $actualDuration jours au lieu de $targetDuration jours",
    )
    glossary.add_phrase(
        "ret-qos-40-expl",
        "es",
        "No hay retraso: $actualDuration días vs $targetDuration días",
    )
    glossary.add_phrase("ret-qos-40-policy", "en", "Retention QoS #40")
    glossary.add_phrase("ret-qos-40-policy", "fr", "Retention QoS #40")
    glossary.add_phrase("ret-qos-40-policy", "es", "Retention QoS #40")
    # id: ret_amount_41, runtimeval = ret-amount-41, ODM val = Retention policy amount #41
    glossary.add_phrase(
        "ret-amount-41-expl",
        "en",
        "Resend to an expert to verify the reimbursed amount",
    )
    glossary.add_phrase(
        "ret-amount-41-expl",
        "fr",
        "Renvoyer à un expert pour vérifier le niveau de remboursement",
    )
    glossary.add_phrase(
        "ret-amount-41-expl",
        "es",
        "Reenviar a un experto para verificar el nivel de reembolso",
    )
    glossary.add_phrase("ret-amount-41-policy", "en", "Retention policy amount #41")
    glossary.add_phrase("ret-amount-41-policy", "fr", "Retention policy amount #41")
    glossary.add_phrase("ret-amount-41-policy", "es", "Retention policy amount #41")
    # id: ret_churn_43, runtimeval = ret-churn-43, ODM val = Retention policy churn #43
    glossary.add_phrase("ret-churn-43-expl", "en", "Sorry about the perception but fair price")
    glossary.add_phrase(
        "ret-churn-43-expl", "fr", "Désolé de la perception mais le prix est juste"
    )
    glossary.add_phrase(
        "ret-churn-43-expl", "es", "Lamentamos la percepción pero el precio es justo"
    )
    glossary.add_phrase("ret-churn-43-policy", "en", "Retention policy churn #43")
    glossary.add_phrase("ret-churn-43-policy", "fr", "Retention policy churn #43")
    glossary.add_phrase("ret-churn-43-policy", "es", "Retention policy churn #43")
    # id: ret_churn_44, runtimeval = ret-churn-44, ODM val = Retention policy churn #44
    glossary.add_phrase(
        "ret-churn-44-expl", "en", "Make an effort given the lifetime customer value"
    )
    glossary.add_phrase(
        "ret-churn-44-expl", "fr", "Faire un geste tenant compte de la valeur client"
    )
    glossary.add_phrase(
        "ret-churn-44-expl",
        "es",
        "Hacer un esfuerzo tomando en cuenta el valor del cliente",
    )
    glossary.add_phrase("ret-churn-44-policy", "en", "Retention policy churn #44")
    glossary.add_phrase("ret-churn-44-policy", "fr", "Retention policy churn #44")
    glossary.add_phrase("ret-churn-44-policy", "es", "Retention policy churn #44")
    # id: ret_churn_45, runtimeval = ret-churn-45, ODM val = Retention policy churn #45
    glossary.add_phrase(
        "ret-churn-45-vip-expl",
        "en",
        "Try to retain a VIP client with a personalized offer",
    )
    glossary.add_phrase(
        "ret-churn-45-vip-expl",
        "fr",
        "Essayer de retenir un client VIP grace à une proposition adaptée",
    )
    glossary.add_phrase(
        "ret-churn-45-vip-expl",
        "es",
        "Intentar retener un cliente VIP con una propuesta personalizada",
    )
    glossary.add_phrase("ret-churn-45-vip-policy", "en", "Retention policy churn #45")
    glossary.add_phrase("ret-churn-45-vip-policy", "fr", "Retention policy churn #45")
    glossary.add_phrase("ret-churn-45-vip-policy", "es", "Retention policy churn #45")
    # id: ret_churn_46, runtimeval = ret-churn-46, ODM val = Retention policy churn #46
    glossary.add_phrase(
        "ret-churn-46-upsell-expl",
        "en",
        "Propose an upsell to a good client that must pay a deductible",
    )
    glossary.add_phrase(
        "ret-churn-46-upsell-expl",
        "fr",
        "Proposer un upsell à un bon client qui doit payer une franchise",
    )
    glossary.add_phrase(
        "ret-churn-46-upsell-expl",
        "es",
        "Proponer un upsell a un buen cliente que debe pagar una franquicia",
    )
    glossary.add_phrase("ret-churn-46-upsell-policy", "en", "Retention policy churn #46")
    glossary.add_phrase("ret-churn-46-upsell-policy", "fr", "Retention policy churn #46")
    glossary.add_phrase("ret-churn-46-upsell-policy", "es", "Retention policy churn #46")


def define_glossary(path: str):
    g=build_get_glossary()
    init_phrases(g)
    g.save_glossary(path)