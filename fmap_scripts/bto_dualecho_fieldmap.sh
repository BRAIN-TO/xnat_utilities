#!/usr/bin/env bash

# Simple formatting
bold=$(tput bold)
normal=$(tput sgr0)

# Help
function Help() {
    cat <<HELP
    
${bold}$(basename $0) ${normal} 

Usage:
$(basename $0) ${bold}--mag1${normal}=Magnitude 1 ${bold}--mag2${normal}=Magnitude 2 ${bold}--phs1${normal}=Phase 1 ${bold}--phs2${normal}=Phase 2 ${bold}--dte${normal}=3.75 ${bold}--out${normal}=bto_fieldmap_in_Radians 
--------------------------------------------------------------------------------
Required arguments:
    --mag1  : 1st echo magnitude image  ( e.g. /path/to/source/gre_mag_e1.nii.gz )
    --mag2  : 2nd echo magnitude image  ( e.g. /path/to/source/gre_mag_e2.nii.gz )
    --phs1  : 1st echo phase image      ( e.g. /path/to/source/gre_phs_e1.nii.gz )
    --phs2  : 2nd echo phase image      ( e.g. /path/to/source/gre_phs_e2.nii.gz )
Optional arguments:
    --dte   : delta TE                  ( default: 3.75 ms )
--------------------------------------------------------------------------------
Original Script created by  : S Kashyap (08-2022), kashyap.sriranga@gmail.com
Modified by                 : Yuexin Xi (05-2023), yuexinxi0220@outlook.com
    to provide BIDS valid fmap filename and json file
Dependencies                : SynthStrip (available in FreeSurfer), FSL, jq
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
    --phs1) # Phase1
        phs1=$(get_imarg1 $1)
        shift
        ;;
    --phs2) # Phase2
        phs2=$(get_imarg1 $1)
        shift
        ;;
    --dte) # delta TE
        dte=$(get_arg1 $1)
        shift
        ;;
    --out) # Phase2
        out=$(get_imarg1 $1)
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
out=${phs1/phase1/fieldmap}

echo " "
echo "++++ ${bold}BRAIN-TO Fieldmap Processing${normal} ++++"
echo " FSL version $Fversion "
echo " $runDate "
echo " "
echo " ++ Inputs "
echo "  - Magnitude 1  : $mag1 "
echo "  - Magnitude 2  : $mag2 "
echo "  - Phase 1      : $phs1 "
echo "  - Phase 2      : $phs2 "
echo "  - Delta TE     : $dte ms "
echo " "
echo " ++ Running FSL steps "

echo -ne " - Convert phase to radians ...\r "
fslmaths \
    $phs1 \
    -mul 3.14159 \
    -div 4096 \
    ${phs1}_in_Radians \
    -odt float

fslmaths \
    $phs2 \
    -mul 3.14159 \
    -div 4096 \
    ${phs2}_in_Radians \
    -odt float
echo " - Convert phase to radians ... Done."

echo -ne " - Creating brain mask ...\r "
mri_synthstrip \
    -i ${mag1}.nii.gz \
    -m ${mag1}_brain_mask.nii.gz &>/dev/null

echo " - Creating brain mask ... Done."

echo -ne " - Unwrapping phase images ...\r "
prelude \
    -a $mag1 \
    -p ${phs1}_in_Radians \
    -m ${mag1}_brain_mask \
    -o ${phs1}_in_Radians_Unwrapped
prelude \
    -a $mag2 \
    -p ${phs2}_in_Radians \
    -m ${mag1}_brain_mask \
    -o ${phs2}_in_Radians_Unwrapped
echo " - Unwrapping phase images ... Done."

echo -ne " - Calculating Fieldmap ...\r "
fslmaths \
    ${phs2}_in_Radians_Unwrapped \
    -sub \
    ${phs1}_in_Radians_Unwrapped \
    -mul 1000 \
    -div $dte \
    $out \
    -odt float
echo " - Calculating Fieldmap ... Done."

echo -ne " - Smoothing Fieldmap...\r "
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
json_read=${phs1}.json
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
