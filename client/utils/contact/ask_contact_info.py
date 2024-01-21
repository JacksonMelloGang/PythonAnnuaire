def ask_contact_information():
    print("Veuillez entrer les informations du contact")
    name = input("Nom*: ").strip()
    first_name = input("Prénom*: ").strip()
    email = input("Email*: ").strip()
    phone = input("Téléphone: ").strip()
    address = input("Adresse: ").strip()
    contact = {"name": name, "first_name": first_name, "email": email, "phone": phone, "address": address}

    if (name == "" or first_name == "" or email == ""):
        print("Les champs marqués d'un * sont obligatoires")
        ask_contact_information()

    if (len(phone) == 0 or phone == ""):
        contact[phone] = "N/A"

    if (len(address) == 0 or address == ""):
        contact[address] = "N/A"

    return contact
