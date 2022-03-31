from datetime import date,datetime,timedelta
import pandas as pd
import os
from matplotlib import font_manager as fm, rcParams, rc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pymongo
import numpy as np

#database
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
mykeynamecollection = mydb["KeyNameData"]
myrecordcollection = mydb["RecordDatabase7"]
mynumbercollection = mydb["RecordDBNumber"]

class get_graph(object):
	"""docstring for get_percentage"""
	def __init__(self, arg):
		super(get_record, self).__init__()
		self.arg = arg

	def find_record(uin):
		keybox = uin[2]
		starting_date = uin[0]
		ending_date   = uin[1]

		#variable
		datetime_list, status_list, key_name_list, dateonly_list, keybox_list = ([] for i in range(5))
		dept_name_list, usr_name_list, id_list, rentcomp_list, rentcompid_list = ([] for i in range(5))
		temp1 = []
		temp2 = []
		date1 = '2020-01-01'
		date2 = '2020-12-31'
		mydates = pd.date_range(date1, date2).tolist()
		for i in range(0,len(mydates)):
			temp1.append(str(mydates[i])[:10])
		mydates = temp1

		if any(x in mydates for x in uin):
			for i in range(1,16):
				collname = "RecordDatabase" + str(i)
				myrecordcollection = mydb[collname]
				findRecord = myrecordcollection.find(filter = { '日付' : { '$gte' : uin[0] , '$lte' : uin[1] }})
				for doc_record in findRecord:
					dateonlyrecord=doc_record["日付"]
					dateonly_list.insert(0, dateonlyrecord)
					status=doc_record["状況"]
					status_list.insert(0, status) 
					key_name=doc_record["キー名"]
					key_name_list.insert(0, key_name)
					dept_name=doc_record["部署名"]
					dept_name_list.insert(0, dept_name)
					epcbox=doc_record["キーボックスNo"]
					keybox_list.insert(0, epcbox)

		df = pd.DataFrame({'日付' : dateonly_list, '状況': status_list, 'キー名': key_name_list, '部署名': dept_name_list, 'キーボックスNo': keybox_list})
		
		df['日付'] = pd.to_datetime(df['日付'], errors='ignore')
		mask = (df['日付'] >= starting_date) & (df['日付'] <= ending_date)
		df = df.loc[mask]
		df['日付'] = df['日付'].dt.strftime('%Y-%m-%d')

		if keybox == "1":
			df = df[df['キーボックスNo'] == "キーボックス 1"]
		if keybox == "2":
			df = df[df['キーボックスNo'] == "キーボックス 2"]
		df = df[df['状況'] == "貸出"]
		df = df[["日付","部署名","キー名"]]

		return df

	def dategraph(uin):
		rowlist = []
		columnlist = []

		#Font
		fpath = os.path.join(rcParams["datapath"], "C:\\Fonts\\NotoSansJP-Regular.otf")
		prop = fm.FontProperties(fname=fpath)
		fname = os.path.split(fpath)[1]

		df = get_graph.find_record(uin)
		df = df[["日付"]]

		starting_date = datetime.strptime(uin[0], '%Y-%m-%d').date()
		ending_date   = datetime.strptime(uin[1], '%Y-%m-%d').date()
		delta = ending_date - starting_date
		# print(delta)

		for i in range(delta.days+1):
			day = starting_date + timedelta(days=i)
			rowlist.append(day)
			columnlist.append(len(df[df['日付'] == str(day)]))

		# Define plot space
		if len(rowlist) <= 30:
			fig, ax = plt.subplots(figsize=(20, 15))
			ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
		else:
			fig, ax = plt.subplots(figsize=(30, 30))
			ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
		rcParams.update({'figure.autolayout': True})

		# Define x and y axes
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
		ax.plot(rowlist, columnlist)
		ax.set_xlabel(u'日付'.format(fname), rotation=0, color='k', labelpad=10, fontproperties=prop, fontsize=30)
		ax.set_ylabel(u'貸出回'.format(fname), rotation=90, color='k', labelpad=10, fontproperties=prop, fontsize=30)

		plt.xticks(rotation=90, fontproperties=prop, fontsize=30)
		plt.yticks(rotation=0, fontproperties=prop, fontsize=30)

		fig.savefig("C:\\Face\\static\\photo\\dategraph.png",bbox_inches='tight')

		url='/static/photo/dategraph.png'
		
		return url

	def keynamegraph(uin):
		keybox = uin[2]
		rowlist, columnlist = ([] for i in range(2))

		#Font
		fpath = os.path.join(rcParams["datapath"], "C:\\Fonts\\NotoSansJP-Regular.otf")
		prop = fm.FontProperties(fname=fpath)
		fname = os.path.split(fpath)[1]

		df = get_graph.find_record(uin)
		df = df[["キー名"]]

		#Find Column
		for i in range(1,101):
			if i <= 9:
				string = "00%i" %i
			elif i <= 99:
				string = "0%i" %i
			elif i == 100:
				string = "100"
			columnlist.insert(0,string)

		#Find Row
		for i in columnlist:
			# rowlist.append(len(df[df['キー名'] == i]))
			rowlist.append(len(df[df['キー名'].str.contains(i, na=False)]))

		# Define plot space
		fig, ax = plt.subplots(figsize=(30, 100))
		rcParams.update({'figure.autolayout': True})

		# Define x and y axes
		ax.barh(columnlist, rowlist)
		ax.set_xlabel(u'貸出回'.format(fname), rotation=0, color='k', labelpad=10, fontproperties=prop, fontsize=50)
		ax.set_ylabel(u'キー'.format(fname), rotation=90, color='k', labelpad=10, fontproperties=prop, fontsize=50)

		plt.xticks(rotation=0, fontproperties=prop, fontsize=50)
		plt.xticks(np.arange(0, max(rowlist)+1, 5))
		plt.yticks(rotation=0, fontproperties=prop, fontsize=50)

		fig.savefig("C:\\Face\\static\\photo\\keyname.png",bbox_inches='tight')

		url='/static/photo/keyname.png'
		
		return url

	def compnamegraph(uin):
		keybox = uin[2]
		compnamelist, per_list = ([] for i in range(2))

		#Font
		fpath = os.path.join(rcParams["datapath"], "C:\\Fonts\\NotoSansJP-Regular.otf")
		prop = fm.FontProperties(fname=fpath)
		fname = os.path.split(fpath)[1]

		df = get_graph.find_record(uin)
		df = df[["日付","部署名"]]

		totalcount = len(df)
		compnamelist = df['部署名'].unique()

		#Find Row
		for a in range(0,len(compnamelist)):
			percount = len(df[df['部署名'] == compnamelist[a]])
			percentage=100*(percount/totalcount)
			per_list.append(round(percentage))
			# if percentage >= 1:
			# 	per_list.append(round(percentage))
		fig1, ax1 = plt.subplots()
		ax1.pie(per_list, autopct='%1.1f%%')
		# ax1.pie(per_list, autopct='%1.1f%%',startangle=90)
		ax1.axis('equal')
		plt.title('部署名グラフ', weight='bold', size=14, fontproperties=prop)
		ax1.legend(compnamelist,loc="center left",bbox_to_anchor=(1, 0, 0.5, 1), prop=prop)
		plt.savefig("C:\\Face\\static\\photo\\companygraph.png",bbox_inches='tight')

		url='/static/photo/companygraph.png'
		
		return url

# uin = ["2020-07-01", "2020-07-13", "2"]
# get_graph.keynamegraph(uin)