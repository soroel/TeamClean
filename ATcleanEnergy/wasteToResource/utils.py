import africastalking



def send_sms_notification(phone_number, message):
    username = "miabritacreation"
    api_key = "atsk_3554501a42f3f1f1448d93ff830158014916064ff660ee2b98611960388b58db9103fb2d"
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

    try:
        response = sms.send(message, [phone_number])
        print("SMS API Response:", response)  # Log the response for debugging
        return response
    except Exception as e:
        print(f"Error while sending SMS: {str(e)}")
        return None