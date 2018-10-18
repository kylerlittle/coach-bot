from user import User
import uuid
import xml.etree.ElementTree as ET

class CoachBot():

    def __init__(self):
        self.user = User()

    def CoachBot(self):
        self.user = User()


    def createNewUser(self):
        print("\nLet's create a new user!\n")
        fName = input("What is your first name?: ")
        lName = input("What is your last name?: ")
        email = input("What is your email address?: ")

        ##Determine new id for user
        newId = uuid.uuid4()

        self.user.User(email, fName, lName, str(newId))

        tree = ET.parse('coach-bot/Users.xml')
        root = tree.getroot()

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

        print("User {} successfully added!".format(self.user.getFullName()))


    def getCurrentUser(self):
        print("\nLet's work with an existing user!\n")
        email = input("What is your email address?: ")

        tree = ET.parse('coach-bot/Users.xml')
        root = tree.getroot()

        for child in root:
            if child[2].text == email:
                print("\nExisting user found!\n")
                self.user.User(child[2].text, child[0].text, child[1].text, child.get('id'))
                break
            else:
                print("\nNo existing user with email: {e}\n".format(e=email))
                continue
            
        print("Welcome back {}\n".format(self.user.getFullName()))

    def printIntro(self):
            print("""         _.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._
         ,'_.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._`.
        ( (                                                         ) )
         ) )  Hello! I am your personal coach. Ask me to schedule  ( (
        ( (   you a workout, display your current schedule, show    ) )
         ) )  your workout stats, or give feedback on a prior      ( (
        ( (   workout. Remember, ask for help if you're confused!   ) )
         ) )                                                       ( (
        ( (_.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._) )
         `._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._,'
        """)

    def getCurrentUserId(self):
        return self.user.getUserId()
        
