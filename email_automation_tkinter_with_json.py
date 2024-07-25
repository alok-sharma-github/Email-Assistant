import smtplib
from tkinter import *
from tkinter import filedialog, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
import language_tool_python
import schedule
import time
from threading import Thread

# Load email templates from a JSON file
def load_templates(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as file:
        return json.load(file)

# Save email templates to a JSON file
def save_templates(filename, templates):
    with open(filename, 'w') as file:
        json.dump(templates, file, indent=4)

# Check and correct grammar
def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

# Send email function
def send_email(from_addr, password, to_addrs, cc_addrs, bcc_addrs, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Cc'] = ', '.join(cc_addrs)
    msg['Bcc'] = ', '.join(bcc_addrs)
    msg['Subject'] = subject

    body = check_grammar(body)
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        filename = os.path.basename(attachment_path)
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

    text = msg.as_string()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addrs + cc_addrs + bcc_addrs, text)
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

# Browse for file attachment
def browse_file():
    filename = filedialog.askopenfilename()
    attachment_var.set(filename)

# Send email button action
def send_email_button():
    from_addr = email_entry.get()
    password = password_entry.get()
    to_addrs = to_entry.get().split(',')
    cc_addrs = cc_entry.get().split(',')
    bcc_addrs = bcc_entry.get().split(',')
    subject = subject_entry.get()
    body = body_entry.get("1.0", END)
    attachment_path = attachment_var.get()
    send_email(from_addr, password, to_addrs, cc_addrs, bcc_addrs, subject, body, attachment_path)

# Populate template fields
def populate_template(*args):
    selected_template = template_var.get()
    if selected_template in email_templates:
        subject_entry.delete(0, END)
        subject_entry.insert(0, email_templates[selected_template]['subject'])
        body_entry.delete("1.0", END)
        body_entry.insert("1.0", email_templates[selected_template]['body'])
    elif selected_template == "No templates available":
        subject_entry.delete(0, END)
        body_entry.delete("1.0", END)

# Add custom template
def add_template():
    template_name = new_template_name_entry.get()
    subject = new_template_subject_entry.get()
    body = new_template_body_entry.get("1.0", END).strip()
    
    if template_name and subject and body:
        email_templates[template_name] = {
            "subject": subject,
            "body": body
        }
        save_templates('email_templates.json', email_templates)
        template_menu['menu'].add_command(label=template_name, command=lambda value=template_name: template_var.set(value))
        new_template_name_entry.delete(0, END)
        new_template_subject_entry.delete(0, END)
        new_template_body_entry.delete("1.0", END)
        messagebox.showinfo("Success", "Template added successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

def schedule_email(schedule_type, send_time, from_addr, password, to_addrs, cc_addrs, bcc_addrs, subject, body, attachment_path=None):
    def job():
        send_email(from_addr, password, to_addrs, cc_addrs, bcc_addrs, subject, body, attachment_path)
    
    hour, minute = map(int, send_time.split(':'))
    
    if schedule_type == "Once":
        schedule.every().day.at(send_time).do(job)
    elif schedule_type == "Daily":
        schedule.every().day.at(send_time).do(job)
    elif schedule_type == "Weekly":
        schedule.every().week.at(send_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduling():
    schedule_type = schedule_var.get()
    send_time = send_time_entry.get()
    from_addr = email_entry.get()
    password = password_entry.get()
    to_addrs = to_entry.get().split(',')
    cc_addrs = cc_entry.get().split(',')
    bcc_addrs = bcc_entry.get().split(',')
    subject = subject_entry.get()
    body = body_entry.get("1.0", END)
    attachment_path = attachment_var.get()

    t = Thread(target=schedule_email, args=(schedule_type, send_time, from_addr, password, to_addrs, cc_addrs, bcc_addrs, subject, body, attachment_path))
    t.start()

# Load templates
email_templates = load_templates('email_templates.json')

app = Tk()
app.title("Email Automation")
app.geometry("700x800")  # Set a default window size

# Layout widgets with better organization and padding
frame1 = Frame(app)
frame1.grid(row=0, column=0, padx=10, pady=10, sticky=W)

frame2 = Frame(app)
frame2.grid(row=0, column=1, padx=10, pady=10, sticky=E)

frame3 = Frame(app)
frame3.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

frame4 = Frame(app)
frame4.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

Label(frame1, text="Email:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
email_entry = Entry(frame1)
email_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="Password:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
password_entry = Entry(frame1, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="To:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
to_entry = Entry(frame1)
to_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="CC:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
cc_entry = Entry(frame1)
cc_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="BCC:").grid(row=4, column=0, sticky=W, padx=5, pady=5)
bcc_entry = Entry(frame1)
bcc_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="Subject:").grid(row=5, column=0, sticky=W, padx=5, pady=5)
subject_entry = Entry(frame1)
subject_entry.grid(row=5, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="Body:").grid(row=6, column=0, sticky=W, padx=5, pady=5)
body_entry = Text(frame1, height=10, width=50)
body_entry.grid(row=6, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="Template:").grid(row=7, column=0, sticky=W, padx=5, pady=5)
template_var = StringVar(app)
template_var.set("Select a template")
template_keys = tuple(email_templates.keys())
if not template_keys:
    template_keys = ("No templates available",)
template_menu = OptionMenu(frame1, template_var, *template_keys)
template_var.trace("w", populate_template)
template_menu.grid(row=7, column=1, padx=5, pady=5, sticky=W+E)

Label(frame1, text="Attachment:").grid(row=8, column=0, sticky=W, padx=5, pady=5)
attachment_var = StringVar()
attachment_entry = Entry(frame1, textvariable=attachment_var)
attachment_entry.grid(row=8, column=1, padx=5, pady=5, sticky=W+E)
browse_button = Button(frame1, text="Browse", command=browse_file)
browse_button.grid(row=8, column=2, padx=5, pady=5)

send_button = Button(frame1, text="Send Email", command=send_email_button)
send_button.grid(row=9, column=1, padx=5, pady=5, sticky=W+E)

Label(frame2, text="Schedule Type*(optional):").grid(row=0, column=0, sticky=W, padx=5, pady=5)
schedule_var = StringVar(app)
schedule_var.set("Once")
schedule_menu = OptionMenu(frame2, schedule_var, "Once", "Daily", "Weekly")
schedule_menu.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)

Label(frame2, text="Send Time (HH:MM):").grid(row=1, column=0, sticky=W, padx=5, pady=5)
send_time_entry = Entry(frame2)
send_time_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W+E)

schedule_button = Button(frame2, text="Schedule Email", command=start_scheduling)
schedule_button.grid(row=2, column=1, padx=5, pady=5, sticky=W+E)

Label(frame3, text="New Template Name:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
new_template_name_entry = Entry(frame3)
new_template_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)

Label(frame3, text="New Template Subject:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
new_template_subject_entry = Entry(frame3)
new_template_subject_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W+E)

Label(frame3, text="New Template Body:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
new_template_body_entry = Text(frame3, height=10, width=50)
new_template_body_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W+E)

add_template_button = Button(frame3, text="Add Template", command=add_template)
add_template_button.grid(row=3, column=1, padx=5, pady=5, sticky=W+E)

app.mainloop()
