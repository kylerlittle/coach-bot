from nlp.tokens_to_action import NaturalLanguageProcessor, InputError

def main():
    # BASIC TESTING
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
