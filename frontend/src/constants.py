# Comicker Frontend - Constants

from browser import window

if "localhost" in window.location.host:
    URL = "http://localhost:801"
else:
    URL = "http://tasuren.f5.si:801"