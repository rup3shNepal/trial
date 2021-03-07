import requests
import smtplib
import datetime
from email.message import EmailMessage

APP_SETTINGS = {
    "SENDER":"nirtech.12345@gmail.com",
    "PASSWORD":"n1_rjal9841",
    "ALLOWED KEYS":["symbol","openPrice","lowPrice","highPrice","closePrice","previousDayClosePrice","totalTradedQuantity"],
    "SYMBOLS":['AIL', 'AKPL', 'GIC', 'NICLBSL', 'NIFRA', 'NRIC', 'NRN', 'PLI', 'RLI', 'SGI', 'UPPER']
  }

def entries_to_remove(json_data):
  for data in json_data:
    keys = list(data.keys())
    for key in keys:
        if key not in APP_SETTINGS["ALLOWED KEYS"]:
            del data[key]
  return json_data

#normal functions
def get_data():
    data = requests.get(
        "https://newweb.nepalstock.com/api/nots/nepse-data/today-price?page=0&size=202",
        headers = {
            "user-agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        })
    return data


# validators
def validate_request(func):
    resp = func()
    if (resp.status_code == 200):
        APP_SETTINGS["SCHEME"] = resp.json()["content"][0].keys()
        return resp.json()
    else:
        return {
            "Error": "Some error occured",
            "status_code": resp.status_code
        }
#works by pass by refrence
def make_html_table_element(data,type_):
  msg= ""
  if (type_=="body"):
    msg+= f"<td>{str(data)}</td>"
  else:
    msg+= f"<th>{str(data)}</th>"

  return msg

#works by pass by refrence
def make_html_table_row(row_data,type_="body"):
  msg =""
  
  msg+="<tr>"
  if (type_=="body"):  
    for key,value in row_data:
      
      msg+=make_html_table_element(value,type_)
  else:
    for key,value in row_data:
      msg+=make_html_table_element(key,type_)
  msg+="</tr>"
  return msg

#works by pass by refrence
def make_table(json_data):
  msg = ""
  print(json_data)
  msg+= make_html_table_row(json_data[0].items(),type_="not body")
  for data in json_data:
    msg += make_html_table_row(data.items());
  return msg


def get_info():
    data = validate_request(get_data)
    if (data.get("status_code") and data.get("status_code") != 200):
        return None
    live_data = []
    all_shares = data["content"]
    for share in all_shares:
        if (share["symbol"] in APP_SETTINGS["SYMBOLS"]):
            live_data.append(share)
    return live_data


def get_basic_info_from_share(share_data):
  new_share_data =   list(share_data.values())
  return new_share_data

    

def send_mail(body):
  time_now = datetime.datetime.now()
  minute_now = time_now.minute;
  hour_now = time_now.hour;

  msgEmail = EmailMessage()
  msgEmail["From"] = APP_SETTINGS["SENDER"]
  msgEmail["To"] = "nirjalcsit2076_18@mbmcsit.edu.np"
  msgEmail["Subject"] = f"Market Report {hour_now} :{minute_now} - {str(datetime.date.today())}"
  msgEmail.set_content("Latest Share Market Data")
  msgEmail.add_alternative(body,subtype="html")
  

  with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
  # with smtplib.SMTP('mail.hamrobakas.com',465) as smtp:
    smtp.login(APP_SETTINGS["SENDER"],APP_SETTINGS["PASSWORD"])
    smtp.send_message(msgEmail)

def makeHTML(htmlBody):
  code = '''<!DOCTYPE html><html><head>
  <title>Page Title</title>
  <style>
  table{
        max-width:400px !important;
        border-collapse: separate !important;
        border-spacing: 15px !important;
        font-size:20px;
       }
  </style>
  </head>
  <body>
  <h3>Share Report - '''+str(datetime.date.today())+'''</h3><hr><br><table>'''+htmlBody+'''</table></body></html>'''
  return code

def main():
  data = get_info()
  entries_to_remove(data)
  msg= make_table(data)
  print(msg)
  HTMLCODE = makeHTML(msg)
  send_mail(HTMLCODE)
  print("FINISHED")  
  
main()
