from selectors import DefaultSelector

selector = DefaultSelector()


def start_loop():
    while True:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key, mask)
