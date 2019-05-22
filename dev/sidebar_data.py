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
        'Data Pipeline': '/data_pipeline',
        'Data Source': '/data_source',
        'Data Core': '/data_core',
    },
    'Notebook': {
        'Export to modules': '/export',
        'Convert to html': '/export_html',
    },
    'Core': {
        'Core': '/core',
        'Test': '/test'
    },
}
