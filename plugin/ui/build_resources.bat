pyrcc5 -o resources_rc_qt5.py resources.qrc 2>NUL

if NOT ["%errorlevel%"]==["0"] pause

exit