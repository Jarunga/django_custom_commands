from django.core.management.base import BaseCommand

import pandas as pd
from django.conf import settings
import os
import numpy as np
from . import bulk_create
import glob
import sys

# BaseCommandを継承して作成
class Command(bulk_create.Command,BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'set initial data jarunga'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):

        for subdir in sorted(glob.glob(os.path.join('datafiles', '**' ,sys.argv[-1],'*'+ os.sep))):

            super().handle(directory=subdir)
