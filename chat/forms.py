from mongodbforms import DocumentForm
from documents import Message


class MessageForm(DocumentForm):
    class Meta:
        document = Message
        fields = ("text",)