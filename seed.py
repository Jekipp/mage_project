import os
import django
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mage_project.settings')
django.setup()

from mage_app.models import *


values= range(1,15)
SUITS

for v in values:
    for suit in SUITS:
        if v == 14 and suit[0] =='d':
            break
        card = Card.objects.get_or_create(value=v, suit=suit[0])
    