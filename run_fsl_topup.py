from sys import argv
from nipype.interfaces.fsl import TOPUP, ApplyTOPUP
import json
import subprocess

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

#fsl topup
topup = TOPUP()
topup.inputs.in_file = "both_b0.nii.gz"
topup.inputs.encoding_file = "acq_param.txt"
topup.inputs.out_field = "fieldmap_Hz.nii.gz"
topup.inputs.out_base = "my_topup"
res = topup.run()

#fslmaths to convert to radian-change
#subprocess.run(["fslmaths", "fieldmap_Hz", "-mul", "6.28", "fieldmap_radian"])

#fsl applytopup
applytopup = ApplyTOPUP()
applytopup.inputs.in_files = [image1, image2]
applytopup.inputs.encoding_file = "acq_param.txt"
applytopup.inputs.in_topup_fieldcoef = "my_topup_fieldcoef.nii.gz"
applytopup.inputs.in_topup_movpar = "my_topup_movpar.txt"
res = applytopup.run()