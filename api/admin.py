from django.contrib import admin
from .models import *

admin.site.register(Organization)
admin.site.register(Factor)
admin.site.register(Subfactor)
admin.site.register(Subsubfactor)
admin.site.register(Emissionrecord)
admin.site.register(Tips)

