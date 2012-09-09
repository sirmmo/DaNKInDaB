from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
import daemon

import gevent
from gevent.pywsgi import WSGIServer
import inspect
from server.models import *
import importlib


def dispatcher(environ, setup_response):
    vh = VirtualHostName.objects.filter(name=environ['HOST_NAME'])
    if len(vh)>0:
        vh = vh[0]
        cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(vh.virtualhost.base_dir))))
        if cmd_folder not in sys.path:
            sys.path.insert(0, cmd_subfolder)
        m = importlib.import_module(vh.virtualhost.wsgi)
        return m(environ, setup_reponse)
    else:
        setup_response('500 ERROR', None)
        return ["ERROR"]
    
    
class DWSGIServer(WSGIServer):
    def _init__(self, listener):
        super(DWSGIServer, self).__init('',listener.port, dispatcher)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--chroot_directory', action='store', dest='chroot_directory',
            help='Full path to a directory to set as the effective root directory of \
            the process.'),
        make_option('--working_directory', action='store', dest='working_directory',
            default="/",
            help='Full path of the working directory to which the process should \
            change on daemon start.'),
        make_option('--umask', action='store', dest='umask', default=0, type="int",
            help='File access creation mask ("umask") to set for the process on \
            daemon start.'),
        make_option('--pidfile', action='store', dest='pidfile',
            help='Context manager for a PID lock file. When the daemon context opens \
            and closes, it enters and exits the `pidfile` context manager.'),
        make_option('--detach_process', action='store', dest='detach_process', 
            help='If ``True``, detach the process context when opening the daemon \
            context; if ``False``, do not detach.'),
        make_option('--uid', action='store', dest='uid', 
            help='The user ID ("UID") value to switch the process to on daemon start.'),
        make_option('--gid', action='store', dest='gid', 
            help='The group ID ("GID") value to switch the process to on daemon start.'),
        make_option('--prevent_core', action='store', dest='prevent_core', default=True,
            help='If true, prevents the generation of core files, in order to avoid \
            leaking sensitive information from daemons run as `root`.'),
    )

    help = 'The DaNKInDaB server'

    def get_option_value(self, options, name, expected=None):
        value = options.get(name)
        if value == expected:
            value = getattr(self, name)
        print name, ' ', value
        return value
    

    def handle(self, **options):
        context= daemon.DaemonContext()
        
        context.chroot_directory = self.get_option_value(options, 'chroot_directory')
        context.working_directory = self.get_option_value(options, 'working_directory', '/')
        context.umask = self.get_option_value(options, 'umask', 0)
        context.detach_process = self.get_option_value(options, 'detach_process')
        context.prevent_core = self.get_option_value(options, 'prevent_core', True)
        
        pidfile = self.get_option_value(options, 'pidfile')
        if pidfile is not None:
            context.pidfile=daemon.writePID(pidfile)
            
        uid = self.get_option_value(options, 'uid')
        if uid is not None:
            context.uid = uid
        
        gid = self.get_option_value(options, 'gid')
        if gid is not None:
            context.gid = uid
        
        context.open()
        
        self.listeners = []
        self.handle_daemon(*args, **options)

    def handle_daemon(self, *args, **options):
        for listener in Listener.objects.all():
            self.listeners.append(DWSGIServer(listener))
        for l in self.listeners:
            l.start()
        