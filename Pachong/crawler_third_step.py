# # -*- coding: utf-8 -*-

import requests;
import csv;
import json;
import time;

def main(name):

	paper_id = [];
	with open("papers_"+name+"_modify.csv","r") as ft:
		reader=csv.reader(ft);
		for row in reader:
			if row[0]!="ID":
				# 存储所有的journal信息
				paper_id.append(row[0]);


	# 对每一篇文章做处理，找到对应的参考文献
	headers = {'Accept':'application/json'};
	str1="http://api.elsevier.com/content/abstract/EID:";
	str2="?apikey=ab6a63d43253501662ea07c589c6c0a8&view=REF";
	paper_total=[];
	first_row=["P_ID","R_ID","Journal","Author"];
	paper_total.append(first_row);

	count=1;
	for eid in paper_id:
		# 打印每篇文章id
		url_paper=str1+eid+str2;
		print(url_paper)
		# time.sleep(10);
		page_response=requests.get(url_paper, headers=headers);
		# print (page_response)
		page=json.loads(page_response.content.decode("utf-8"));
		# print(page.keys())
		# print(page['abstracts-retrieval-response'].keys())
		# 安全检查
		if page==None or 'abstracts-retrieval-response' in page.keys()==False:
			continue;

		if page['abstracts-retrieval-response']==None or 'references' in page['abstracts-retrieval-response']==False:
			continue;

		if page['abstracts-retrieval-response']['references']==None or 'reference' in page['abstracts-retrieval-response']['references'].keys()==False:
			continue;

		# 解析得到结果
		for paper in page['abstracts-retrieval-response']['references']['reference']:
			# print(paper)
			sourcetitle=paper['sourcetitle'];
			if sourcetitle==None: # 没有期刊
				continue;
			temp_author=[];
			if paper['author-list']==None:#没有作者
				continue;
			for element in paper['author-list']['author']:
				if 'ce:given-name' in element.keys():
					temp_author.append(element['ce:given-name']+" "+element['ce:surname']);
				else:
					temp_author.append(element['ce:indexed-name']);
			temp=[];
			temp.append(eid);#存入文章id
			temp.append(paper['scopus-eid']);#存入参考文献id
			temp.append(sourcetitle);#存入参考文献所在期刊
			temp.extend(temp_author);
			paper_total.append(temp);
			# print(temp)

		count=count+1;

	# 保存参考文献
	with open("papers_reference_journal_of_" + name + ".csv", "w", errors="ignore") as ft:
		writer = csv.writer(ft, dialect='unix')
		for x in paper_total:
			writer.writerow(x);


if __name__ == '__main__':
	main(name="neural_computation");