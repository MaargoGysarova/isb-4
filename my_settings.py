from settings import read_settings

def my_function(path):
    setting = read_settings('settings.json')
    return setting
