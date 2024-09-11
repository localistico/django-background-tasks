# -*- coding: utf-8 -*-
import logging

from django import VERSION
from django.core.management.base import BaseCommand

from background_task.tasks import tasks, autodiscover


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Show discovered tasks that can be run on the queue'

    # Command options are specified in an abstract way to enable Django < 1.8 compatibility
    OPTIONS = (
        (('--queue', ), {
            'action': 'store',
            'dest': 'queue',
            'help': 'Only show tasks configured to run on this named queue',
        }),
    )

    if VERSION < (1, 8):
        from optparse import make_option
        option_list = BaseCommand.option_list + tuple([make_option(*args, **kwargs) for args, kwargs in OPTIONS])

    # Used in Django >= 1.8
    def add_arguments(self, parser):
        for (args, kwargs) in self.OPTIONS:
            parser.add_argument(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        queue = options.get('queue', None)

        autodiscover()
        task_names = list(tasks._tasks.keys())
        if queue is not None:
            task_names = [
                n for n in task_names if tasks._tasks[n].queue == queue
            ]
        for task_name in task_names:
            print(task_name)
