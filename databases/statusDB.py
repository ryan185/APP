import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

myStatuscollection = mydb["KeyStatus"]

df1 = pd.DataFrame(data = {"user_id": 1,"Status1": "   -   ", "Status2":"-" , "Status3": "-", "Status4": "-", "Status5": "-", "Status6": "-", "Status7": "-", "Status8": "-", "Status9": "-", "Status10": "-",
                                        "Status11": "-", "Status12": "-", "Status13":"-", "Status14": "-", "Status15": "-", "Status16": "-", "Status17": "-", "Status18":"-", "Status19": "-", "Status20": "-",
                                        "Status21": "-", "Status22": "-", "Status23":"-", "Status24": "-", "Status25": "-", "Status26": "-", "Status27": "-", "Status28":"-", "Status29": "-", "Status30": "-",
                                        "Status31": "-", "Status32": "-", "Status33":"-", "Status34": "-", "Status35": "-", "Status36": "-", "Status37": "-", "Status38":"-", "Status39": "-", "Status40": "-",
                                        "Status41": "-", "Status42": "-", "Status43":"-", "Status44": "-", "Status45": "-", "Status46": "-", "Status47": "-", "Status48":"-", "Status49": "-", "Status50": "-",
                                        "Status51": "-", "Status52": "-", "Status53":"-", "Status54": "-", "Status55": "-", "Status56": "-", "Status57": "-", "Status58":"-", "Status59": "-", "Status60": "-",
                                        "Status61": "-", "Status62": "-", "Status63":"-", "Status64": "-", "Status65": "-", "Status66": "-", "Status67": "-", "Status68":"-",  "Status69": "-", "Status70": "-",
                                        "Status71": "-", "Status72": "-", "Status73":"-", "Status74": "-", "Status75": "-", "Status76": "-", "Status77": "-", "Status78":"-", "Status79": "-", "Status80": "-",
                                        "Status81": "-", "Status82": "-", "Status83":"-", "Status84": "-", "Status85": "-", "Status86": "-", "Status87": "-", "Status88":"-", "Status89": "-", "Status90": "-",
                                        "Status91": "-", "Status92": "-", "Status93":"-", "Status94": "-", "Status95": "-", "Status96": "-", "Status97": "-", "Status98":"-", "Status99": "-", "Status100":"-"}, index=[0])

df2 = pd.DataFrame(data = {"user_id": 2,"Status1": "-", "Status2": "-", "Status3": "-", "Status4": "-", "Status5": "-", "Status6": "-", "Status7": "-", "Status8": "-", "Status9": "-", "Status10": "-",
                                        "Status11": "-", "Status12": "-", "Status13":"-", "Status14": "-", "Status15": "-", "Status16": "-", "Status17": "-", "Status18":"-", "Status19": "-", "Status20": "-",
                                        "Status21": "-", "Status22": "-", "Status23":"-", "Status24": "-", "Status25": "-", "Status26": "-", "Status27": "-", "Status28":"-", "Status29": "-", "Status30": "-",
                                        "Status31": "-", "Status32": "-", "Status33":"-", "Status34": "-", "Status35": "-", "Status36": "-", "Status37": "-", "Status38":"-", "Status39": "-", "Status40": "-",
                                        "Status41": "-", "Status42": "-", "Status43":"-", "Status44": "-", "Status45": "-", "Status46": "-", "Status47": "-", "Status48":"-", "Status49": "-", "Status50": "-",
                                        "Status51": "-", "Status52": "-", "Status53":"-", "Status54": "-", "Status55": "-", "Status56": "-", "Status57": "-", "Status58":"-", "Status59": "-", "Status60": "-",
                                        "Status61": "-", "Status62": "-", "Status63":"-", "Status64": "-", "Status65": "-", "Status66": "-", "Status67": "-", "Status68":"-",  "Status69": "-", "Status70": "-",
                                        "Status71": "-", "Status72": "-", "Status73":"-", "Status74": "-", "Status75": "-", "Status76": "-", "Status77": "-", "Status78":"-", "Status79": "-", "Status80": "-",
                                        "Status81": "-", "Status82": "-", "Status83":"-", "Status84": "-", "Status85": "-", "Status86": "-", "Status87": "-", "Status88":"-", "Status89": "-", "Status90": "-",
                                        "Status91": "-", "Status92": "-", "Status93":"-", "Status94": "-", "Status95": "-", "Status96": "-", "Status97": "-", "Status98":"-", "Status99": "-", "Status100":"-"}, index=[0])

df3 = pd.DataFrame(data = {"user_id": 3,"Status1": "-", "Status2":"-", "Status3": "-", "Status4": "-", "Status5": "-", "Status6": "-", "Status7": "-", "Status8": "-", "Status9": "-", "Status10": "-",
                                        "Status11": "-", "Status12": "-", "Status13":"-", "Status14": "-", "Status15": "-", "Status16": "-", "Status17": "-", "Status18":"-", "Status19": "-", "Status20": "-",
                                        "Status21": "-", "Status22": "-", "Status23":"-", "Status24": "-", "Status25": "-", "Status26": "-", "Status27": "-", "Status28":"-", "Status29": "-", "Status30": "-",
                                        "Status31": "-", "Status32": "-", "Status33":"-", "Status34": "-", "Status35": "-", "Status36": "-", "Status37": "-", "Status38":"-", "Status39": "-", "Status40": "-",
                                        "Status41": "-", "Status42": "-", "Status43":"-", "Status44": "-", "Status45": "-", "Status46": "-", "Status47": "-", "Status48":"-", "Status49": "-", "Status50": "-",
                                        "Status51": "-", "Status52": "-", "Status53":"-", "Status54": "-", "Status55": "-", "Status56": "-", "Status57": "-", "Status58":"-", "Status59": "-", "Status60": "-",
                                        "Status61": "-", "Status62": "-", "Status63":"-", "Status64": "-", "Status65": "-", "Status66": "-", "Status67": "-", "Status68":"-",  "Status69": "-", "Status70": "-",
                                        "Status71": "-", "Status72": "-", "Status73":"-", "Status74": "-", "Status75": "-", "Status76": "-", "Status77": "-", "Status78":"-", "Status79": "-", "Status80": "-",
                                        "Status81": "-", "Status82": "-", "Status83":"-", "Status84": "-", "Status85": "-", "Status86": "-", "Status87": "-", "Status88":"-", "Status89": "-", "Status90": "-",
                                        "Status91": "-", "Status92": "-", "Status93":"-", "Status94": "-", "Status95": "-", "Status96": "-", "Status97": "-", "Status98":"-", "Status99": "-", "Status100":"-"}, index=[0])

df4 = pd.DataFrame(data = {"user_id": 4,"Status1": "-", "Status2": "-", "Status3": "-", "Status4": "-", "Status5": "-", "Status6": "-", "Status7": "-", "Status8": "-", "Status9": "-", "Status10": "-",
                                        "Status11": "-", "Status12": "-", "Status13":"-", "Status14": "-", "Status15": "-", "Status16": "-", "Status17": "-", "Status18":"-", "Status19": "-", "Status20": "-",
                                        "Status21": "-", "Status22": "-", "Status23":"-", "Status24": "-", "Status25": "-", "Status26": "-", "Status27": "-", "Status28":"-", "Status29": "-", "Status30": "-",
                                        "Status31": "-", "Status32": "-", "Status33":"-", "Status34": "-", "Status35": "-", "Status36": "-", "Status37": "-", "Status38":"-", "Status39": "-", "Status40": "-",
                                        "Status41": "-", "Status42": "-", "Status43":"-", "Status44": "-", "Status45": "-", "Status46": "-", "Status47": "-", "Status48":"-", "Status49": "-", "Status50": "-",
                                        "Status51": "-", "Status52": "-", "Status53":"-", "Status54": "-", "Status55": "-", "Status56": "-", "Status57": "-", "Status58":"-", "Status59": "-", "Status60": "-",
                                        "Status61": "-", "Status62": "-", "Status63":"-", "Status64": "-", "Status65": "-", "Status66": "-", "Status67": "-", "Status68":"-",  "Status69": "-", "Status70": "-",
                                        "Status71": "-", "Status72": "-", "Status73":"-", "Status74": "-", "Status75": "-", "Status76": "-", "Status77": "-", "Status78":"-", "Status79": "-", "Status80": "-",
                                        "Status81": "-", "Status82": "-", "Status83":"-", "Status84": "-", "Status85": "-", "Status86": "-", "Status87": "-", "Status88":"-", "Status89": "-", "Status90": "-",
                                        "Status91": "-", "Status92": "-", "Status93":"-", "Status94": "-", "Status95": "-", "Status96": "-", "Status97": "-", "Status98":"-", "Status99": "-", "Status100":"-"}, index=[0])






myStatuscollection.insert_many(df1.to_dict('records'))
myStatuscollection.insert_many(df2.to_dict('records'))
myStatuscollection.insert_many(df3.to_dict('records'))
myStatuscollection.insert_many(df4.to_dict('records'))

