import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

mytempepccountcollection = mydb["TempEPCCountData"]

list1=[]
list2=[]

df1 = pd.DataFrame(data = {"user_id": 1,"epccount1": 0, "epccount2": 0, "epccount3": 0, "epccount4": 0, "epccount5": 0, "epccount6": 0, "epccount7": 0, "epccount8": 0, "epccount9": 0, "epccount10": 0,
                                        "epccount11": 0, "epccount12": 0, "epccount13": 0, "epccount14": 0, "epccount15": 0, "epccount16": 0, "epccount17": 0, "epccount18": 0, "epccount19": 0, "epccount20": 0,
                                        "epccount21": 0, "epccount22": 0, "epccount23": 0, "epccount24": 0, "epccount25": 0, "epccount26": 0, "epccount27": 0, "epccount28": 0, "epccount29": 0, "epccount30": 0,
                                        "epccount31": 0, "epccount32": 0, "epccount33": 0, "epccount34": 0, "epccount35": 0, "epccount36": 0, "epccount37": 0, "epccount38": 0, "epccount39": 0, "epccount40": 0,
                                        "epccount41": 0, "epccount42": 0, "epccount43": 0, "epccount44": 0, "epccount45": 0, "epccount46": 0, "epccount47": 0, "epccount48": 0, "epccount49": 0, "epccount50": 0,
                                        "epccount51": 0, "epccount52": 0, "epccount53": 0, "epccount54": 0, "epccount55": 0, "epccount56": 0, "epccount57": 0, "epccount58": 0, "epccount59": 0, "epccount60": 0,
                                        "epccount61": 0, "epccount62": 0, "epccount63": 0, "epccount64": 0, "epccount65": 0, "epccount66": 0, "epccount67": 0, "epccount68": 0, "epccount69": 0, "epccount70": 0,
                                        "epccount71": 0, "epccount72": 0, "epccount73": 0, "epccount74": 0, "epccount75": 0, "epccount76": 0, "epccount77": 0, "epccount78": 0, "epccount79": 0, "epccount80": 0,
                                        "epccount81": 0, "epccount82": 0, "epccount83": 0, "epccount84": 0, "epccount85": 0, "epccount86": 0, "epccount87": 0, "epccount88": 0, "epccount89": 0, "epccount90": 0,
                                        "epccount91": 0, "epccount92": 0, "epccount93": 0, "epccount94": 0, "epccount95": 0, "epccount96": 0, "epccount97": 0, "epccount98": 0, "epccount99": 0, "epccount100": 0}, index=[0])

df2 = pd.DataFrame(data = {"user_id": 2,"epccount1": 0, "epccount2": 0, "epccount3": 0, "epccount4": 0, "epccount5": 0, "epccount6": 0, "epccount7": 0, "epccount8": 0, "epccount9": 0, "epccount10": 0,
                                        "epccount11": 0, "epccount12": 0, "epccount13": 0, "epccount14": 0, "epccount15": 0, "epccount16": 0, "epccount17": 0, "epccount18": 0, "epccount19": 0, "epccount20": 0,
                                        "epccount21": 0, "epccount22": 0, "epccount23": 0, "epccount24": 0, "epccount25": 0, "epccount26": 0, "epccount27": 0, "epccount28": 0, "epccount29": 0, "epccount30": 0,
                                        "epccount31": 0, "epccount32": 0, "epccount33": 0, "epccount34": 0, "epccount35": 0, "epccount36": 0, "epccount37": 0, "epccount38": 0, "epccount39": 0, "epccount40": 0,
                                        "epccount41": 0, "epccount42": 0, "epccount43": 0, "epccount44": 0, "epccount45": 0, "epccount46": 0, "epccount47": 0, "epccount48": 0, "epccount49": 0, "epccount50": 0,
                                        "epccount51": 0, "epccount52": 0, "epccount53": 0, "epccount54": 0, "epccount55": 0, "epccount56": 0, "epccount57": 0, "epccount58": 0, "epccount59": 0, "epccount60": 0,
                                        "epccount61": 0, "epccount62": 0, "epccount63": 0, "epccount64": 0, "epccount65": 0, "epccount66": 0, "epccount67": 0, "epccount68": 0, "epccount69": 0, "epccount70": 0,
                                        "epccount71": 0, "epccount72": 0, "epccount73": 0, "epccount74": 0, "epccount75": 0, "epccount76": 0, "epccount77": 0, "epccount78": 0, "epccount79": 0, "epccount80": 0,
                                        "epccount81": 0, "epccount82": 0, "epccount83": 0, "epccount84": 0, "epccount85": 0, "epccount86": 0, "epccount87": 0, "epccount88": 0, "epccount89": 0, "epccount90": 0,
                                        "epccount91": 0, "epccount92": 0, "epccount93": 0, "epccount94": 0, "epccount95": 0, "epccount96": 0, "epccount97": 0, "epccount98": 0, "epccount99": 0, "epccount100": 0}, index=[0])

df3 = pd.DataFrame(data = {"user_id": 3,"epccount1": 0, "epccount2": 0, "epccount3": 0, "epccount4": 0, "epccount5": 0, "epccount6": 0, "epccount7": 0, "epccount8": 0, "epccount9": 0, "epccount10": 0,
                                        "epccount11": 0, "epccount12": 0, "epccount13": 0, "epccount14": 0, "epccount15": 0, "epccount16": 0, "epccount17": 0, "epccount18": 0, "epccount19": 0, "epccount20": 0,
                                        "epccount21": 0, "epccount22": 0, "epccount23": 0, "epccount24": 0, "epccount25": 0, "epccount26": 0, "epccount27": 0, "epccount28": 0, "epccount29": 0, "epccount30": 0,
                                        "epccount31": 0, "epccount32": 0, "epccount33": 0, "epccount34": 0, "epccount35": 0, "epccount36": 0, "epccount37": 0, "epccount38": 0, "epccount39": 0, "epccount40": 0,
                                        "epccount41": 0, "epccount42": 0, "epccount43": 0, "epccount44": 0, "epccount45": 0, "epccount46": 0, "epccount47": 0, "epccount48": 0, "epccount49": 0, "epccount50": 0,
                                        "epccount51": 0, "epccount52": 0, "epccount53": 0, "epccount54": 0, "epccount55": 0, "epccount56": 0, "epccount57": 0, "epccount58": 0, "epccount59": 0, "epccount60": 0,
                                        "epccount61": 0, "epccount62": 0, "epccount63": 0, "epccount64": 0, "epccount65": 0, "epccount66": 0, "epccount67": 0, "epccount68": 0, "epccount69": 0, "epccount70": 0,
                                        "epccount71": 0, "epccount72": 0, "epccount73": 0, "epccount74": 0, "epccount75": 0, "epccount76": 0, "epccount77": 0, "epccount78": 0, "epccount79": 0, "epccount80": 0,
                                        "epccount81": 0, "epccount82": 0, "epccount83": 0, "epccount84": 0, "epccount85": 0, "epccount86": 0, "epccount87": 0, "epccount88": 0, "epccount89": 0, "epccount90": 0,
                                        "epccount91": 0, "epccount92": 0, "epccount93": 0, "epccount94": 0, "epccount95": 0, "epccount96": 0, "epccount97": 0, "epccount98": 0, "epccount99": 0, "epccount100": 0}, index=[0])

df4 = pd.DataFrame(data = {"user_id": 4,"epccount1": 0, "epccount2": 0, "epccount3": 0, "epccount4": 0, "epccount5": 0, "epccount6": 0, "epccount7": 0, "epccount8": 0, "epccount9": 0, "epccount10": 0,
                                        "epccount11": 0, "epccount12": 0, "epccount13": 0, "epccount14": 0, "epccount15": 0, "epccount16": 0, "epccount17": 0, "epccount18": 0, "epccount19": 0, "epccount20": 0,
                                        "epccount21": 0, "epccount22": 0, "epccount23": 0, "epccount24": 0, "epccount25": 0, "epccount26": 0, "epccount27": 0, "epccount28": 0, "epccount29": 0, "epccount30": 0,
                                        "epccount31": 0, "epccount32": 0, "epccount33": 0, "epccount34": 0, "epccount35": 0, "epccount36": 0, "epccount37": 0, "epccount38": 0, "epccount39": 0, "epccount40": 0,
                                        "epccount41": 0, "epccount42": 0, "epccount43": 0, "epccount44": 0, "epccount45": 0, "epccount46": 0, "epccount47": 0, "epccount48": 0, "epccount49": 0, "epccount50": 0,
                                        "epccount51": 0, "epccount52": 0, "epccount53": 0, "epccount54": 0, "epccount55": 0, "epccount56": 0, "epccount57": 0, "epccount58": 0, "epccount59": 0, "epccount60": 0,
                                        "epccount61": 0, "epccount62": 0, "epccount63": 0, "epccount64": 0, "epccount65": 0, "epccount66": 0, "epccount67": 0, "epccount68": 0, "epccount69": 0, "epccount70": 0,
                                        "epccount71": 0, "epccount72": 0, "epccount73": 0, "epccount74": 0, "epccount75": 0, "epccount76": 0, "epccount77": 0, "epccount78": 0, "epccount79": 0, "epccount80": 0,
                                        "epccount81": 0, "epccount82": 0, "epccount83": 0, "epccount84": 0, "epccount85": 0, "epccount86": 0, "epccount87": 0, "epccount88": 0, "epccount89": 0, "epccount90": 0,
                                        "epccount91": 0, "epccount92": 0, "epccount93": 0, "epccount94": 0, "epccount95": 0, "epccount96": 0, "epccount97": 0, "epccount98": 0, "epccount99": 0, "epccount100": 0}, index=[0])



# mytempepccountcollection.insert_many(df1.to_dict('records'))
# mytempepccountcollection.insert_many(df2.to_dict('records'))
# mytempepccountcollection.insert_many(df3.to_dict('records'))
mytempepccountcollection.insert_many(df4.to_dict('records'))