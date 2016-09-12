class Item(object):
    def __init__(self, description, command, topic_id):
        self.description = description
        self.command = command.encode('utf-8')
        self.topic_id = topic_id

    def __str__(self):
        return "{0}\n{1}\n{2}".format(self.topic_id, self.description, self.command)


class Topic(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "{0}".format(self.name)


