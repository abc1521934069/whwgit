import datetime
import random


def generate_id():
    return str(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randrange(1000, 9999, 1)) + str(random.randrange(1000, 9999, 1)))



