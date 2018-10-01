# coach-bot

## Team
- Chris Young
- Connor Wright
- Kelsey Nash
- Kyler Little
- Lucy Tran
- Shusanta Bhattarai

## Usage
Set up environment on Ubuntu.
```
source ./scripts/setup.sh
```
Activate python virtual environment.
```
source ./venv/bin/activate
```
Ensure running ```which python``` prints the same as ```pwd``` + '/venv/bin/python'.

Next, install dependencies.
```
pip install -r requirements.txt
```
Before running the application, we need to train our model. Of course, in production, this will already be readily available.
```
python coach-bot/nlp/train_intent_parser.py
```
Run application.
```
python coach-bot
```
Run tests.
```
python tests
```
Deactivate environment.
```
deactivate
```

## Description
This is a Python console application. Specifically, it's a chat bot that's a 
personal coach for people who want to work out, eat better, and/or live 
healthier. The coach bot's target customer is the full-time worker who doesn't 
have very much time on their hands to plan and live such a lifestyle. This is 
a fairly vague description, but it will be elaborated over time.

## Use Cases
- Users can register for an account and/or login.
- Users can schedule/request a workout targeting specific areas (i.e. cardio, legs, etc.)
- Users can display workout statistics.
- Users can import schedule via the calendar application Google Calendar.
- Users can input/set number of calories for a given day.
- Users can input feedback on workout so that the bot can learn the users' preferences.
- Users can view workout history.