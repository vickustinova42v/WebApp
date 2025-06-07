from http.cookies import SimpleCookie

def get_logged_in_user(handler):
    if "Cookie" in handler.headers:
        cookie = SimpleCookie(handler.headers["Cookie"])
        if "user_id" in cookie:
            return cookie["user_id"].value
    return None
