"""
not sure if this is needed, but authorization doesn't seem to work with it

I'm shoving this in here in case we need it. It use to live in the config.py file
"""

# async_mode = None
# if async_mode is None:
#     try:
#         import eventlet

#         async_mode = "eventlet"
#     except ImportError:
#         pass

#     if async_mode is None:
#         try:
#             from gevent import monkey

#             async_mode = "gevent"
#         except ImportError:
#             pass

#     if async_mode is None:
#         async_mode = "threading"

#     print("async_mode is " + async_mode)

# # monkey patching is necessary because this application uses a background
# # thread
# if async_mode == "eventlet":
#     import eventlet

#     eventlet.monkey_patch()
# elif async_mode == "gevent":
#     from gevent import monkey

#     monkey.patch_all()
