from agents.nda_agent.pandadoc_api import create_document

template_id = "sv2AtexweVA7QNBZAWac8k"
recipient = {
    "email": "sathvik@aixccelerate.com",
    "first_name": "Sathvik",
    "last_name": "VK",
    "role": "signer"
}
tokens = [
    {"name": "Client.FirstName", "value": "Sathvik"},
    {"name": "Client.Company", "value": "Ai Xccelerate"}
]

doc = create_document(template_id, recipient, tokens)
print(doc)