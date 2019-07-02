def question_y_n(question):
    """
    Send them an answer and it will return a 'y' or 'n'. It will not 
    continue with answers differents than Yes or No. It only takes 
    the user answer first character and make it lower for return and 
    testing.
    """
    answer = ''
    while(answer != 'n' and answer != 'y'):
        print(question)
        answer = input("Yes (y) or no (n): ")
        answer = str(answer[0]).lower()
    return answer

def text_input(request, min_lenght, max_lenght, character_size):
    """
    Send the request for the user, the minimum lenght and the maximum lenght,
    also you can set if the return will be upper or lower. If you don't care
    about if it's upper or lower, you can put an empty string on that camp,
    then it will be ignored.
    """
    prequisites_acomplished = False
    while(prequisites_acomplished == False):
        user_input = input(request)
        if(character_size == "upper"):
            user_input = user_input.upper()
        if(character_size == "lower"):
            user_input = user_input.lower()
        if(len(user_input) > min_lenght and len(user_input) < max_lenght):
            prequisites_acomplished = True
        else:
            if(min_lenght != 0):
                print("Minimum amount of characters: %i" % min_lenght)
            if(max_lenght != 0):
                print("Maximum amount of characters: %i" % max_lenght)
    return user_input