import pandas as pd
import os
import re
from django.conf import settings
from importlib import import_module
from django.utils.timezone import make_aware
from datetime import datetime, timezone
from pathlib import Path
import glob
import importlib
import sys
from .settings import DATETIME_FIELDS,UPDATE_FIELD_NAME
from django.utils import timezone

class Target:
    
    def __init__(self,path,is_through=False):
        self.__path=path
        self.__app_name=Path(path).parts[1]
        
        if is_through:
            self.__model_name=os.path.splitext(os.path.basename(Path(path).parts[-2]))[0]
            self.__col_name=self.get_col_name()
        else:
            self.__model_name=os.path.splitext(os.path.basename(Path(path).parts[-1]))[0]
            self.__col_name=None
        
        self.__through_dir=self.get_through_dir()

        self.__model=self.get_model()

        if '.csv' in path:
            self.__df=self.read_frame()
            self.__data_list=self.get_data_list()

    def get_through_dir(self):
        through_dir=os.path.join(os.path.dirname(self.path),self.model_name)

        if os.path.isdir(through_dir):
            return through_dir
        else:
            return None

    def get_col_name(self):
        return os.path.splitext(os.path.basename(Path(self.path).parts[-1]))[0]

    def get_model(self):
        models=importlib.import_module('%s.models'% self.app_name)

        if self.col_name is None:        
            model=eval('models.%s' % self.model_name)
        else:
            model=eval("models.%s.%s.through" % (self.model_name,self.col_name))

        return model

    def read_frame(self):
        df=pd.read_csv(self.path,dtype=str,na_filter=False)

        df=self.native_to_aware(df)
        df=df.applymap(lambda x:None if str(x)=='' else str(x))

        if sys.argv[1]=='bulk_update':
            df[UPDATE_FIELD_NAME]=timezone.now()

        return df

    def native_to_aware(self,df):
        for field in DATETIME_FIELDS:
            if field in df.columns:
                df[field]=df[field].map(lambda x:make_aware(datetime.fromisoformat(str(x))) if str(x)!="" else "")
        return df

    def get_data_list(self):
        data_list = [
            self.model(**{key:self.df.loc[i,key] for key in self.df.columns}) for i in range(len(self.df))
        ]

        return data_list

    @property
    def path(self):
        return self.__path
    
    @property
    def app_name(self):
        return self.__app_name

    @property
    def model_name(self):
        return self.__model_name

    @property
    def df(self):
        return self.__df

    @property
    def model(self):
        return self.__model

    @property
    def through_dir(self):
        return self.__through_dir

    @property
    def data_list(self):
        return self.__data_list

    @property
    def col_name(self):
        return self.__col_name

class CommandMixin:

    def get_directory(self, *args, **options):
        if 'directory' in options:
            directory=os.path.join(options['directory'],'*.csv')
            
        else:
            directory=os.path.join('datafiles','**',sys.argv[-1],'*')

        return directory

    def remove(self,target):
        os.remove(target.path)

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):

        for path in glob.glob(self.get_directory(*args, **options),recursive=True):
            print(path)

            target=Target(path)

            if '.csv' in path:

                print("「%s」テーブル %s件 (%s) を追加します。はい=1,いいえ=0" % (target.model_name,str(len(target.df)),",".join([n for n in target.df.columns])))

                select=input()

                if select=="1":
                    self.main(target)
                    self.remove(target)
                    print("更新が完了しました。") 

                else:
                    print("更新がキャンセルされました。")

            else:
                
                if target.through_dir is not None:
                    for path in glob.glob(target.through_dir+'/*'):
                        target_m2m=Target(path,is_through=True)
                        print("throughフィールド_"+target_m2m.col_name+"の更新をします。はい=1,いいえ=0")
                        select=input()

                        if select=="1":
                            self.main(target_m2m)
                            self.remove(target_m2m)
                            print("更新が完了しました。")
                            
                        else:
                            print("更新がキャンセルされました。")

    def add_arguments(self , parser):
        parser.add_argument('--file', action='append', type=str)
        parser.add_argument('--models', action='append', type=str)
        parser.add_argument('--all', action='store_true')


