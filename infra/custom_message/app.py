def lambda_handler(event, context):
    trigger = event["triggerSource"]
    user_email = event["request"]["userAttributes"].get("email", "Unknown email")

    brand_name = "MARP"
    brand_color = "#1A1A1A"  # Bold minimal dark tone
    accent_color = "#D72638" # A striking red accent for buttons or highlights

    def build_html_email(title, message, code=None):
        code_block = f"""
            <p style="font-size: 18px; font-weight: bold; color: {accent_color};">
                {code}
            </p>
        """ if code else ""

        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #F9F9F9; padding: 20px;">
                <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <h1 style="color: {brand_color}; font-size: 28px; margin-bottom: 10px;">{brand_name}</h1>
                    <h2 style="color: {brand_color}; font-size: 20px; margin-bottom: 20px;">{title}</h2>
                    <p style="color: #333; font-size: 16px; line-height: 1.5;">{message}</p>
                    {code_block}
                    <p style="margin-top: 30px; font-size: 12px; color: #888;">If you did not request this, please ignore this email.</p>
                </div>
            </body>
        </html>
        """

    if trigger == "CustomMessage_SignUp":
        event["response"]["emailSubject"] = f"Welcome to {brand_name}!"
        event["response"]["emailMessage"] = build_html_email(
            title="Verify Your Email",
            message=f"Hi {user_email},<br><br>Thanks for signing up. Please use this code to verify your account:",
            code=event['request']['codeParameter']
        )

    elif trigger == "CustomMessage_AdminCreateUser":
        event["response"]["emailSubject"] = f"You’ve been invited to {brand_name}"
        event["response"]["emailMessage"] = build_html_email(
            title="Your Account Invitation",
            message="Hello,<br><br>You have been invited to our Incident Reporting system. "
                    "Use the temporary password below to log in and set a new password:",
            code=event['request']['codeParameter']
        )

    elif trigger == "CustomMessage_ForgotPassword":
        event["response"]["emailSubject"] = f"{brand_name} - Password Reset"
        event["response"]["emailMessage"] = build_html_email(
            title="Password Reset Request",
            message="Hello,<br><br>Use this code to reset your password:",
            code=event['request']['codeParameter']
        )

    else:
        event["response"]["emailSubject"] = f"{brand_name} Notification"
        event["response"]["emailMessage"] = build_html_email(
            title="Notification",
            message="This is a default message."
        )

    return event
