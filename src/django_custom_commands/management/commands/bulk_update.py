from django.core.management.base import BaseCommand

import pandas as pd
from django.conf import settings
import os
from .mixins import CommandMixin,Target
from .settings import UPDATE_FIELD_NAME
from django.utils import timezone

# BaseCommandを継承して作成
class Command(CommandMixin,BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'set initial data jarunga'

    def main(self,target):

        target.model.objects.bulk_update(target.data_list,fields=[field for field in target.df.columns if field!=target.model._meta.pk.name]+[UPDATE_FIELD_NAME])
 
        print("更新が完了しました。")
