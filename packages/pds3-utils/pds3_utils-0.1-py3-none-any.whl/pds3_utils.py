#!/usr/bin/python
"""
pds3_utils.py

Mark S. Bentley (mark@lunartech.org), 2021

A module containing a set of PDS3 utilities 

"""

# Internal modules

import glob
import os
import logging
from functools import reduce

try:
   import cPickle as pickle
except:
   import pickle

# External dependencies
import pvl
import pandas as pd
import numpy as np
import yaml

log = logging.getLogger(__name__)

default_config = os.path.join(
    os.environ.get('APPDATA') or
    os.environ.get('XDG_CONFIG_HOME') or
    os.path.join(os.environ['HOME'], '.config'),
    "pds_dbase.yml")



def index_products(directory='.', pattern='*.LBL', recursive=True):
    """
    Accepts a directory containing PDS3 products, indexes the labels and returns a 
    Pandas data-frame containng meta-data for each product.
    """

    # recursively find all labels
    labels = select_files(pattern, directory=directory, recursive=recursive)

    cols = ['filename', 'dataset', 'mission_id', 'prod_id', 'start_time', 'stop_time', 'instr_id']
    index = []

    for label in labels:

        lbl = pvl.load(label)

        prod_id = lbl['PRODUCT_ID']
        instr_id = lbl['INSTRUMENT_ID']
        dataset = lbl['DATA_SET_ID']
        mission_id = lbl['MISSION_ID']
        start_time = lbl['START_TIME']
        start_time = pd.to_datetime(start_time) # add logic for non times, check for key errors
        stop_time = lbl['STOP_TIME']
        stop_time = pd.to_datetime(stop_time)

        index.append({
            'filename': label,
            'dataset': dataset,
            'prod_id': prod_id,
            'mission_id': mission_id,
            'start_time': start_time,
            'stop_time': stop_time,
            'instr_id': instr_id
            })


    index = pd.DataFrame.from_records(index)

    # make sure timestamps are stripped of timezones
    index.start_time=pd.to_datetime(index.start_time.fillna(pd.NaT)).dt.tz_localize(None)
    index.stop_time=pd.to_datetime(index.stop_time.fillna(pd.NaT)).dt.tz_localize(None)

    log.info('{:d} PDS3 labels indexed'.format(len(index)))

    return index



class Database:

    def __init__(self, files=None, directory='.', config_file=default_config, recursive=True):
        
        from yaml.scanner import ScannerError

        # read configuration file (YAML format)
        try:
            f = open(config_file, 'r')
            self.config = yaml.load(f, Loader=yaml.SafeLoader)
            log.debug('configuration file loaded with {:d} templates'.format(len(self.config)-1))
        except FileNotFoundError:
            log.error('config file {:s} not found'.format(config_file))
            return None
        except ScannerError as e:
            log.error('error loading YAML configuration file (error: {:s})'.format(e.problem))
            return None


        # build an initial index
        if files is not None:
            self.index = index_products(directory=directory, pattern=files, recursive=recursive)
        else:
            self.index = index_products(directory=directory, pattern='*.LBL', recursive=recursive)
        
        self.dbase = {}
        # build the database according to the config file and indexed
        self.build()


    def build(self):

        # group by product types
        instr_ids = self.index.instr_id.unique()

        for instr_id in instr_ids:

            if instr_id not in self.config.keys():
                log.warn('no configuration found for instrument ID {:s}, skipping ingestion'.format(instr_id))
                continue

            rules = self.config[instr_id]
            
            # see which products in the index match this product pattern and instrument ID
            for name in rules:

                log.debug('processing {:s} products for rule {:s}'.format(instr_id, name))
                prod_id = self.config[instr_id][name]['prod_id']
                prods = self.index[ (self.index.instr_id==instr_id) & (self.index.prod_id.str.contains(prod_id))]

                if len(prods) == 0:
                    continue

                # create a new dataframe (index as per the product index)
                keywords = self.config[instr_id][name]['keywords'].keys()
                dbase = pd.DataFrame([], columns=keywords, index=prods.index)

                # now we need to parse the file for the listed meta-data
                for idx, product in prods.iterrows():

                    label = pvl.load(product.filename)
                    log.debug('processing label {:s}'.format(product.filename))
                    
                    # for each keyword/path pair in the config, populate the database
                    for keyword in keywords:
                        # from the path keyword get a slash separated path
                        path = self.config[instr_id][name]['keywords'][keyword]
                        # get_value accepts a slash separated nested dictionary path
                        result = get_value(label, path['path'])
                        # none is returned if the dictionary key does not exist
                        if result is None:
                            dbase[keyword].loc[idx] = None
                            log.warning('meta-data for keyword {:s} not found in product {:s}'.format(
                                keyword, product.prod_id))
                        else:
                            # there are a few cases to deal with here
                            # firstly it could be set to "N/A"
                            if result=='N/A':
                                result = None

                            # if the returned value is a list (multi value) the user should specify one field per element
                            # using the index keyword
                            array_idx = path.get('index')
                            if array_idx is not None and result is not None:
                                result = list(result)[array_idx]

                            # there are also values which have attached units. for simplicity we check for this
                            # and simply return the value
                            if isinstance(result, pvl.collections.Quantity):
                                result = result.value
                            
                            # at the end this is written into the appropriate element in the dbase DataFrame
                            dbase[keyword].loc[idx] = result

                self.dbase.update({name: dbase})
                log.info('database table {:s} created for {:d} products'.format(name, len(dbase)))

        return 

    def list_tables(self):

        if len(self.dbase) == 0:
            log.warn('no tables found - use build() to create')
        else:
            log.info('{:d} tables found: {:s}'.format(len(self.dbase), ', '.join(self.dbase.keys())))
        return

    def get_table(self, table):

        if table not in self.dbase.keys():
            log.error('table {:s} not found'.format(table))
            return None
        else:
            return self.index.join(self.dbase[table], how='inner')

    def save_dbase(self, filename='database.pkl', directory='.'):
        
        pkl_f = open(os.path.join(directory, filename), 'wb')
        pickle.dump((self.index, self.dbase), file=pkl_f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_dbase(self, filename='database.pkl'):

        f = open(filename, 'rb')
        self.index, self.dbase = pickle.load(f)
        self.list_tables()





def get_datasets(arc_path='.', latest=True):
    """Scans PDS3 datasets in the directory given by arc_path= and
    returns the dataset ID and start/stop times for each.
    
    If latest=True then only the latest version of each dataset is
    returned, otherwise all versions are returned."""

    # Build a live list of archive datasets and their start/stop times

    # look at CATALOG/DATASET.CAT for start/stop times
    catalogues = locate('DATASET.CAT', arc_path)
    catalogues = [file for file in catalogues]

    if len(catalogues)==0:
        log.error('no catalogue files found')
        return None

    dsets = {}

    for cat in catalogues:
        label = pvl.load(cat)
        start = label['DATA_SET']['DATA_SET_INFORMATION']['START_TIME']
        stop = label['DATA_SET']['DATA_SET_INFORMATION']['STOP_TIME']
        dset_id = label['DATA_SET']['DATA_SET_ID']
        vid = float(dset_id.split('-V')[-1])
        lid = dset_id.split('-V')[0]
        dsets.update({dset_id: (start, stop, lid, vid)})

    dsets = pd.DataFrame(dsets).T
    dsets.columns=['start_time', 'stop_time', 'lid', 'vid']
    dsets.sort_values(['lid', 'vid'], inplace=True)

    if latest:
        dsets.drop_duplicates('lid', keep='last', inplace=True)

    return dsets


def get_products(arc_path='.', what='data', latest=True):
    """Scans PDS3 datsets in the directory given by arc_path=
    and returns the dataset, product IDs and paths to each product.
    what can be
        data - all products in the data collections
        images - all midas images
        all - every product in the dataset"""

    log.debug('indexing PDS products in root %s' % arc_path)

    valid = ['data', 'images', 'all']
    if what not in valid:
        log.error('option what not valid!')
        return None

    cols = ['dataset', 'prod_id', 'start']
    products = pd.DataFrame([], columns=cols)

    dsets = get_datasets(arc_path, latest=latest)
    for idx, dset in dsets.iterrows():
        log.debug('processing dataset %s' % dset)
        dset_root = os.path.join(arc_path, dset.name)
        if what == 'images':
            image_root = os.path.join(dset_root, 'DATA/IMG') 
            labels = select_files('*.LBL', directory=image_root, recursive=True)
        elif what == 'data':
            data_root = os.path.join(dset_root, 'DATA')
            labels = select_files('*.LBL', directory=data_root, recursive=True)
        else:
            labels = select_files('*.LBL', directory=dset_root, recursive=True)
        for lab in labels:
            label = pvl.load(lab)
            prod_id = label['PRODUCT_ID'].encode()
            start = pd.Timestamp(label['START_TIME']) if 'START_TIME' in label.keys() else pd.NaT
            products = products.append(pd.DataFrame([[dset.name, prod_id, start]], columns=cols), ignore_index=True)

    products.sort_values('start', inplace=True)
    log.info('located %d products in %d datasets' % (len(products), len(dsets)))

    return products



def select_files(wildcard, directory='.', recursive=False):
    """Create a file list from a directory and wildcard - recusively if
    recursive=True"""

    # recursive search
    # result = [os.path.join(dp, f) for dp, dn, filenames in os.walk('.') for f in filenames if os.path.splitext(f)[1] == '.DAT']

    if recursive:
        selectfiles = locate(wildcard, directory)
        filelist = [file for file in selectfiles]
    else:
        filelist = glob.glob(os.path.join(directory, wildcard))

    filelist.sort()

    return filelist



def locate(pattern, root_path):
    """Returns a generator using os.walk and fnmatch to recursively
    match files with pattern under root_path"""

    import fnmatch

    for path, dirs, files in os.walk(os.path.abspath(root_path)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)


def get_value(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split('/'), dictionary)