from nlp.tokens_to_action import NaturalLanguageProcessor, InputError
from coachbot import CoachBot
from actions.actions import ActionManager

def main():
    print('Welcome to coachbot!')
    coachbot = CoachBot()

    while True:
        userOption = input('Please select an option:\n1: New User\n2: Existing User\n3: Exit application\n::')

        if userOption == '1':
            coachbot.createNewUser()
            break
        
        elif userOption == '2':
            coachbot.getCurrentUser()
            break

        elif userOption == '3':
            print("\nThank you, see you next time!")
            ##CLOSE APP
            exit(0)
            
        else:
            print("\nI'm sorry, that wasn't one of the options, let's try that again!\n")

    # Commence the conversation with Coach Bot.
    coachbot.printIntro()

    # Declare ActionManager class
    am = ActionManager(coachbot.getCurrentUserId())  # TODO -- pass in correct id

    # Coach Bot Conversation Loop
    while True:
        print("What can I do for you? Hit [Return]/[Enter] to exit.")
        try:
            _input = input("::")
            print("\n")   # add a newline for prettiness
            #exit if the user just hits return
            if(_input == ""):
                exit(0)
            action = NaturalLanguageProcessor.process_input(_input)
            am.enqueue(action)   # add action to pipeline
            print("\n\n")
        except InputError as ie:
            print("Error processing: {input_str}\n{error_msg}".format(input_str=ie.expression, error_msg=ie.message))
    
    # Basic Testing -- note this is never executed in the current set-up.
    test_texts = ["Schedule me a leg workout for 5PM tomorrow",
                  "Display my workout calendar",
                  "Enter my calories for today",
                  "Display my normal calendar",
                  "Show my workout statistics from yesterday",
                  "Set feedback for my workout earlier at 3PM",
                  "Help me"]
    for test_text in test_texts:
        try:
            action = NaturalLanguageProcessor.process_input(test_text)
            print("INPUT: {user_input}".format(user_input=test_text))
            action.execute()
            print("\n\n")
        except InputError as ie:
            print("Error processing: {input_str}\n{error_msg}".format(input_str=ie.expression, error_msg=ie.message))


if __name__ == '__main__':
    main()
