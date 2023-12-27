import random
# from hashids import Hashids

# hashids = Hashids(salt="your_salt_here", min_length=8)

# def encoded_id(id):
#         return hashids.encode(id)

# def decode_id(encoded_id):
#         decoded_ids = hashids.decode(encoded_id)
#         if decoded_ids:
#             return decoded_ids[0]  # Assuming there's only one ID in the list
#         return None


def otp_generator():
    return str(random.randint(1000, 9999))

