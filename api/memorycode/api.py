import aiohttp
from memorycode.config import MEMORYCODE_EMAIL, MEMORYCODE_PASSWORD, MEMORYCODE_BASE_URL
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


async def get_access_token(email, password, device='bot-v0.0.1'):
    """
    Asynchronously retrieves an access token using the provided email, password, and device parameters.

    Parameters:
        email (str): The email of the user.
        password (str): The password of the user.
        device (str): The device identifier (default is 'bot-v0.0.1').

    Returns:
        str: The access token if available in the response data, otherwise returns the data itself.
    """
    url = f"{MEMORYCODE_BASE_URL}/api/v1/get-access-token?email={email}&password={password}&device={device}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()
        return data.get('access_token')


async def update_memory_page(page_id, access_token):
    """
    A function to update a memory page with the given page_id and access_token.
    
    Parameters:
    - page_id: int, the id of the memory page to update
    - access_token: str, the access token for authorization
    
    Returns:
    None
    """
    url = f"{MEMORYCODE_BASE_URL}/page/{page_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            if response.status == 200:
                logger.info("Страница памяти успешно обновлена!")
            else:
                logger.error("Произошла ошибка при обновлении страницы памяти.")
                logger.error(f"Код ошибки: {response.status}")
                logger.error(f"Текст ошибки: {await response.text()}")


async def search_pages(query_params):
    """
    Asynchronously searches for pages using the provided query parameters.

    Parameters:
        query_params (dict): The parameters for the page search.

    Returns:
        dict: The JSON response from the page search.
    """
    url = f"{MEMORYCODE_BASE_URL}/page/search"
    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json=query_params)
        return await response.json()


async def link_pages(access_token, link_data):
    """
    Asynchronously links pages using the provided access token and link data.

    Parameters:
        access_token (str): The access token for authorization.
        link_data (dict): The data for linking the pages.

    Returns:
        dict: The JSON response from the page link operation.
    """
    url = f"{MEMORYCODE_BASE_URL}/page/relative"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(link_data)) as response:
            return await response.json()


async def get_individual_page_by_name(access_token, name):
    """
    Asynchronously retrieves an individual page by name using the provided access token and name parameters. 
    It makes a GET request to the specified URL with the provided headers and processes the response accordingly. 
    If the page is found, it returns the page data. If the page is not found, it logs a warning and returns None. 
    If an error occurs during the request, it logs the error and returns None.
    """
    url = f"{MEMORYCODE_BASE_URL}/api/cabinet/individual-pages?name={name}"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                data = await response.json(content_type=None)
                if isinstance(data, list) and data[0].get('name') == name:
                    return data[0]
        except (aiohttp.ContentTypeError, json.JSONDecodeError):
            pass

        logger.warning("Страница памяти не найдена.")
        return None


async def main():
    """
    Asynchronous function to fetch access token and retrieve individual's page information by name.
    """
    access_token = await get_access_token(MEMORYCODE_EMAIL, MEMORYCODE_PASSWORD)
    if access_token:
        person_name = "Иванов Иван Иванович"
        url = f"{MEMORYCODE_BASE_URL}/api/cabinet/individual-pages?name={person_name}"
        headers = {"Authorization": f"Bearer {access_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                page_info = data[0] if data and isinstance(data, list) and data[0].get('name') == person_name else None
                if page_info:
                    logger.info("Информация о человеке:")
                    logger.info("Имя:", page_info.get('name'))
                    logger.info("Дата рождения:", page_info.get('birthday_at'))
                    logger.info("Дата смерти:", page_info.get('died_at'))
                    logger.info("Эпитафия:", page_info.get('epitaph'))
                else:
                    logger.info(f"Страница с именем '{person_name}' не найдена.")
    else:
        logger.error("Не удалось получить токен доступа.")


asyncio.run(main())