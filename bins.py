#! /usr/bin/env python3
import requests
import json
from datetime import date as dt
from datetime import datetime

def getBins():
  #Setup Session Token
  initUrl = "https://devmaps.rockingham.wa.gov.au/IntraMaps910/ApplicationEngine/Configuration/PublicLite/Config/e15da824-2d34-4588-bedc-d5e77b4e4c29?configId=00000000-0000-0000-0000-000000000000"
  x = requests.get(initUrl)
  initResult = json.loads(x.text)
  projectId = initResult["intraMapsSettings"]["project"]
  moduleId = initResult["intraMapsSettings"]["module"]
  init2Url = "https://devmaps.rockingham.wa.gov.au/IntraMaps910/ApplicationEngine/Projects/?configId=00000000-0000-0000-0000-000000000000&appType=MapBuilder&project=" + projectId
  x = requests.post(init2Url)
  sessionId = x.headers["X-IntraMaps-Session"]
  init3Url = "https://devmaps.rockingham.wa.gov.au/IntraMaps910/ApplicationEngine/Modules/?IntraMapsSession=" + sessionId
  params = {"module": moduleId,"includeWktInSelection": True}
  x = requests.post(init3Url, json = params)
  init3Result = json.loads(x.text)
  templateId = ""

  for form in init3Result["forms"]:
    if(form["name"] == "Quick Address"):
      templateId = form["templateId"]

  #Search Property
  f = open("config.txt", "r")
  address = f.readline()
  address = ' '.join(address.split())

  url = 'https://devmaps.rockingham.wa.gov.au/IntraMaps910/ApplicationEngine/Search/?infoPanelWidth=0&mode=Refresh&form=' + templateId + '&resubmit=false&IntraMapsSession=' + sessionId
  params = {"fields":[address]}
  x = requests.post(url, json = params)

  result = json.loads(x.text)
  propertyDetails = result["fullText"][0]
  selectionLayer = propertyDetails["selectionLayer"]
  mapKey = propertyDetails["mapKey"]
  dbKey = propertyDetails["dbKey"]


  # Request info
  url = 'https://devmaps.rockingham.wa.gov.au/IntraMaps910/ApplicationEngine/Search/Refine/Set?IntraMapsSession=' + sessionId
  params = {"selectionLayer":selectionLayer,"mapKey":mapKey, "dbKey": dbKey}

  x = requests.post(url, json = params)

  result = json.loads(x.text)

  fields = result["infoPanels"]["info1"]["feature"]["fields"]

  now = dt.today()
  today = now.strftime("%d %B %Y")
  currentDate = datetime.strptime(today, "%d %B %Y")

  data = { }

  for field in fields:
    if(field["name"] == "Recycling Bin (yellow lid)"):
      bindaySentence = field["value"]["value"]
      binday = bindaySentence.split("collection ")[1]
      binDate = datetime.strptime(binday, "%d %B %Y")
      diff = binDate - currentDate
      data["nextRecycleDate"] = binday
      if(diff.days < 7):
        data["isRecycleWeek"] = True
      else:
        data["isRecycleWeek"] = False
    if(field["name"] == "Green Waste Bin (lime green lid)"):
      bindaySentence = field["value"]["value"]
      binday = bindaySentence.split("collection ")[1]
      binDate = datetime.strptime(binday, "%d %B %Y")
      diff = binDate - currentDate
      data["nextGreenWasteDate"] = binday
      if(diff.days < 7):
        data["isGreenWasteWeek"] = True
      else:
        data["isGreenWasteWeek"] = False
    if(field["name"] == "Waste Bin (red lid)"):
      binday = field["value"]["value"]
      data["binday"] = binday
    if(field["name"] == "Verge Collection Green Waste"):
      bindaySentence = field["value"]["value"]
      bindays = bindaySentence.split("starting : ")[1].split(",")
      nextGreenVergeDay = "N/A"
      for binday in bindays:
        day = binday.strip()
        date = datetime.strptime(day, "%d %B %Y")
        diff = date - currentDate
        if(diff.days >= 0):
          if(nextGreenVergeDay == "N/A"):
            nextGreenVergeDay = date.strftime("%d %B %Y")
          else:
            prevNextDay = datetime.strptime(nextGreenVergeDay, "%d %B %Y")
            if(prevNextDay > date):
              nextGreenVergeDay = date.strftime("%d %B %Y")
      data["nextVergeGreenWasteDate"] = nextGreenVergeDay
      if(nextGreenVergeDay == "N/A"):
        data["isVergeGreenWasteWeek"] = False
      else:
        date = datetime.strptime(nextGreenVergeDay, "%d %B %Y")
        diff = date - currentDate
        if(diff.days < 7):
          data["isVergeGreenWasteWeek"] = True
        else:
          data["isVergeGreenWasteWeek"] = False
    if(field["name"] == "Verge Collection General"):
      bindaySentence = field["value"]["value"]
      bindays = bindaySentence.split("starting : ")[1].split(",")
      nextGreenVergeDay = "N/A"
      for binday in bindays:
        day = binday.strip()
        date = datetime.strptime(day, "%d %B %Y")
        diff = date - currentDate
        if(diff.days >= 0):
          if(nextGreenVergeDay == "N/A"):
            nextGreenVergeDay = date.strftime("%d %B %Y")
          else:
            prevNextDay = datetime.strptime(nextGreenVergeDay, "%d %B %Y")
            if(prevNextDay > date):
              nextGreenVergeDay = date.strftime("%d %B %Y")
      data["nextVergeGeneralWasteDate"] = nextGreenVergeDay
      if(nextGreenVergeDay == "N/A"):
        data["isVergeGeneralWasteWeek"] = False
      else:
        date = datetime.strptime(nextGreenVergeDay, "%d %B %Y")
        diff = date - currentDate
        if(diff.days < 7):
          data["isVergeGeneralWasteWeek"] = True
        else:
          data["isVergeGeneralWasteWeek"] = False

  fields = result["infoPanels"]["info2"]["fields"]

  info = {}

  for field in fields:
    if(field["name"] == "Address"):
      info["address"] = field["value"]["value"]
    if(field["name"] == "Suburb"):
      info["suburb"] = field["value"]["value"]
    if(field["name"] == "Lot on Plan"):
      info["lot"] = field["value"]["value"]
    if(field["name"] == "Area"):
      area = field["value"]["value"]
      info["area"] = area

  data["info"] = info


  print(data)

  if(data["isRecycleWeek"]):
    print("YELLOW")
  if(data["isGreenWasteWeek"]):
    print("GREEN")

  with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)