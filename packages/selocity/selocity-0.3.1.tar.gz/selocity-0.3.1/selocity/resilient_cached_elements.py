import logging
import time
from functools import partial

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

LOGGER = logging.getLogger(__name__)

POLL_INTERVAL = 0.5  # Interval between retries
DEFAULT_TIMEOUT = 5  # Maximum time to retry fetching the element


class ObjectProxy:
    """A simple proxy that delegates all operations to the wrapped object."""

    def __init__(self, wrapped):
        self.__wrapped__ = wrapped

    @property
    def __class__(self):
        return self.__wrapped__.__class__

    @__class__.setter
    def __class__(self, value):  # noqa: F811
        self.__wrapped__.__class__ = value

    def __getattr__(self, name):
        return getattr(self.__wrapped__, name)

    def __repr__(self):
        return repr(self.__wrapped__)


class WebElementProxy(ObjectProxy):
    """
    A proxy for WebElement that logs every attribute access,
    handles StaleElementReferenceException by re-fetching,
    and retries the original method.
    """

    def __init__(self, element, owner, attr_name, fetch_func):
        super().__init__(element)
        self._owner = owner
        self._attr_name = attr_name
        self._fetch_func = fetch_func

    def __getattr__(self, name):
        try:
            # Try to get the attribute from the wrapped element.
            result = getattr(self.__wrapped__, name)
        except StaleElementReferenceException:
            LOGGER.warning(
                f"StaleElementReferenceException on '{self._attr_name}' for {id(self._owner)}"
            )
            refreshed_proxy = self._handle_stale_element()
            if refreshed_proxy is None:
                raise
            # Immediately return the attribute from the refreshed element.
            return getattr(refreshed_proxy, name)

        LOGGER.debug(
            f"Intercepted access to '{name}' on '{self._attr_name}' for '{id(self._owner)}'."
        )
        # If the attribute is callable, wrap it so that its calls are resilient.
        if callable(result):
            return self._method_wrapper(result, name)
        else:
            return result

    def _method_wrapper(self, method, method_name):
        """
        Wraps a method so that if a StaleElementReferenceException occurs,
        it re-fetches the element, updates the cache, and retries the method.
        """

        def wrapped(*args, **kwargs):
            try:
                LOGGER.debug(
                    f"Calling method {method_name} on '{self._attr_name}' for '{id(self._owner)}'"
                )
                return method(*args, **kwargs)

            except StaleElementReferenceException:
                LOGGER.warning(
                    f"StaleElementReferenceException during '{method_name}' on '{self._attr_name}'"
                )
                if new_element := self._handle_stale_element():
                    return getattr(new_element, method_name)(*args, **kwargs)
                raise

        return wrapped

    def _handle_stale_element(self):
        """
        Re-fetches the element with polling to ensure stability.
        Returns the new proxy only if the last two fetches match.
        """
        LOGGER.debug(f"Handling stale element for '{self._attr_name}'. Re-fetching...")

        start_time = time.time()

        while time.time() - start_time < DEFAULT_TIMEOUT:
            try:
                new_element: WebElement = self._fetch_func()
                time.sleep(POLL_INTERVAL)  # Wait before checking if element is stable
                new_element.is_displayed()
                LOGGER.debug(f"Element '{self._attr_name}' stabilized, updating proxy.")
                new_proxy = WebElementProxy(
                    new_element, self._owner, self._attr_name, self._fetch_func
                )
                setattr(self._owner, self._attr_name, new_proxy)
                return new_proxy

            except StaleElementReferenceException:
                LOGGER.warning(
                    f"Still encountering stale element for '{self._attr_name}', retrying..."
                )

            except Exception as e:
                LOGGER.error(f"Failed to refresh element '{self._attr_name}': {e}")
                break  # Exit if an unexpected error occurs

        LOGGER.error(f"Timeout reached while refetching element '{self._attr_name}'.")
        return None


class WebElementListProxy:
    """A proxy for a list of WebElements that re-fetches stale elements automatically."""

    def __init__(self, elements, owner, attr_name, fetch_func):
        self._owner = owner
        self._attr_name = attr_name
        self._fetch_func = fetch_func
        self._elements = [
            WebElementProxy(el, owner, f"{attr_name}[{i}]", lambda i=i: self._fetch_func()[i])
            for i, el in enumerate(elements)
        ]

    def __getitem__(self, index):
        try:
            return self._elements[index]
        except IndexError:
            raise IndexError(f"Index {index} out of range for '{self._attr_name}'")

    def __iter__(self):
        return iter(self._elements)

    def __len__(self):
        return len(self._elements)

    def __repr__(self):
        return repr(self._elements)

    def _handle_stale_list(self):
        """Re-fetches the entire list with polling until the last two fetches match."""
        LOGGER.debug(f"Re-fetching stale list '{self._attr_name}' for '{id(self._owner)}'...")

        start_time = time.time()
        last_fetched = self._elements.copy()

        while time.time() - start_time < DEFAULT_TIMEOUT:
            try:
                new_elements = self._fetch_func()

                def lists_have_same_ids():
                    new_ids = {el.id for el in new_elements}
                    last_ids = {el.id for el in last_fetched}
                    return new_ids == last_ids

                if lists_have_same_ids():
                    LOGGER.debug(f"List '{self._attr_name}' stabilized, updating proxies.")

                    def create_proxy(index, element):
                        return WebElementProxy(
                            element,
                            self._owner,
                            f"{self._attr_name}[{index}]",
                            lambda: new_elements[index],
                        )

                    self._elements = [create_proxy(i, el) for i, el in enumerate(new_elements)]
                    return

                last_fetched = new_elements
                time.sleep(POLL_INTERVAL)  # Wait before next attempt if needed

            except StaleElementReferenceException:
                LOGGER.warning(
                    f"Still encountering stale elements in '{self._attr_name}', retrying..."
                )

            except Exception as e:
                LOGGER.error(f"Failed to refresh list '{self._attr_name}': {e}")
                break  # Exit on unexpected error

        LOGGER.error(f"Timeout reached while refetching list '{self._attr_name}'.")
        self._elements = []


def resilient_cached_webelement(func):
    """Decorator to cache a WebElement and re-fetch it if stale.

    It waits until the element exists if NoSuchElementException is raised.
    """
    attr_name = f"_cached_{func.__name__}"

    def wrapper(self):
        if not hasattr(self, attr_name):
            LOGGER.debug(f"Setting {attr_name} for {id(self)}")
            start_time = time.time()
            while True:
                try:
                    # Try to fetch the element
                    element = func(self)
                    break
                except NoSuchElementException as e:
                    if time.time() - start_time > DEFAULT_TIMEOUT:
                        LOGGER.error(f"Timeout reached while waiting for element in {attr_name}.")
                        raise e
                    time.sleep(POLL_INTERVAL)
            # Create a fetch function using partial so that the proxy can re-fetch later
            fetch_func = partial(func, self)
            proxy = WebElementProxy(element, self, attr_name, fetch_func)
            setattr(self, attr_name, proxy)
        else:
            LOGGER.debug(f"Cache hit for {attr_name} for {id(self)}")

        return getattr(self, attr_name)

    return wrapper


def resilient_cached_webelements(func):
    """Decorator to cache a list of WebElements and re-fetch them if stale.

    It waits until the list of elements exists if NoSuchElementException is raised.
    """
    attr_name = f"_cached_{func.__name__}"

    def wrapper(self):
        if not hasattr(self, attr_name):
            LOGGER.debug(f"Setting {attr_name} for {id(self)}")
            start_time = time.time()
            while True:
                try:
                    # Try to fetch the list of elements
                    elements = func(self)
                    break
                except NoSuchElementException as e:
                    if time.time() - start_time > DEFAULT_TIMEOUT:
                        LOGGER.error(
                            f"Timeout reached while waiting for element list in {attr_name}."
                        )
                        raise e
                    time.sleep(POLL_INTERVAL)
            fetch_func = partial(func, self)
            proxy = WebElementListProxy(elements, self, attr_name, fetch_func)
            setattr(self, attr_name, proxy)
        else:
            LOGGER.debug(f"Cache hit for {attr_name} for {id(self)}")

        return getattr(self, attr_name)

    return wrapper
