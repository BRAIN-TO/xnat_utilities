#!/usr/bin/env bash

# Simple formatting
bold=$(tput bold)
normal=$(tput sgr0)

# Help
function Help() {
    cat <<HELP
    
${bold}$(basename $0) ${normal} 

Usage:
$(basename $0) ${bold}--mag1${normal}=Magnitude 1 ${bold}--mag2${normal}=Magnitude 2 ${bold}--phs${normal}=Phasediff ${bold}--dte${normal}=3.75
--------------------------------------------------------------------------------
Required arguments:
    --mag1  : 1st echo magnitude image  ( e.g. /path/to/source/sub-01_magnitude1.nii.gz )
    --mag2  : 2nd echo magnitude image  ( e.g. /path/to/source/sub-01_magnitude2.nii.gz )
    --phs  : phasediff image            ( e.g. /path/to/source/sub-01_phasediff.nii.gz )
Optional arguments:
    --dte   : delta TE                  ( default: 3.75 ms )  
--------------------------------------------------------------------------------
Original Script created by  : S Kashyap (08-2022), kashyap.sriranga@gmail.com
Modified by                 : Yuexin Xi (05-2023), yuexinxi0220@outlook.com
    to provide BIDS valid fmap filename and json file (dependent on jq)
Learn more                  : https://jqlang.github.io/jq/
Learn more                  : https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FUGUE/Guide
--------------------------------------------------------------------------------
Citable(s):
    1. Jezzard & Balaban (1995), https://doi.org/10.1002/mrm.1910340111
    2. Andersson et al. (2001), https://doi.org/10.1006/nimg.2001.0746
    3. Hutton et al. (2002), https://doi.org/10.1006/nimg.2001.1054
--------------------------------------------------------------------------------

HELP
    exit 1
}

# Check for flag
if [[ "$1" == "-h" || $# -eq 0 ]]; then
    Help >&2
fi

# Get some info
Fversion=$(cat -v ${FSLDIR}/etc/fslversion)
runDate=$(echo $(date))

# Establish some functions
get_opt1() {
    arg=$(echo $1 | sed 's/=.*//')
    echo $arg
}

get_arg1() {
    if [ X$(echo $1 | grep '=') = X ]; then
        echo "Option $1 requires an argument" 1>&2
        exit 1
    else
        arg=$(echo $1 | sed 's/.*=//')
        if [ X$arg = X ]; then
            echo "Option $1 requires an argument" 1>&2
            exit 1
        fi
        echo $arg
    fi
}

get_imarg1() {
    arg=$(get_arg1 $1)
    arg=$($FSLDIR/bin/remove_ext $arg)
    echo $arg
}

# Defaults
dte=3.75

# Parse input arguments
while [ $# -ge 1 ]; do
    iarg=$(get_opt1 $1)
    case "$iarg" in

    --mag1) # Magnitude1
        mag1=$(get_imarg1 $1)
        shift
        ;;
    --mag2) # Magnitude2
        mag2=$(get_imarg1 $1)
        shift
        ;;
    --phs) # Phasediff
        phs=$(get_imarg1 $1)
        shift
        ;;
    --dte) # delta TE
        dte=$(get_arg1 $1)
        shift
        ;;
    -h)
        Help
        exit 0
        ;;
    *)
        echo "Unrecognised option $1" 1>&2
        exit 1
        ;;
    esac
done

# Default output name
out=${phs/phasediff/fieldmap}

echo " "
echo "++++ ${bold}BRAIN-TO Fieldmap Processing${normal} ++++"
echo " FSL version $Fversion "
echo " $runDate "
echo " "
echo " ++ Inputs "
echo "  - Magnitude 1  : $mag1 "
echo "  - Magnitude 2  : $mag2 "
echo "  - Phasediff    : $phs "
echo "  - Delta TE     : $dte ms "
echo " "
echo " ++ Running FSL steps "

echo -ne " - Creating brain mask ...\r "
mri_synthstrip \
    -i ${mag1}.nii.gz \
    -o ${mag1}_brain.nii.gz \
    -m brainmask.nii.gz

echo " - Creating brain mask ... Done."

echo -ne " - Creating stripped magnitude and phase images ...\r "
fslmaths \
    $mag2 \
    -mul brainmask \
    ${mag2}_brain

fslmaths \
    ${phs} \
    -mul brainmask \
    ${phs}_brain

echo " - Creating stripped magnitude and phase images ... Done."

echo -ne " - Calculating Fieldmap ...\r "
fsl_prepare_fieldmap \
    SIEMENS \
    ${phs}_brain \
    ${mag1}_brain \
    ${out} \
    $dte

echo " - Calculating Fieldmap ... Done."

echo -ne " - Smoothing Fieldmap ...\r "
fugue \
    --loadfmap=${out} \
    -s 1 \
    --savefmap=${out}

fugue \
    --loadfmap=${out} \
    --despike \
    --savefmap=${out}

echo " - Smoothing Fieldmap ... Done."

echo -ne " - Reading IntendedFor ...\r "
json_read=${phs}.json
intendedfor=$(jq '.IntendedFor' "$json_read")

echo " - Reading IntendedFor ... Done."

echo -ne " - Writing in json ... \r "
json_write="${out}.json"

json_string=$(
    jq --null-input \
        --arg Units "rad/s" \
        --argjson IntendedFor "$intendedfor" \
        --arg B0FieldIdentifier "b0map_fmap0" \
        '$ARGS.named'
)

echo "$json_string" > "${json_write}"

echo -ne " - Writing in json ... Done."


echo " "
echo " ++ Output "
echo "  - Fieldmap     : $out "
echo " "
echo "++++ ${bold}Processing Completed${normal} ++++"
echo " "