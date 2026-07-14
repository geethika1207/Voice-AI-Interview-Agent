class AudioBuffer:

    def __init__(self):

        self.chunks = []


    def add_chunk(self, chunk: bytes):

        self.chunks.append(chunk)


    def get_audio(self):

        return b"".join(self.chunks)


    def reset(self):

        self.chunks.clear()