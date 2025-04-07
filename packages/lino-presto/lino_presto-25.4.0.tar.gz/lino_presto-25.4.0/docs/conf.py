# -*- coding: utf-8 -*-

# from rstgen.sphinxconf import interproject
# interproject.configure(globals(), 'atelier etgen')

from atelier.sphinxconf import configure

configure(globals())
from lino.sphinxcontrib import configure

configure(globals(), 'lino_presto.projects.presto1.settings.doctests')

extensions += ['lino.sphinxcontrib.logo']
project = "Lino Presto"
copyright = '2018-2021 Rumma & Ko Ltd'

extensions += ['lino.sphinxcontrib.help_texts_extractor']
help_texts_builder_targets = {'lino_presto.': 'lino_presto.lib.presto'}

# html_context.update(public_url='https://lino-framework.gitlab.io/presto/')
