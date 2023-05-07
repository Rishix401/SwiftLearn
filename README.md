# Swiftlearn e-learning platform README

Swiftlearn is an e-learning platform designed to help students learn online in a convenient and interactive way. This platform has been created using Django, JavaScript and Tailwind CSS to provide a responsive and user-friendly experience.

## **Distinctiveness and Complexity:**
Swiftlearn is distinct from previous projects because of the complexity of the features that it offers. Some of the features that set it apart include:

- Users can view featured courses or subscribe to the email list from the home page.
- The dashboard section allows users to track their course progress and access lectures they have enrolled in. Additionally, it provides recommendations for courses based on the categories of courses the user has purchased.
- The catalog page includes a filter section where users can filter courses based on different criteria such as subject, price, and status.
- The coupon system allows admin and staff members to create one-time, forever, or time-based use coupons for paid courses.
- Users can add notes, comment, and give a rating on lectures.
- The profile page enables users to view and edit their profile information.
- The login page features interactive animation and includes a "forgot password" button that, when clicked, sends an email to the user's registered email address to change their password.

## **How to Run the Application:**


Clone the repository to your local machine:

``` 
git clone https://github.com/<your-github-username>/Swiftlearn.git 
```

Create a virtual environment:

``` 
python3 -m venv env 
```
activate the venv (Windows):
```
env\Scripts\activate.bat
```
activate the venv (Linux):
```
source env/bin/activate 
```

Install the requirements:

```
pip install -r requirements.txt
```


Run the server:
```
python manage.py runserver
```

**Note:** You can log in using the superuser account with the following credentials: username **'admin'** and password **'password'**.

Open your browser and go to the following URL: http://localhost:8000/

## **How to make payments works:**

To enable Stripe payments, you need to follow these steps:

- Rename the .env.example file to .env.

- Obtain your Stripe API keys by creating a Stripe account and navigating to the API Keys section in your dashboard. 

- You will need the STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY variables for the payment process.

- Generate a Stripe webhook secret by creating a webhook endpoint in the Stripe dashboard and copying the "Signing secret" value. Set this value as the STRIPE_WEBHOOK_SECRET variable in the .env file.

- Install the Stripe CLI on your computer.

- Login to your Stripe account using the CLI by typing ```stripe login``` in the terminal and following the prompts.

- Use the CLI to create a webhook endpoint on your local machine by typing 
```stripe listen --forward-to localhost:8000/webhooks/stripe```.
This will allow Stripe to send payment confirmation messages to your website.

**Note:** Admin or staff members can create coupons for discounts on paid courses. These coupons can be used for a limited time or indefinitely. To apply a coupon, users can enter the coupon code during the payment process.
