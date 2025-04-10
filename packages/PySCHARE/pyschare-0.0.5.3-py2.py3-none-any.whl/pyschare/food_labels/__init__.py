from .data_labels import get_labels
from .create_labels import print_labels


labels = get_labels()
printlabels = print_labels()

__all__=['labels', 'printlabels']