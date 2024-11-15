import auth

authorization_code = ""


if __name__ == '__main__':
    authorization_code = auth.get_discord_token()
    print(authorization_code)