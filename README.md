# Email Automation Application

This Email Automation application allows you to send emails with attachments and use pre-defined templates. The application is built using Python and packaged as an executable for easy use.

## Getting Started

### Requirements

- **Python** (for development): Ensure you have Python 3.6 or later installed. The executable is self-contained and does not require Python.
- **Webmail Account**: You'll need an email account to send emails. For Gmail and other providers, you may need to generate an app-specific password for security reasons.

### Running the Application

1. **Download the Executable**

   - Obtain the executable file from the distribution source or build it using PyInstaller.

2. **Run the Executable**

   - Double-click the executable file to open the application.

3. **Using the Application**

   - **Email:** Enter your email address.
   - **Password:** Enter your email account password or app-specific password.
   - **To:** Enter the recipient's email address(es) (separated by commas).
   - **CC:** Enter email addresses to be added in CC (separated by commas).
   - **BCC:** Enter email addresses to be added in BCC (separated by commas).
   - **Subject:** Enter the subject of the email.
   - **Body:** Enter the body text of the email.
   - **Template:** Select a pre-defined template from the dropdown menu to auto-fill the subject and body. If no templates are available, you can add new ones.
   - **Attachment:** Click the "Browse" button to select a file to attach.

4. **Send Email**
   - Click the "Send Email" button to send the email with the provided details.

### Adding and Using Templates

1. **Add New Template**

   - Fill in the "New Template Name," "New Template Subject," and "New Template Body" fields.
   - Click the "Add Template" button to save the new template.

2. **Use Template**
   - Select a template from the "Template" dropdown menu to auto-fill the subject and body fields with the template's content.

### App-Specific Passwords

For enhanced security, many webmail providers require you to use an app-specific password instead of your main account password. Here’s how to generate one for popular providers:

#### Gmail

1. Go to your [Google Account](https://myaccount.google.com/).
2. Navigate to "Security" in the sidebar.
3. Under "Signing in to Google," select "App passwords."
4. If prompted, sign in with your Google account password.
5. Select "Mail" from the "Select app" dropdown and "Windows Computer" or the device you're using.
6. Click "Generate" to create an app-specific password.
7. Use this generated password in the application instead of your main Google account password.

#### Yahoo Mail

1. Sign in to your Yahoo account.
2. Go to [Account Security](https://login.yahoo.com/account/security).
3. Click on "Generate app password" or "App passwords."
4. Choose "Other App" and enter a name (e.g., "Email Automation").
5. Click "Generate" and copy the generated password.
6. Use this password in the application.

#### Outlook

1. Go to the [Microsoft Account Security](https://account.microsoft.com/security).
2. Click on "Advanced security options."
3. Under "App passwords," select "Create a new app password."
4. Follow the prompts to generate the password.
5. Use this password in the application.

### Troubleshooting

- **No Templates Available:** Ensure the `email_templates.json` file is present in the same directory as the executable and contains valid template data.
- **Failed to Send Email:** Check your email settings, ensure the correct password is used, and verify internet connectivity.

## License

This application is provided under the MIT License. See the LICENSE file for details.

## Contact

For further assistance, please contact [your support email].

---

Thank you for using the Email Automation Application!
