import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

MY_ADDRESS = 'anhnv@i-com.vn'
PASSWORD = 'Vietanh1996'

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def email_sending(mess="error"):
    try:
        names, emails = get_contacts('/home/vietanh/PythonProjects/chamcong_version2/broadcast/contacts.txt') # read contacts
        message_template = read_template('/home/vietanh/PythonProjects/chamcong_version2/broadcast/message.txt')

        # set up the SMTP server
        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)

        # For each contact, send the email:
        for name, email in zip(names, emails):
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=name.title())

            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=email
            msg['Subject']=mess
            
            # Create the plain-text and HTML version of your message
            html = """\
            <html>
              <body>
                <p>
                    Xin chào Nguyễn Văn A<br>
                    Chúc bạn một buổi sáng tốt lành! Chỉ cần mỉm cười bạn sẽ thấy cuộc sống rất thú vị!<br>
                    Hệ thống nhân diện hình ảnh tự động bằng camera bắt gặp hình ảnh chào ngày mới của bạn.<br>
                    Check in:2020-02-26 08:13:30 <br>

                    <img src="cid:image0" alt="Italian Trulli">

                    <br>

                    Nếu quả nhận diện chưa chính xác làm ơn recheck giúp hệ thống cải thiện hơn.<br> 

                    <img src="cid:image1" alt="Italian Trulli">

                    <img src="cid:image2" alt="Italian Trulli">

                    <img src="cid:image3" alt="Italian Trulli">

                </p>
              </body>
            </html>
            """

            # add in the message body
            msg.attach(MIMEText(html, 'html'))

            fp = open("recheck1.png", "rb")
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<image0>')
            msg.attach(msgImage)

            fp = open("recheck1.png", "rb")
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<image1>')
            msg.attach(msgImage)

            fp = open("recheck2.png", "rb")
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<image2>')
            msg.attach(msgImage)

            fp = open("recheck3.png", "rb")
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<image3>')
            msg.attach(msgImage)
            
            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
            
        # Terminate the SMTP session and close the connection
        s.quit()
    except Exception as e:
        raise e
    finally:
        pass
    
    
if __name__ == '__main__':
    email_sending()