# Email Monitor

![Acenet Technology Logo](acenelog.png)

## Overview

The **Email Monitor** is a simple, user-friendly desktop application built with Python and Tkinter that allows you to display the latest 10 email messages from a specified email address in your Gmail account. It features a modern, attractive interface with dark and light theme options, a menu bar for navigation, and robust error handling. The app uses the Gmail API for email retrieval, requiring OAuth 2.0 authentication for secure access.

This application was developed with guidance and assistance from **Grok**, an AI developed by **xAI**, which provided invaluable support in coding, troubleshooting, and optimizing the project.

## Features

- Display the latest 10 emails from a specified Gmail address.
- Modern GUI with dark and light theme toggling via settings.
- Menu bar with options for File (Exit), About, and Settings.
- Progress bar while loading emails.
- Customizable styling with padding and dividers in the email list.
- Error handling for authentication, GUI setup, and email listing.
- Includes a logo and app icon for branding.

## Prerequisites

Before running or packaging the Email Monitor, ensure you have the following:

- **Python 3.8+** installed on your system.
- The following Python libraries installed (install via pip):
  - `google-api-python-client`
  - `google-auth-httplib2`
  - `google-auth-oauthlib`
  - `tkinter` (usually included with Python, but verify installation)
  - `Pillow` (for image handling)

You can install these libraries using:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib Pillow
```

- A Google Cloud project with the Gmail API enabled and OAuth 2.0 credentials (`credentials.json`) downloaded.
- The `acenelog.png` logo file in the project directory for branding.

## Installation

### 1. Clone or Download the Repository

Clone this repository to your local machine or download the source code as a ZIP file:

```bash
git clone <repository-url>
cd email_monitor
```

### 2. Set Up Google Cloud Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Gmail API for your project.
4. Create OAuth 2.0 credentials (Desktop application type).
5. Download the `credentials.json` file and place it in the root directory of this project.

### 3. Install Dependencies

Run the following command in your terminal or PyCharm terminal to install the required Python libraries:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib Pillow
```

### 4. Run the Application

- Open the `email_monitor.py` file in your Python environment (e.g., PyCharm or a Python IDE).
- Run the script:

```bash
python email_monitor.py
```

- Follow the on-screen instructions to authenticate with Google using the OAuth 2.0 flow (a browser window will open for login and permissions).

## Usage

1. Launch the `Email Monitor` application.
2. In the GUI, enter the email address of the sender whose emails you want to view in the "Enter Email Address" field.
3. Click the "Display Emails" button to list the latest 10 emails from that address in the table below.
4. Use the menu bar to:
   - Navigate to "File > Exit" to close the program.
   - Open "About > About Email Monitor" to view program details, including the logo, owner, and company information.
   - Access "Settings > Page Settings" to toggle between dark and light themes.
5. A progress bar will appear while emails are loading, and you’ll see a confirmation message when emails are displayed.

## Packaging into an Executable

To create a standalone executable (`Email_Monitor.exe`) for Windows, use PyInstaller:

1. Ensure `credentials.json` and `acenelog.png` are in the same directory as `email_monitor.py`.
2. Run the following command in your terminal:

```bash
pyinstaller --onefile --windowed --add-data "credentials.json;." --add-data "acenelog.png;." email_monitor.py
```

3. After packaging, find the executable in the `dist` folder. Run `Email_Monitor.exe` to launch the application.

## Troubleshooting

- **Authentication Error**: If you encounter an error about `credentials.json`, ensure it’s in the project directory and correctly named. Verify your Google Cloud project settings and OAuth 2.0 credentials.
- **Icon/Logo Error**: If the app fails to load the icon or logo, check that `acenelog.png` is in the project directory and included in the PyInstaller command.
- **Dependencies Missing**: If libraries are missing, reinstall them using the `pip install` command above.
- **Theme Error**: If toggling themes fails, ensure your Tkinter installation supports all styling options (update Python or Tkinter if necessary).

## Author

- **Name**: Opeyemi Adedotun
- **Email**: ope_adedotun@live.com
- **Company**: Acenet Technology

## Acknowledgments

This project was developed with the assistance of **Grok**, an AI developed by **xAI**. Their innovative technology and support were instrumental in creating this application. Special thanks to xAI for their contributions to advancing human scientific discovery through AI.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (if applicable, or specify your license here).

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. You are allowed to make any major changes without having to request for permission.
