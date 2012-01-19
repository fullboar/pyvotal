
API
======

PTracker
------------
.. autoclass:: pyvotal.PTracker
   :members:
   :undoc-members:

Projects
--------------
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

      Returns all user`s projects::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  for project in ptracker.projects.all():
	      print project.id, project.name
      


   .. method:: get(project_id)

      :param project_id: Integer project id
      :return: :class:`~pyvotal.projects.Project` object

      Returns user`s project with given id::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(31337)
	  print project.id, project.name


.. autoclass:: pyvotal.projects.Project
   :members:

      

Memberships
--------------
.. autoclass:: pyvotal.memberships.MembershipManager
   :members:

   .. method:: add(membership)

      :param membership: :class:`~pyvotal.memberships.Membership`
      :return:  :class:`~pyvotal.memberships.Membership`

      Adds new member to project::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')
	  membership = ptracker.Membership()
	  membership.role = 'Owner'
	  membership.person.email = 'test@example.com'
	  membership.person.name = 'Anatoly Kudinov'
	  membership.person.initials = 'AK'

	  project = ptracker.projects.get(1231)
	  membership = project.memberships.add(membership)

	  print membership.id
      


   .. method:: all()

      :return: list of :class:`~pyvotal.memberships.Membership` objects

      Returns all project`s memberships::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  
	  for membership im project.memberships.all():
	      print membership.id, membership.role, membership.person.email
          


   .. method:: get(membership_id)

      :param membership_id: Integer membership id
      :return: :class:`~pyvotal.memberships.Membership` object

      Returns project`s membership with given id::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  membership = projects.memberships.get(1232)
	  print membership.id, membership.role, membership.person.email


   .. method:: delete(membership_id)

      :param membership_id: Integer membership id
      :return: Deleted :class:`~pyvotal.memberships.Membership` object

      Deletes membership with given id::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  membership = projects.memberships.delete(1232)
	  print "Membership", membership.id, "deleted"

.. autoclass:: pyvotal.memberships.Membership
   :members:

.. autoclass:: pyvotal.memberships.Person
   :members:


Iterations
------------
.. autoclass:: pyvotal.iterations.IterationManager

   .. method:: all(filter=None, limit=None, offset=None)

      :param filter: Iterations group: done, current, backlog, or current_backlog.
      :param limit: Max number of iterations to return
      :param offset: Number of iterations to skip

      :return: list of :class:`~pyvotal.iterations.Iteration` objects

      Returns project`s iterations, optionally filtered by group. For done iterations, offset should be negative, relative to the most recent done iteration::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  
	  for iteration in project.iterations.all(filter='done', offset=-6):
	      print iteration.id, iteration.number, iteration.finish


.. autoclass:: pyvotal.iterations.Iteration
   :members:

Stories
--------
.. autoclass:: pyvotal.stories.StoryManager
   :members:

   .. method:: add(story)

      :param story: :class:`~pyvotal.stories.Story`
      :return:  :class:`~pyvotal.stories.Story`

      Adds new story to project::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')
	  story = ptracker.Story()
	  story.type = "feature"
	  story.name = "New story"
	  project = ptracker.projects.get(1231)
	  story = project.stories.add(story)

	  print story.id
      

   .. method:: all(limit=None, offset=None, **kwargs)
     
     :param limit: Max number of stories to return
     :param offset: Number of stories to skip
     :param kwargs: You can optionally pass filter options as described here https://www.pivotaltracker.com/help#howcanasearchberefined.
     :return: list of :class:`~pyvotal.stories.Story` objects

     Returns optionally filtered project`s stories::
      
         from pyvotal import PTracker
	  
	 ptracker = PTracker(token='token')

	 project = ptracker.projects.get(1231)
	  
	 for story im project.stories.all(type="Feature", state="unstarted", limit=10, offset=20):
	     print story.id, story.name, story.description


   .. method:: get(story_id)

      :param story_id: Integer story id
      :return: :class:`~pyvotal.stories.Story` object

      Returns project`s story with given id::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  story = projects.stories.get(1232)
	  print story.id, story.name, story.description


   .. method:: delete(story_id)

      :param story_id: Id of story to delete.
      :return: Deleted :class:`~pyvotal.stories.Story` object

      Deletes story with given id::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  story = projects.stories.delete(1232)
	  print "Story", story.id, story.name, "deleted"


.. autoclass:: pyvotal.stories.Story
  :members:



   
        
     
