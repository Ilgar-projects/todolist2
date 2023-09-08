from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    model = TgUser
    serializer_class = TgUserSerializer

    def patch(self, request: Request, *args, **kwargs):
        s: TgUserSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)

        s.tg_user.user = request.user
        s.tg_user.save()

        TgClient().send_message(s.tg_user.chat_id, 'verification_have been completed')

        return Response(self.get_serializer(s.tg_user).data)