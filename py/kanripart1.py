import time, sys, pymongo, datetime, logging, smtplib, pandas as pd,os
from datetime import datetime, timedelta,date
from logging.handlers import TimedRotatingFileHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from save_log import get_log
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myrecordcollection = mydb["RecordDatabase"]
mysavedaycollection = mydb["SaveDayData"]
mysavehourcollection = mydb["SaveHourData"]
mysaveminutecollection = mydb["SaveMinuteData"]
mysavealertcollection = mydb["SaveAlertData"]
mymonthlysaveemailcollection = mydb["MonthlySaveEmailData"]
# myTempKeycollection = mydb["TemporaryKeyData"]
# mycheckdaycollection = mydb["CheckUserInputDays"]
# mysendemaildbcollection = mydb["SendEmailDatabase"]
# mystopkanripart2dbcollection = mydb["StopKanriPart2DB"]

log_dir = 'C:\\Face\\log1'
os.chmod(log_dir, 0o777)
get_log.setup_logger('log5', 'C:\\Face\\log1\\KanriPart1.log')
kanri1_logger = logging.getLogger('log5')
# print(kanri1_logger)
kanri1_logger.info("Started")

mail_content = '''Hello,
In this mail we are sending the record csv files of previous month.
The mail is sent using Python SMTP library.
Thank You
'''
#The mail addresses and password
sender_address = 'ercfacetemperature@gmail.com'
sender_pass = 'obayashi0884'
CC = 'erckeysystem@gmail.com'

def send_mail(receiver_address, file1, file2, file3):
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Monthly Record of Key Taken/Return'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    files = [file1, file2, file3]

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

class kanrisavemonthly(object):
    def FindDf():
        df = pd.DataFrame()
        datetime_list, dateonly_list, status_list, key_name_list, dept_name_list= ([] for i in range(5))
        usr_name_list, id_list, keybox_list, rentcomp_list, rentcompid_list= ([] for i in range(5))
        for i in range(1,16):
            
            collname = "RecordDatabase" + str(i)
            myrecordcollection = mydb[collname]
            
            findRecord = myrecordcollection.find()
            
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
        df = pd.DataFrame({'時刻': datetime_list, '状況': status_list, 'キー名': key_name_list, '部署名': dept_name_list, '貸出者': usr_name_list, 'タグID': id_list, "キーボックスNo" : keybox_list, 'レンタル会社': rentcomp_list, '番号': rentcompid_list})
        return df

    def job1():
        record_df = pd.DataFrame()
        record_df = kanrisavemonthly.FindDf()
        record_df = record_df[record_df['キーボックスNo'] == "キーボックス 1"]
        export_csv = record_df.to_csv (r'C:\\record\\RecordCSVBOX_1_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d'))), index = False, header=True,encoding="utf-16", mode = 'w', sep='\t')
        csv_name = 'C:\\record\\RecordCSVBOX_1_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d')))
        return csv_name
    
    def job2():
        record_df = pd.DataFrame()
        record_df = kanrisavemonthly.FindDf()
        record_df = record_df[record_df['キーボックスNo'] == "キーボックス 2"]
        record_df.index = record_df.index + 1
        export_excel = record_df.to_csv (r'C:\\record\\RecordCSVBOX_2_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d'))), index = False, header=True,encoding="utf-16", mode = 'w', sep='\t')
        csv_name = 'C:\\record\\RecordCSVBOX_2_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d')))
        return csv_name

    def job3():
        record_df = pd.DataFrame()
        record_df = kanrisavemonthly.FindDf()
        record_df = record_df[record_df['キーボックスNo'] == "キーボックス 3"]
        record_df.index = record_df.index + 1
        export_excel = record_df.to_csv (r'C:\\record\\RecordCSVBOX_3_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d'))), index = False, header=True,encoding="utf-16", mode = 'w', sep='\t')
        csv_name = 'C:\\record\\RecordCSVBOX_3_{}.csv'.format(str(datetime.strftime(datetime.now(), '%Y-%m-%d')))
        return csv_name

class kanri_part1_sendEmailMonthly():
    def part1():
        var1 = var2 = var3 = time_variable = True
        while True:
            try:
                findday = mysavedaycollection.find()
                findhour = mysavehourcollection.find()
                findminute = mysaveminutecollection.find()

                for doc_day in findday:
                    dday=doc_day["day"]

                for doc_hour in findhour:
                    dhour=doc_hour["hour"]

                for doc_minute in findminute:
                    dminute=doc_minute["minute"]

                if len(str(dday)) == 1:
                    dday = str(0) + str(dday)

                if len(str(dhour)) == 1:
                    dhour = str(0) + str(dhour)

                if len(str(dminute)) == 1:
                    dminute = str(0) + str(dminute)

                if dminute == "":
                    dminute = "00"

                time_string1 = str(dday) + ":" + dhour + ":" + dminute 
                dateSTR1 = datetime.now().strftime("%d:%H:%M" )

                if str(dateSTR1) == time_string1:
                    start_time = time.time()
                    if time_variable:
                        time_variable = False
                        end_time = start_time + 35

                    if var1 == True:
                        csv_file1 = kanrisavemonthly.job1()
                        var1 = False
                    if var2 == True:
                        csv_file2 = kanrisavemonthly.job2()
                        var2 = False
                    if var3 == True:
                        csv_file3 = kanrisavemonthly.job3()
                        var3 = False
                    
                    # if start_time < end_time:
                    for i in range(1,5):
                        findEmailAddress = mymonthlysaveemailcollection.find()
                        for doc_emailaddress in findEmailAddress:
                            receiver_address = doc_emailaddress["email%i" %i]
                            if receiver_address != "":
                                send_mail(receiver_address, csv_file1, csv_file2, csv_file3)
                                kanri1_logger.info("Mail send")
                                # print("mailsend")
                    time.sleep(70)
                
                if str(dateSTR1) != time_string1:
                    var1 = var2 = var3 = time_variable = True

            except Exception as e:
                kanri1_logger.error(e)

# kanri_part1_sendEmailMonthly.part1()