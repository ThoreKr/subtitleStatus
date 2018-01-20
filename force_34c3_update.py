﻿#!/usr/bin/python3
# -*- coding: utf-8 -*-

#==============================================================================
# This script removes all schedule versions from the database which causes the
# schedule update script to import every schedule again
#==============================================================================

import os
import sys
from lxml import etree
from urllib import request

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subtitleStatus.settings")

import django
django.setup()
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from www.models import Event

try:
    event_34c3 = Event.objects.get(id = 6)
    event_34c3.schedule_version = "force update"
    event_34c3.save()
except:
    print("Fehler")
    
print("Fahrplanversion für 34c3 zurück gesetzt!")


