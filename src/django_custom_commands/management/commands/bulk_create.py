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
        if target.through_dir is not None:
            shutil.rmtree(target.through_dir)

    def main(self,target):

        target.model.objects.bulk_create(target.data_list)


