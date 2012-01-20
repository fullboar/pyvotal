
API
======

.. contents ::

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

      Adds new project to Pivotal Tracker.
      You can set no_owner attribute if you want to leave created project without owner

      :param project: :class:`~pyvotal.projects.Project`
      :return: :class:`~pyvotal.projects.Project`

      ::

          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.Project()
	  project.name = "My project"
	  project.no_owner = True
	  project = ptracker.projects.add(project)

	  print project.id
	        
	

   .. method:: all()
      
      Returns all user`s projects.

      :return: list of :class:`~pyvotal.projects.Project` objects

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  for project in ptracker.projects.all():
	      print project.id, project.name
      


   .. method:: get(project_id)
      
      Returns user`s project with given id

      :param project_id: Integer project id
      :return: :class:`~pyvotal.projects.Project` object


      ::
      
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

      Adds new member to project.

      :param membership: :class:`~pyvotal.memberships.Membership`
      :return:  :class:`~pyvotal.memberships.Membership`

      ::
      
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

      Returns all project`s memberships

      :return: list of :class:`~pyvotal.memberships.Membership` objects

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  
	  for membership in project.memberships.all():
	      print membership.id, membership.role, membership.person.email
          


   .. method:: get(membership_id)

      Returns project`s membership with given id.

      :param membership_id: Integer membership id
      :return: :class:`~pyvotal.memberships.Membership` object

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  membership = projects.memberships.get(1232)
	  print membership.id, membership.role, membership.person.email


   .. method:: delete(membership_id)

      Deletes membership with given id

      :param membership_id: Integer membership id
      :return: Deleted :class:`~pyvotal.memberships.Membership` object

      ::
      
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

      Returns project`s iterations, optionally filtered by group. For done iterations, offset should be negative, relative to the most recent done iteration

      :param filter: Iterations group: done, current, backlog, or current_backlog.
      :param limit: Max number of iterations to return
      :param offset: Number of iterations to skip

      :return: list of :class:`~pyvotal.iterations.Iteration` objects

      ::
      
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

      Adds new story to project.

      :param story: :class:`~pyvotal.stories.Story`
      :return:  :class:`~pyvotal.stories.Story`

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')
	  story = ptracker.Story()
	  story.type = "feature"
	  story.name = "New story"
	  project = ptracker.projects.get(1231)
	  story = project.stories.add(story)

	  print story.id
      

   .. method:: all(limit=None, offset=None, **kwargs)

     Returns optionally filtered project`s stories.
     
     :param limit: Max number of stories to return
     :param offset: Number of stories to skip
     :param kwargs: You can optionally pass filter options as described here https://www.pivotaltracker.com/help#howcanasearchberefined.
     :return: list of :class:`~pyvotal.stories.Story` objects

     ::
      
         from pyvotal import PTracker
	  
	 ptracker = PTracker(token='token')

	 project = ptracker.projects.get(1231)
	  
	 for story in project.stories.all(type="Feature", state="unstarted", limit=10, offset=20):
	     print story.id, story.name, story.description


   .. method:: get(story_id)

      Returns project`s story with given id

      :param story_id: Integer story id
      :return: :class:`~pyvotal.stories.Story` object


      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  story = projects.stories.get(1232)
	  print story.id, story.name, story.description


   .. method:: delete(story_id)

      Deletes story with given id.

      :param story_id: Id of story to delete.
      :return: Deleted :class:`~pyvotal.stories.Story` object

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')

	  project = ptracker.projects.get(1231)
	  story = projects.stories.delete(1232)
	  print "Story", story.id, story.name, "deleted"


.. autoclass:: pyvotal.stories.Story
  :members:



Tasks
--------
.. autoclass:: pyvotal.tasks.TaskManager
   :members:

   .. method:: add(task)

      Adds new task to story.

      :param task: :class:`~pyvotal.tasks.Task`
      :return:  :class:`~pyvotal.tasks.Task`

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')
	  story = ptracker.Story()
	  story.id = story_id
	  story.project_id = project_id
	 
	  task = ptracker.Task()
	  task.description = "clean shields"
	  task = story.tasks.add(task)
	  print "Task", task.id, "added"
      

   .. method:: all()

     Returns story`s tasks.
     
     :return: list of :class:`~pyvotal.tasks.Task` objects

     ::
      
         from pyvotal import PTracker
	  
	 ptracker = PTracker(token='token')
	 story = ptracker.Story()
	 story.id = story_id
	 story.project_id = project_id
	  
	 for task in story.tasks.all():
	     print task.id, task.description


   .. method:: get(task_id)

      Returns story`s task with given id.

      :param task_id: Integer task id
      :return: :class:`~pyvotal.tasks.Task` object

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')
	  story = ptracker.Story()
	  story.id = story_id
	  story.project_id = project_id

	  task = story.tasks.get(task_id)
	  print task.id, task.description

   .. method:: delete(task_id)

      Deletes task with given id

      :param task_id: Id of task to delete.
      :return: Deleted :class:`~pyvotal.tasks.Task` object

      ::
      
          from pyvotal import PTracker
	  
	  ptracker = PTracker(token='token')
	  story = ptracker.Story()
	  story.id = story_id
	  story.project_id = project_id

	  task = story.tasks.delete(task_id)
	  print "Task", task.id, task.description, "deleted"


.. autoclass:: pyvotal.tasks.Task
  :members:



   
        
     
