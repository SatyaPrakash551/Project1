import bcrypt
def hashedPassword(password : str):
    password_byte = password.encode('utf-8')
    salt = bcrypt.gensalt(12)
    return  bcrypt.hashpw(password_byte,salt).decode('utf-8')

def decryptPassword(password:str,hashed_pass : str):
    password_byte = password.encode('utf-8')
    hashed_pass_byte = hashed_pass.encode('utf-8')
    return bcrypt.checkpw(password_byte,hashed_pass_byte)   