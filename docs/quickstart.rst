Quickstart
============

The main entry point for api is :class:`~pyvotal.PTracker` class.

Authorization
-------------

You can supply :class:`~pyvotal.PTracker` with username and password::

    from pyvotal import PTracker

    ptracker = PTracker(user='someuser', password='somepassword')
    print "Token for this credentials is", ptracker.token


or directly pass `api token <https://www.pivotaltracker.com/help/api?version=v3#access_control>`_::

    from pyvotal import PTracker

    ptracker = PTracker(token='token')

Projects
-------------

All project related calls are made using :class:`~pyvotal.projects.ProjectManager` which is availiable as :attr:`pyvotal.PTracker.projects`

Get
+++++++++++++

You can get all your projects using :meth:`pyvotal.projects.ProjectManager.all`::

    from pyvotal import PTracker

    ptracker = PTracker(token=token)

    for project in ptracker.projects.all():
        print project.id, project.name
	
You can get single project using :meth:`pyvotal.projects.ProjectManager.get`::

    from pyvotal import PTracker

    ptracker = PTracker(token=token)

    project = ptracker.projects.get(project_id)










