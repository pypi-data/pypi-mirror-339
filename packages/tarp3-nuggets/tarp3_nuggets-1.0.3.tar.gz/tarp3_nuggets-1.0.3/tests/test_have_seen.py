from tarp3_nuggets import have_seen

def test_string_is_in_list() -> None:
    assert have_seen("this",['this', 'that']) == True
    
def test_number_is_in_list() -> None:
    assert have_seen(2,[1,2,3,4]) == True

def test_string_is_NOT_in_list() -> None:
    assert have_seen("this",['that','the','other']) == False
    
def test_number_is_NOT_list() -> None:    
    assert have_seen(2,[1,12,22,34]) == False