import asyncio
import json
import logging
from contextlib import asynccontextmanager
from functools import partial
from pathlib import Path
from typing import List, Optional, Tuple, Union

import aiofiles

from pydoll.commands import (
    DomCommands,
    FetchCommands,
    NetworkCommands,
    PageCommands,
    RuntimeCommands,
    StorageCommands,
)
from pydoll.connection.connection import ConnectionHandler
from pydoll.constants import By
from pydoll.element import WebElement
from pydoll.events import PageEvents
from pydoll.exceptions import InvalidFileExtension
from pydoll.mixins.find_elements import FindElementsMixin
from pydoll.utils import decode_image_to_bytes

logger = logging.getLogger(__name__)


class Page(FindElementsMixin):  # noqa: PLR0904
    def __init__(self, connection_port: int, page_id: str):
        """
        Initializes the Page instance.

        Args:
            connection_port (int): The port number for the connection to the
                browser.
            page_id (str): The ID of the page, obtained via the DevTools
                Protocol.
        """
        self._connection_handler = ConnectionHandler(connection_port, page_id)
        self._page_events_enabled = False
        self._network_events_enabled = False
        self._fetch_events_enabled = False
        self._dom_events_enabled = False
        self._intercept_file_chooser_dialog_enabled = False
        self._cloudflare_captcha_callback_id = None

    @property
    def page_events_enabled(self) -> bool:
        """
        Returns whether page events are enabled or not.

        Returns:
            bool: True if page events are enabled, False otherwise.
        """
        return self._page_events_enabled

    @property
    def network_events_enabled(self) -> bool:
        """
        Returns whether network events are enabled or not.

        Returns:
            bool: True if network events are enabled, False otherwise.
        """
        return self._network_events_enabled

    @property
    def fetch_events_enabled(self) -> bool:
        """
        Returns whether fetch events are enabled or not.

        Returns:
            bool: True if fetch events are enabled, False otherwise.
        """
        return self._fetch_events_enabled

    @property
    def dom_events_enabled(self) -> bool:
        """
        Returns whether DOM events are enabled or not.

        Returns:
            bool: True if DOM events are enabled, False otherwise.
        """
        return self._dom_events_enabled

    @property
    def intercept_file_chooser_dialog_enabled(self) -> bool:
        """
        Returns whether file chooser dialogs are being intercepted or not.

        Returns:
            bool: True if file chooser dialogs are being intercepted,
                False otherwise.
        """
        return self._intercept_file_chooser_dialog_enabled

    @property
    async def current_url(self) -> str:
        """
        Retrieves the current URL of the page.

        Returns:
            str: The current URL of the page.
        """
        response = await self._execute_command(DomCommands.get_current_url())
        return response['result']['result']['value']

    @property
    async def page_source(self) -> str:
        """
        Retrieves the source code of the page.

        Returns:
            str: The source code of the page.

        """
        response = await self._execute_command(
            RuntimeCommands.evaluate_script(
                'document.documentElement.outerHTML'
            )
        )
        return response['result']['result']['value']

    async def close(self):
        """
        Closes the page.

        This method closes the current page in the browser.

        Returns:
            None
        """
        await self._execute_command(PageCommands.close())

    async def get_cookies(self) -> list[dict]:
        """
        Retrieves the cookies of the page.

        Returns:
            list[dict]: A list of dictionaries containing cookie data from
                the current page.
        """
        response = await self._execute_command(
            NetworkCommands.get_all_cookies()
        )
        return response['result']['cookies']

    async def set_cookies(self, cookies: list[dict]):
        """
        Sets cookies for the page.

        Args:
            cookies (list[dict]): A list of dictionaries containing cookie
                data to set for the current page.
        """
        await self._execute_command(StorageCommands.set_cookies(cookies))
        await self._execute_command(NetworkCommands.set_cookies(cookies))

    async def delete_all_cookies(self):
        """
        Deletes all cookies from the browser.

        This clears both storage cookies and browser cookies associated with
        the current page.

        Returns:
            None
        """
        await self._execute_command(StorageCommands.clear_cookies())
        await self._execute_command(NetworkCommands.clear_browser_cookies())

    async def has_dialog(self) -> bool:
        """
        Checks if a dialog is present on the page.

        Returns:
            bool: True if a dialog is present, False otherwise.
        """
        if self._connection_handler.dialog:
            return True

        return False

    async def get_dialog_message(self) -> str:
        """
        Retrieves the message of the dialog on the page.

        Returns:
            str: The message of the dialog.
        """
        if not await self.has_dialog():
            raise LookupError('No dialog present on the page')
        return self._connection_handler.dialog['params']['message']

    async def accept_dialog(self):
        """
        Accepts the dialog on the page.

        Raises:
            LookupError: If no dialog is present on the page.
        """
        if not await self.has_dialog():
            raise LookupError('No dialog present on the page')
        await self._execute_command(PageCommands.handle_dialog(True))

    async def go_to(self, url: str, timeout=300):
        """
        Navigates to a URL in the page.

        Args:
            url (str): The URL to navigate to.
            timeout (int): Maximum time in seconds to wait for page to load.
                Defaults to 300 seconds.

        Raises:
            TimeoutError: If the page fails to load within the specified
                timeout.
        """
        if await self._refresh_if_url_not_changed(url):
            return

        await self._execute_command(PageCommands.go_to(url))

        try:
            await self._wait_page_load(timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError('Page load timed out')

    async def refresh(self):
        """
        Refreshes the page.

        This method reloads the current page and waits for it to finish
        loading.

        Raises:
            TimeoutError: If the page does not finish loading within the
                default timeout period (300 seconds).

        Returns:
            None
        """
        await self._execute_command(PageCommands.refresh())
        try:
            await self._wait_page_load()
        except asyncio.TimeoutError:
            raise TimeoutError('Page load timed out')

    async def get_screenshot(self, path: str):
        """
        Captures a screenshot of the page.

        Args:
            path (str): The file path to save the screenshot to.

        Returns:
            None
        """
        fmt = path.split('.')[-1]
        if fmt not in {'jpeg', 'jpg', 'png'}:
            raise InvalidFileExtension(f'{fmt} extension is not supported.')

        response = await self._execute_command(
            PageCommands.screenshot(fmt=fmt)
        )
        screenshot_b64 = response['result']['data'].encode('utf-8')
        screenshot_bytes = decode_image_to_bytes(screenshot_b64)
        async with aiofiles.open(path, 'wb') as file:
            await file.write(screenshot_bytes)

    async def get_screenshot_base64(self):
        """
        Retrieves the screenshot of the page as a base64 encoded string.

        Returns:
            str: The base64 encoded screenshot.

        # TODO: remove the duplicated logic
        """
        response = await self._execute_command(PageCommands.screenshot())
        return response['result']['data']

    async def set_download_path(self, path: str):
        """
        Sets the download path for the page.

        Args:
            path (str): The path where the downloaded files should be saved.
        """
        await self._execute_command(PageCommands.set_download_path(path))

    async def get_pdf_base64(self):
        """
        Retrieves the PDF data of the page.

        Returns:
            str: The PDF data of the page.
        """
        response = await self._execute_command(PageCommands.print_to_pdf())
        return response['result']['data']

    async def print_to_pdf(self, path: str):
        """
        Prints the page to a PDF file.

        Args:
            path (str): The file path to save the PDF file to.
        """
        response = await self._execute_command(PageCommands.print_to_pdf())
        pdf_b64 = response['result']['data'].encode('utf-8')
        pdf_bytes = decode_image_to_bytes(pdf_b64)
        async with aiofiles.open(path, 'wb') as file:
            await file.write(pdf_bytes)

    async def get_network_logs(self, matches: list[str] = []):
        """
        Retrieves network logs from the page.

        Args:
            matches (list[str]): A list of URL patterns to match network logs
                against. If empty, all logs are returned.

        Returns:
            list: A list of network logs that match the specified patterns.

        Raises:
            LookupError: If no network logs match the specified patterns.
        """
        network_logs = self._connection_handler.network_logs
        logs_matched = []
        for log in network_logs:
            if not log.get('params', {}).get('request', {}).get('url'):
                continue
            for match in matches:
                if match in log['params']['request']['url']:
                    logs_matched.append(log)
                    break

        if not logs_matched:
            raise LookupError('No network logs matched the specified pattern')

        return logs_matched

    async def get_network_response_bodies(self, matches: list[str] = []):
        """
        Retrieves the response bodies of network requests that match the
        specified pattern.

        Args:
            matches (list): The URL patterns to match network requests against.

        Returns:
            list: A list of response bodies from network requests that match
                the specified patterns.
        """
        logs_matched = await self.get_network_logs(matches)
        responses = []
        for log in logs_matched:
            try:
                body, base64encoded = await self.get_network_response_body(
                    log['params']['requestId']
                )
            except KeyError:
                continue
            response = json.loads(body) if not base64encoded else body
            responses.append(response)
        return responses

    async def get_network_response_body(self, request_id: str):
        """
        Retrieves the response body of a network request.

        Args:
            request_id (str): The ID of the network request.

        Returns:
            tuple: A tuple containing:
                - str: The response body content
                - bool: Flag indicating if the body is base64 encoded
        """
        response = await self._execute_command(
            NetworkCommands.get_response_body(request_id)
        )
        return (
            response['result']['body'],
            response['result']['base64Encoded'],
        )

    async def enable_page_events(self):
        """
        Enables page events for the page.

        This allows listening for page-related events such as load, navigate,
        and content change events. These events can be captured with the `on`
        method.

        Returns:
            None
        """
        await self._execute_command(PageCommands.enable_page())
        self._page_events_enabled = True

    async def enable_network_events(self):
        """
        Enables network events for the page.

        This allows listening for network-related events such as request and
        response events. These events can be captured with the `on` method.

        Returns:
            None
        """
        await self._execute_command(NetworkCommands.enable_network_events())
        self._network_events_enabled = True

    async def enable_fetch_events(
        self, handle_auth: bool = False, resource_type: str = 'Document'
    ):
        """
        Enables fetch events for the page.

        This allows interception of network requests before they are sent.

        Args:
            handle_auth (bool): Whether to handle authentication requests.
                Defaults to False.
            resource_type (str): The type of resource to intercept.
                Defaults to 'Document'.

        Returns:
            None
        """
        await self._execute_command(
            FetchCommands.enable_fetch_events(handle_auth, resource_type)
        )
        self._fetch_events_enabled = True

    async def enable_dom_events(self):
        """
        Enables DOM events for the page.

        This allows listening for DOM-related events such as node creation,
        attribute modification, and node removal events. These events can be
        captured with the `on` method.

        Returns:
            None
        """
        await self._execute_command(DomCommands.enable_dom_events())
        self._dom_events_enabled = True

    async def enable_intercept_file_chooser_dialog(self):
        """
        Enable intercepting file chooser dialogs.

        When file chooser interception is enabled, native file chooser dialog
        is not shown. Instead, a protocol event Page.fileChooserOpened is
        emitted.

        Returns:
            None
        """
        await self._execute_command(
            PageCommands.set_intercept_file_chooser_dialog(True)
        )
        self._intercept_file_chooser_dialog_enabled = True

    async def disable_fetch_events(self):
        """
        Disables fetch events for the page.

        This stops the interception of network requests that was previously
        enabled with enable_fetch_events().

        Returns:
            None
        """
        await self._execute_command(FetchCommands.disable_fetch_events())
        self._fetch_events_enabled = False

    async def disable_page_events(self):
        """
        Disables page events for the page.

        This stops listening for page-related events that were previously
        enabled with enable_page_events().

        Returns:
            None
        """
        await self._execute_command(PageCommands.disable_page())
        self._page_events_enabled = False

    async def disable_intercept_file_chooser_dialog(self):
        """
        Disable intercepting file chooser dialogs.

        When file chooser interception is disabled, native file chooser
        dialog is shown.

        Returns:
            None
        """
        await self._execute_command(
            PageCommands.set_intercept_file_chooser_dialog(False)
        )
        self._intercept_file_chooser_dialog_enabled = False

    async def on(
        self, event_name: str, callback: callable, temporary: bool = False
    ):
        """
        Registers an event listener for the page.

        Args:
            event_name (str): The event name to listen for.
            callback (callable): The callback function to execute when the
                event is triggered.
            temporary (bool): If True, the callback will be removed after it's
                triggered once. Defaults to False.

        Returns:
            int: The ID of the registered callback, which can be used to
                remove the listener later.
        """

        async def callback_wrapper(event):
            asyncio.create_task(callback(event))

        if asyncio.iscoroutinefunction(callback):
            function_to_register = callback_wrapper
        else:
            function_to_register = callback

        return await self._connection_handler.register_callback(
            event_name, function_to_register, temporary
        )

    async def execute_script(self, script: str, element: WebElement = None):
        """
        Executes a JavaScript script in the page.
        If an element is provided, the script will be executed in the context
        of that element. To provide the element context, use the 'argument'
        keyword in the script.

        Examples:
        ```python
        await page.execute_script('argument.click()', element)
        await page.execute_script('argument.value = "Hello, World!"', element)
        ```

        Args:
            script (str): The JavaScript script to execute.
            element (WebElement, optional): The element to execute the script
                on. Use 'argument' in your script to refer to this element.
                Defaults to None.

        Returns:
            dict: The result of the script execution from the browser.
        """
        if element:
            script = script.replace('argument', 'this')
            script = f'function(){{ {script} }}'
            object_id = element._object_id
            command = RuntimeCommands.call_function_on(
                object_id, script, return_by_value=True
            )
        else:
            command = RuntimeCommands.evaluate_script(script)
        return await self._execute_command(command)

    async def _refresh_if_url_not_changed(self, url: str):
        """
        Refreshes the page if the URL has not changed.

        Args:
            url (str): The URL to compare against.
        """
        current_url = await self.current_url
        if current_url == url:
            await self.refresh()
            return True
        return False

    async def _wait_page_load(self, timeout: int = 300):
        """
        Waits for the page to finish loading.

        Args:
            timeout (int): Maximum time in seconds to wait for the page
                to load. Defaults to 300 seconds.

        Raises:
            asyncio.TimeoutError: If the page does not finish loading within
                the specified timeout.
        """
        start_time = asyncio.get_event_loop().time()
        while True:
            response = await self._execute_command(
                RuntimeCommands.evaluate_script('document.readyState')
            )
            if response['result']['result']['value'] == 'complete':
                break
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise asyncio.TimeoutError('Page load timed out')
            await asyncio.sleep(0.5)

    @asynccontextmanager
    async def expect_file_chooser(
        self, files: Union[str, Path, List[Union[str, Path]]]
    ):
        """
        Provide a context manager that expects a file chooser dialog to be
        opened and handles the file upload. When a file selection signal
        is captured, the file is uploaded.

        Args:
            files (Union[str, Path, List[Union[str, Path]]]): The files to be
                uploaded.

        Returns:

        """

        async def event_handler(event):
            await self._execute_command(
                DomCommands.upload_files(
                    files=files,
                    backend_node_id=event['params']['backendNodeId'],
                )
            )

        if self.page_events_enabled is False:
            _before_page_events_enabled = False
            await self.enable_page_events()
        else:
            _before_page_events_enabled = True

        if self.intercept_file_chooser_dialog_enabled is False:
            await self.enable_intercept_file_chooser_dialog()

        await self.on(
            PageEvents.FILE_CHOOSER_OPENED, event_handler, temporary=True
        )

        yield

        if self.intercept_file_chooser_dialog_enabled is True:
            await self.disable_intercept_file_chooser_dialog()

        if _before_page_events_enabled is False:
            await self.disable_page_events()

    async def _bypass_cloudflare(
        self,
        event: dict,
        custom_selector: Optional[Tuple[By, str]] = None,
        timeout: int = 5,
    ):
        """
        Attempt to bypass Cloudflare Turnstile captcha when detected.

        Args:
            event (dict): The event payload (unused)
            custom_selector (Optional[Tuple[By, str]]): Custom selector
                to locate the captcha element. Defaults to
                (By.CLASS_NAME, 'cf-turnstile').
            timeout (int): Timeout for the captcha element to be found
                in seconds. Defaults to 5 seconds.
        """
        try:
            selector = custom_selector or (By.CLASS_NAME, 'cf-turnstile')
            if element := await self.wait_element(
                *selector, timeout=timeout, raise_exc=False
            ):
                # adjust the div size to shadow root size
                await self.execute_script(
                    'argument.style="width: 300px"', element
                )
                await asyncio.sleep(2)
                await element.click()
        except Exception as exc:
            logger.error(f'Error in cloudflare bypass: {exc}')

    @asynccontextmanager
    async def expect_and_bypass_cloudflare_captcha(
        self,
        custom_selector: Optional[Tuple[By, str]] = None,
        timeout: Optional[int] = 5,
    ):
        """
        Context manager to handle Cloudflare Turnstile captcha.

        This method sets up a callback that will automatically attempt to
        bypass the Cloudflare captcha when the page loads. The main code
        will wait until the captcha handling is complete before continuing.

        It creates an event to coordinate between the callback and the main
        code.

        Args:
            custom_selector (Optional[Tuple[By, str]]): Custom selector
                to locate the captcha element. Defaults to
                (By.CLASS_NAME, 'cf-turnstile').
            timeout (Optional[int]): Timeout for the captcha element to be
                found. Defaults to 5 seconds.

        Returns:
            None
        """
        captcha_processed = asyncio.Event()

        async def bypass_cloudflare(_: dict):
            try:
                await self._bypass_cloudflare(_, custom_selector, timeout)
            finally:
                captcha_processed.set()

        _before_page_events_enabled = self.page_events_enabled

        if not _before_page_events_enabled:
            await self.enable_page_events()

        callback_id = await self.on(PageEvents.PAGE_LOADED, bypass_cloudflare)

        try:
            yield
            await captcha_processed.wait()
        finally:
            await self._connection_handler.remove_callback(callback_id)
            if not _before_page_events_enabled:
                await self.disable_page_events()

    async def enable_auto_solve_cloudflare_captcha(
        self,
        custom_selector: Optional[Tuple[By, str]] = None,
        timeout: int = 5,
    ):
        """
        Enables automatic solving of Cloudflare Turnstile captcha.

        This method sets up a callback that will automatically attempt to
        bypass the Cloudflare captcha when the page loads. Unlike the
        context manager version, this keeps the callback active until
        explicitly disabled.

        Args:
            custom_selector (Optional[Tuple[By, str]]): Custom selector
                to locate the captcha element. Defaults to
                (By.CLASS_NAME, 'cf-turnstile').
            timeout (int): Timeout for the captcha element to be
                found in seconds. Defaults to 5 seconds.

        Returns:
            int: Callback ID that can be used to disable the auto-solving
        """
        if not self.page_events_enabled:
            await self.enable_page_events()

        callback = partial(
            self._bypass_cloudflare,
            custom_selector=custom_selector,
            timeout=timeout,
        )

        self._cloudflare_captcha_callback_id = await self.on(
            PageEvents.PAGE_LOADED, callback
        )

    async def disable_auto_solve_cloudflare_captcha(self):
        """
        Disables automatic solving of Cloudflare Turnstile captcha.

        Returns:
            None
        """
        await self._connection_handler.remove_callback(
            self._cloudflare_captcha_callback_id
        )
        self._cloudflare_captcha_callback_id = None
