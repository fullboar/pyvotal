.. Pyvotal documentation master file, created by
   sphinx-quickstart on Tue Jan 17 21:54:34 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. contents ::

Welcome to Pyvotal's documentation!
===================================


Pyvotal is python client to `Pivotal Tracker API <https://www.pivotaltracker.com/help/api?version=v3>`_.

Python 2.x >= 2.5 is supported.

Covers all api, except integrations and activity feed.

Pyvotal can be installed using `pip <http://www.pip-installer.org>`_::

    pip install pyvotal


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


Howto
-------------

Get all projects
################

::

    from pyvotal import PTracker
    
    ptracker = PTracker(user='someuser', password='somepassword')
    
    for project in p.projects.all():
        print "#%s '%s' @ %s\n" % (project.id, project.name, project.account)

Get stories
####################

::

    from pyvotal import PTracker
    
    ptracker = PTracker(user='someuser', password='somepassword')
    
    project = p.projects.get(project_id)
    for story in project.stories.all():
        print "#%s '%s'\n" % (story.id, story.name)

Change story
####################

::

    from pyvotal import PTracker
    
    ptracker = PTracker(user='someuser', password='somepassword')
    
    project = p.projects.get(project_id)
    story =  project.stories.get(project_id)
    story.description = "New desc"
    story.save()
    story.add_note("Note text")
    story.add_attachment("FileName", open('/etc/hosts'))


API
============

.. toctree::
   :maxdepth: 2

   api



