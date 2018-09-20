"""
src="https://github.com/explosion/spacy/blob/master/examples/training/train_intent_parser.py"

This is a message parser for a common "chat intent": talking with our coach bot. 
Our message semantics will have the following types of relations: 
ROOT, WHAT, ATTRIBUTE, TIME.

Example:
"show me my workout schedule for tomorrow"
('show', 'ROOT', 'show')
('workout', 'ATTRIBUTE', 'schedule') --> schedule with ATTRIBUTE workout
('schedule', 'WHAT', 'show') --> show WHAT schedule
('tomorrow', 'WHEN', 'schedule') --> schedule WHEN tomorrow

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
import spacy
from pathlib import Path

MODEL_DIR = './model'


# training data: texts, heads and dependency labels
# for no relation, we simply chose an arbitrary dependency label, e.g. '-'
# 'heads' refers to the index of the token head (e.g. 'workout' is attached to 'schedule' as 'WHAT')
# 'deps' describes the semantic meaning (i.e. 'schedule' is the ROOT action of the sentence)
TRAIN_DATA = [
    ("schedule me a cardio workout for today", {
        'heads': [0, 0, 4, 4, 0, 4, 4],
        'deps': ['ROOT', '-', '-', 'ATTRIBUTE', 'WHAT', '-', 'TIME']
    }),
    ("display my workout schedule", {
        'heads': [0, 3, 3, 0],
        'deps': ['ROOT', '-', 'ATTRIBUTE', 'WHAT']
    }),
    ("show me my workout schedule for tomorrow", {
        'heads': [0, 0, 4, 4, 0, 4, 4],
        'deps': ['ROOT', '-', '-', 'ATTRIBUTE', 'WHAT', '-', 'TIME']
    }),
    ("display my calendar", {
        'heads': [0, 2, 0],
        'deps': ['ROOT', '-', 'WHAT']
    }),
    ("show my most recent workout stats", {
        'heads': [0, 5, 3, 4, 5, 0],
        'deps': ['ROOT', '-', '-', 'ATTRIBUTE', 'ATTRIBUTE', 'WHAT']
    }),
    ("enter feedback for my workout on Tuesday", {
        'heads': [0, 0, 1, 3, 1, 4, 4],
        'deps': ['ROOT', 'WHAT', '-', '-', 'ATTRIBUTE', '-', 'TIME']
    }),
    ("enter calories for today", {
        'heads': [0, 0, 1, 1],
        'deps': ['ROOT', 'WHAT', '-', 'TIME']
    }),
    ("show my workout schedule for today", {
        'heads': [0, 3, 3, 0, 3, 3],
        'deps': ['ROOT', '-', 'ATTRIBUTE', 'WHAT', '-', 'TIME']
    }),
    ("plan a workout for 5PM today", {
        'heads': [0, 2, 0, 2, 5, 2],
        'deps': ['ROOT', '-', 'WHAT', '-', 'TIME', 'TIME']
    })
]


@plac.annotations(
    model=("en", "option", "m", str),
    output_dir=(MODEL_DIR, "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=5):
    """Load the model, set up the pipeline and train the parser."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # We'll use the built-in dependency parser class, but we want to create a
    # fresh instance – just in case.
    if 'parser' in nlp.pipe_names:
        nlp.remove_pipe('parser')
    parser = nlp.create_pipe('parser')
    nlp.add_pipe(parser, first=True)

    for text, annotations in TRAIN_DATA:
        for dep in annotations.get('deps', []):
            parser.add_label(dep)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']
    with nlp.disable_pipes(*other_pipes):  # only train parser
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations], sgd=optimizer, losses=losses)
            print(losses)

    # test the trained model
    test_model(nlp)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        test_model(nlp2)


def test_model(nlp):
    texts = ["schedule an arms workout for Thursday",
             "show me my workout schedule for tomorrow",
             "display my current calendar"]
    docs = nlp.pipe(texts)
    for doc in docs:  # doc is a spaCy Token object
        print(doc.text)
        print([(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != '-'])

if __name__ == '__main__':
    plac.call(main, ['-m', 'en', '-o', MODEL_DIR, '-n', '5'])

