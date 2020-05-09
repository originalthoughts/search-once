import requests
import genanki

base = "https://api.dictionaryapi.dev/api/v2/entries/en/"


my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name':'example'},
    {'name':'synonyms'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><br>{{example}}<br><br>{{synonyms}}',
    },
  ])
my_deck = genanki.Deck(
  2059400110,
  'session')


def get_definition(word):
    url = base + word
    r = requests.get(url)
    out = r.json()[0]['meanings']
    return out

running = True
while running:
    word = input("type in word\n")
    defi = get_definition(word)
    for i in defi:
        print((defi.index(i)+1),'. ')

        print(i['partOfSpeech'],'\nDefinition:',i['definitions'][0]['definition'])
        try:print('\nExample:',i['definitions'][0]['example'])
        except:print('\nExample: None')
        try:print('\nsynonyms:',i['definitions'][0]['synonyms'])
        except:print('\nsynonyms: None')

    choice = int(input("\nWhich definition is applicable?"))
    choice = defi[choice-1]

    question = choice['partOfSpeech']+": "+word
    answer = choice['definitions'][0]['definition']
    try:example = choice['definitions'][0]['example']
    except:example = ''
    try:synonyms = str(choice['definitions'][0]['synonyms'])
    except:synonyms = ''

    my_note = genanki.Note(
    model=my_model,
    fields=[question,answer,example,synonyms]
    )
    my_deck.add_note(my_note)
    
    end = input('press enter to continue, q to quit')
    if end == 'q':
        running = False

genanki.Package(my_deck).write_to_file('output.apkg')