import os
from datetime import datetime as dt
PATH = os.getcwd()  # Здесь можно подставить путь, куда будут сохраняться логи


def params_logger(path):

    def func_logger(function):

        def logger(*args, **kwargs):
            file_name = 'logs.txt'
            full_path = os.path.join(path, file_name)
            current_time = dt.now()
            name = function.__name__
            args_list = args
            kwargs_list = kwargs
            result = function(*args, **kwargs)
            if result is None:
                result = 'Void function'
            with open(full_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f'Date and time: {str(current_time)}\n')
                log_file.write(f'Function name: {name}\n')
                log_file.write(f'Arguments: {str(args_list)}\n')
                log_file.write(f'Keyword arguments: {str(kwargs_list)}\n')
                log_file.write(f'Function result: {str(result)}\n')
                log_file.write('_' * 100)
                log_file.write('\n\n')
            return result
        return logger
    return func_logger


@params_logger(PATH)
class ListIter:

    def __init__(self, nested_list):
        self.cursor = -1
        self.nested_list = nested_list
        self.inner_list = None

    def __iter__(self):
        return self.__next__()

    def __next__(self):
        while True:
            if self.inner_list:
                yield from self.inner_list
                self.inner_list = None
            else:
                self.cursor += 1
                if self.cursor == len(self.nested_list):
                    break
                value = self.nested_list[self.cursor]
                if type(value) is list:
                    self.inner_list = ListIter(value)
                else:
                    yield value


@params_logger(PATH)
def my_generator(target: list):
    start = 0
    end = len(target)
    while start < end:
        value = target[start]
        if type(value) is list:
            yield from my_generator(value)
        else:
            yield value
        start += 1


def main():
    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
        [[1, [2]], 5],
        [11, 7]
    ]
    print('Flat list in iterator:')
    for item in ListIter(nested_list):
        print(item)
    print('_' * 30)
    print('Flat list in generator:')
    for item in my_generator(nested_list):
        print(item)


if __name__ == '__main__':
    main()
