# Experiments
import re

# Sanitize time string: leave only digits & ':' symbol
s = "Example String 123 dfghdf:sdfgsd"

replaced = re.sub('[^\d\:]', '', s)

print(replaced)