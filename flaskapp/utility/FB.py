import facebook

#token expires in 3 months as of 15/04/2019
#Posted to a page in CIMS with the name of "Crisis Management System"
#message parameter defines what message is posted to the page.
def Facebook():
    token = {"EAAeh4hKwY8EBAGwoaTxM9UBqu6zD2mpTtiEjGWyAUFfwMTEfERGbR91zxYvyClzt4ZA1KZChBxzoRZBkQ2ettRPUM0rmEK0RHwYeP6QDgw2726isN43o63W11bUHx4nAcDjJHGrzLCBFZB9ZCPKI1GX3xnzBEH9ifGN0cN6ND7ZCrC3Atss88Bf278WpXmX0k2KHU5RqdlqQgOsjp32s35"}
    graph = facebook.GraphAPI(token)

    graph.put_object(parent_object='me', connection_name='feed',message='THIS TOOK ME FUCKING 1 DAY TO FINISH')
    return "WEEEEEEEEEEEEEEEE"