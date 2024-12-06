def remove_duplicates(lst):
    return list(set(lst))


def custom_sort(lst):
    numbers = sorted([x for x in lst if isinstance(x, int)])
    strings = sorted([x for x in lst if isinstance(x, str)])

    return numbers + strings


def process_list(lst):
    unique_list = remove_duplicates(lst)
    sorted_list = custom_sort(unique_list)
    return sorted_list


list_practice = [1, 2, 3, 4, 5, 6, 3, 4, 5, 7, 6, 5, 4, 3, 4, 5, 4, 3, 'Привіт','Анаконда']
result_practice = process_list(list_practice)
print(result_practice)