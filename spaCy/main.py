from spaCy import runSpaCy

flag = True
while flag:

    # Start application by prompting the user for the initial statement
    input_string = input("Indtast en prompt: ")

    # Run SpaCy, function will take a user prompt as input and return key entities based on the prompt
    output = runSpaCy(input_string)
    print(output)

    # The output from SpaCy should now be used as input of a query to the KG API
    # which should return the appropriate data in JSON format, which will be saved
    #kgData = knowledgeGraphSearch()

    # The next step is to prompt the LLM, given the original user prompt, and the data returned in the KG.
    # llmOutput = promptLLama2(input_string, kgData)

    # Lastly the output of LLama 2 will be printed for the user.
    # print(llmOutput)

    # run a loop that determines if the user would like to enter a new prompt
    repeat = "flag"
    while repeat != "y" and repeat != "n":
        repeat = input("Har du lyst til at spørge om noget nyt? (y/n)")
    if repeat == "n":
        flag = False


