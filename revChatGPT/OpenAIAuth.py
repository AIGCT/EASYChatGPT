# Credits to github.com/rawandahmad698/PyChatGPT
import re
import urllib
import base64

import tls_client


class Debugger:
    def __init__(self, debug: bool = False):
        if debug:
            print("Debugger enabled on OpenAIAuth")
        self.debug = debug

    def set_debug(self, debug: bool):
        self.debug = debug

    def log(self, message: str, end: str = "\n"):
        if self.debug:
            print(message, end=end)


class OpenAIAuth:
    def __init__(
        self,
        email_address: str,
        password: str,
        use_proxy: bool = False,
        proxy: str = None,
        debug: bool = False,
        use_captcha: bool = True,
        captcha_solver: any = None
    ):
        self.session_token = None
        self.email_address = email_address
        self.password = password
        self.use_proxy = use_proxy
        self.proxy = proxy
        self.session = tls_client.Session(
            client_identifier="chrome_105"
        )
        self.access_token: str = None
        self.debugger = Debugger(debug)
        self.use_capcha = use_captcha
        self.captcha_solver: any = captcha_solver

    @staticmethod
    def url_encode(string: str) -> str:
        """
        URL encode a string
        :param string:
        :return:
        """
        return urllib.parse.quote(string)

    def begin(self) -> None:
        """
        Begin the auth process
        """
        self.debugger.log("Beginning auth process")
        if not self.email_address or not self.password:
            return

        if self.use_proxy:
            if not self.proxy:
                return

            proxies = {
                "http": self.proxy,
                "https": self.proxy,
            }
            self.session.proxies = proxies

        # First, make a request to https://chat.openai.com/auth/login
        url = "https://chat.openai.com/auth/login"
        headers = {
            "Host": "ask.openai.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        response = self.session.get(url=url, headers=headers)
        if response.status_code == 200:
            self.part_two()
        else:
            self.debugger.log("Error in part one")
            self.debugger.log("Response: ", end="")
            self.debugger.log(response.text)
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            raise Exception("API error")

    def part_two(self) -> None:
        """
        In part two, We make a request to https://chat.openai.com/api/auth/csrf and grab a fresh csrf token
        """
        self.debugger.log("Beginning part two")

        url = "https://chat.openai.com/api/auth/csrf"
        headers = {
            "Host": "ask.openai.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Referer": "https://chat.openai.com/auth/login",
            "Accept-Encoding": "gzip, deflate, br",
        }
        response = self.session.get(url=url, headers=headers)
        if response.status_code == 200 and "json" in response.headers["Content-Type"]:
            csrf_token = response.json()["csrfToken"]
            self.part_three(token=csrf_token)
        else:
            self.debugger.log("Error in part two")
            self.debugger.log("Response: ", end="")
            self.debugger.log(response.text)
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            raise Exception("Error logging in")

    def part_three(self, token: str) -> None:
        """
        We reuse the token from part to make a request to /api/auth/signin/auth0?prompt=login
        """
        self.debugger.log("Beginning part three")
        url = "https://chat.openai.com/api/auth/signin/auth0?prompt=login"

        payload = f"callbackUrl=%2F&csrfToken={token}&json=true"
        headers = {
            "Host": "ask.openai.com",
            "Origin": "https://chat.openai.com",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Referer": "https://chat.openai.com/auth/login",
            "Content-Length": "100",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = self.session.post(url=url, headers=headers, data=payload)
        if response.status_code == 200 and "json" in response.headers["Content-Type"]:
            url = response.json()["url"]
            if url == "https://chat.openai.com/api/auth/error?error=OAuthSignin" or 'error' in url:
                self.debugger.log("You have been rate limited")
                raise Exception("You have been rate limited.")
            self.part_four(url=url)
        elif response.status_code == 400:
            self.debugger.log("Error in part three")
            self.debugger.log("Invalid credentials")
            raise Exception("Invalid credentials")
        else:
            self.debugger.log("Error in part three")
            self.debugger.log("Response: ", end="")
            self.debugger.log(response.text)
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            raise Exception("Unknown error")

    def part_four(self, url: str) -> None:
        """
        We make a GET request to url
        :param url:
        :return:
        """
        self.debugger.log("Beginning part four")
        headers = {
            "Host": "auth0.openai.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://chat.openai.com/",
        }
        response = self.session.get(url=url, headers=headers)
        if response.status_code == 302:
            try:
                state = re.findall(r"state=(.*)", response.text)[0]
                state = state.split('"')[0]
                self.part_five(state=state)
            except IndexError as exc:
                self.debugger.log("Error in part four")
                self.debugger.log("Status code: ", end="")
                self.debugger.log(response.status_code)
                self.debugger.log("Rate limit hit")
                self.debugger.log("Response: " + str(response.text))
                raise Exception("Rate limit hit") from exc
        else:
            self.debugger.log("Error in part four")
            self.debugger.log("Response: ", end="")
            self.debugger.log(response.text)
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            self.debugger.log("Wrong response code")
            raise Exception("Unknown error")

    def part_five(self, state: str) -> None:
        """
        We use the state to get the login page & check for a captcha
        """
        self.debugger.log("Beginning part five")
        url = f"https://auth0.openai.com/u/login/identifier?state={state}"

        headers = {
            "Host": "auth0.openai.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://chat.openai.com/",
        }
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            captcha_code = None
            if re.search(r'<img[^>]+alt="captcha"[^>]+>', response.text):
                self.debugger.log("Captcha detected")
                if self.use_capcha == False:
                    self.debugger.log("Captcha detected but not used")
                    raise Exception("Captcha detected but not used")
                pattern = re.compile(
                    r'<img[^>]+alt="captcha"[^>]+src="(.+?)"[^>]+>')
                match = pattern.search(response.text)
                if match and self.captcha_solver:
                    captcha = match.group(1)
                    self.debugger.log("Captcha extracted")
                    # Save captcha (in JavaScript src format) to real svg file
                    captcha = captcha.replace("data:image/svg+xml;base64,", "")
                    # Convert base64 to svg
                    captcha = base64.b64decode(captcha)
                    captcha = captcha.decode("utf-8")
                    # Save captcha to file
                    captcha_code = self.captcha_solver.solve_captcha(
                        captcha)
                else:
                    self.debugger.log("Failed to find captcha")
                    raise ValueError("Captcha detected")
            self.part_six(state=state, captcha=captcha_code)
        else:
            self.debugger.log("Error in part five")
            self.debugger.log("Response: ", end="")
            self.debugger.log(response.text)
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            raise ValueError("Invalid response code")

    def part_six(self, state: str, captcha: str or None) -> None:
        """
        We make a POST request to the login page with the captcha, email
        :param state:
        :param captcha:
        :return:
        """
        self.debugger.log("Beginning part six")
        url = f"https://auth0.openai.com/u/login/identifier?state={state}"
        email_url_encoded = self.url_encode(self.email_address)
        payload = (
            f"state={state}&username={email_url_encoded}&captcha={captcha}&js-available=true&webauthn-available"
            f"=true&is-brave=false&webauthn-platform-available=true&action=default "
        )

        if captcha is None:
            payload = (
                f"state={state}&username={email_url_encoded}&js-available=false&webauthn-available=true&is"
                f"-brave=false&webauthn-platform-available=true&action=default "
            )

        headers = {
            "Host": "auth0.openai.com",
            "Origin": "https://auth0.openai.com",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Referer": f"https://auth0.openai.com/u/login/identifier?state={state}",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = self.session.post(url, headers=headers, data=payload)
        if response.status_code == 302:
            self.part_seven(state=state)
        else:
            self.debugger.log("Error in part six")
            self.debugger.log("Response: ", end="")
            self.debugger.log(response.text)
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            raise Exception("Unknown error")

    def part_seven(self, state: str) -> None:
        """
        We enter the password
        :param state:
        :return:
        """
        url = f"https://auth0.openai.com/u/login/password?state={state}"
        self.debugger.log("Beginning part seven")
        email_url_encoded = self.url_encode(self.email_address)
        password_url_encoded = self.url_encode(self.password)
        payload = f"state={state}&username={email_url_encoded}&password={password_url_encoded}&action=default"
        headers = {
            "Host": "auth0.openai.com",
            "Origin": "https://auth0.openai.com",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Referer": f"https://auth0.openai.com/u/login/password?state={state}",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            response = self.session.post(url, headers=headers, data=payload)
            self.debugger.log("Request went through")
        except Exception as exc:
            self.debugger.log("Error in part seven")
            self.debugger.log("Exception: ", end="")
            self.debugger.log(exc)
            raise Exception("Could not get response") from exc
        if response.status_code == 302:
            self.debugger.log("Response code is 302")
            try:
                new_state = re.findall(r"state=(.*)", response.text)[0]
                new_state = new_state.split('"')[0]
                self.debugger.log("New state found")
                self.part_eight(old_state=state, new_state=new_state)
            except Exception as exc:
                self.debugger.log("Error in part seven")
                self.debugger.log("Exception: ", end="")
                self.debugger.log(exc)
                raise Exception("State not found") from exc
        elif response.status_code == 400:
            self.debugger.log("Error in part seven")
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            raise Exception("Wrong email or password")
        else:
            self.debugger.log("Error in part seven")
            self.debugger.log("Status code: ", end="")
            self.debugger.log(response.status_code)
            raise Exception("Wrong status code")

    def part_eight(self, old_state: str, new_state) -> None:
        self.debugger.log("Beginning part eight")
        url = f"https://auth0.openai.com/authorize/resume?state={new_state}"
        headers = {
            "Host": "auth0.openai.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Referer": f"https://auth0.openai.com/u/login/password?state={old_state}",
        }
        response = self.session.get(url, headers=headers, allow_redirects=True)
        is_200 = response.status_code == 200
        if is_200:
            # Access Token
            access_token = re.findall(
                r"accessToken\":\"(.*)\"",
                response.text,
            )
            if access_token:
                try:
                    access_token = access_token[0]
                    access_token = access_token.split('"')[0]
                except Exception as e:
                    self.debugger.log("Error in part eight")
                    self.debugger.log("Response: ", end="")
                    self.debugger.log(response.text)
                    self.debugger.log("Status code: ", end="")
                    self.debugger.log(response.status_code)
                    raise e
            else:
                self.debugger.log("Error in part eight")
                self.debugger.log("Response: ", end="")
                self.debugger.log(response.text)
                self.debugger.log("Status code: ", end="")
                self.debugger.log(response.status_code)
                raise Exception("Auth0 did not issue an access token")
            self.part_nine()
        else:
            self.debugger.log("Incorrect response code in part eight")
            raise Exception("Incorrect response code")

    def save_access_token(self, access_token: str) -> None:
        """
        Save access_token and an hour from now on ./Classes/auth.json
        :param access_token:
        :return:
        """
        self.access_token = access_token

    def part_nine(self) -> bool:
        self.debugger.log("Beginning part nine")
        url = "https://chat.openai.com/api/auth/session"
        headers = {
            "Host": "ask.openai.com",
            "Connection": "keep-alive",
            "If-None-Match": '"bwc9mymkdm2"',
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/16.1 Safari/605.1.15",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Referer": "https://chat.openai.com/chat",
            "Accept-Encoding": "gzip, deflate, br",
        }
        response = self.session.get(url, headers=headers)
        is_200 = response.status_code == 200
        if is_200:
            # Get session token
            self.session_token = response.cookies.get(
                "__Secure-next-auth.session-token",
            )
            if 'json' in response.headers['Content-Type']:
                json_response = response.json()
                access_token = json_response['accessToken']
                self.save_access_token(access_token=access_token)
                self.debugger.log("SUCCESS")
                return True
            else:
                self.debugger.log(
                    "Please try again with a proxy (or use a new proxy if you are using one)")
        else:
            self.debugger.log(
                "Please try again with a proxy (or use a new proxy if you are using one)")
        self.session_token = None
        self.debugger.log("Failed to get session token")
        raise Exception("Failed to get session token")
