# input_handlers.py

var_options = ["Territory", "Brewery", "Beer", "Zak", "Jon", "Had", "Style", "ABV", "Added", "SRC"]

def get_valid_input(prompt, valid_options):
    response = input(prompt)
    while response not in valid_options:
        print("Invalid input.\n")
        response = input(prompt)
    return response

def query(n):
    if n == 1:
        return get_valid_input("What variable would you like to test?\n"
                               """Options are \"Territory,\" \"Brewery,\" \"Beer,\" \"Style,\" \"ABV,\" \"Added,\" and \"SRC.\" Your choice? """, var_options)
    elif n == 2:
        print("What two variables would you like to test?\n"
              "Options are \"Territory,\" \"Brewery,\" \"Beer,\" \"Zak,\" \"Jon,\" \"Had,\" \"Style,\" \"ABV,\" \"Added,\" and \"SRC.\"")
        return get_valid_input("X axis variable: ", var_options)
    elif n == 3:
        print("Pick a drinker (Jon or Zak) and a variable you'd like to test against.\n"
              "Options are \"Territory,\" \"Brewery,\" \"Beer,\" \"Style,\" \"ABV,\" \"Added,\" and \"SRC.\"")
        return get_valid_input("Who's drinking? ", var_options)
    elif n == 4:
        return get_valid_input("Who's drinking, Jon or Zak? ", var_options)

def query_2(m):
    if m == 1:
        return get_valid_input("Y axis variable: ", var_options)
    elif m == 2:
        return get_valid_input("Variable to test: ", var_options)


def collect_responses(b, best_data_options):
    var_options = ["Territory", "Brewery", "Beer", "Zak", "Jon", "Had", "Style", "ABV", "SRC"]
    if b == 0:
        print("Choose any three variables in the list below by entering their corresponding\n"
              "number separated by commas.\n"
              "1: Territory, 2: Brewery, 3: Beer, 4: Zak, 5: Jon, 6: Had, 7: Style, 8: ABV, 9: SRC")
        choices = input("Which variables are we testing? ")
    elif b == 1:
        choices = best_data_options  # Add before this function for every analysis
    listified = [item.strip() for item in choices.split(",")]
    for i in range(len(listified)):
        listified[i] = int(listified[i]) - 1

    selected_vars = []
    for z in listified:
        user_choice = var_options[z]
        selected_vars.append(user_choice)

    print()  # for newline after printed list

    if b == 0:
        return selected_vars
        # print(selected_vars)
    elif b == 1:
        print(f"the best variables to use are: {selected_vars}")