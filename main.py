from telegram import send_message


print("CROUS Hunter démarre !")

message = """
🤖 CROUS Alert Perso

✅ Connexion réussie !

Nel-Crous-Bot est opérationnel.
La surveillance des logements CROUS Montpellier va bientôt commencer.
"""

send_message(message)

print("Message Telegram envoyé !")
