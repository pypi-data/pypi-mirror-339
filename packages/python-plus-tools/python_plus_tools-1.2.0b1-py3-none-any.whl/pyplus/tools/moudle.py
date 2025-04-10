from sys import modules

def get_import_moudle_path():
    if __name__ != "__main__":
        main_moudle = modules['__main__']
        if hasattr(main_moudle, '__file__'):
            return main_moudle.__file__
        else:
            return 'This '