from atelier.invlib import setup_from_tasks

ns = setup_from_tasks(
    globals(),
    "lino_presto",
    languages="en de fr".split(),
    # tolerate_sphinx_warnings = True,
    blogref_url='https://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_presto/lib/presto/locale',
    cleanable_files=['docs/api/lino_presto.*'],
    demo_projects=['lino_presto.projects.presto1'],
    selectable_languages='en de'.split())
