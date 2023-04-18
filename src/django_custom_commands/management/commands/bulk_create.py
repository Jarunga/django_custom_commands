from django.core.management.base import BaseCommand
import pandas as pd
from django.conf import settings
import os
import re
from .mixins import CommandMixin,Target,TargetM2M
import glob
import shutil

# BaseCommandを継承して作成
class Command(CommandMixin,BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'set initial data jarunga'

    def main(self,target):

        if os.path.isfile(target.path):
            target.model.objects.bulk_create(target.data_list)

        if target.through_dir is not None:
            for path in glob.glob(target.through_dir+'/*'):
                target_m2m=TargetM2M(path)
                print("throughフィールド_"+target_m2m.col_name+"を追加します。")
                target_m2m.model.objects.bulk_create(target_m2m.data_list)
                shutil.rmtree(path)

        print("更新が完了しました。")
