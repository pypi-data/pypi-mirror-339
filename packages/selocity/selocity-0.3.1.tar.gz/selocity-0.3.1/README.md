# Selocity

**Selocity** is a Python library that enhances Selenium's reliability by automatically handling stale elements. With its caching decorators and proxy-based approach, your Selenium tests become more robust and less prone to flakiness caused by dynamic web pages.

## Features

- **Automatic Re-Fetching:** Seamlessly recovers from `StaleElementReferenceException` by re-fetching WebElements.
- **Decorators for Caching:** Use `@resilient_cached_webelement` and `@resilient_cached_webelements` to cache elements or lists of elements.
- **Proxy-Based Wrapping:** Every WebElement is wrapped in a proxy that logs attribute accesses and method calls.
- **Retry Mechanism:** Uses a polling strategy with configurable intervals and timeouts to ensure element stability.

## Installation

Install Selocity directly from our GitLab artifact repository. You can add the following to your `requirements.txt`:

```txt
--extra-index-url https://gitlab.developers.cam.ac.uk/api/v4/projects/10297/packages/pypi/simple

selocity==0.2.0
```

Or install it via pip:

```bash
pip install git+https://gitlab.developers.cam.ac.uk/uis/qa/selocity.git#egg=selocity
```

## Usage

Selocity provides two main decorators:

- `@resilient_cached_webelement`
  Caches a single `WebElement`. If the element becomes stale, the proxy automatically re-fetches and updates the cached reference.
- `@resilient_cached_webelements`
  Caches a list of `WebElement`s and re-fetches them if any element in the list becomes stale.

### How They Work

1. **Caching on First Access:**
   When you first access a decorated element method, the library attempts to fetch the element. If it isn’t immediately available (raising a `NoSuchElementException`), it retries until the element is found or a timeout is reached.

2. **Proxy Wrapping:**
   The fetched element is wrapped in a proxy object. This proxy intercepts all attribute accesses and method calls.

3. **Automatic Recovery:**
   If a `StaleElementReferenceException` is encountered during any operation, the proxy uses the original locator function to re-fetch the element, ensuring that your tests continue running smoothly.

4. **Logging and Debugging:**
   Detailed logs help you understand when and why elements are being re-fetched, which aids in debugging flaky tests.

### Benefits

- **Improved Test Stability:** Automatically handles dynamic changes in the DOM.
- **Reduced Flakiness:** Ensures that transient issues with stale elements don’t break your tests.
- **Seamless POM Integration:** Easily integrate with your Page Object Model (POM) without significant code changes.
- **Efficient Error Recovery:** Retries operations with a built-in polling mechanism, making your tests more resilient.

## Example: Basic Page Object Model (POM)

Below is a simple example showing how to use the decorators in a basic POM structure:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selocity import resilient_cached_webelement, resilient_cached_webelements

class BasePage:
    def __init__(self, driver):
        self.driver = driver

class LoginPage(BasePage):
    @property
    @resilient_cached_webelement
    def username_input(self) -> WebElement:
        return self.driver.find_element(By.ID, "username")

    @property
    @resilient_cached_webelement
    def password_input(self) -> WebElement:
        return self.driver.find_element(By.ID, "password")

    @property
    @resilient_cached_webelement
    def submit_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    def login(self, username: str, password: str):
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.submit_button.click()
```

Usage in your test code:

```python
from selenium import webdriver

def test_login():
    driver = webdriver.Chrome()
    login_page = LoginPage(driver)
    login_page.login("myusername", "mypassword")
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests on our GitLab repository.

## Contact

For questions or support, please contact **jsa34@cam.ac.uk**
