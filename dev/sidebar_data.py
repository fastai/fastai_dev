# Usage: After editing this file, next run:
#
# tools/make_sidebar.py
# git commit docs/_data/sidebars/home_sidebar.yml docs_src/sidebar/sidebar_data.py
# git push

# This dict defines the structure:

sidebar_d = {
    'Getting started': {
        'Installation': 'https://github.com/fastai/fastai/blob/master/README.md#installation',
        #'Installation Extras': '/install',
        #'Troubleshooting': '/troubleshoot',
        #'Performance': '/performance',
        #'Support': '/support'
    },
    'Data': {
        'Data Pipeline': '/data.pipeline',
        'Data Source': '/data.source',
        'Data Core': '/data.core',
    },
    'Notebook': {
        'Export to modules': '/notebook.export',
        'Convert to html': '/notebook.export2html',
        'Show doc': '/notebook.showdoc'
    },
    'Core': {
        'Core': '/core',
        'Test': '/test'
    },
}
