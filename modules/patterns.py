import re


# Bot replies to comments starting with this keyword.
main_trigger = '@translate'
# Regular expressions for the parameters.
# Comment must follow this structure: main_trigger language(2 chars) query(~)
lang_re = '[\w]{2}'
query_re = '.+'
full_trigger_pattern = re.compile(f'{main_trigger} ({lang_re}) ({query_re})')