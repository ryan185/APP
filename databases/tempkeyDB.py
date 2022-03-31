import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

myTempKeycollection = mydb["TemporaryKeyData"]

list1=[]
list2=[]

df1 = pd.DataFrame(data = {"user_id": 1,"Tag1": 1, "Tag2": 1, "Tag3": 1, "Tag4": 1, "Tag5": 1, "Tag6": 1, "Tag7": 1, "Tag8": 1, "Tag9": 1, "Tag10": 1,
                                        "Tag11": 1, "Tag12": 1, "Tag13": 1, "Tag14": 1, "Tag15": 1, "Tag16": 1, "Tag17": 1, "Tag18": 1, "Tag19": 1, "Tag20": 1,
                                        "Tag21": 1, "Tag22": 1, "Tag23": 1, "Tag24": 1, "Tag25": 1, "Tag26": 1, "Tag27": 1, "Tag28": 1, "Tag29": 1, "Tag30": 1,
                                        "Tag31": 1, "Tag32": 1, "Tag33": 1, "Tag34": 1, "Tag35": 1, "Tag36": 1, "Tag37": 1, "Tag38": 1, "Tag39": 1, "Tag40": 1,
                                        "Tag41": 1, "Tag42": 1, "Tag43": 1, "Tag44": 1, "Tag45": 1, "Tag46": 1, "Tag47": 1, "Tag48": 1, "Tag49": 1, "Tag50": 1,
                                        "Tag51": 1, "Tag52": 1, "Tag53": 1, "Tag54": 1, "Tag55": 1, "Tag56": 1, "Tag57": 1, "Tag58": 1, "Tag59": 1, "Tag60": 1,
                                        "Tag61": 1, "Tag62": 1, "Tag63": 1, "Tag64": 1, "Tag65": 1, "Tag66": 1, "Tag67": 1, "Tag68": 1, "Tag69": 1, "Tag70": 1,
                                        "Tag71": 1, "Tag72": 1, "Tag73": 1, "Tag74": 1, "Tag75": 1, "Tag76": 1, "Tag77": 1, "Tag78": 1, "Tag79": 1, "Tag80": 1,
                                        "Tag81": 1, "Tag82": 1, "Tag83": 1, "Tag84": 1, "Tag85": 1, "Tag86": 1, "Tag87": 1, "Tag88": 1, "Tag89": 1, "Tag90": 1,
                                        "Tag91": 1, "Tag92": 1, "Tag93": 1, "Tag94": 1, "Tag95": 1, "Tag96": 1, "Tag97": 1, "Tag98": 1, "Tag99": 1, "Tag100": 1}, index=[0])

df2 = pd.DataFrame(data = {"user_id": 2,"Tag1": 1, "Tag2": 1, "Tag3": 1, "Tag4": 1, "Tag5": 1, "Tag6": 1, "Tag7": 1, "Tag8": 1, "Tag9": 1, "Tag10": 1,
                                        "Tag11": 1, "Tag12": 1, "Tag13": 1, "Tag14": 1, "Tag15": 1, "Tag16": 1, "Tag17": 1, "Tag18": 1, "Tag19": 1, "Tag20": 1,
                                        "Tag21": 1, "Tag22": 1, "Tag23": 1, "Tag24": 1, "Tag25": 1, "Tag26": 1, "Tag27": 1, "Tag28": 1, "Tag29": 1, "Tag30": 1,
                                        "Tag31": 1, "Tag32": 1, "Tag33": 1, "Tag34": 1, "Tag35": 1, "Tag36": 1, "Tag37": 1, "Tag38": 1, "Tag39": 1, "Tag40": 1,
                                        "Tag41": 1, "Tag42": 1, "Tag43": 1, "Tag44": 1, "Tag45": 1, "Tag46": 1, "Tag47": 1, "Tag48": 1, "Tag49": 1, "Tag50": 1,
                                        "Tag51": 1, "Tag52": 1, "Tag53": 1, "Tag54": 1, "Tag55": 1, "Tag56": 1, "Tag57": 1, "Tag58": 1, "Tag59": 1, "Tag60": 1,
                                        "Tag61": 1, "Tag62": 1, "Tag63": 1, "Tag64": 1, "Tag65": 1, "Tag66": 1, "Tag67": 1, "Tag68": 1, "Tag69": 1, "Tag70": 1,
                                        "Tag71": 1, "Tag72": 1, "Tag73": 1, "Tag74": 1, "Tag75": 1, "Tag76": 1, "Tag77": 1, "Tag78": 1, "Tag79": 1, "Tag80": 1,
                                        "Tag81": 1, "Tag82": 1, "Tag83": 1, "Tag84": 1, "Tag85": 1, "Tag86": 1, "Tag87": 1, "Tag88": 1, "Tag89": 1, "Tag90": 1,
                                        "Tag91": 1, "Tag92": 1, "Tag93": 1, "Tag94": 1, "Tag95": 1, "Tag96": 1, "Tag97": 1, "Tag98": 1, "Tag99": 1, "Tag100": 1}, index=[0])

df3 = pd.DataFrame(data = {"user_id": 3,"Tag1": 1, "Tag2": 1, "Tag3": 1, "Tag4": 1, "Tag5": 1, "Tag6": 1, "Tag7": 1, "Tag8": 1, "Tag9": 1, "Tag10": 1,
                                        "Tag11": 1, "Tag12": 1, "Tag13": 1, "Tag14": 1, "Tag15": 1, "Tag16": 1, "Tag17": 1, "Tag18": 1, "Tag19": 1, "Tag20": 1,
                                        "Tag21": 1, "Tag22": 1, "Tag23": 1, "Tag24": 1, "Tag25": 1, "Tag26": 1, "Tag27": 1, "Tag28": 1, "Tag29": 1, "Tag30": 1,
                                        "Tag31": 1, "Tag32": 1, "Tag33": 1, "Tag34": 1, "Tag35": 1, "Tag36": 1, "Tag37": 1, "Tag38": 1, "Tag39": 1, "Tag40": 1,
                                        "Tag41": 1, "Tag42": 1, "Tag43": 1, "Tag44": 1, "Tag45": 1, "Tag46": 1, "Tag47": 1, "Tag48": 1, "Tag49": 1, "Tag50": 1,
                                        "Tag51": 1, "Tag52": 1, "Tag53": 1, "Tag54": 1, "Tag55": 1, "Tag56": 1, "Tag57": 1, "Tag58": 1, "Tag59": 1, "Tag60": 1,
                                        "Tag61": 1, "Tag62": 1, "Tag63": 1, "Tag64": 1, "Tag65": 1, "Tag66": 1, "Tag67": 1, "Tag68": 1, "Tag69": 1, "Tag70": 1,
                                        "Tag71": 1, "Tag72": 1, "Tag73": 1, "Tag74": 1, "Tag75": 1, "Tag76": 1, "Tag77": 1, "Tag78": 1, "Tag79": 1, "Tag80": 1,
                                        "Tag81": 1, "Tag82": 1, "Tag83": 1, "Tag84": 1, "Tag85": 1, "Tag86": 1, "Tag87": 1, "Tag88": 1, "Tag89": 1, "Tag90": 1,
                                        "Tag91": 1, "Tag92": 1, "Tag93": 1, "Tag94": 1, "Tag95": 1, "Tag96": 1, "Tag97": 1, "Tag98": 1, "Tag99": 1, "Tag100": 1}, index=[0])

df4 = pd.DataFrame(data = {"user_id": 4,"Tag1": 1, "Tag2": 1, "Tag3": 1, "Tag4": 1, "Tag5": 1, "Tag6": 1, "Tag7": 1, "Tag8": 1, "Tag9": 1, "Tag10": 1,
                                        "Tag11": 1, "Tag12": 1, "Tag13": 1, "Tag14": 1, "Tag15": 1, "Tag16": 1, "Tag17": 1, "Tag18": 1, "Tag19": 1, "Tag20": 1,
                                        "Tag21": 1, "Tag22": 1, "Tag23": 1, "Tag24": 1, "Tag25": 1, "Tag26": 1, "Tag27": 1, "Tag28": 1, "Tag29": 1, "Tag30": 1,
                                        "Tag31": 1, "Tag32": 1, "Tag33": 1, "Tag34": 1, "Tag35": 1, "Tag36": 1, "Tag37": 1, "Tag38": 1, "Tag39": 1, "Tag40": 1,
                                        "Tag41": 1, "Tag42": 1, "Tag43": 1, "Tag44": 1, "Tag45": 1, "Tag46": 1, "Tag47": 1, "Tag48": 1, "Tag49": 1, "Tag50": 1,
                                        "Tag51": 1, "Tag52": 1, "Tag53": 1, "Tag54": 1, "Tag55": 1, "Tag56": 1, "Tag57": 1, "Tag58": 1, "Tag59": 1, "Tag60": 1,
                                        "Tag61": 1, "Tag62": 1, "Tag63": 1, "Tag64": 1, "Tag65": 1, "Tag66": 1, "Tag67": 1, "Tag68": 1, "Tag69": 1, "Tag70": 1,
                                        "Tag71": 1, "Tag72": 1, "Tag73": 1, "Tag74": 1, "Tag75": 1, "Tag76": 1, "Tag77": 1, "Tag78": 1, "Tag79": 1, "Tag80": 1,
                                        "Tag81": 1, "Tag82": 1, "Tag83": 1, "Tag84": 1, "Tag85": 1, "Tag86": 1, "Tag87": 1, "Tag88": 1, "Tag89": 1, "Tag90": 1,
                                        "Tag91": 1, "Tag92": 1, "Tag93": 1, "Tag94": 1, "Tag95": 1, "Tag96": 1, "Tag97": 1, "Tag98": 1, "Tag99": 1, "Tag100": 1}, index=[0])

# myTempKeycollection.insert_many(df1.to_dict('records'))
# myTempKeycollection.insert_many(df2.to_dict('records'))
# myTempKeycollection.insert_many(df3.to_dict('records'))
myTempKeycollection.insert_many(df4.to_dict('records'))

