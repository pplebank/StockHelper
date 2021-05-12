# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import sys, os
import numpy as np
import pandas as pd
from stockscrape.Credentials import Credentials as creds
import pandas.io.sql as psql


class StockscrapePipeline(object):

    def open_spider(self, spider):
        try:
            connect_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER +" password="+ creds.PGPASSWORD
            self.connect=psycopg2.connect(connect_string)
            self.cursor = self.connect.cursor()

        except(Exception,psycopg2.Error) as error:
            print("Failed to connect with table", error)

    def close_spider(self, spider):
        self.connect.close()
        
    def process_item(self, item, spider):
        postgres_sql_command = '''INSERT INTO stock_links(stock_name,stock_link,stock_last_update) VALUES (%s,%s,%s)'''
        item_to_add = (item.get('name'),item.get('URL'),item.get('date'))
        self.cursor.execute(postgres_sql_command,item_to_add)
        self.connect.commit()
        return item