from discussions.settings.base import *

import mongoengine


# TODO this setting works in dev environments.  Define it as well for production.
mongoengine.connect('cs_comments_service_development')
