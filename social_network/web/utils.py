from datetime import datetime, timedelta

from social_network.settings import NewsCacheSettings
from social_network.db.managers import NewsManager
from social_network.db.models import TIMESTAMP_FORMAT
from social_network.services.kafka.producer import KafkaProducer


async def warmup_news(conf: NewsCacheSettings,
                      news_manager: NewsManager,
                      producer: KafkaProducer):
    timestamp = datetime.now() - timedelta(seconds=conf.WARMUP_CACHE_PERIOD)
    timestamp = timestamp.strftime(TIMESTAMP_FORMAT)
    news = await news_manager.list_after_timestamp(timestamp)
    for new in news:
        print(new)
        new.populated, new.stored = True, True
        await producer.send(new.json())
