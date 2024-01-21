import time


def list_contacts(contacts):
    time.sleep(1)
    for index, contact in enumerate(contacts):
        contact_info = contact.split(",")
        if len(contact_info) < 5:  # Check if there are enough elements in contact_info
            continue

        # if contact_info[x] is empty or does not exist, we set contact_name to N/A
        contact_name = "N/A" if (not contact_info or contact_info[0] == "") else contact_info[0]
        contact_first_name = "N/A" if (not contact_info or contact_info[1] == "") else contact_info[1]
        contact_email = "N/A" if (not contact_info or contact_info[2] == "") else contact_info[2]
        contact_phone = "N/A" if (not contact_info or contact_info[3] == "") else contact_info[3]
        contact_address = "N/A" if (not contact_info or contact_info[4] == "") else contact_info[4]

        print(
            f"{index + 1}. Nom: {contact_name.strip()} | Prenom: {contact_first_name.strip()} | Email: {contact_email.strip()} | Tel: {contact_phone.strip()} | Adresse: {contact_address.strip()}")
