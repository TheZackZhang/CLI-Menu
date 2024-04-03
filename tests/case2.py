from source.prompt import Prompt, DatePrompt

any_value = Prompt('Enter any value: ').loop()

date = DatePrompt('Enter a date: ').loop()