import dataclasses as dc
import datetime


@dc.dataclass(unsafe_hash=True)
class AssetDto:
    id: int
    name: str
    image_urls: list
    creator: str
    updater: str
    created_at: str
    updated_at: str
    asset_url: str
    details: str


date_format = '%Y-%M-%d'


def get_asset_dto(result):
    asset_dto = AssetDto(result[0], result[1], result[2].split(","), result[3], result[4],
                         result[5].strftime(date_format), result[6].strftime(date_format), result[7], result[8])
    return asset_dto
