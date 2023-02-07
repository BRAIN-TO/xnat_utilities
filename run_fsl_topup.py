from builtins import range
import nipype.interfaces.io as nio  # Data i/o
import nipype.interfaces.fsl as fsl
from nipype.interfaces.fsl.epi import TOPUP, ApplyTOPUP
from nipype.interfaces.fsl.preprocess import FUGUE
import nipype.pipeline.engine as pe  # pypeline engine
from nipype.interfaces.base import Bunch
from sys import argv
import nipype.interfaces.io as nio
import json
import subprocess
import os

script, file1, file2 = argv

json1 = file1 + ".json"
json2 = file2 + ".json"
image1 = file1 + ".nii.gz"
image2 = file2 + ".nii.gz"
b01 = "b0_" + file1
b02 = "b0_" + file2


#fslroi for b0 image
subprocess.run(["fslroi", image1, b01, "0", "1"])
subprocess.run(["fslroi", image2, b02, "0", "1"])

#fslmerge
subprocess.run(["fslmerge", "-t", "both_b0", b01, b02])

#create the c4 file
try:
    with open(json1, 'r') as json_file:
        data = json.load(json_file)
    value1 = float(data["EffectiveEchoSpacing"])
    value2 = float(data["AcquisitionMatrixPE"])
    c4 = value1 * value2
except FileNotFoundError:
    print("Json file is missing.")
except KeyError:
    print("Effective Echo Spacing and/or Acquisition Matrix PE do not exist.")
        
f = open('acq_param.txt', 'a')
f.write(f"0 -1 0 {c4}\n0 1 0 {c4}")
f.close

"""
#fsl topup
topup = pe.Node(interface=fsl.TOPUP(), name="topup")
topup.inputs.in_file = "both_b0.nii.gz"
topup.inputs.encoding_file = "acq_param.txt"
topup.inputs.out_field = "fieldmap_Hz.nii.gz"

#fslmath to convert to radian-change
fslmaths = pe.Node(interface=fsl.BinaryMaths(), name="fslmaths")
fslmaths.inputs.operation = 'mul'
fslmaths.inputs.operand_value = 5
fslmaths.inputs.out_file = "fieldmap_radian.nii.gz"

#fsl fugue
fugue = pe.Node(interface=fsl.FUGUE(), name="fugue")
fugue.inputs.in_file = image1
fugue.inputs.dwell_time = value1
fugue.inputs.unwarped_file = f"{image1}_corrected.nii.gz"
fugue.inputs.unwarp_direction = "y-"
fugue.inputs.save_shift = True

#connect the outputs to the inputs
preprocessing = pe.Workflow(name="preprocesing")
preprocessing.connect(topup, "out_field", fslmaths, "in_file")
preprocessing.connect(fslmaths, "out_file", fugue, "fmap_in_file")

#datasource
datasource = pe.Node(
    interface=nio.DataGrabber(outfields=['func']), name='datasource')
datasource.inputs.base_directory = "/home/yuexin/Documents/topup/"
datasource.inputs.sort_filelist = True
datasource.inputs.template = 'both_b0.nii.gz'

#connect preprocessing to datasource
preprocessing.connect(datasource, 'func', topup, 'in_file')

datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = os.path.abspath('/home/yuexin/Documents/topup/output/')
preprocessing.connect(fugue, 'unwarped_file', datasink, 'contrasts.@T')


preprocessing.config['execution']['job_finished_timeout'] = 60
preprocessing.run()
"""

#fsl topup
topup = TOPUP()
topup.inputs.in_file = "both_b0.nii.gz"
topup.inputs.encoding_file = "acq_param.txt"
topup.inputs.out_field = "fieldmap_Hz.nii.gz"
topup.inputs.out_base = "my_topup"
res = topup.run()

"""
#fsl applytopup
applytopup = ApplyTOPUP()
applytopup.inputs.in_files = [image1, image2]
applytopup.inputs.encoding_file = "acq_param.txt"
applytopup.inputs.in_topup_fieldcoef = "my_topup_fieldcoef.nii.gz"
applytopup.inputs.in_topup_movpar = "my_topup_movpar.txt"
res = applytopup.run()
"""

#fslmath to convert to radian-change
subprocess.run(["fslmaths", "fieldmap_Hz", "-mul", "6.28", "fieldmap_radian"])

#fsl fugue
fugue = FUGUE()
fugue.inputs.in_file = image1
fugue.inputs.dwell_time = value1
fugue.inputs.fmap_in_file = "fieldmap_radian.nii.gz"
fugue.inputs.unwarped_file = f"{image1}_corrected.nii.gz"
fugue.inputs.unwarp_direction = "y-"
fugue.inputs.save_shift = True
res = fugue.run()