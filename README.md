# Boxing Club Sign-In Application

A web-based sign-in and membership management system for boxing clubs or gyms. This application allows members to sign in, request membership, and provides an admin interface for managing member data.

## Features
- **Member Sign-In:**
  - Members can sign in using a simple web interface.
  - QR code support for quick access.
- **Membership Requests:**
  - New users can request membership via a form.
  - Requests are stored for admin review.
- **Admin Dashboard:**
  - View and manage current members and membership requests.
  - Approve or reject new member requests.
- **Data Storage:**
  - Member and request data are stored in JSON files for easy management and portability.
- **Static Assets:**
  - Includes club logo and QR code images for branding and quick access.

## Project Structure

```
Boxing_signin/
│
├── app.py                    # Main Flask application
├── members.json              # Current members data
├── requested_members.json    # Pending membership requests
├── static/
│   └── images/
│       ├── join_membershipqrcode.jpeg
│       └── logo.jpg
└── templates/
    ├── admin.html            # Admin dashboard
    └── index.html            # Main sign-in and request page
```

### File Descriptions
- `app.py`: Main backend logic using Flask.
- `members.json`: Stores registered member data.
- `requested_members.json`: Stores pending membership requests.
- `static/images/`: Contains logo and QR code images.
- `templates/`: HTML templates for the user and admin interfaces.

## Customization
- Update `logo.jpg` and `join_membershipqrcode.jpeg` in `static/images/` to match your club branding.
- Modify HTML templates in `templates/` for custom UI/UX.

## License
This project is provided as-is for educational and club use. Please customize and extend as needed for your organization.
