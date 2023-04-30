#!/usr/bin/python3
"""
initialize the models package
"""

import importlib
import os
import pkgutil


storage = None
storage_t = os.getenv("HBNB_TYPE_STORAGE")

classes = pkgutil.iter_modules(__path__)
classes = (module[1] for module in classes if not module[2])
classes = ((name.title().replace('_', ''), name) for name in classes)
classes = (
    (cls, importlib.import_module('models.' + mod))
    for cls, mod in classes
)
classes = {cls: getattr(mod, cls) for cls, mod in classes}

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
