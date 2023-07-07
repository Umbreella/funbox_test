import time
from datetime import datetime, timedelta

from fastapi import status

url = '/api/visited_domains'


async def test_When_PostForDomainList_Should_ErrorWith405(client):
    response = await client.post(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForDomainList_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForDomainList_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForDomainList_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForDomainListWithOutQueryParams_Should_ErrorWith422(
        client,
):
    response = await client.get(url)

    expected_status = status.HTTP_422_UNPROCESSABLE_ENTITY
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForDomainListWithEmptyData_Should_ReturnEmptyWith200(
        client,
):
    response = await client.get(f'{url}?from_=0&to=1000000')

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'domains': [],
        'status': 'ok',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForDomainListWithData_Should_ReturnDataWith200(
        client, redis_client,
):
    await client.post('/api/visited_links', json={
        'links': [
            'https://ya.ru',
            'https://ya.ru?q=123',
        ],
    })
    await client.post('/api/visited_links', json={
        'links': [
            'https://ya.ru?q=qwer',
            'https://yandex.ru?q=123',
        ],
    })

    end_date = datetime.now() + timedelta(days=1)
    end_time = int(time.mktime(end_date.timetuple()))

    response = await client.get(f'{url}?from_=0&to={end_time}')

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'domains': [
            'ya.ru',
            'yandex.ru',
        ],
        'status': 'ok',
    }
    real_data = response.json()

    real_data['domains'].sort()

    assert expected_status == real_status
    assert expected_data == real_data
