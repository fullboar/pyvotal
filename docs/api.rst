
API
======

PTracker
------------
.. autoclass:: pyvotal.PTracker
   :members:
   :undoc-members:

Project
--------------
.. autoclass:: pyvotal.projects.Project
   :members:

.. autoclass:: pyvotal.projects.ProjectManager
   :members:
   :undoc-members:

   .. method:: add(project)

      :param project: :class:`~pyvotal.projects.Project`
      :return: :class:`~pyvotal.projects.Project`

      Adds new project to Pivotal Tracker.
      You can set no_owner attribute if you want to leave created project without owner::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.Project()
	  project.name = "My project"
	  project.no_owner = True
	  project = ptracker.projects.add(project)

	  print project.id
      


   .. method:: all()

      :return: list of :class:`~pyvotal.projects.Project` objects

      Returns all user projects::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  for project in ptracker.projects.all():
	      print project.id, project.name
      


   .. method:: get(project_id)

      :param: Integer project id
      :return: :class:`~pyvotal.projects.Project` object

      Returns user project with given id::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(31337)
	  print project.id, project.name
      

Story
------------

