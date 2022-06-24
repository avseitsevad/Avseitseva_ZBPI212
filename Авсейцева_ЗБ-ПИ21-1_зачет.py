def test_problem(func, test_data):
  """test helper"""
  for inputs, true_answer in test_data:
    if isinstance(inputs, tuple):
        answer = func(*inputs)
    else:
        answer = func(inputs)
    if answer != true_answer:
      print("wrong")
      return 0
  return 1

#массивы
#1. написать функцию, которая перемещает все элементы одного типа в конец списка
# https://edabit.com/challenge/nTW4KgmJxpLDXcWPt
def test_move_to_end(move_to_end_func):
    test_data = [
    (([1, 3, 2, 4, 4, 1], 1), [3, 2, 4, 4, 1, 1]),
    ([7, 8, 9, 1, 2, 3, 4], 9, [7, 8, 1, 2, 3, 4, 9])]
    return test_problem(move_to_end_func, test_data)
    

def move_to_end(lst, el):
    return sorted(lst, key = lambda x: x == el)

assert test_move_to_end(move_to_end) == 1, "Неправильно, попробуй еще раз"
    
#написать функцию, которая принимает на ввод список и возвращает два числа:
#первое - сумма четных чисел списка, второе - сумма нечетных
#https://edabit.com/challenge/5XXXppAdfcGaootD9
def test_sum_odd_and_even(sum_func):
    test_data = [
    ([1, 2, 3, 4, 5, 6], [12, 9]),
    ([-1, -2, -3, -4, -5, -6], [-12, -9]),
    ([0, 0], [0, 0])]
    return test_problem(sum_func, test_data)

def sum_odd_and_even(lst):
	return [sum(i for i in lst if not i%2), sum(i for i in lst if i%2)]
assert test_sum_odd_and_even(sum_odd_and_even) == 1, "Неправильно, попробуй еще раз"


#в списке положительных и отрицательных элементов найти число, для которого нет
#противоположной пары
#https://edabit.com/challenge/onGPLPhXkLr3KCJpF
def test_lonely_integer(lonely_integer_func):
    test_data = [
        ([1, -1, 2, -2, 3], 3),
        ([-3, 1, 2, 3, -1, -4, -2], -4),
        ([-9, -105, -9, -9, -9, -9, 105], -9)]
def lonely_integer(lst):
	return sum(set(lst))
assert test_lonely_integer(lonely_integer) == 1, "Неправильно, попробуй еще раз"
