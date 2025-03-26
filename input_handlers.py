# input_handlers.py

var_options = ["Territory", "Brewery", "Beer", "Zak", "Jon", "Had", "Style", "ABV", "SRC"]

def get_valid_input(prompt, valid_options):
    response = input(prompt)
    while response not in valid_options:
        print("Invalid input.\n")
        response = input(prompt)
    return response

def query(n):
    if n == 1:
        return get_valid_input("What variable would you like to test? ", var_options)
    elif n == 2:
        print("What two variables would you like to test?\n"
              "Options are \"Territory,\" \"Brewery,\" \"Beer,\" \"Zak,\" \"Jon,\" \"Had,\" \"Style,\" \"ABV,\" and \"SRC.\"")
        return get_valid_input("X axis variable: ", var_options)
    elif n == 3:
        print("Pick a drinker (Jon or Zak) and a variable you'd like to test against.\n"
              "Options are \"Territory,\" \"Brewery,\" \"Beer,\" \"Style,\" \"ABV,\" and \"SRC.\"")
        return get_valid_input("Who's drinking? ", var_options)

def query_2(m):
    if m == 1:
        return get_valid_input("Y axis variable: ", var_options)
    elif m == 2:
        return get_valid_input("Variable to test: ", var_options)