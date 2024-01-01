def get_todays_metadata():
    import requests, json
    r = requests.get("https://www.nytimes.com/puzzles/letter-boxed")

    # identify gameData from console
    start_string = r.text.index("window.gameData")
    start_parens = start_string + r.text[start_string:].index("{")
    end_string = start_parens+ r.text[start_parens:].index(",\"dictionary")
    todays_metadata = json.loads(r.text[start_parens:end_string]+"}")

    # identify dictionary
    start_dict = r.text.index(",\"dictionary\":")
    start_dict = start_dict + r.text[start_dict:].index("[")
    end_dict = start_dict+ r.text[start_dict:].index("]")
    todays_dictionary = r.text[start_dict:end_dict+1]

    #print(r.text)

    return {'sides': todays_metadata['sides'], 'nyt_solution': todays_metadata['ourSolution'], 'date': todays_metadata['printDate'], 'dictionary': todays_dictionary}

def save_todays_dictionary():
    import ast
    from datetime import datetime
    import os

    todays_metadata = get_todays_metadata()
    words = ast.literal_eval(todays_metadata['dictionary'])
    current_date = datetime.now().strftime("%Y-%m-%d")

    directory = r".\words\nyt"
    file_name = f"{current_date}.txt"
    file_path = os.path.join(directory, file_name)
    file_content = "\n".join(words)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w') as file:
        file.write(file_content)

    print(f"Today's dictionary saved to: {file_path}")