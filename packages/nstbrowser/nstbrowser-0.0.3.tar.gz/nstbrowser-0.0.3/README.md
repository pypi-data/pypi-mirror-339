# Nstbrowser SDK for Python

A Python SDK for interacting with [Nstbrowser API v2](https://apidocs.nstbrowser.io/)

## Overview

This SDK implements Nstbrowser API v2, which is the recommended API with complete functionality from v1 plus additional features. It provides a comprehensive set of tools for managing browser profiles, controlling browser instances, managing local browser data, and utilizing Chrome DevTools Protocol (CDP) for browser automation.

The SDK enables you to:
- Create and manage browser profiles with detailed fingerprint configurations
- Start and stop browser instances individually or in batch
- Configure and manage proxies for profiles
- Manage profile tags for better organization
- Clear browser cache and cookies
- Connect to browsers using Chrome DevTools Protocol (CDP)
- Automate browser actions through CDP integration

## Installation

```bash
pip install nstbrowser
```

## Getting Started

To use the SDK, you need an API key from Nstbrowser:

```python
from nstbrowser import NstbrowserClient

# Initialize the client with your API key
client = NstbrowserClient(api_key="your_api_key")

# Now you can use the various services
profile_id = "your_profile_id"

# Start a browser instance
response = client.browsers.start_browser(profile_id=profile_id)
print(f"Browser started: {response}")

# Stop the browser instance
response = client.browsers.stop_browser(profile_id=profile_id)
print(f"Browser stopped: {response}")
```

## Available Services

The SDK provides the following services:

### BrowsersService

Manages browser instances, including starting, stopping, and getting information about browsers.

```python
# Start a browser for a specific profile
response = client.browsers.start_browser(profile_id="your_profile_id")

# Start multiple browsers in batch
response = client.browsers.start_browsers(profile_ids=["profile_id_1", "profile_id_2"])

# Start a once-off browser with custom configuration
config = {
    "name": "testProfile",
    "platform": "Windows",
    "kernelMilestone": "132",
    "headless": False,
    "proxy": "http://admin:123456@127.0.0.1:8000",
    "fingerprint": {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
        "screen": {"width": 1280, "height": 1024}
    },
    "startupUrls": ["https://www.example.com"]
}
response = client.browsers.start_once_browser(data=config)

# Stop a browser
response = client.browsers.stop_browser(profile_id="your_profile_id")

# Stop multiple browsers
response = client.browsers.stop_browsers(profile_ids=["profile_id_1", "profile_id_2"])

# Get active browsers
response = client.browsers.get_browsers(status="running")

# Get browser pages
response = client.browsers.get_browser_pages(profile_id="your_profile_id")

# Get browser debugger information
response = client.browsers.get_browser_debugger(profile_id="your_profile_id")
```

### ProfilesService

Manages browser profiles, including creation, deletion, proxy configuration, and tag management.

```python
# Create a new profile
profile_data = {
    "name": "New Profile",
    "platform": "Windows",
    "kernelMilestone": "132",
    "fingerprint": {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
        "timezone": "Asia/Hong_Kong"
    }
}
response = client.profiles.create_profile(data=profile_data)

# Get profiles with filtering
response = client.profiles.get_profiles(data={"page": 1, "pageSize": 10})

# Delete a profile
response = client.profiles.delete_profile(profile_id="your_profile_id")

# Delete multiple profiles
response = client.profiles.delete_profiles(profile_ids=["profile_id_1", "profile_id_2"])

# Update a profile's proxy
response = client.profiles.update_profile_proxy(profile_id="your_profile_id", data={"url": "http://admin:654321@127.0.0.1:8000"})

# Reset a profile's proxy
response = client.profiles.reset_profile_proxy(profile_id="your_profile_id")

# Manage profile tags
response = client.profiles.create_profile_tags(profile_id="your_profile_id", data=[{"name": "social", "color": "#646AEE"}])
response = client.profiles.get_profile_tags()
```

### LocalsService

Manages local browser data, such as cache and cookies.

```python
# Clear browser cache
response = client.locals.clear_profile_cache(profile_id="your_profile_id")

# Clear browser cookies
response = client.locals.clear_profile_cookies(profile_id="your_profile_id")
```

### CdpEndpointsService

Provides connections to browsers using Chrome DevTools Protocol (CDP) for automation.

```python
# Connect to a browser using CDP
config = {
    "headless": False,
    "autoClose": False
}
response = client.cdp_endpoints.connect_browser(profile_id="your_profile_id", config=config)

# Connect to a once-off browser using CDP
config = {
    "name": "testProfile",
    "platform": "Windows",
    "kernelMilestone": "132",
    "autoClose": False,
    "headless": False
}
response = client.cdp_endpoints.connect_once_browser(config=config)
```

## Examples

The SDK comes with a comprehensive set of examples in the `/examples` directory, organized by service:

### Browser Examples
- `browsers/start_browser.py`: Start a browser for a specific profile
- `browsers/start_browsers.py`: Start multiple browsers in batch
- `browsers/start_once_browser.py`: Start a once-off browser with custom configuration
- `browsers/stop_browser.py`: Stop a browser
- `browsers/stop_browsers.py`: Stop multiple browsers
- `browsers/get_browsers.py`: Get browser status information
- `browsers/get_browser_pages.py`: Get browser pages information
- `browsers/get_browser_debugger.py`: Get browser debugger information

### Profile Examples
- `profiles/create_profile.py`: Create a new profile with detailed configuration
- `profiles/get_profiles.py`: Get profiles with filtering options
- `profiles/delete_profile.py`: Delete a specific profile
- `profiles/delete_profiles.py`: Delete multiple profiles
- `profiles/update_profile_proxy.py`: Update a profile's proxy
- `profiles/batch_update_proxy.py`: Update proxies for multiple profiles
- `profiles/reset_profile_proxy.py`: Reset a profile's proxy
- `profiles/batch_reset_profile_proxy.py`: Reset proxies for multiple profiles
- `profiles/create_profile_tags.py`: Create tags for a profile
- `profiles/get_profile_tags.py`: Get all profile tags
- `profiles/update_profile_tags.py`: Update tags for a profile
- `profiles/batch_update_profile_tags.py`: Update tags for multiple profiles
- `profiles/clear_profile_tags.py`: Clear all tags from a profile
- `profiles/batch_clear_profile_tags.py`: Clear tags from multiple profiles
- `profiles/batch_create_profile_tags.py`: Create tags for multiple profiles
- `profiles/get_all_profile_groups.py`: Get all profile groups
- `profiles/change_profile_group.py`: Change a profile group
- `profiles/batch_change_profile_group.py`: Batch changes to profile groups

### Local Data Examples
- `locals/clear_profile_cache.py`: Clear browser cache
- `locals/clear_profile_cookies.py`: Clear browser cookies

### CDP Endpoint Examples
- `cdp_endpoints/connect_browser.py`: Connect to a browser using CDP and automate with Playwright
- `cdp_endpoints/connect_once_browser.py`: Connect to a once-off browser with CDP and automate with Playwright

To run an example:

```bash
python examples/browsers/start_browser.py
```

## CDP Integration with Playwright

One powerful feature is the ability to connect to browsers using Chrome DevTools Protocol (CDP) and automate them with Playwright:

```python
# Get the CDP WebSocket URL
websocket_url = client.cdp_endpoints.connect_browser(
    profile_id="your_profile_id", 
    config={"headless": False}
)["data"]["webSocketDebuggerUrl"]

# Use the URL with Playwright for automation
from playwright.async_api import async_playwright

async def automate():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(websocket_url)
        page = browser.contexts[0].pages[0]
        await page.goto("https://example.com")
        # ... perform other actions
```

Complete examples for CDP automation are available in the `examples/cdp_endpoints` directory.


## Support

For support, feel free to reach out to us via [Discord](https://api.nstbrowser.io/api/v1/links/discord). For more detailed documentation, visit the official Nstbrowser documentation: [Nstbrowser API Documentation](https://apidocs.nstbrowser.io).


