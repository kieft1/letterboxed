def count_of_letters(input_string:str):
    letter_count = {}
    repeated_count = {}

    for char in input_string:
        if char.isalpha():
            letter_count[char] = letter_count.get(char, 0) + 1
            repeated_count[char] = repeated_count.get(char, -1) + 1

    max_value = max(letter_count.values())
    count_max_keys = sum(value == max_value for value in letter_count.values())
    total_repeated_count = sum(repeated_count.values())

    return {"max_letter_count":max_value,"count_of_max_letter_count":count_max_keys,"total_repeated_count":total_repeated_count}

def results_scoring(list_of_chains:list):
    chains_with_results_profiling = {}
    for chain in list_of_chains:
        chains_with_results_profiling[chain]=count_of_letters(chain)
    return chains_with_results_profiling

def top_results(list_of_chains:list,top_n:int,ranking_criteria:str):
    # get the scoring for the list of chains
    rs = results_scoring(list_of_chains)

    # sort the results based on "max_letter_count" and then "count_of_max_letter_count"
    if ranking_criteria == "max_letter_count":
        sorted_items = sorted(rs.items(), key=lambda x: (x[1]['max_letter_count'], x[1]['count_of_max_letter_count']))
    elif ranking_criteria == "total_repeated_count":
        sorted_items = sorted(rs.items(), key=lambda x: (x[1]['total_repeated_count']))

    #for i in sorted_items: print(i)

    # rank the results
    previous_values = None
    rank = 0
    tie_rank = 1

    for word, values in sorted_items:
        if ranking_criteria == "max_letter_count":
            current_values = (values['max_letter_count'], values['count_of_max_letter_count'])
        elif ranking_criteria == "total_repeated_count":
            current_values = (values['total_repeated_count'])

        rank += 1

        if current_values != previous_values:
            tie_rank = rank

        values['rank'] = tie_rank
        previous_values = current_values

    # return results for top_n
    results = []
    for word, values in sorted_items:
        if values['rank'] <= top_n:
            results.append(f"{values['rank']}. {word}")

    return results