# import pandas as pd, pymongo, datetime, logging
#TORONOMOM SITE no room 
import pandas as pd, pymongo, datetime, logging,numpy as np

import time, sys, pymongo,os
from save_log import get_log
import os
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
from datetime import date, timedelta

from keystatusclass import get_list


myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myrecordcollection = mydb["RecordDatabase2"]
mynumbercollection = mydb["RecordDBNumber"]
myStatuscollection = mydb["KeyStatus"]
myrecordpgshowdatedbcollection = mydb["RecordShowDateDB"]

#log saving
log_dir = 'C:\\Face\\log1'
os.chmod(log_dir, 0o777)
get_log.setup_logger('log4', 'C:\\Face\\log1\\Rpilog.log')
logger_4 = logging.getLogger('log4')

class get_record(object):
	def __init__(self, arg):
		super(get_record, self).__init__()
		self.arg = arg

	def output_df(uinlist, tagnamelist, nolist, dateoftoday):
		findRecord = keyidtofilter = starting_date = ending_date = keynametofilter = compnamefilt = usernamefilt = ""
		datetime_identifier, status_identifier, key_name_identifier, indexlist = ([] for i in range(4))
		dept_name_identifier, usr_name_identifier, id_identifier, keybox_identifier = ([] for i in range(4))
		keynamelist, keyIdlist, rentcomp_identifier, rentcompid_identifier = ([] for i in range(4))
		datedb_list, dates,dateonly ,keyname_list = ([] for i in range(4))

		uin = uinlist
		keynamelist = tagnamelist
		numberlist = nolist
		finddates = myrecordpgshowdatedbcollection.find()  # from database get the start and end date
		for doc_mode in finddates:
			startdate = doc_mode["starting_date"]
			enddate = doc_mode["ending_date"]

		try:
			if len(uin) > 0:
				if "today" in uin:
					for i in range(1,16):
						collname = "RecordDatabase" + str(i)
						myrecordcollection = mydb[collname]
						findRecord = myrecordcollection.find(filter = { '日付' : dateoftoday})
						for doc_record in findRecord:
							datetimerecord=doc_record["時刻"]
							datetime_identifier.insert(0,datetimerecord)
							status=doc_record["状況"]
							status_identifier.insert(0,status) 
							key_name=doc_record["キー名"]
							key_name_identifier.insert(0,key_name)
							dept_name=doc_record["部署名"]
							dept_name_identifier.insert(0,dept_name)
							usr_name=doc_record["貸出者"]
							usr_name_identifier.insert(0,usr_name)
							id_=doc_record["タグID"]
							id_identifier.insert(0,id_)
							epcbox=doc_record["キーボックスNo"]
							keybox_identifier.insert(0,epcbox)
							rentcmp=doc_record["レンタル会社"]
							rentcomp_identifier.insert(0,rentcmp)
							rentcmpid=doc_record["番号"]
							rentcompid_identifier.insert(0,rentcmpid)

				if "past" in uin:
					uin.remove('past')

				if "today" not in uin:
					try:
						if datetime.datetime.strptime(uin[0], '%Y-%m-%d') or datetime.datetime.strptime(uin[1], '%Y-%m-%d'):
							for i in range(1,16):
								collname = "RecordDatabase" + str(i)
								myrecordcollection = mydb[collname]
								findRecord = myrecordcollection.find(filter = { '日付' : { '$gte' : uin[0] , '$lte' : uin[1] }})
								for doc_record in findRecord:
									datetimerecord=doc_record["時刻"]
									datetime_identifier.insert(0,datetimerecord)
									status=doc_record["状況"]
									status_identifier.insert(0,status) 
									key_name=doc_record["キー名"]
									key_name_identifier.insert(0,key_name)
									dept_name=doc_record["部署名"]
									dept_name_identifier.insert(0,dept_name)
									usr_name=doc_record["貸出者"]
									usr_name_identifier.insert(0,usr_name)
									id_=doc_record["タグID"]
									id_identifier.insert(0,id_)
									epcbox=doc_record["キーボックスNo"]
									keybox_identifier.insert(0,epcbox)
									rentcmp=doc_record["レンタル会社"]
									rentcomp_identifier.insert(0,rentcmp)
									rentcmpid=doc_record["番号"]
									rentcompid_identifier.insert(0,rentcmpid)
					except Exception as e:
						for i in range(1,16):
							collname = "RecordDatabase" + str(i)
							myrecordcollection = mydb[collname]
							findRecord = myrecordcollection.find()
							for doc_record in findRecord:
								datetimerecord=doc_record["時刻"]
								datetime_identifier.insert(0,datetimerecord)
								status=doc_record["状況"]
								status_identifier.insert(0,status) 
								key_name=doc_record["キー名"]
								key_name_identifier.insert(0,key_name)
								dept_name=doc_record["部署名"]
								dept_name_identifier.insert(0,dept_name)
								usr_name=doc_record["貸出者"]
								usr_name_identifier.insert(0,usr_name)
								id_=doc_record["タグID"]
								id_identifier.insert(0,id_)
								epcbox=doc_record["キーボックスNo"]
								keybox_identifier.insert(0,epcbox)
								rentcmp=doc_record["レンタル会社"]
								rentcomp_identifier.insert(0,rentcmp)
								rentcmpid=doc_record["番号"]
								rentcompid_identifier.insert(0,rentcmpid)
				
				for i in datetime_identifier:
					datedb_list.append(i[0:10])
					dateonly.append(i[0:10])
				dateonly = list(dict.fromkeys(dateonly))	#to avoid duplicacy
			
				
				smonth=startdate  # assign date
				emonth=enddate

				sm=int(smonth[5:7]) # splits month
				em=int(emonth[5:7])

				sy=int(smonth[0:4]) # splits year
				ey=int(emonth[0:4])
			
				sd=int(smonth[8:10]) #splits day
				ed=int(emonth[8:10])
                

				keyidlist      = get_list.keyid_list(1)
				statusidlist   = get_list.statusid_list(1)
				keyname_list   = get_list.epcname_list(1)
				keyidlist2      = get_list.keyid_list(2)
				statusidlist2   = get_list.statusid_list(2)
				keyname_list2   = get_list.epcname_list(2)
				keyidlist3      = get_list.keyid_list(3)
				statusidlist3   = get_list.statusid_list(3)
				keyname_list3   = get_list.epcname_list(3)
				keyidlist4      = get_list.keyid_list(4)
				statusidlist4   = get_list.statusid_list(4)
				keyname_list4   = get_list.epcname_list(4)
				
				# print(len(dateonly))
				# print(keyname_list)
				

				df = pd.DataFrame({'日付' : datedb_list, '時刻': datetime_identifier, '状況': status_identifier, 'キー名': key_name_identifier, '部署名': dept_name_identifier, '貸出者': usr_name_identifier, 'タグID': id_identifier, 'キーボックスNo': keybox_identifier, 'レンタル会社': rentcomp_identifier, '番号': rentcompid_identifier })
				df['日付']=pd.to_datetime(df['日付'], errors='ignore', format="%Y-%m-%d")

				df_copy1 =pd.DataFrame(df[["日付","状況","キー名","部署名","貸出者","タグID","キーボックスNo","レンタル会社","番号"]])
				df_copy2 =pd.DataFrame(df[["日付","状況","キー名","部署名","貸出者","タグID","キーボックスNo","レンタル会社","番号"]])
				df_copy3 =pd.DataFrame(df[["日付","状況","キー名","部署名","貸出者","タグID","キーボックスNo","レンタル会社","番号"]])
				df_copy4 =pd.DataFrame(df[["日付","状況","キー名","部署名","貸出者","タグID","キーボックスNo","レンタル会社","番号"]])
				today = dateoftoday
				# print(df)

				if "box1" in uin:
					df = df[df['キーボックスNo'] == "キーボックス 1"]
				if "box2" in uin:
					df = df[df['キーボックスNo'] == "キーボックス 2"]
				if "box3" in uin:
					df = df[df['キーボックスNo'] == "キーボックス 3"]
				if "box4" in uin:
					df = df[df['キーボックスNo'] == "キーボックス 4"]	
				if "all" in uin:
					df = df
				if "box1" not in uin and "box2" not in uin and "box3" not in uin and "box4" not in uin and "all" not in uin:
					df = df

				if "today" in uin:
					df = df[df['日付'] == dateoftoday]
					if uin[3] != "":
						compnamefilt = uin[3]
						df = df[df['部署名'].str.contains(compnamefilt, na=False)]
					if uin[4] != "":
						usernamefilt = uin[4]
						df = df[df['貸出者'].str.contains(usernamefilt, na=False)]
					if any(x in numberlist for x in uin):
						keynametofilter = uin[6]
						for n in range(1,11):
							if keynametofilter == str(n):
								keynametofilter = "00" + keynametofilter
						for n in range(10,100):
							if keynametofilter == str(n):
								keynametofilter = "0" + keynametofilter
						if keynametofilter == str(100):
							keynametofilter = "100"
						df = df[df['キー名'].str.contains(keynametofilter, na=False)]

				else:
					if uin[2] != "":
						compnamefilt = uin[2]
						df = df[df['部署名'].str.contains(compnamefilt, na=False)]
					if uin[3] != "":
						usernamefilt = uin[3]
						df = df[df['貸出者'].str.contains(usernamefilt, na=False)]
					if any(x in numberlist for x in uin):
						keynametofilter = uin[5]
						for n in range(1,11):
							if keynametofilter == str(n):
								keynametofilter = "00" + keynametofilter
						for n in range(10,100):
							if keynametofilter == str(n):
								keynametofilter = "0" + keynametofilter
						if keynametofilter == str(100):
							keynametofilter = "100"
						df = df[df['キー名'].str.contains(keynametofilter, na=False)]

				if "both" not in uin and "returned" in uin:
					df = df[df['状況'] == '返却']
				if "both" not in uin and "taken" in uin:
					df = df[df['状況'] == '貸出']

				df = df[["時刻","状況","キー名","部署名","貸出者","タグID","キーボックスNo","レンタル会社","番号"]]

				try:
					d1 = date(sy, sm, sd)
					# print(d1)
					d2 = date(ey, em, ed)
					# print(d2)
					delta = d2 - d1
					list1=[(d1 + timedelta(days=i)).strftime('%m-%d') for i in range(delta.days + 1)]
					name=list1[0]
					
					time=pd.DataFrame()
					
					
					time['Status']=statusidlist #created a dataframe with these three column
					time['Keyname']=keyidlist
					time['Key'] = keyname_list
					time["Day"]=pd.Series(list1)


					time=time.pivot(index=["Keyname","Key"],columns='Day',values='Status')
					time=time.fillna("-")
					time = time.iloc[: , 1:]

					df_new=pd.DataFrame(df_copy1[["日付","状況","キー名","キーボックスNo","タグID"]])
		
					df_new=df_new.loc[df_new['キーボックスNo']=='キーボックス 1']
					
					df_box1=pd.DataFrame(df_new[["日付","状況","キー名","タグID"]])	
					# print(df_box1)
				
					for j in range(0,len(dateonly)):
						fd_a=pd.DataFrame(df_box1.loc[df_box1["日付"] == (dateonly[j])])

						fd_b=fd_a[["タグID"]]
						
						fd_b=fd_b.drop_duplicates()
						
					
						for i in range(0,len(fd_b)):
							
							# print(list1[i])
							a=str(fd_b.iloc[i].values)
							a=a[2:-2]
						
							b=dateonly[j]
							b=b[5:]
							
							time.at[a,b]=u"\u039F"
							
				
					status1="C:\\record\\statusBOX1" + str(name)
					# print(time)
					time.to_csv (str((status1 + '.csv')), index = True, header=True,encoding="utf-16", mode = 'w', sep='\t')				


						
	          ############################box2###################

					time2=pd.DataFrame()
					
					
					
					time2['Status']=statusidlist2 #created a dataframe with these three column
					time2['Keyname']=keyidlist2
					time2['Key'] = keyname_list2
					time2["Day"]=pd.Series(list1)


					time2=time2.pivot(index=["Keyname","Key"],columns='Day',values='Status')
					time2=time2.fillna("-")
					time2 = time2.iloc[: , 1:]

					df_new2=pd.DataFrame(df_copy2[["日付","状況","キー名","キーボックスNo","タグID"]])
		
					df_new2=df_new2.loc[df_new2['キーボックスNo']=='キーボックス 2']
				
					
					df_box2=pd.DataFrame(df_new2[["日付","状況","キー名","タグID"]])

					
					for j in range(0,len(dateonly)):
						fd_a2=pd.DataFrame(df_box2.loc[df_box2["日付"] == (dateonly[j])])
						
						fd_b2=fd_a2[["タグID"]]
						
						fd_b2=fd_b2.drop_duplicates()
						
					
						for i in range(0,len(fd_b2)):
							
						
							a2=str(fd_b2.iloc[i].values)
						
							
							a2=a2[2:-2]
						
							b2=dateonly[j]
							b2=b2[5:]
							
							time2.at[a2,b2]=u"\u039F"
							
				    
					
					status2="C:\\record\\statusBOX2" + str(name)
					# print(time2)
					time2.to_csv (str((status2 + '.csv')), index = True, header=True,encoding="utf-16", mode = 'w', sep='\t')

                 ######### #############box3###################

					time3=pd.DataFrame()
					
					
					time3['Status']=statusidlist3 #created a dataframe with these three column
					time3['Keyname']=keyidlist3
					time3['Key'] = keyname_list3
					time3["Day"]=pd.Series(list1)


					time3=time3.pivot(index=["Keyname","Key"],columns='Day',values='Status')
					time3=time3.fillna("-")
					time3 = time3.iloc[: , 1:]

					df_new3=pd.DataFrame(df_copy3[["日付","状況","キー名","キーボックスNo","タグID"]])
		
					df_new3=df_new3.loc[df_new3['キーボックスNo']=='キーボックス 3']
					
					df_box3=pd.DataFrame(df_new3[["日付","状況","キー名","タグID"]])	
					
					for j in range(0,len(dateonly)):
						fd_a3=pd.DataFrame(df_box3.loc[df_box3["日付"] == (dateonly[j])])
						

						fd_b3=fd_a3[["タグID"]]
						
						fd_b3=fd_b3.drop_duplicates()
						
					
						for i in range(0,len(fd_b3)):
							
							
							a3=str(fd_b3.iloc[i].values)
						
							
							a3=a3[2:-2]
						
							b3=dateonly[j]
							b3=b3[5:]
						
							time3.at[a3,b3]=u"\u039F"
							
				    
					
					status3="C:\\record\\statusBOX3" + str(name)
					# print(time3)
					time3.to_csv (str((status3 + '.csv')), index = True, header=True,encoding="utf-16", mode = 'w', sep='\t')
#########################box4#######################

					time4=pd.DataFrame()
					
					
					time4['Status']=statusidlist4 #created a dataframe with these three column
					time4['Keyname']=keyidlist4
					time4['Key'] = keyname_list4
					time4["Day"]=pd.Series(list1)


					time4=time4.pivot(index=["Keyname","Key"],columns='Day',values='Status')
					time4=time4.fillna("-")
					time4 = time4.iloc[: , 1:]

					df_new4=pd.DataFrame(df_copy4[["日付","状況","キー名","キーボックスNo","タグID"]])
		
					df_new4=df_new4.loc[df_new4['キーボックスNo']=='キーボックス 4']
					
					 
					df_box4=pd.DataFrame(df_new4[["日付","状況","キー名","タグID"]])	
					
					for j in range(0,len(dateonly)):
						fd_a4=pd.DataFrame(df_box4.loc[df_box4["日付"] == (dateonly[j])])
						

						fd_b4=fd_a4[["タグID"]]
						
						fd_b4=fd_b4.drop_duplicates()
						
					
						for i in range(0,len(fd_b4)):
							
						
							a4=str(fd_b4.iloc[i].values)
							
							
							a4=a4[2:-2]
							
							b4=dateonly[j]
							b4=b4[5:]
							
							time4.at[a4,b4]=u"\u039F"
							

					status4="C:\\record\\statusBOX4" + str(name)
					print(time4)
					time4.to_csv (str((status4 + '.csv')), index = True, header=True,encoding="utf-16", mode = 'w', sep='\t')
				

				except Exception as e:
					print(e)


				df = df.replace(r'\r\n','', regex=True) 
				df.dropna(inplace=True)

				df_length = len(df)

				string_to_add = '<button type="button" data-toggle="modal" data-target="#myModal" class="btn fixbtn" style="border: 1px solid #e9ebf5; color: white; background-color: #92d050; font-size: 20px; padding: 7px 20px; margin: 0;">修正</button>'

				for i in range(1,df_length+1):
					indexlist.append(string_to_add)
				df.insert(5, "button", indexlist, True)

			else:
				df = pd.DataFrame()
				# print("here")

		except Exception as e:
			df = pd.DataFrame()
			print(e)
			logger_4.error(e)
	

		df1 = pd.DataFrame()
		df2 = pd.DataFrame()
		df1 = df
	
		try:
	
			df2 = df1.drop(columns=["button"])
		except Exception as e:
			print(e)
	
		current_date=datetime.datetime.now()
	
		current_time=current_date.strftime("%m_%d_%H_%M_%S")
	
		filename1="C:\\record\\USERINPUTRecord" + str(current_time)
		# df2=df2.drop_duplicates()
		# print(df2)
	
		export_excel1 = df2.to_csv (str((filename1 + '.csv')), index = True, header=True,encoding="utf-16", mode = 'w', sep='\t')
	
		return df
