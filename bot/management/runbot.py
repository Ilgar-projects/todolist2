import logging
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal, Category

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        offset = 0
        logger.info('Bot start handling')

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        logger.info(f'Created: {created}')

        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle_unauthorized(self, tg_user: TgUser, msg: Message):
        self.tg_client.send_message(msg.chat.id, 'Hello!')
        code = tg_user.set_verification_code()
        self.tg_client.send_message(tg_user.chat_id, f'Your verification code is {code}')

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        logger.info('Authorized')
        if tg_user.state == 0:
            if msg.text == '/goals':
                goals = Goal.objects.filter(category__board__participants__user=tg_user.user,
                                            category__is_deleted=False,).exclude(status=Goal.Status.archived)
                self.tg_client.send_message(tg_user.chat_id, f'Ваши цели: {[goal.title for goal in goals]}')
            elif msg.text == '/create':
                categories = Category.objects.filter(board__participants__user=tg_user.user, is_deleted=False)
                self.tg_client.send_message(tg_user.chat_id,
                                            f'Выберите категорию: {[category.title for category in categories]}\n'
                                            )
                tg_user.state = 1
                tg_user.save()
            else:
                self.tg_client.send_message(tg_user.chat_id, f'Unknown command')
        elif tg_user.state == 1:
            self.choice_category(tg_user, msg)
        elif tg_user.state == 2:
            self.create_goal(tg_user, msg)

    def choice_category(self, tg_user: TgUser, msg):
        if Category.objects.filter(title=msg.text, board__participants__user=tg_user.user,
                                       is_deleted=False).exists():
            category = Category.objects.get(title=msg.text, board__participants__user=tg_user.user,
                                                is_deleted=False)
            tg_user.category = category
            tg_user.state = 2
            tg_user.save()

            self.tg_client.send_message(tg_user.chat_id, f'Ведите название цели: ')
        else:
            self.tg_client.send_message(tg_user.chat_id, 'категория не найдена')
            tg_user.state = 0
            tg_user.save()

    def create_goal(self, tg_user: TgUser, msg):

        goal = Goal.objects.create(category=tg_user.category, title=msg.text,
                                   user=tg_user.user)
        self.tg_client.send_message(tg_user.chat_id, f'ваша цель {goal.id} {goal.title} создана')
        tg_user.state = 0
        tg_user.category = None
        tg_user.save()
