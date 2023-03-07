from django.core.management.base import BaseCommand

from ...dict_list import *
import pandas as pd
from django.conf import settings
import os
from .mixins import CommandMixin

# BaseCommandを継承して作成
class Command(CommandMixin,BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'set initial data jarunga'
        
    def main(self,target):

        target.model.objects.bulk_update(target.data_list)
 
        print("更新が完了しました。")
