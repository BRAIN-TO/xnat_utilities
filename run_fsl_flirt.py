import os
import os.path as op

import pkg_resources as pkgr
from nipype.interfaces import fsl
from nipype.interfaces import utility as niu
from nipype.pipeline import engine as pe

from niworkflows.engine.workflows import LiterateWorkflow as Workflow

from sys import argv

script, in_file, reference, wm_seg, fieldmap = argv

def run_fsl_flirt(in_file, reference, wm_seg, fieldmap, cost_function, schedule, nosearch_resample_sample, in_matrix_file):
    """ 
    This runs fsl FLIRT with same parameters as in fMRIPrep
    
    Default parameters:
    dof = 6
    """
    flt = fsl.FLIRT(in_file = in_file, reference = reference, cost = cost_function)
    flt.inputs.wm_seg = wm_seg
    flt.inputs.dof = 6
    flt.inputs.args = "-basescale 1"
    if fieldmap != 'nofieldmap':
        flt.inputs.fieldmap = fieldmap
    if schedule:
        flt.inputs.schedule = schedule
    flt.inputs.no_search = nosearch_resample_sample
    flt.inputs.no_resample = nosearch_resample_sample
    flt.inputs.no_resample_blur = nosearch_resample_sample
    if in_matrix_file:
        flt.inputs.in_matrix_file = in_file.split(".")[0] + "_flirt.mat"
    print(f"\nProcessing\n{flt.cmdline}\n")
    res = flt.run()
    
def run_fsl_epi_reg(in_file, reference, reference_brain, fieldmap):
    epireg = fsl.EpiReg(epi = in_file, t1_head = reference, t1_brain = reference_brain)
    if fieldmap != 'nofieldmap':
        epireg.inputs.fmap = fieldmap
    print(f"\nProcessing\n{epireg.cmdline}\n")


FSLDIR = os.getenv('FSLDIR')
bbrschedule = os.path.join(FSLDIR, 'etc/flirtsch/bbr.sch')

run_fsl_flirt(in_file, reference, wm_seg, fieldmap, cost_function='normmi', schedule ='', nosearch_resample_sample = True, in_matrix_file = False)
run_fsl_flirt(in_file, reference, wm_seg, fieldmap, cost_function='bbr', schedule = bbrschedule, nosearch_resample_sample = False, in_matrix_file = True)