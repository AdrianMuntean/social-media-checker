import config

login_ids = {'linkedin': {'email': 'login-email', 'password': 'login-password', 'submit': 'login-submit'},
             'facebook': {'email': 'email', 'password': 'pass', 'submit': 'loginbutton'}}


def login(browser, site):
    browser.find_element_by_id(login_ids[site]['email']).send_keys(config.credentials[site]['email'])
    browser.find_element_by_id(login_ids[site]['password']).send_keys(config.credentials[site]['password'])
    browser.find_element_by_id(login_ids[site]['submit']).click()


def parse_text(text):
    return "".join(set(text.split('\n')))
