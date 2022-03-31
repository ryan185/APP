import pymongo
import  sys
import re
from textwrap import wrap
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
# -----------------------------------------------------------------
class get_pdf(object):
	def __init__(self, arg):
		super(get_pdf, self).__init__()
		self.arg = arg

	def isJapanese(s):
		if re.search("[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]", s):
			return True
		else:
			return False

	def get_one_line_font_size(string):
		length = len(string)
		font_size = 110
		if length < 7:
			font_size = 120
		elif length == 7:
			font_size = 110
		else:
			font_size = 100
		return font_size

	def get_multiple_line_font_size(string):
		length = len(string)
		font_size = 110
		if length <= 7:
			font_size = 110
		else:
			font_size = 100
		return font_size

	def get_jp_x(string,font_size):
		length = len(string)
		width = 345
		if length >= 8:
			width = 27
		if font_size == 110:
			if length == 1:
				width = 365
			if length == 2:
				# print("worked")
				width = 365-50
			if length == 3:
				width = 365-100
			if length == 4:
				width = 365-160
			if length == 5:
				# print("worked")
				width = 365-220
			if length == 6:
				width = 365-265
			if length == 7:
				width = 365-330
		if font_size == 120:
			if length == 1:
				width = 345
			if length == 2:
				width = 345-50
			if length == 3:
				width = 345-100
			if length == 4:
				width = 345-160
			if length == 5:
				width = 345-220
			if length == 6:
				width = 345-275
		return width

	def get_eng_x(string,font_size):
		length = len(string)
		width = 345
		if length >= 8:
			width = 200
		if font_size == 110:
			if length == 1:
				width = 420
			if length == 2:
				width = 420-70
			if length == 3:
				width = 420-90
			if length == 4:
				width = 420-120
			if length == 5:
				width = 420-160
			if length == 6:
				width = 420-180
			if length == 7:
				width = 420-200
		if font_size == 120:
			if length == 1:
				width = 400
			if length == 2:
				width = 400-50
			if length == 3:
				width = 400-80
			if length == 4:
				width = 400-120
			if length == 5:
				width = 400-140
			if length == 6:
				width = 400-160
		return width

	def return_pdf(boxnum):
		def onelinekeyname(boxnum,number,name,comp,compid):
			if comp == "-":
				comp = " "
			if compid == "-":
				compid = " "
			
			pdf_canvas.setFont('yugothib', 120)
			pdf_canvas.drawString(25, 480, number)
			if get_pdf.isJapanese(name):
				fontsize = get_pdf.get_one_line_font_size(name)
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_jp_x(name,fontsize), 260, name)
			else:
				fontsize = get_pdf.get_one_line_font_size(name)
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_eng_x(name,fontsize), 260, name)

			pdf_canvas.setFont('meiryo', 20)
			pdf_canvas.drawString(25, 15, "Box No")
			pdf_canvas.setFont('meiryo', 20)
			pdf_canvas.drawString(125, 15, "Key No")
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(50, 40, boxnum)
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(65, 40, " - ")
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(100, 40, number)

			if comp != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(280, 51, comp) #Limit Length : 5
				pdf_canvas.setFont('meiryo', 15)
				pdf_canvas.drawString(290, 15, "レンタル会社")
			if comp != " " and compid != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(435, 50, " - ")
			if compid != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(475, 50, compid) #Limit Length : 11
				pdf_canvas.setFont('meiryo', 15)
				pdf_canvas.drawString(530, 15, "管理番号")
			pdf_canvas.showPage()

		def twolinekeyname(boxnum,number,name,comp,compid):
			line_list = []
			if comp == "-":
				comp = " "
			if compid == "-":
				compid = " "
			
			pdf_canvas.setFont('yugothib', 100)
			pdf_canvas.drawString(25, 480, number) #Limit Length : 16
			
			for line in name.splitlines(False):
				line_list.append(line)

			if get_pdf.isJapanese(line_list[0]):
				fontsize = get_pdf.get_multiple_line_font_size(line_list[0])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_jp_x(line_list[0],fontsize), 340, line_list[0])
			else:
				fontsize = get_pdf.get_multiple_line_font_size(line_list[0])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_eng_x(line_list[0],fontsize), 340, line_list[0])

			if get_pdf.isJapanese(line_list[1]):
				fontsize = get_pdf.get_multiple_line_font_size(line_list[1])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_jp_x(line_list[1],fontsize), 210, line_list[1])
			else:
				fontsize = get_pdf.get_multiple_line_font_size(line_list[1])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_eng_x(line_list[1],fontsize), 210, line_list[1])

			pdf_canvas.setFont('meiryo', 20)
			pdf_canvas.drawString(25, 15, "Box No")
			pdf_canvas.setFont('meiryo', 20)
			pdf_canvas.drawString(125, 15, "Key No")
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(50, 40, boxnum)
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(65, 40, " - ")
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(100, 40, number)

			if comp != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(280, 51, comp) #Limit Length : 5
				pdf_canvas.setFont('meiryo', 15)
				pdf_canvas.drawString(290, 15, "レンタル会社")
			if comp != " " and compid != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(435, 50, " - ")
			if compid != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(475, 50, compid) #Limit Length : 11
				pdf_canvas.setFont('meiryo', 15)
				pdf_canvas.drawString(530, 15, "管理番号")
			pdf_canvas.showPage()

		def threelinekeyname(boxnum,number,name,comp,compid):
			line_list = []
			if comp == "-":
				comp = " "
			if compid == "-":
				compid = " "
			
			pdf_canvas.setFont('yugothib', 100)
			pdf_canvas.drawString(25, 480, number)

			for line in name.splitlines(False):
				line_list.append(line)

			if get_pdf.isJapanese(line_list[0]):
				fontsize = get_pdf.get_multiple_line_font_size(line_list[0])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_jp_x(line_list[0],fontsize), 390, line_list[0])
			else:
				fontsize = get_pdf.get_multiple_line_font_size(line_list[0])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_eng_x(line_list[0],fontsize), 390, line_list[0])

			if get_pdf.isJapanese(line_list[1]):
				fontsize = get_pdf.get_multiple_line_font_size(line_list[1])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_jp_x(line_list[1],fontsize), 260, line_list[1])
			else:
				fontsize = get_pdf.get_multiple_line_font_size(line_list[1])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_eng_x(line_list[1],fontsize), 260, line_list[1])

			if get_pdf.isJapanese(line_list[2]):
				fontsize = get_pdf.get_multiple_line_font_size(line_list[2])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_jp_x(line_list[2],fontsize), 130, line_list[2])
			else:
				fontsize = get_pdf.get_multiple_line_font_size(line_list[2])
				pdf_canvas.setFont('yugothib', fontsize)
				pdf_canvas.drawString(get_pdf.get_eng_x(line_list[2],fontsize), 130, line_list[2])
			
			pdf_canvas.setFont('meiryo', 20)
			pdf_canvas.drawString(25, 15, "Box No")
			pdf_canvas.setFont('meiryo', 20)
			pdf_canvas.drawString(125, 15, "Key No")
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(50, 40, boxnum)
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(65, 40, " - ")
			pdf_canvas.setFont('meiryo', 40)
			pdf_canvas.drawString(100, 40, number)

			if comp != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(280, 51, comp) #Limit Length : 5
				pdf_canvas.setFont('meiryo', 15)
				pdf_canvas.drawString(290, 15, "レンタル会社")
			if comp != " " and compid != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(435, 50, " - ")
			if compid != " ":
				pdf_canvas.setFont('meiryo', 20)
				pdf_canvas.drawString(475, 50, compid) #Limit Length : 11
				pdf_canvas.setFont('meiryo', 15)
				pdf_canvas.drawString(530, 15, "管理番号")
			pdf_canvas.showPage()

		#database
		myclient = pymongo.MongoClient("localhost", 27017)
		mydb = myclient['key']

		mykeynamecollection = mydb["KeyNameData"]
		myrentalcompanycollection = mydb["RentalCompanyData"]
		myrentalcompanyidcollection = mydb["RentalCompanyIdData"]
		# boxnum = "1"

		findKeyName = mykeynamecollection.find(filter = { "user_id" : int(boxnum)})
		findRentalComp = myrentalcompanycollection.find(filter = { "user_id" : int(boxnum)})
		findRentalCompId = myrentalcompanyidcollection.find(filter = { "user_id" : int(boxnum)})

		countlist, keynamelist, keynumberlist, rentcomplist, rentcompidlist = ([] for i in range(5))
		substring = "\n"

		for doc_keyname in findKeyName:
			for i in range(1,101):
				check = doc_keyname["keyname%i" %i]
				check = check.replace('\r\n','\n')
				count = check.count(substring)
				countlist.insert(i-1, count)
				if i <= 9:
					string = "00%i" %i + " " + check
					keynamelist.insert(i-1, string)
					keynumberlist.insert(i-1, "00%i" %i)
				elif i <= 99:
					string = "0%i" %i + " " + check
					keynamelist.insert(i-1, string)
					keynumberlist.insert(i-1, "0%i" %i)
				elif i == 100:
					string = "100" + " " + check
					keynamelist.insert(i-1, string)
					keynumberlist.insert(i-1, "100")

		for doc_rentcomp in findRentalComp:
			for i in range(1,101):
				rentcomplist.append(doc_rentcomp["rentcomp%i" %i])

		for doc_rentcompid in findRentalCompId:
			for i in range(1,101):
				rentcompidlist.append(doc_rentcompid["rentcompid%i" %i])

		file_out = "C:\\Face\\pdf\\KeyInfo.pdf"

		meiryo = "C:\\Fonts\\meiryo.ttc"
		YUGOTHIB_TTF = "C:\\Fonts\\yugothib.ttf"

		registerFont(TTFont('meiryo', meiryo))
		registerFont(TTFont('yugothib', YUGOTHIB_TTF))

		pdf_canvas = canvas.Canvas(file_out,pagesize=landscape(A4))

		for i in range(0,100):
			if countlist[i]<2:
				if countlist[i]<1:
					onelinekeyname(boxnum,keynumberlist[i],keynamelist[i][4:],rentcomplist[i],rentcompidlist[i])
				else:
					twolinekeyname(boxnum,keynumberlist[i],keynamelist[i][4:],rentcomplist[i],rentcompidlist[i])
			else:
				threelinekeyname(boxnum,keynumberlist[i],keynamelist[i][4:],rentcomplist[i],rentcompidlist[i])
		pdf_canvas.save()

# get_pdf.return_pdf("1")