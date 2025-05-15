import imaplib, email
from email.header import decode_header

# user = 'outboundcca@cyara.com'
# password = 'aznslklvgtpctbka'
# imap_url = 'imap.gmail.com'

user = 'qatestcyara@gmail.com'
password = 'nblrfnjctesuouht'
imap_url = 'imap.gmail.com'


con = imaplib.IMAP4_SSL(imap_url)
con.login(user, password)
(res, count) = con.select('Inbox')
if res == "OK":

    # (res, data) = con.search(None, "FROM", "service@ringcentral.com")
    subject = ""
    (res, data) = con.search(None, f'(SUBJECT "{subject}")')

    data = data[0].split()
    latest_msg_id = data[-1]
    (status,msg_data) = con.fetch(latest_msg_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            email_subject = decode_header(msg["Subject"])[0][0]
            if isinstance(email_subject, bytes):
                email_subject = email_subject.decode()

    print(f"Email Subject : {email_subject}")
con.logout()
# msgs = get_emails(data[-1])
#
# for msg in msgs[::-1]:
#     for sent in msg:
#         if type(sent) is tuple:
#
#             # encoding set as utf-8
#             content = str(sent[1], 'utf-8')
#             data = str(content)
#
#             # Handling errors related to unicodenecode
#             try:
#                 indexstart = data.find("ltr")
#                 data2 = data[indexstart + 5: len(data)]
#                 indexend = data2.find("</div>")
#
#                 # printtng the required content which we need
#                 # to extract from our email i.e our body
#                 print(data2[0: indexend])
#
#             except UnicodeEncodeError as e:
#                 pass