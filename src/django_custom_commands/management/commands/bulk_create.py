from django.core.management.base import BaseCommand
import pandas as pd
from django.conf import settings
import os
import re
from .mixins import CommandMixin,Target
import glob
import shutil

# BaseCommandを継承して作成
class Command(CommandMixin,BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'set initial data jarunga'

    def remove(self,target):
        super().remove(target)
        if target.__through_dir is not None:
            shutil.rmtree(target.__through_dir)

    def main(self,target):

        target.model.objects.bulk_create(target.data_list)

        if target.through_dir is not None:
            for path in glob.glob(target.through_dir+'/*'):
                target_m2m=Target(path,is_through=True)
                print("throughフィールド_"+target_m2m.col_name+"の更新をします。")
                target_m2m.model.objects.bulk_create(target_m2m.data_list)

        print("更新が完了しました。")
