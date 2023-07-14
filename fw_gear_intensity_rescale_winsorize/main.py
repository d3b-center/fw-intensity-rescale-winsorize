"""Main module."""
import logging
import os

from fw_core_client import CoreClient
from flywheel_gear_toolkit import GearToolkitContext
import flywheel
import nibabel as nib

from .run_level import get_analysis_run_level_and_hierarchy
from .normalize_images import scale_winorize

log = logging.getLogger(__name__)

fw_context = flywheel.GearContext()
fw = fw_context.client

def run(file_path, gtk_context: GearToolkitContext):
    """Processes file at file_path.

    Args:
        file_type (str): String defining file type.
        file_path (AnyPath): A Path-like to file input.
        project (flywheel.Project): The flywheel project the file is originating
            (Default: None).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.

    """
    destination_id = gtk_context.destination["id"] # if gear is run on a file, this is the acquisition ID
    hierarchy = get_analysis_run_level_and_hierarchy(gtk_context.client, destination_id)
    sub_label = hierarchy['subject_label']
    ses_label = hierarchy['session_label']
    project_label = hierarchy['project_label']
    group_name = hierarchy['group']
    acq_label = hierarchy['acquisition_label']

    log.info(f"Normalizing the input image : {file_path}")
    normalized_image = scale_winorize(file_path)

    # find the acquisition that the input file came from
    dest_path = f'{group_name}/{project_label}/{sub_label}/{ses_label}/{acq_label}'

    # define the output file name based on the input file name
    in_fname = os.path.basename(file_path)
    if '.nii.gz' in in_fname:
        in_fname_suffix = in_fname.split('.nii.gz')[0]
        in_fname_ending = '.nii.gz'
    else:
        in_fname_suffix = os.path.splitext(in_fname)[0]
        in_fname_ending = os.path.splitext(in_fname)[-1]
    out_fname = in_fname_suffix + '_scaled' + in_fname_ending

    # save the normalized image to the instance
    nib.save(normalized_image, out_fname)
    
    # upload the normalized file to the target acquisition
    log.info(f"Saving output file {out_fname} to: {dest_path}")
    fw.upload_file_to_acquisition(destination_id, out_fname)
    os.remove(out_fname)
