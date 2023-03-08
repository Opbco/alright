from alright import WhatsApp
import random

messenger = WhatsApp()

#messages_replied = ['Welcome sir', 'Good day, How can we help?', 'I like it!!!', 'Dossier encours de traitement', 'Welcom to MINESEC Administration How can we help?']

while True:
    unread_chats = messenger.fetch_all_unread_chats(limit=True, top=100)

    if len(unread_chats) < 1:
        try:
            message_received = messenger.get_last_message_active_chat()
            if message_received:
                if not message_received["out"]:
                    result = messenger.choix_menu(message_received["message"])
                    messenger.send_message(result["message"])
        except Exception as e:
            messenger.send_message("Erreur system please try again later")
            print(e)

    for chat in unread_chats:
        if not chat["group"]:
            messenger.find_by_username(chat["sender"])
            try:
                message_received = messenger.get_last_message_received(chat["sender"])
                result = messenger.choix_menu(message_received["message"])
                messenger.send_message(result["message"])
            except Exception as e:
                messenger.send_message("Erreur system please try again later")
                print(e)
            finally:
                messenger.clear_search_box()

            """ message_sent = messenger.get_last_message_sent()
            if message_sent is None:
                messenger.send_message("Welcom to MINESEC Administration How can we help?")
            elif message_sent['message'] not in messages_replied:
                messenger.send_message("Welcom to MINESEC Administration How can we help?")
            else: """
            
# messenger.close_when_message_successfully_sent()
