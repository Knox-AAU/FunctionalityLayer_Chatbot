import requests
keywords = ["Aalborg", "Berlin"]
url = "http://localhost:8000/knowledge-base"


def add_url_query(keyword, type):
    if (not(type == "subject" or type == "object")):
        raise Exception("type has to be subject or object.")

    if type == "subject":
        print(url + "?s=" + keyword)
        return url + "?s=" + keyword

    elif type == "object":
        print(url + "?o=" + keyword)
        return url + "?o=" + keyword

def call_database_API():
    for entity in keywords:
        # Add each entity add as subject and object
        subURL = add_url_query(entity, "subject")
        objURL = add_url_query(entity, "object")

        response = requests.get(subURL,
                                verify=False)  # only works if you are connected to KNOXserver: ssh <studiemail>@knox-kb01.srv.aau.dk -L 8000:localhost:8081.
        print(response.status_code)
        print(response.json())

        response2 = requests.get(objURL,
                                verify=False)  # only works if you are connected to KNOXserver: ssh <studiemail>@knox-kb01.srv.aau.dk -L 8000:localhost:8081.
        print(response2.status_code)
        print(response2.json())

call_database_API()



#s=aablorg?s=berlin?o=aalborg?o=berlin
