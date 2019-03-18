from zipfile import ZipFile
import glob
from torchpie.logging import logger


def snapshot_as_zip(name: str, file_list: list = None, patterns=['**/*.py']):
    with ZipFile(name, 'w') as zf:

        if file_list is None:
            file_list = []
        for pattern in patterns:
            file_list.extend(glob.glob(pattern))

        for filename in file_list:
            zf.write(filename)

        logger.info('taking a snapshot of \n{}'.format(file_list))
