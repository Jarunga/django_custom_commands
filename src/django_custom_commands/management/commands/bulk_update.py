from django.core.management.base import BaseCommand

import pandas as pd
from django.conf import settings
import os
from .mixins import CommandMixin,Target
from django.utils import timezone

# BaseCommandを継承して作成
class Command(CommandMixin,BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'set initial data jarunga'

    def main(self,target):

        target.model.objects.bulk_update(target.data_list,fields=[field for field in target.df.columns if field!=target.model._meta.pk.name]+[target.UPDATE_FIELD_NAME],batch_size=10000)
 
        print("更新が完了しました。")
