from peewee import *
from settings import config

#database = MySQLDatabase('annots', **config)
database = SqliteDatabase('annotations.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AnnotidField(AutoField):

    def db_value(self, value):
        return int(value, 16)

    def python_value(self, value):
        return hex(value)
        


class Annotation(BaseModel):
    annotid = AnnotidField()
    file_name = TextField(null=True)
    month = TextField(null=True)
    object_name = TextField(null=True)
    object_present = TextField(null=True)
    speaker = TextField(null=True)
    utterance_type = TextField(null=True)
    audio_video = TextField(null=True)
    date_added = DateField(null=True)

    def __str__(self):
        return '''
        annotid = %s
        file_name = %s
        month = %s
        object_name = %s
        object_present = %s
        speaker = %s
        utterance_type = %s
        audio_video = %s
        date_added = %s
        '''



if __name__ == "__main__":
    database.create_tables([Annotation])


