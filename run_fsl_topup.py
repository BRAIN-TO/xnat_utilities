from builtins import range
import nipype.interfaces.io as nio  # Data i/o
from nipype.interfaces.fsl.epi import TOPUP, ApplyTOPUP
from nipype.interfaces.fsl.preprocess import FUGUE
from nipype.interfaces.fsl.maths import BinaryMaths
import nipype.interfaces.fsl as fsl
import nipype.pipeline.engine as pe  # pypeline engine
from nipype.interfaces.base import Bunch

from sys import argv
import json
import subprocess
import os

script, file1, file2 = argv

json1 = file1.split(".")[0] + ".json"
json2 = file2.split(".")[0] + ".json"
image1 = file1.split(".")[0] + ".nii.gz"
image2 = file2.split(".")[0] + ".nii.gz"
b01 = "b0_" + file1.split(".")[0] + ".nii.gz"
b02 = "b0_" + file2.split(".")[0] + ".nii.gz"

#create the parameter file with C4
try:
    with open(json1, 'r') as json_file:
        data = json.load(json_file)
    value1 = float(data["EffectiveEchoSpacing"])
    value2 = float(data["AcquisitionMatrixPE"])
    c4 = value1 * value2
except FileNotFoundError:
    print("Error: Json file is missing.")
except KeyError:
    print("Error: Effective Echo Spacing and/or Acquisition Matrix PE do not exist.")
        
f = open('acq_param.txt', 'a')
f.write(f"0 -1 0 {c4}\n0 1 0 {c4}")
f.close

def run_nipype_interface():
    #fslroi for b0 image
    fslroi = fsl.ExtractROI(in_file=image1, roi_file=b01, t_min=0, t_size=1)
    res = fslroi.run()
    fslroi = fsl.ExtractROI(in_file=image2, roi_file=b02, t_min=0, t_size=1)
    res = fslroi.run()

    #fslmerge
    merger = fsl.Merge(in_file=[b01,b02], dimension='t', merged_file='both_b0.nii.gz')
    res = merger.run()
    
    #fsl topup
    topup = TOPUP(in_file = "both_b0.nii.gz", encoding_file = "acq_param.txt", out_field = "fieldmap_Hz.nii.gz", out_base = "my_topup")
    res = topup.run()

    #fsl applytopup
    #applytopup = ApplyTOPUP(in_files = [image1, image2], encoding_file = "acq_param.txt", in_topup_fieldcoef = "my_topup_fieldcoef.nii.gz", in_topup_movpar = "my_topup_movpar.txt")
    #res = applytopup.run()

    #fslmath to convert to radian
    fslmaths = BinaryMaths(in_file = "fieldmap_Hz.nii.gz", operation = 'mul', operand_value = 6.28, out_file = "fieldmap_radian.nii.gz")
    res = fslmaths.run()
    
    #fsl fugue
    fugue = FUGUE(in_file = image1, dwell_time = value1, fmap_in_file = "fieldmap_radian.nii.gz", unwarped_file = f"{file1}_corrected.nii.gz", unwarp_direction = "y-", save_shift = True)
    res = fugue.run()

def run_nipype_workflow():
    #fslroi for b0 image
    fslroi = fsl.ExtractROI(in_file=image1, roi_file=b01, t_min=0, t_size=1)
    res = fslroi.run()
    fslroi = fsl.ExtractROI(in_file=image2, roi_file=b02, t_min=0, t_size=1)
    res = fslroi.run()
    
    #fslmerge
    fslmerge = pe.Node(interface=fsl.Merge(), name="fslmerge")
    fslmerge.inputs.dimension = "t"
    fslmerge.inputs.merged_file = "both_b0.nii.gz"
    
    #fsl topup
    topup = pe.Node(interface=TOPUP(), name="topup")
    topup.inputs.encoding_file = "acq_param.txt"
    topup.inputs.out_field = "fieldmap_Hz.nii.gz"

    #fsl applytopup

    #fslmath to convert to radian-change
    fslmaths = pe.Node(interface=BinaryMaths(), name="fslmaths")
    fslmaths.inputs.operation = 'mul'
    fslmaths.inputs.operand_value = 6.28
    fslmaths.inputs.out_file = "fieldmap_radian.nii.gz"

    #fsl fugue
    fugue = pe.Node(interface=FUGUE(), name="fugue")
    fugue.inputs.in_file = image1
    fugue.inputs.dwell_time = value1
    fugue.inputs.unwarped_file = f"{image1}_corrected.nii.gz"
    fugue.inputs.unwarp_direction = "y-"
    fugue.inputs.save_shift = True

    # create the processing workflow
    # connect the outputs to the inputs
    preprocessing = pe.Workflow(name="preprocesing")
    preprocessing.connect(fslmerge, "merged_file", topup, "in_file")
    preprocessing.connect(topup, "out_field", fslmaths, "in_file")
    preprocessing.connect(fslmaths, "out_file", fugue, "fmap_in_file")

    #datasource
    datasource = pe.Node(
        interface=nio.DataGrabber(outfields=['func']), name='datasource')
    datasource.inputs.base_directory = "/home/yuexin/Documents/topup/"
    datasource.inputs.sort_filelist = True
    datasource.inputs.template = 'b0_sub-01_ses-01_task-rest_acq-EP2D_rec-2x2_dir-*_run-1_part-mag_bold.nii.gz'

    #connect preprocessing to datasource
    preprocessing.connect(datasource, 'func', fslmerge, 'in_files')

    #connect datasink to preprocessing
    datasink = pe.Node(interface=nio.DataSink(), name="datasink")
    datasink.inputs.base_directory = os.path.abspath('/home/yuexin/Documents/topup/output/')
    preprocessing.connect(fugue, 'unwarped_file', datasink, 'contrasts.@T')

    #run preprocessing
    preprocessing.config['execution']['job_finished_timeout'] = 60
    preprocessing.run()

def run_command():
    #fslroi for b0 image
    subprocess.run(["fslroi", image1, b01, "0", "1"])
    subprocess.run(["fslroi", image2, b02, "0", "1"])
    
    #fslmerge
    subprocess.run(["fslmerge", "-t", "both_b0.nii.gz", b01, b02])
    
    #fsl topup
    subprocess.run(["topup", "--imain=both_b0.nii.gz", "--datain=acq_param.txt", "--config=b02b0.cnf", "--out=my_topup", "--fout=fieldmap_Hz.nii.gz"])
    
    #fslmaths to convert Hz to radian
    subprocess.run(["fslmaths", "fieldmap_Hz.nii.gz", "-mul", "6.28", "fieldmap_radian.nii.gz"])
    
    #fsl fugue
    subprocess.run(["fugue", "-i", image1, f"--dwell={value1}", "--loadfmap=fieldmap_radian.nii.gz", "-u", "{file1}_corrected.nii.gz", "--unwarpdir=y-", "--saveshift=my_shift"])
    
#run_nipype_interface()
run_nipype_workflow()
#run_command()