# Author:Haozhen Liu
# # -*- coding: utf-8 -*-

import requests;
import csv;
from bs4 import BeautifulSoup;

def main(name=""):

    # 构造URL需要用
    str1 = "http://www.scopus.com/results/results.uri?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1=";
    str2 = "&field1=TITLE&dateType=Publication_Date_Type&yearFrom=Before+1960&yearTo=Present&loadDate=7&documenttype=All&subjects=LFSC&_subjects=on&subjects=HLSC&_subjects=on&subjects=PHSC&_subjects=on&subjects=SOSC&_subjects=on&st1="
    str3 = "&st2=&sot=b&sdt=b&sl=66&s=TITLE%28";
    str4 = "%29&sid=B1008C74CB35D28A3D2FA576D9FBD993.53bsOu7mi7A1NSY7fPJf1g%3A380&searchId=B1008C74CB35D28A3D2FA576D9FBD993.53bsOu7mi7A1NSY7fPJf1g%3A380&txGid=B1008C74CB35D28A3D2FA576D9FBD993.53bsOu7mi7A1NSY7fPJf1g%3A38&sort=plf-f&originationType=b&rr=&null="

    papers_all = []  # paper_all存所有的查询结果，最后从paper_all存入csv文件
    first_row = ["ID", "Title", "Year", "Journal", "Author"];
    papers_all.append(first_row);#第一=“行加上列名称,每一行都是一个list
    # 读取每篇论文的题目，构造URL
    count = 0
    with open("papers_" + name + ".csv", "r") as ft:
        reader = csv.reader(ft);
        for row in reader:
            if row[0] != "ID" and row[0]!="":
                count = count + 1;
                str5 = row[1].replace(" ","+");#将标题以空格为分隔符分裂,分裂成一个list
                print(str5)
                str6 = str1 + str5 + str2 + str5 + str3 + str5 + str4;
                url_paper = str6;  # 构造好的url


                # 解析该url，得到每篇文章的id
                response_paper = requests.get(url_paper);
                soup_paper = BeautifulSoup(response_paper.content.decode("utf-8"), "html5lib");

                for tag_paper in soup_paper.find_all("input", attrs={"name": "selectedEIDs"}):
                    tag1 = tag_paper['id']
                    pid = str(tag1[11:])  # 得到每篇文章的id
                    temp_row = [];
                    temp_row.append(pid);
                    temp_row.extend(row[1:]);#将原表中除id外的信息都加入
                    papers_all.append(temp_row);  # 把每篇文章的信息得到
                    print (count, temp_row)

    #保存到csv文件中
    with open("papers_" + name + "_modify.csv", "w",errors="ignore") as ft:
        writer = csv.writer(ft, dialect='unix')
        for x in papers_all:
            writer.writerow(x);


if __name__ == '__main__':
    main(name="neural_networks");
