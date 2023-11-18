import hashlib


# SHA224 hash of the contact_info
def generate_uuid(contact_info):
    hash_object = hashlib.sha224(contact_info.encode())
    generated_uuid = hash_object.hexdigest()
    return generated_uuid
