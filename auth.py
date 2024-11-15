import undetected_chromedriver as uc
import time

bearer_token = None
cookie_auth = None

def get_auth():
    global cookie_auth, bearer_token
    auth_url = "https://discord.com/oauth2/authorize?client_id=1206918887426494495&redirect_uri=https%3A%2F%2Flogs.flashbackfa.fr&response_type=code&scope=identify%20email"
    driver = uc.Chrome()
    driver.get(auth_url)

    # Vérifier que l'utilisateur est bien redirigé sur l'URL cible
    redirect_url = "https://logs.flashbackfa.fr"
    max_wait_time = 60  # Temps maximum d'attente en secondes
    wait_interval = 3  # Intervalle de vérification en secondes

    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        current_url = driver.current_url
        if current_url.startswith(redirect_url):
            print("Redirection réussie vers l'URL cible.")
            break
        time.sleep(wait_interval)
    else:
        print("Erreur : Redirection vers l'URL cible non détectée.")
        driver.quit()
        return None

    # Réessayer la récupération du token jusqu'à un nombre maximum de tentatives
    max_attempts = 10  # Nombre maximum de tentatives
    attempt = 0


    while attempt < max_attempts and not bearer_token:
        bearer_token = driver.execute_script("return localStorage.getItem('token');")
        attempt += 1
        if bearer_token:
            print(f"Token Bearer récupéré à la tentative {attempt}: {bearer_token}")
        else:
            print(f"Tentative {attempt} : Token non trouvé, réessayer...")
        time.sleep(3)  # Pause entre les tentatives

    attempt = 0
    while attempt < max_attempts and not cookie_auth:
        cookie = driver.get_cookie("cf_clearance")
        if cookie:
            cookie_auth = cookie['value']
        attempt += 1
        if cookie_auth:
            print(f"Cookie récupéré à la tentative {attempt}: {cookie_auth}")
        else:
            print(f"Tentative {attempt} : Token non trouvé, réessayer...")
        time.sleep(3)

    # Fermer le navigateur
    driver.quit()

    # Vérifier si le token a été récupéré après toutes les tentatives
    if not bearer_token:
        print("Erreur : Impossible de récupérer le token après plusieurs tentatives.")
    if not cookie_auth:
        print("Erreur : Impossible de récupérer le cookie après plusieurs tentatives.")


# Appel de la fonction
get_auth()
print("Token d'accès (Bearer token) :" + str(bearer_token))
print("Cookie d'accès:" + cookie_auth)