def is_a_sublist_of_b(list_a, list_b):
    if not list_a:
        return True
    if not list_b:
        return False
    if list_a[0] == list_b[0]:
        return is_a_sublist_of_b(list_a[1:], list_b[1:])
    return is_a_sublist_of_b(list_a, list_b[1:])

def list_contains(list_a, element_b):
    return any(element_a == element_b for element_a in list_a)

def is_a_beginning_of_b(list_a, list_b):
    if not list_a:
        return True
    if not list_b:
        return False
    if list_a[0] == list_b[0]:
        return is_a_sublist_of_b(list_a[1:], list_b[1:])
    return False

def is_list_a_equal_to_b(list_a, list_b):
    if len(list_a) != len(list_b):
        return False
    for i in range(len(list_a)):
        if list_a[i] != list_b[i]:
            return False
    return True