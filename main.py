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
def get_word():
  try:  
    word = input("type in word\n")
    defin = get_definition(word)
    return word,defin
  except:
    word = input("type in word\n")
    defin = get_definition(word)
    return word,defin
def get_choice(source):
  try:
    choice = int(input("\nWhich definition is applicable?"))-1
    choice = source[choice]
    return choice
  except:
    choice = int(input("\nWhich definition is applicable?"))-1
    choice = source[choice]
    return choice
  

running = True
while running:
    word,defi = get_word()
    for i in defi:

        print((defi.index(i)+1),'. ')
        print(i['partOfSpeech'],'\nDefinition:',i['definitions'][0]['definition'])
        try:print('\nExample:',i['definitions'][0]['example'])
        except:print('\nExample: None')
        try:print('\nsynonyms:',i['definitions'][0]['synonyms'])
        except:print('\nsynonyms: None')

    choice = get_choice(defi)

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