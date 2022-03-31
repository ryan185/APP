
import time, sys, pymongo, datetime, logging, smtplib, pandas as pd,os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta,date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from save_log import get_log
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myrecordcollection = mydb["RecordDatabase"]
mysavealertcollection = mydb["SaveAlertData"]
mykanripart2savehourcollection = mydb["KanriPart2SaveHourData"]
mykanripart2saveminutecollection = mydb["KanriPart2SaveMinuteData"]
myTempKeycollection = mydb["TemporaryKeyData"]
mycheckdaycollection = mydb["CheckUserInputDays"]
mysavedaycollection = mydb["SaveDayData"]
mysendemaildbcollection = mydb["SendEmailDatabase"]
mykeynotreturnemailcollection = mydb["KeyNotReturnEmailData"]
mystopkanripart2dbcollection = mydb["StopKanriPart2DB"]
mydb2 = myclient['mydatabase']
myrecord2collection = mydb2["Database"]

log_dir = 'C:\\Face\\log1'
os.chmod(log_dir, 0o777)
get_log.setup_logger('log6', 'C:\\Face\\log1\\KanriPart2.log')
kanri_logger = logging.getLogger('log6')
# print(kanri_logger)
kanri_logger.info("Started")


mail_content = '''Hello,
In this mail we are sending not returned key.
The mail is sent using Python SMTP library.
Thank You
'''
#The mail addresses and password
sender_address ='ercfacetemperature@gmail.com'
sender_pass = 'obayashi0884'
CC = 'erckeysystem@gmail.com'


def send_mail(receiver_address, file1, file2):
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Monthly Record of Key Taken/Return'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    files = [file1, file2]

    for a_file in files:
        attach_file_name = a_file
        attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        #add payload header with filename
        payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
        message.attach(payload)

    #Create SMTP session for sending the mail
    
    
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    rcpt = CC.split(",") + [receiver_address]
    session.sendmail(sender_address, rcpt, text)
    session.quit()

    

class kanrialertfunc():
    def getdataframe(firstdate,lastdate,keyboxno):
        df = pd.DataFrame()
        datetime_list, dateonly_list, status_list, key_name_list, dept_name_list= ([] for i in range(5))
        usr_name_list, id_list, keybox_list, rentcomp_list, rentcompid_list= ([] for i in range(5))
        for i in range(1,16):
            collname = "RecordDatabase" + str(i)
            myrecordcollection = mydb[collname]
            findRecord = myrecordcollection.find(filter = { '日付' : { '$gte' : firstdate , '$lte' : lastdate }})
            for doc_record in findRecord:
                datetimu=doc_record["時刻"]
                datetime_list.insert(0, datetimu) 
                status=doc_record["状況"]
                status_list.insert(0, status)
                key_name=doc_record["キー名"]
                key_name_list.insert(0, key_name)
                dept_name=doc_record["部署名"]
                dept_name_list.insert(0, dept_name)
                usr_name=doc_record["貸出者"]
                usr_name_list.insert(0, usr_name)
                id_=doc_record["タグID"]
                id_list.insert(0, id_)
                epcbox=doc_record["キーボックスNo"]
                keybox_list.insert(0, epcbox)
                rentcomp=doc_record["レンタル会社"]
                rentcomp_list.insert(0, rentcomp)
                rentcompid=doc_record["番号"]
                rentcompid_list.insert(0, rentcompid)

        for i in datetime_list:
            dateonly_list.append(i[0:10])

        df = pd.DataFrame({'日付' : dateonly_list, '時刻': datetime_list, '状況': status_list, 'キー名': key_name_list, '部署名': dept_name_list, '貸出者': usr_name_list, 'タグID': id_list, "キーボックスNo" : keybox_list, 'レンタル会社': rentcomp_list, '番号': rentcompid_list})
        i = keyboxno
        df = df[df['キーボックスNo'] == "キーボックス %i" %i]
        return df
        
    def getdays():
        findDays = mycheckdaycollection.find(filter = { "user_id" : 1})
        for doc_days in findDays:
            days = doc_days["daynum"]
        return days

    def getemaildata():
        
        email_data = []
        dateandtime = name = comp = keyno = boxno = rentcomp = rentcompid = ""
        
        findEmailData = mysendemaildbcollection.find(filter = { "user_id" : 1})
        for doc_emaildata in findEmailData:
            dateandtime = doc_emaildata["date&time"]
            name = doc_emaildata["name"]
            comp = doc_emaildata["comp"]
            keyno = doc_emaildata["keyno"]
            boxno = doc_emaildata["boxno"]
            rentcomp = doc_emaildata["rentcomp"]
            rentcompid = doc_emaildata["rentcompid"]
        
        email_data.append(dateandtime)
        email_data.append(name)
        email_data.append(comp)
        email_data.append(keyno)
        email_data.append(boxno)
        email_data.append(rentcomp)
        email_data.append(rentcompid)
        # df = pd.DataFrame([email_data],columns=['date&time','name','comp','keyno','boxno','rentcomp','rentcompid'])
          # 2021-04-16 15:49:32      Shun  大林組  100 不整地フォークリフト  キーボックス 1  ニッケン  5865
        # print(df)
        return email_data

    def getdatelist(N_DAYS_AGO):
        datelist = []

        today = date.today()    
        for x in range(1,int(N_DAYS_AGO)+1):
            n_days_ago = today - timedelta(days=x)
            datelist.append(str(n_days_ago))
        return datelist

    def getresult(kiname,daycount,keybox):
        thelist = []
        result = False
        thelist = kanrialertfunc.getdatelist(int(daycount)) # ['2021-04-14', '2021-04-13', '2021-04-12']
        record_df = pd.DataFrame()
        record_df = kanrialertfunc.getdataframe(thelist[-1],thelist[0],keybox)
        # print(record_df)
        if len(record_df) > 0:
            record_df = record_df[record_df['キー名'].str.contains(kiname, na=False)]
        for i in range(0,len(thelist)):
            df = pd.DataFrame()
            df = record_df[record_df['日付'] == thelist[i]]
            """
            I have a dataframe from which I remove some rows. As a result, I get a dataframe in which index is 
            something like that: [1,5,6,10,11] and I would like to reset it to [0,1,2,3,4]. How can I do it?

            The answer is : df = df.reset_index()
            """
            df = df.reset_index()
            if len(df) > 0:
                if df["状況"][0] == "貸出":
                    updateDF = pd.DataFrame()
                    updateDF = df.iloc[0,:]
                    # print(kiname)
                    # print(kiname)
                    mysendemaildbcollection.update_one({"user_id": 1},{'$set':{"date&time": updateDF["時刻"], "name": updateDF["貸出者"], "comp": updateDF["部署名"], "keyno": updateDF["キー名"], "boxno": updateDF["キーボックスNo"], "rentcomp": updateDF["レンタル会社"], "rentcompid": updateDF["番号"]}})
                    # print("貸出")
                    result = True
                if df["状況"][0] == "返却":
                    # print(kiname)
                    # print("返却")
                    result = False
                    break
        return result

    def getkeyname(num):
        for n in range(1,11):
            if num == n:
                num = "00" + num
        for n in range(11,100):
            if num == n:
                num = "0" + num
        num = str(num) 
        return num

    
        
    def decide(boxnum, to_addr):
        findTempKey = myTempKeycollection.find(filter = { "user_id" : boxnum})

        columns=['date&time','name','comp','keyno','boxno','rentcomp','rentcompid']
        df1 = pd.DataFrame([],columns=columns)
        df2 = pd.DataFrame([],columns=columns)
        # print(boxnum)
        for doc_tempkey in findTempKey:
            for i in range(1,101):
                keyvalue = doc_tempkey["Tag%i" %i]
                if keyvalue == 0:
                    keyname = kanrialertfunc.getkeyname(str(i)) #"024"
                    days = kanrialertfunc.getdays() #"3"
                    sendMail = kanrialertfunc.getresult(keyname,days,boxnum)
                    if sendMail:
                    
                        emaildata = kanrialertfunc.getemaildata()
                        email = pd.DataFrame([emaildata],columns=columns)
                        df1 = df1.append(email,ignore_index=True)
                         
                       
                    else:
                        kanri_logger.info("キーボックス番号: " + str(boxnum))
                        kanri_logger.info(kanrialertfunc.getkeyname(str(i)))
                        kanri_logger.info("返却")
                      
                        continue
                else:
                    continue
        #
        return df1
        # print(df2)
    def job1():
        for i in range(1,5):
            findEmailAddress = mykeynotreturnemailcollection.find()
            for doc_emailaddress in findEmailAddress:
                receiver_address = doc_emailaddress["email%i" %i]
                if receiver_address != "":
                    databox1=pd.DataFrame() 
                    databox1=kanrialertfunc.decide(1, receiver_address)
                    export_csv1 = databox1.to_csv (r'C:\\record\\KEYNOTRETURNEDBOX_1_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d'))), index = False, header=True,encoding="utf-16", mode = 'w', sep='\t')
                    # smtplib.SMTP_SSL() itime.sleep(10)
                    csv_name1 = 'C:\\record\\KEYNOTRETURNEDBOX_1_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d')))
                    
        # print(csv_name1)
        return csv_name1
    
    def job2():
        for i in range(1,5):
            findEmailAddress = mykeynotreturnemailcollection.find()
            for doc_emailaddress in findEmailAddress:
                receiver_address = doc_emailaddress["email%i" %i]
                if receiver_address != "":
                    databox2=pd.DataFrame() 
                    databox2=kanrialertfunc.decide(2, receiver_address)
                    export_csv2 = databox2.to_csv (r'C:\\record\\KEYNOTRETURNEDBOX_2_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d'))), index = False, header=True,encoding="utf-16", mode = 'w', sep='\t')
                    # time.sleep(10)
                    csv_name2 = 'C:\\record\\KEYNOTRETURNEDBOX_2_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d')))

        # print(csv_name2)
        return csv_name2
    
class kanri_part2_run():
    def part2():
        decision_variable = time_variable = True
        var1 = var2 = var3  = True
        while True:
            try:
             
                findhour = mykanripart2savehourcollection.find()
                findminute = mykanripart2saveminutecollection.find()

             
                for doc_hour in findhour:
                    dhour=doc_hour["hour"]

                for doc_minute in findminute:
                    dminute=doc_minute["minute"]
                
               

                if len(str(dhour)) == 1:
                    dhour = str(0) + str(dhour)

                if len(str(dminute)) == 1:
                    dminute = str(0) + str(dminute)

                if dminute == "":
                    dminute = "00"

                time_string1 = dhour + ":" + dminute 
                dateSTR1 = datetime.now().strftime("%H:%M" )
                
                if str(dateSTR1) == time_string1:
                    start_time = time.time()
                    if time_variable:
                        time_variable = False
                        end_time = start_time + 35


                    if var1 == True:
                        csv_file1 = kanrialertfunc.job1()
                        var1 = False
                    if var2 == True:
                        csv_file2 = kanrialertfunc.job2()
                        var2 = False
                    # if var3 == True:
                    #     csv_file3 = kanrialertfunc.job3()
                    #     var3 = False
                    
                    # if var3 == True:
                    #     # csv_file3 = kanrisavemonthly.job3()
                    #     var3 = False

                    # if start_time < end_time:
                    for i in range(1,5):
                        findEmailAddress = mykeynotreturnemailcollection.find()
                        for doc_emailaddress in findEmailAddress:
                            receiver_address = doc_emailaddress["email%i" %i]
                            if receiver_address != "":
                                send_mail(receiver_address, csv_file1, csv_file2)
                                # print("email send")
                                kanri_logger.info("email send")
                    time.sleep(70)            
                if str(dateSTR1) != time_string1:
                    var1 = var2 = time_variable = True
            except Exception as e:
                print(e)
                  #kanri_logger.info("Done")
                kanri_logger.error(e)

#kanri_part2_run.part2()