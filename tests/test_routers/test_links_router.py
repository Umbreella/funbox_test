import copy
import time
from datetime import datetime, timedelta

from fastapi import status

url = '/api/visited_links'
data = {
    'links': [
        'https://ya.ru',
        'https://ya.ru?q=123',
        'funbox.ru',
        'https://stackoverflow.com/questions/11828270/how-to-exit',
    ],
}


async def test_When_GetForLinksList_Should_ErrorWith405(client):
    response = await client.get(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForLinksList_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForLinksList_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForLinksList_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForLinksListWithEmpltyLinks_Should_ErrorWith400(
        client,
):
    local_data = copy.copy(data)
    local_data.update({
        'links': [],
    })

    response = await client.post(url, json=local_data)

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'status': 'Links is empty.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForLinksListWithNotValidUrl_Should_ErrorWith400(
        client,
):
    local_data = copy.copy(data)
    local_data.update({
        'links': [
            'funboxru',
        ],
    })

    response = await client.post(url, json=local_data)

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'status': 'Url is not valid.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForLinksListWithValiddata_Should_ReturnDataWith201(
        client, redis_client,
):
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=1)

    start_time = int(time.mktime(start_date.timetuple()))
    end_time = int(time.mktime(end_date.timetuple()))

    response = await client.post(url, json=data)

    expected_status = status.HTTP_201_CREATED
    real_status = response.status_code

    expected_data = {
        'status': 'ok',
    }
    real_data = response.json()

    expected_data_in_redis = []
    real_data_in_redis = redis_client.ft().search(
        f'@created_at:[{start_time} {end_time}]'
    )

    assert expected_status == real_status
    assert expected_data == real_data
    assert expected_data_in_redis != real_data_in_redis
