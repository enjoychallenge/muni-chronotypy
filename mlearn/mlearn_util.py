import logging
from pandas import set_option


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(levelname)s]:\t%(message)s')
logger = logging.getLogger(__name__)


def print_dataset_info(dataset, grouping_column):
    # logger.info(f"  Scattering matrix")
    # scatter_matrix(dataset)
    # logger.info(f"  Showing pyplot")
    # pyplot.show()

    set_option('display.width', 100)
    set_option('precision', 2)
    logger.info('****************************************************************************************************')
    logger.info(f'Describe each attribute\n{dataset.describe()}')

    logger.info('****************************************************************************************************')
    count_class = dataset.groupby(grouping_column).size()
    logger.info(f'Show target data distribution\n{count_class}')

    logger.info('****************************************************************************************************')
    correlations = dataset.corr(method='pearson')
    logger.info(f'Show correlation between attributes\n{correlations}')

    unstack_correlations = correlations.abs().unstack()
    logger.info(f'unstack_correlations\n{unstack_correlations}')
    pairs_to_drop = set()
    cols = correlations.columns
    for i in range(0, correlations.shape[1]):
        for j in range(0, i + 1):
            pairs_to_drop.add((cols[i], cols[j]))
    au_corr = unstack_correlations.drop(labels=pairs_to_drop).sort_values(ascending=False)
    # au_corr = unstack_correlations.sort_values(ascending=False)
    logger.info(f'Highest correlations\n{au_corr[0:20]}')

    logger.info('****************************************************************************************************')
    logger.info(f'Show attribute skewness\n{dataset.skew()}')
