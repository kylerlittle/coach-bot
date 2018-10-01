from nlp.tokens_to_action import NaturalLanguageProcessor, InputError
import xml.etree.ElementTree as ET
from user import User

def main():
    print('Welcome to coachbot!')
    user = User()

    while True:
        userOption = input('Please select an option:\n1: New User\n2: Existing User\n3: Exit application\n::')

        if userOption == '1':
            print("\nLet's create a new user!\n")
            fName = input("What is your first name?: ")
            lName = input("What is your last name?: ")
            email = input("What is your email address?: ")

            user.User(email, fName, lName)

            tree = ET.parse('coach-bot/Users.xml')
            root = tree.getroot()

            ##Determine new id for user
            newId = 0
            for child in root:
                
                if child.attrib.get('id') >= str(newId):
                    newId = int(child.attrib.get('id')) + 1

            newUser = ET.Element('user')
            newUser.set('id', str(newId))
            newUser.tail = "\n"

            fNameElement = ET.SubElement(newUser, 'FirstName')
            fNameElement.text = fName
            fNameElement.tail = "\n"

            lNameElement = ET.SubElement(newUser, 'LastName')
            lNameElement.text = lName
            lNameElement.tail = "\n"

            emailElement = ET.SubElement(newUser, 'Email')
            emailElement.text = email
            emailElement.tail = "\n"
            print(emailElement.text)


            root.append(newUser)
            tree.write('coach-bot/Users.xml')

            print("User {} successfully added!".format(user.getFullName()))
            break
        
        elif userOption == '2':
            print("\nLet's work with an existing user!\n")
            email = input("What is your email address?: ")

            tree = ET.parse('coach-bot/Users.xml')
            root = tree.getroot()

            for child in root:
                if child[2].text == email:
                    print("\nExisting user found!\n")
                    user.User(child[2].text, child[0].text, child[1].text)
                    break
            
            print("Welcome back {}\n".format(user.getFullName()))
            break

        elif userOption == '3':
            print("\nThank you, see you next time!")
            ##CLOSE APP
            exit(0)
            
        else:
            print("\nI'm sorry, that wasn't one of the options, let's try that again!\n")

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
