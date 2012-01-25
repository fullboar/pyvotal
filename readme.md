Pyvotal is python client to [pivotal tracker api] (https://www.pivotaltracker.com/help/api?version=v3)

Install
=======

Use [pip] (http://pip-installer.org/):

    pip install pyvotal

Usage
=======

Docs avaliable at [readthedocs.org] (http://readthedocs.org/docs/pyvotal/en/latest/)

Quick example:

    from pyvotal import PTracker
    
    ptracker = PTracker(user='someuser', password='somepassword')
    
    project = p.projects.get(project_id)
    story =  project.stories.get(project_id)
    story.description = "New desc"
    story.save()
    story.add_note("Note text")
    story.add_attachment("FileName", open('/etc/hosts'))
