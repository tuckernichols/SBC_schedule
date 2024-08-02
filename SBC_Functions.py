import pdfplumber
import pandas as pd
import openpyxl
import email
import imaplib
import ssl
import os

print("Schedule options")
print(os.listdir("saveFolder")[1:])
print()
print("Output:")


def save_name(PDFName):
    name = ""
    for l in PDFName:
        try:
            l = int(l)
            name = name + str(l)
        except:
            if l == "-":
                name = name + l
    return f"saveFolder/{name}.xlsx"


def pdf_to_pandas(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        page = pdf.pages[0]
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            all_tables.append(df)
        combined_df = pd.concat(all_tables, ignore_index=True)
    return combined_df


weekly_Col_Mapping = { "monday": 1, "tuesday": 3, "wednesday": 5, "thursday": 7, "friday": 9,
                      "saturday": 11, "sunday": 13}
reversed_weekly_col_mapping = {value: key for key, value in weekly_Col_Mapping.items()}


def reverse_mappings(col: int):
    if col % 2 == 0:
        col -= 1
        time = "Dinner"
    else:
        time = "Lunch"
    day = reversed_weekly_col_mapping[col]
    return f"{day} {time}"


def data_col(day, lunch):
    n = weekly_Col_Mapping[day]
    if not lunch:
        n += 1
    return n


def number_of_employes(pandas_df):
    count = 0
    for i in range(3, 100):
        if str(pandas_df.iat[i, 0]) == "Arrive at-->":
            break
        count += 1
    return count


def collect_data(pandas_df, col):
    returnList = []
    _range = number_of_employes(pandas_df=pandas_df)
    for idx in range(3,_range + 3):
        if len(pandas_df.iat[idx, col]) > 0:
            shift = pandas_df.iat[idx, col]
            name = pandas_df.iat[idx, 0]
            returnList.append([name, shift])
    return returnList


def sort_data(data: list):
    x = ""
    gates = ""
    snackBar = ""
    captains = ""
    pit = ""
    TL = ""
    for i in data:
        if i[1] == "X":
            x = x + f"{i[0]}, "
        elif i[1] == "EX" or i[1] == "FC" or i[1] == "*":
            captains = captains + f"{i[0]}, "
        elif i[1] == "A1" or i[1] == "B1" or i[1] == 'CHECK1' or i[1] == "A2":
            gates = gates + f"{i[0]}, "
        elif i[1][:2] == "SB":
            snackBar = snackBar + f"{i[0]}, "
        elif i[1][0] == "P":
            pit = i[0]
        elif i[1] == "T/L":
            TL = i[0]


    return f"""
        CAPTAINS:
    {captains}    
        WAITSTAFF:
    {x} 
        GATES:
    {gates}  
        SNACK BAR:
    {snackBar}
        PIT:
    {pit}
        T/L
    {TL}    
    """


emailsBack = 1
server =  "imap.gmail.com"
emailAdress = "tuckernmilly@gmail.com"
password = "google app password"   # app pasword


def save_schedule_PDF():
    context = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(server, port=993, ssl_context=context)
    imap.login(emailAdress, password)
    imap.select("Inbox")

    status, messages = imap.search(None, f'(FROM "{"acarey@singingbeachclub.com"}")')
    emailIDS = messages[0].split()
    _, data = imap.fetch(emailIDS[0 - emailsBack], '(RFC822)')     # -1 gives most recent
    emailData = email.message_from_bytes(data[0][1])
    filename = str(emailData.get("Subject"))
    for part in emailData.walk():
        if part.get_content_type() == "application/pdf":
            filename = part.get_filename()
            filepath = os.path.join("saveFolder", str(filename))
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))

    imap.close()
    print("pdf saved as ", filename)
    return filename

