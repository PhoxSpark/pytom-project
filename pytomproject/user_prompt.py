def question_y_n(question=""):
    """
    Send them an answer and it will return a 'y' or 'n'. It will not 
    continue with answers differents than Yes or No. It only takes 
    the user answer first character and make it lower for return and 
    testing.

    Returns 'y' or 'n'
    """
    answer = ''
    while(answer != 'n' and answer != 'y'):
        print(question)
        answer = input("Yes (y) or no (n): ")
        answer = str(answer[0]).lower()
    return answer
