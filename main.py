import json
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

import shaarli_client.client as c

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        searchtags = event.get_argument()
        logger.info('preferences %s' % json.dumps(extension.preferences))

        setting_url = extension.preferences['setting_url']
        setting_api = extension.preferences['setting_api']
        setting_limit = extension.preferences['setting_limit']

        response = c.ShaarliV1Client(setting_url, setting_api)

        answer = response.get_links({'searchtags': searchtags, 'limit': str(setting_limit)})
        j = answer.text
        a = json.loads(j)

        for i in a:
            item_title = i['title']
            item_url = i['url']
            item_desc = i['description']
            item_tags = i['tags']

            def listToString(s):
                str1 = " "
                return (str1.join(s))

            list_tags = listToString(item_tags)

            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s' % item_title,
                                             description='URL: %s\nDescription: %s\nTags: %s' % (item_url, item_desc, list_tags),
                                             on_enter=OpenUrlAction(item_url)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
