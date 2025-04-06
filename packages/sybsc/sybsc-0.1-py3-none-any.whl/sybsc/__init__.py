
import pkgutil

def get_text():
    return pkgutil.get_data(__name__, 'data.txt').decode('utf-8')
