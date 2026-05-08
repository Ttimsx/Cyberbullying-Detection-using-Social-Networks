from ml_model import CyberbullyingModel
from user_registration import setup_database, register_user, get_parent_email
from email_service import send_email

def main():
    setup_database()

    model = CyberbullyingModel()
    model.train_model()

    choice = input("Do you want to register? (yes/no): ").lower()
    if choice == "yes":
        register_user()

    username = input("Enter your registered username: ")
    parent_email = get_parent_email(username)
    if not parent_email:
        print("❌ User not found. Please register first.")
        return

    print("\nType a sentence to detect cyberbullying (type 'exit' to quit):")
    while True:
        user_input = input(">> ")
        if user_input.lower() == 'exit':
            break
        prediction = model.predict(user_input)
        label = 'Cyberbullying' if prediction == 1 else 'Non-Cyberbullying'
        print(f"Prediction: {label}")

        if prediction == 1:
            subject = "⚠️ Cyberbullying Alert"
            message = f"Dear Parent,\n\nThe system detected a cyberbullying message from '{username}':\n\n\"{user_input}\""
            send_email(parent_email, subject, message)

if __name__ == "__main__":
    main()
