# InboxCleaner

InboxCleaner is a web application that helps users manage their Gmail inbox by moving old unread emails to the trash. This project is built using Django and the Gmail API.

## Features

- **Gmail Authentication**: Users can authenticate their Gmail account to access their inbox.

- **Confirm Cleanup Date**: Users can confirm a cleanup date, and the application will move unread emails older than that date to the trash.

- **Cleanup Success**: After the cleanup process, users receive a confirmation with the number of unread emails moved to the trash.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Gmail API credentials (client secrets)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/InboxCleaner.git
    cd InboxCleaner
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure Gmail API:

    - Follow the Gmail API Python Quickstart guide to obtain credentials.json: [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart)

4. Run the application:

    ```bash
    python manage.py runserver
    ```

5. Access the application in your web browser: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage

1. Open the application in your web browser.

2. Click on "Get Started" to initiate Gmail authentication.

3. Confirm a cleanup date to move unread emails older than that date to the trash.

4. receive a success message.

## Contributing

Contributions are welcome! Fork the repository, create a new branch, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

