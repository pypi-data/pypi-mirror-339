#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input/output functions - Gaussian Linear Hidden Markov Model
@author: Diego Vidaurre 2023
"""

import numpy as np
import scipy.special
import scipy.io
import pickle
import os
import warnings
import h5py
from zipfile import ZipFile
from tqdm import tqdm
from pathlib import Path
import requests

from . import glhmm
from . import auxiliary

def load_files(files,I=None,do_only_indices=False):
    """
    Loads data from files and returns the loaded data, indices, and individual indices for each file.
    """       

    X = []
    Y = []
    indices = []
    indices_individual = []
    sum_T = 0

    if I is None:
        I = np.arange(len(files))
    elif type(I) is int:
        I = np.array([I])

    for ij in range(I.shape[0]):

        j = I[ij]

        # if type(files[j]) is tuple:
        #     if len(files[j][0]) > 0: # X
        #         if files[j][0][-4:] == '.npy':
        #             X.append(np.load(files[j][0]))
        #         elif files[j][0][-4:] == '.txt':

        if files[j][-4:] == '.mat':
            # depending on the matlab version used to create the data, 
            #scipy.io or h5py will be used to load them
            try:
                dat = scipy.io.loadmat(files[j])
            except:
                dat = h5py.File(files[j],'r')
                

        elif files[j][-4:] == '.npz':
            dat = np.load(files[j])
            
        if not do_only_indices:
            if ('X' in dat) and (not 'Y' in dat): 
                Y.append(np.array(dat["X"]))
            else:
                if 'X' in dat: X.append(np.array(dat["X"]))
                Y.append(np.array(dat["Y"]))
        if 'indices' in dat: 
            ind = np.array(dat['indices'])
        elif 'T' in dat:
            ind = auxiliary.make_indices_from_T(np.array(dat['T']))
        else:
            ind = np.zeros((1,2)).astype(int)
            ind[0,0] = 0
            ind[0,1] = Y[-1].shape[0]
        if len(ind.shape) == 1: ind = np.expand_dims(ind,axis=0)
        indices_individual.append(ind)
        indices.append(ind + sum_T)

        sum_T += dat["Y"].shape[0]

    if not do_only_indices:
        if len(X) > 0: X = np.concatenate(X)
        Y = np.concatenate(Y)
    indices = np.concatenate(indices)
    if len(indices.shape) == 1: indices = np.expand_dims(indices,axis=0)
    if len(X) == 0: X = None

    return X,Y,indices,indices_individual


def read_flattened_hmm_mat(file):
    """
    Reads a MATLAB file containing hidden Markov model (HMM) parameters from the HMM-MAR toolbox, 
    and initializes a Gaussian linear hidden Markov model (GLHMM) using those parameters.
    """
    
    hmm_mat = scipy.io.loadmat(file)

    K = hmm_mat["K"][0][0]
    covtype = hmm_mat["train"]["covtype"][0][0][0]
    zeromean = hmm_mat["train"]["zeromean"][0][0][0][0]
    if not zeromean: model_mean = 'state'
    else: model_mean = 'no'
    if "state_0_Mu_W" in hmm_mat: 
        if (model_mean == 'state') and (hmm_mat["state_0_Mu_W"].shape[0] == 1):
            model_beta = 'no'
        elif hmm_mat["state_0_Mu_W"].shape[0] == 0:
            model_beta = 'no'
        else:
            model_beta = 'state'
    else: 
        model_beta = 'no'
    dirichlet_diag = hmm_mat["train"]["DirichletDiag"][0][0][0][0]
    connectivity = hmm_mat["train"]["S"][0][0]
    Pstructure = np.array(hmm_mat["train"]["Pstructure"][0][0], dtype=bool)
    Pistructure = np.squeeze(np.array(hmm_mat["train"]["Pistructure"][0][0], dtype=bool))
    shared_covmat = (covtype == 'shareddiag') or (covtype == 'sharedfull') 
    diagonal_covmat = (covtype == 'shareddiag') or (covtype == 'diag') 

    if "prior_Omega_Gam_rate" in hmm_mat:
        prior_Omega_Gam_rate = hmm_mat["prior_Omega_Gam_rate"]
        prior_Omega_Gam_shape = hmm_mat["prior_Omega_Gam_shape"][0][0]
    else:
        prior_Omega_Gam_rate = hmm_mat["state_0_prior_Omega_Gam_rate"]
        prior_Omega_Gam_shape = hmm_mat["state_0_prior_Omega_Gam_shape"][0][0]    
    if diagonal_covmat: prior_Omega_Gam_rate = np.squeeze(prior_Omega_Gam_rate)
    q = prior_Omega_Gam_rate.shape[0]

    if "state_0_Mu_W" in hmm_mat:
        p = hmm_mat["state_0_Mu_W"].shape[0]
        if model_mean == 'state': p -= 1
    else: p = 0

    hmm = glhmm.glhmm(
        K=K,
        covtype=covtype,
        model_mean=model_mean,
        model_beta=model_beta,
        dirichlet_diag=dirichlet_diag,
        connectivity=connectivity,
        Pstructure=Pstructure,
        Pistructure=Pistructure
        )

    # mean 
    if model_mean == 'state':
        hmm.mean = []
        for k in range(K):
            hmm.mean.append({})
            Sigma_W = np.squeeze(hmm_mat["state_" + str(k) + "_S_W"])
            Mu_W = np.squeeze(hmm_mat["state_" + str(k) + "_Mu_W"])
            if model_beta == 'state':
                if q==1: hmm.mean[k]["Mu"] = np.array(Mu_W[0])
                else: hmm.mean[k]["Mu"] = Mu_W[0,:]
            else: 
                if q==1: hmm.mean[k]["Mu"] = np.array(Mu_W)
                else: hmm.mean[k]["Mu"] = Mu_W
            if diagonal_covmat:
                if model_beta == 'state':
                    if q==1: hmm.mean[k]["Sigma"] = np.array([[Sigma_W[0,0]]])
                    else: hmm.mean[k]["Sigma"] = np.diag(Sigma_W[:,0,0])
                else:
                    if q==1: hmm.mean[k]["Sigma"] = np.array([[Sigma_W]])
                    hmm.mean[k]["Sigma"] = np.diag(Sigma_W)
            else:
                if q==1: np.array([[Sigma_W[0,0]]])
                else: hmm.mean[k]["Sigma"] = Sigma_W[0:q,0:q]

    # beta
    if model_beta == 'state':
        if model_mean == 'state': j0 = 1
        else: j0 = 0
        hmm.beta = []
        for k in range(K):
            hmm.beta.append({})
            Sigma_W = hmm_mat["state_" + str(k) + "_S_W"]
            Mu_W = hmm_mat["state_" + str(k) + "_Mu_W"]
            hmm.beta[k]["Mu"] = np.zeros((p,q))
            hmm.beta[k]["Mu"][:,:] = Mu_W[j0:,:]
            if diagonal_covmat:
                hmm.beta[k]["Sigma"] = np.zeros((p,p,q))
                if q==1:
                    hmm.beta[k]["Sigma"][:,:,0] = Sigma_W[j0:,j0:]
                else:
                    for j in range(q):
                        hmm.beta[k]["Sigma"][:,:,j] = Sigma_W[j,j0:,j0:]
            else:
                hmm.beta[k]["Sigma"] = Sigma_W[(j0*q):,(j0*q):]

    hmm._glhmm__init_priors_sub(prior_Omega_Gam_rate,prior_Omega_Gam_shape,p,q)
    hmm._glhmm__update_priors()

    # covmatrix
    hmm.Sigma = []
    if diagonal_covmat and shared_covmat:
        hmm.Sigma.append({})
        hmm.Sigma[0]["rate"] = np.zeros(q)
        hmm.Sigma[0]["rate"][:] = hmm_mat["Omega_Gam_rate"]
        hmm.Sigma[0]["shape"] = hmm_mat["Omega_Gam_shape"][0][0]
    elif diagonal_covmat and not shared_covmat:
        for k in range(K):
            hmm.Sigma.append({})
            hmm.Sigma[k]["rate"] = np.zeros(q)
            hmm.Sigma[k]["rate"][:] = hmm_mat["state_" + str(k) + "_Omega_Gam_rate"]
            hmm.Sigma[k]["shape"] = hmm_mat["state_" + str(k) + "_Omega_Gam_shape"][0][0]
    elif not diagonal_covmat and shared_covmat:
        hmm.Sigma.append({})
        hmm.Sigma[0]["rate"] = hmm_mat["Omega_Gam_rate"]
        hmm.Sigma[0]["irate"] = hmm_mat["Omega_Gam_irate"]
        hmm.Sigma[0]["shape"] = hmm_mat["Omega_Gam_shape"][0][0]
    else: # not diagonal_covmat and not shared_covmat
        for k in range(K):
            hmm.Sigma.append({})
            hmm.Sigma[k]["rate"] = hmm_mat["state_" + str(k) + "_Omega_Gam_rate"]
            hmm.Sigma[k]["irate"] = hmm_mat["state_" + str(k) + "_Omega_Gam_irate"]
            hmm.Sigma[k]["shape"] = hmm_mat["state_" + str(k) + "_Omega_Gam_shape"][0][0]

    #hmm.init_dynamics()
    hmm.P = hmm_mat["P"]
    hmm.Pi = np.squeeze(hmm_mat["Pi"])
    hmm.Dir2d_alpha = hmm_mat["Dir2d_alpha"]
    hmm.Dir_alpha = np.squeeze(hmm_mat["Dir_alpha"])
    
    hmm.trained = True
    
    return hmm


def save_hmm(hmm, filename, directory=None):
    """
    Save a glhmm object in the specified directory with the given filename.

    Parameters:
    -----------
    hmm (object)
        The glhmm object to be saved.
    filename (str)
        The name of the file to which the object will be saved.
    directory (str, optional), default=None:
        The directory where the file will be saved. If None, saves in the current working directory.

    """
    # Combine the directory path and filename
    if directory:
        # Ensure the directory exists, create it if not
        if not os.path.exists(directory):
            print(f"Created a folder here: {directory}")
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        
    else:
        filepath = filename
    
    # Save the glhmm object to the specified file
    with open(filepath, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(hmm, outp, pickle.HIGHEST_PROTOCOL)
    
    print(f"{filename} saved to: {filepath}") if directory else print(f"{filename} saved")
        

def load_hmm(filename, directory=None):
    """
    Load a glhmm object from the specified file.

    Parameters:
    -----------
    filename (str):
        Name of the file containing the glhmm object.
    directory (str, optional), default=None:
        Directory where the file is located. If None, searches in the current working directory.

    Returns:
    --------
    glhmm : object
        Loaded glhmm object.
    """
    # Combine the directory path and filename
    if directory:
        filepath = os.path.join(directory, filename)
    else:
        filepath = filename
        
    # Check if the directory exists
    if directory and not os.path.exists(directory):
        warnings.warn(f"The specified directory '{directory}' does not exist.")

    # Load the glhmm object from the specified file
    with open(filepath, 'rb') as inp:
        hmm = pickle.load(inp)
    return hmm



def save_statistics(data_dict, filename='statistics', directory=None, format='npy'):
    """
    Save statistics data to a file in the specified directory with optional format (npy or npz).

    Parameters
    ----------
    data_dict (dict):
        Dictionary containing statistics data to be saved.
    filename (str, optional), default='statistics':
        Name of the file.
    directory (str, optional), default=None:
        Directory path where the file will be saved (default is the current working directory).
    format (str, optional), default='npy':
        Serialization format ('npy' or 'npz').
    """
    
    # Construct the full file path
    if directory:
        # Ensure the directory exists, create it if not
        if not os.path.exists(directory):
            print(f"Created a folder here: {directory}")
            os.makedirs(directory)
        filepath = os.path.join(directory, f'{filename}.{format}')
    else:
        filepath = f'{filename}.{format}'

    # Save the dictionary to the file using the specified format
    if format == 'npy':
        np.save(filepath, data_dict)
    elif format == 'npz':
        np.savez(filepath, **data_dict)
    else:
        raise ValueError("Invalid format. Use 'npy' or 'npz'.")
    print(f"{filename}.{format} saved to: {filepath}") if directory else print(f"{filename}.{format} saved")

def load_statistics(filename, directory=None):
    """
    Load statistics data from a file.

    Parameters
    ----------
    filename : str
        The name of the file containing the saved statistics data, with or without extension.
    load_directory (str, optional), default=None:
        The directory path where the file is located (default is the current working directory).

    Returns
    -------
    data_dict : dict
        The dictionary containing the loaded statistics data.
    """
    # Set default directory to current working directory if not provided
    directory = directory or os.getcwd()

    # Construct the full file path
    file_path = os.path.join(directory, filename)

    if not os.path.exists(file_path):
        # If the file with the given name does not exist, try adding '.npy' and '.npz' extensions
        file_path_npy = file_path + '.npy'
        file_path_npz = file_path + '.npz'

        if not (os.path.exists(file_path_npy) or os.path.exists(file_path_npz)):
            raise FileNotFoundError(f"File not found: {filename} or {filename}.npy or {filename}.npz")

    try:
        if os.path.exists(file_path):
            # If the file exists with the given name, use it
            # The .item() method extracts the single item from the loaded data.
            data_dict = np.load(file_path, allow_pickle=True).item()
        elif os.path.exists(file_path_npy):
            data_dict = np.load(file_path_npy, allow_pickle=True).item()
        elif os.path.exists(file_path_npz):
            loaded_data = np.load(file_path_npz, allow_pickle=True)
            data_dict = {key: loaded_data[key] for key in loaded_data.files}
    except Exception as e:
        raise ValueError(f"Error loading data from {filename}: {e}")

    return data_dict


def download_file_with_progress_bar(url: str, dest_path: Path):
    """
    Download a file with a progress bar.

    Parameters
    ----------
    url : str
        URL of the file to download.
    dest_path : Path
        Path to save the downloaded file.

    """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad responses
    total_size = int(response.headers.get('content-length', 0))  # Get the file size from headers
    block_size = 1024  # 1 Kilobyte per block

    with open(dest_path, 'wb') as file, tqdm(
        desc=f"Downloading {dest_path.name}",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress:
        for data in response.iter_content(block_size):
            file.write(data)
            progress.update(len(data))

def prepare_data_directory(PATH_DATA: Path, zenodo_url: str = "https://zenodo.org/record/14756003/files/data.zip"):
    """
    Ensure the data directory is prepared. If the specified directory does not exist, 
    download and extract the data from Zenodo.

    Parameters
    ----------
    data_dir : Path
        Path to the specific data directory (e.g., 'data/Procedure_1').
    zenodo_url : str, optional, default='https://zenodo.org/record/14756003/files/data.zip'
        URL of the Zenodo zip file containing the data.

    Returns
    -------
    Path
        Path to the specific data directory where the data is stored.
    """
    # Check if the specific data directory exists
    if PATH_DATA.exists():    
        return PATH_DATA

    # Define the parent directory for downloading and extracting the data
    PATH_PARENT = PATH_DATA.parent.parent # that is the folder of the working directory

    # Define the zip file name in the parent directory
    zip_path = PATH_PARENT / "data.zip"

    # Download the data zip file from Zenodo with a progress bar
    print(f"Downloading data from {zenodo_url}...")
    download_file_with_progress_bar(zenodo_url, zip_path)

    # Extract the zip file
    print(f"Extracting data to {PATH_PARENT}...")
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(PATH_PARENT)
    print(f"Data extracted successfully.")

    # Remove the zip file after extraction
    zip_path.unlink()
    print(f"Removed temporary zip file: {zip_path}.")

    return PATH_DATA
