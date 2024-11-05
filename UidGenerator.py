last_id = 0

def generate_uid():
    global last_id
    last_id += 1
    return last_id