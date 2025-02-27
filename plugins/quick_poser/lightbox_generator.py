import datetime
import json
import shutil
from operator import itemgetter
from pathlib import Path
from tempfile import TemporaryDirectory

import requests
import yadisk
from pelican import signals
from pelican.contents import Article
from pelican.readers import BaseReader


def add_article(article_generator):
    settings = article_generator.settings

    (
        yadisk_path_prefix,
        yadisk_listings_path,
        yandex_client_id,
        yandex_client_secret,
        yandex_access_token,
        content_path,
    ) = itemgetter(
        'YADISK_PATH_PREFIX',
        'YADISK_LISTINGS_PATH',
        'YANDEX_CLIENT_ID',
        'YANDEX_CLIENT_SECRET',
        'YANDEX_ACCESS_TOKEN',
        'PATH',
    )(settings)

    ya_client = yadisk.Client(yandex_client_id, yandex_client_secret, yandex_access_token)

    with ya_client, TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        assert ya_client.check_token()
        listing_files = [
            Path(obj.path[len(yadisk_path_prefix):])
            for obj in ya_client.listdir(f'{yadisk_path_prefix}{yadisk_listings_path}')
            if obj.is_file()
        ]
        base_reader = BaseReader(settings)

        for listing_file in listing_files:
            local_filepath = tmppath.joinpath(listing_file.name)
            category = local_filepath.stem
            ya_client.download(f'/{str(listing_file)}', str(local_filepath))
            with open(local_filepath, mode='r', encoding='utf-8') as fp:
                lines = fp.readlines()
                images = []
                for line in lines:
                    image_details = json.loads(line)
                    r = requests.get(image_details['original_url'], allow_redirects=True, stream=True)
                    if r.status_code == 200:
                        root_path, obj_path = Path(image_details['root_path']), Path(image_details['obj_path'])
                        image_path = obj_path.relative_to(root_path)
                        image_filepath = content_path / Path('images') / image_path
                        image_filepath.parent.mkdir(parents=True, exist_ok=True)
                        image_url = f'images/{image_path}'
                        with open(image_filepath, 'wb') as f:
                            shutil.copyfileobj(r.raw, f)
                        images.append(image_url)

                new_article = Article('', {
                    'template': 'lightbox',
                    'title': category,
                    'date': datetime.datetime.now(),
                    'category': base_reader.process_metadata('category', category),
                    'images': images,
                })
                article_generator.articles.insert(0, new_article)


def register():
    signals.article_generator_pretaxonomy.connect(add_article)
