from weather_api_service import db, secret_key, encrypt, decrypt
import User_model as model



def validate_user_credentials(user_name: str, password: str) -> (int, str, dict):
    status = 401
    message = 'Incorrect username or password'
    user = None
    try:
        user_obj = (
            db.session.query(model.UserModel)
            .filter(model.UserModel.username == user_name)
            .first()
        )
        if user_obj:
            entered_password_enc = encrypt(secret_key=secret_key, plain_text=password)
            if entered_password_enc == user_obj.password:
                status = 200
                message = 'User successfully authenticated'
                user = {
                    'user_name': user_obj.username, 'first_name': user_obj.full_name
                }
        else:
            message = 'Invalid username or password'
            status = 500
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, user

def countrylist():
    status = 401
    message = ''
    obj = None
    try:
        obj = (
            db.session.query(model.DataModel.country).all()
        )
        status =200
        message = 'country list generated'
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, obj
    
def citylist():
    status = 401
    message = ''
    obj = None
    try:
        obj = (
            db.session.query(model.DataModel.city).all()
        )
        status =200
        message = 'city list generated'
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, obj