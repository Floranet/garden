================================================================================
                            🌱  FLORANET
              Django-Based Gardening Community Platform
          BCA Final Year Project | Python • Django • Razorpay • Render
================================================================================

Floranet is a Django-based gardening community platform designed to connect
users, gardening experts, and shops. It provides educational resources,
shopping features, and community interaction in one place.

--------------------------------------------------------------------------------
🚀 FEATURES
--------------------------------------------------------------------------------

👤 User Module
  • User registration & login
  • Profile management
  • View shops and products

👨‍🏫 Professor Module
  • Upload gardening videos (vdo.html)
  • Manage personal profile (profProfile.html)
  • Provide educational resources

🛒 Shop & Product Module
  • Add and manage shops
  • Add gardening products
  • Browse shop list (shoplist.html, user_shoplist.html)
  • Cart system (cart_list.html)

💳 Payment System
  • Razorpay integration
  • Payment success/failure pages
  • Invoice generation

🌿 Community Features
  • Gardening resources (resource_list.html)
  • Educational content (edu.html)
  • Chat system (chat.html)
  • Feedback & ratings

⏰ Task & Reminder System
  • Task list (tasklist.html)
  • Reminder management (reminders.html)
  • Calendar view (calendar.html)

--------------------------------------------------------------------------------
🛠️ TECH STACK
--------------------------------------------------------------------------------

  Backend          : Python, Django
  Frontend         : HTML, CSS, JavaScript
  Database         : SQLite
  Async Tasks      : Celery
  Payment Gateway  : Razorpay
  Deployment       : Render

--------------------------------------------------------------------------------
📂 PROJECT STRUCTURE
--------------------------------------------------------------------------------

  Floranet/
  │── garden_app/          # Main Django app
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   ├── forms.py
  │   ├── tasks.py
  │   ├── templates/
  │   └── static/
  │── assets/              # Static assets
  │── media/               # Uploaded files (images/videos)
  │── env/                 # Virtual environment
  │── manage.py
  │── db.sqlite3
  └── requirements.txt

--------------------------------------------------------------------------------
⚙️ INSTALLATION & SETUP
--------------------------------------------------------------------------------

1. Clone Repository
   git clone https://github.com/your-username/floranet.git
   cd floranet

2. Create Virtual Environment
   python -m venv env
   source env/bin/activate       # Windows: env\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Run Migrations
   python manage.py migrate

5. Start Server
   python manage.py runserver

   Visit: http://127.0.0.1:8000/

--------------------------------------------------------------------------------
🔑 ENVIRONMENT VARIABLES
--------------------------------------------------------------------------------

  Create a .env file in the project root:

  SECRET_KEY=your_secret_key
  DEBUG=True
  RAZORPAY_KEY_ID=your_key
  RAZORPAY_KEY_SECRET=your_secret

--------------------------------------------------------------------------------
📸 KEY PAGES
--------------------------------------------------------------------------------

  🏠 Homepage            →  index.html
  🛒 Shop List           →  shoplist.html
  👤 User Dashboard      →  userHome.html
  👨‍🏫 Professor Dashboard →  profhome.html
  🎥 Video Upload        →  vdo.html
  💳 Payment             →  payment.html

--------------------------------------------------------------------------------
🔮 FUTURE ENHANCEMENTS
--------------------------------------------------------------------------------

  • Advanced shop filtering (category + location)
  • Fully responsive UI improvements
  • Smart notifications for reminders
  • Reviews & ratings for shops/products

--------------------------------------------------------------------------------
🤝 CONTRIBUTING
--------------------------------------------------------------------------------

  1. Fork the repository
  2. Create your feature branch
  3. Commit your changes
  4. Submit a pull request

--------------------------------------------------------------------------------
📄 LICENSE
--------------------------------------------------------------------------------

  This project is licensed under the MIT License.

--------------------------------------------------------------------------------
👨‍💻 AUTHORS
--------------------------------------------------------------------------------

  Drisya C C  |  Surya M S  |  Siyana Fathima  |  Laya M A

  BCA Final Year Project — Floranet 🌱

================================================================================
