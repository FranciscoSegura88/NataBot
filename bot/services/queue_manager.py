class QueueManager:
    def __init__(self):
        self.queue = []

    def add_to_queue(self, song):
        self.queue.append(song)

    def get_next_song(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def clear_queue(self):
        self.queue.clear()

    def get_queue(self):
        return self.queue

    def is_empty(self):
        return len(self.queue) == 0

    def queue_size(self):
        return len(self.queue)
