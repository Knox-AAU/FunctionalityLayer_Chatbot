from spaCy.spaCy import extract_entities

#Nedestående funktioner kan bare slettes og erstattes med de rigtige :)

def promptUser():
    print("What would you like to ask the chatbot?")
    prompt = input("")
    print("Question: " + prompt)
    return prompt

def processKeywords(keywords):
    processedKeywords = []
    raise Exception("'processKeywords' Not yet implemented")
    return processedKeywords

def getGraphAPIData(processedKeywords):
    knowledgeGraphdata = []
    raise Exception("'getGraphAPIData' Not yet implemented")
    return knowledgeGraphdata

def processGraphData(knowledgeGraphdata):
    processedKnowledgeGraphData = []
    raise Exception("'processGraphData' Not yet implemented")
    return processedKnowledgeGraphData

def getChatbotResponse(processedData):
    response = ""

    print("Answer: " + response)
    raise Exception("'getChatbotResponse' Not yet implemented")
    return response

userInput = promptUser()

#Uses spaCy
keywords = extract_entities(userInput)

#processedKeywords = processKeywords(keywords)

#calls API to get Knowledge Graph data
#knowledgeGraphdata = getGraphAPIData(processedKeywords)

#processedData = processGraphData(knowledgeGraphdata)

#response = getChatbotResponse(processedData)






