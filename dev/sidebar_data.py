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
    'Tutorials': {
        'Pets tutorial': '/pets.tutorial',
        'Imagenette tutorial': '/tutorial.imagenette'
    },
    'Training': {
        'Training loop': '/learner',
        'Optimizer': '/optimizer',
        'Metrics': '/metrics',
        '': {
            'Callbacks': {
                'Schedulers': '/callback.schedule',
                'Hooks and callbacks': '/callback.hook',
                'Mixed precision': '/callback.fp16',
                'Mixup': '/callback.mixup',
                'Trackers': '/callback.tracker',
                'Progress': '/callback.progress'
            }
        },
    },
    'Data': {
        'Data Transforms': '/data.transforms',
        'Data Pipeline': '/data.pipeline',
        'Data Source': '/data.source',
        'Data External': '/data.external',
        'Data Core': '/data.core',
    },
    'Notebook': {
        'Export to modules': '/notebook.export',
        'Convert to html': '/notebook.export2html',
        'Show doc': '/notebook.showdoc',
        'Core functions': 'notebook.core',
    },
    'Core': {
        'Layers': '/layers',
        'Core': '/core',
        'Test': '/test',
    },
}
