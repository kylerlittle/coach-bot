# coach-bot

## Team
- Chris Young
- Connor Wright
- Kelsey Nash
- Kyler Little
- Lucy Tran
- Shusanta Bhattarai

## Developor Usage
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
This is a chat bot that's a personal coach for people who want to work out, 
eat better, and/or live healthier. Specifically, the coach bot's target customer
is the full-time worker who doesn't have very much time on their hands to plan
and live such a lifestyle. This is a fairly vague description, but it will be 
elaborated over the next week.

## Possible Use Cases
- Users can manually specify desired frequency of working out at both daily and weekly granularities.
- Users can import schedule via a calendar application like Google Calendar or iCloud Calendar.
- Users can subscribe to notification reminders of when to work out.
- Users can input feedback on workout so that the bot can learn the users' preferences.
- Users can view workout history.