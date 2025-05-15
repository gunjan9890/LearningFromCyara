import imapclient
import pyzmail

imap_url = "imap.gmail.com"
imap_port = 993
mail_username = "qa.tester6@cyara.com"
mail_password = "nxlxwhooadbjfonq"

# connect to imap server
mail = imapclient.IMAPClient(host=imap_url, port=imap_port)

# login
mail.login(mail_username, mail_password)

# select the mail box
mail.select_folder("INBOX")

subject = "TRIGGERED"

# search
messages = mail.search(['SUBJECT', subject])
# messages = mail.search('ALL')
# messages = mail.gmail_search('after:2024/05/19 AND from:webportal@cyarasolutions.com')

print(f"Total Message found = {len(messages)}")
# print(message)

# fetched_dict_all = mail.fetch(messages[0], 'ALL')
# print(fetched_dict_all)
fetched_dict = mail.fetch(messages, ['ENVELOPE'])
print(f"Total length of dictionary = {len(fetched_dict)}")
for msg_id in messages:
    # print(fetched_dict)
    sub_dict = fetched_dict[msg_id]
    mail_subject = sub_dict[b'ENVELOPE'].subject.decode()
    mail_from = sub_dict[b'ENVELOPE'].from_[0].name.decode()
    print(sub_dict)
    if "Pulse Major Alert (TC In)" in mail_subject:
        print(sub_dict)
        # print(f"dict items in msg = [{msg_id}] are [{len(sub_dict)}]")
        print("Envelope", sub_dict[b'ENVELOPE'])
        print("Subject", mail_subject)
        print(f"From = [{mail_from}]")
        # print(f"Date = [{sub_dict[b'ENVELOPE'].date}]")
        print("-"*80)

mail.logout()
