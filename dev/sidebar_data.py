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
        'Vision tutorial': '/tutorial.transfer.learning',
        'Pets tutorial': '/pets.tutorial',
        'Imagenette tutorial': '/tutorial.imagenette',
        'UlMFiT tutorial': '/tutorial.ulmfit',
        'Wikitext tutorial': '/tutorial.wikitext'
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
                'RNN': '/callback.rnn',
                'Progress': '/callback.progress'
            }
        },
    },
    'Data': {
        'Data Blocks': '/data.block',
        'Data Transforms': '/data.transforms',
        'Data External': '/data.external',
        'Data Core': '/data.core',
        'DataLoader': '/data.load',
    },
    'Core': {
        'Core': '/core',
        'Utility functions': '/utils',
        'PyTorch Core': '/torch_core',
        'Type dispatch': '/dispatch',
        'Transforms and Pipelines': '/transform',
        'Layers': '/layers',
        'Test': '/test',
        'Script': '/script',
    },
    'Vision': {
        'Vision Core': '/vision.core',
        'Vision Learner': '/vision.learner',
        'Vision Data Augmentation': '/vision.augment',
        '': {
            'Models': {
                'XResnet': '/vision.models.xresnet',
            }
        },
    },
    'Text': {
        'Text Core': '/text.core',
        'Text Data': '/text.data',
        'Text Learner': '/text.learner',
        '': {
            'Models': {
                'Core': '/text.models.core',
                'AWD LSTM': '/text.models.awdlstm',
                'QRNN': '/text.models.qrnn',
            }
        },
    },
    'Tabular': {
        'Tabular Core': '/tabular.core',
        'Tabular Model': '/tabular.model',
        'RapidsAI': '/tabular.rapids',
    },
    'Medical': {
        'Medical imagery': '/medical.imaging',
        'Medical text': '/medical.text',
    },
    'Notebook': {
        'Export to modules': '/notebook.export',
        'Convert to html': '/notebook.export2html',
        'Show doc': '/notebook.showdoc',
        'Test functions': 'notebook.test',
        'Core functions': 'notebook.core',
    },
}
