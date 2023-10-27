from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import  Filterlog
from .serializers import AllFilterLogSerializer


class PostConsumer(ListModelMixin, GenericAsyncAPIConsumer):

    queryset = Filterlog.objects.all()
    serializer_class = AllFilterLogSerializer
    permissions = (permissions.AllowAny,)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Filterlog)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=AllFilterLogSerializer(instance=instance).data, action=action.value)
