import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    #20221122 Yuexin Xi - bug: keyerror for extra - fixed: add key-value pair in all cases of extra
    
    # MPRAGE
    mprage_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_run-{item:02d}_T1w')
    mp2rage_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_run-{item:02d}_T1w')
    
    # FGATIR
    fgatir_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FGATIR_run-{item:02d}_T1w')
    edge3d_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-3DEDGE_run-{item:02d}_T1w')
    wair_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-WAIR_run-{item:02d}_T2w')
    stir_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-STIR_run-{item:02d}_T2w')
    
    # anatomical
    #t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
    t2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T2w')
    t2starw = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}{part}_T2starw')
    
    # SPACE
    spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T2w')
    spc_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T1w')
    spc_FLAIR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_FLAIR')
    
    # FLAIR
    flair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_FLAIR')
    
    # BOLD
    bold = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}{dir}_task-taskName_run-{item:02d}_{suffix}')
    
    # Perfusion
    asl = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}{dir}_run-{item:02d}_asl')
    perfusion = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_perfusion')
    dce = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_dce')
    dsc = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_dsc')
    rcbf = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_cbf')
    m0scan = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}{dir}_run-{item:02d}_m0scan')
    bat = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_bat')
    
    # Diffusion
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
    dwi_FA = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_FA')
    dwi_TENSOR = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSOR')
    dwi_TENSORB0 = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSORB0')
    dwi_TRACE = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_TRACE')
    dwi_ADC = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_ADC')
    
    # Field Maps
    # fm2d2r
    fmap_diff = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo-0_part-phase_MEGRE')
    fmap_magnitude = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_MEGRE')
    
    # MEGRE
    # fl2d2 + fieldmap in names -> fmap/two phase maps and two magnitude images -> check results whether it says 1 and 2
    # fl2d2 - fieldmap in names -> anat/..._MEGRE.nii
    fmap_megre_magnitude = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-MEGRE_magnitude')
    fmap_megre_phase = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-MEGRE_phase')
    megre = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_MEGRE')
    # epi = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}{dir}_epi')
    
    # Angiography
    angio = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_angio')
    angio_MIP = create_key('{bids_subject_session_dir}/extra/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_MIP')
    
    #SWI, QSM
    
    # extra
    extra = create_key('{bids_subject_session_dir}/extra/extra/{bids_subject_session_prefix}_acq-{acq}_{des}_run-{item:02d}_extra')
    
    info = {mprage_T1w: [], \
        mp2rage_T1w: [], \
        fgatir_T1w: [], \
        edge3d_T1w: [], \
        wair_T2w: [], \
        stir_T2w: [], \
        t2w: [], \
        t2starw: [], \
        spc_T2w: [], \
        spc_T1w: [], \
        spc_FLAIR: [], \
        flair: [], \
        bold: [], \
        asl: [], \
        perfusion: [], \
        dce: [], \
        dsc: [], \
        rcbf: [], \
        m0scan: [], \
        bat: [], \
        dwi: [], \
        dwi_FA: [], \
        dwi_TENSOR: [], \
        dwi_TENSORB0: [], \
        dwi_TRACE: [], \
        dwi_ADC: [], \
        fmap_megre_magnitude: [], \
        fmap_megre_phase: [], \
        megre: [], \
        # epi: [], \
        fmap_diff: [], \
        fmap_magnitude: [], \
        angio: [], \
        angio_MIP: [], \
        extra: []}
    # last_run = len(seqinfo)

    for idx, s in enumerate(seqinfo):
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * series_files
        * image_type
        * sequence_name
        """
        
        description = (s.series_description + '_' + s.protocol_name).strip().upper()
        
        #ABCD
        if ('ABCD3d' in s.sequence_name or 'tfl_me3d1' in s.sequence_name):
            if ('MPR' in description):
                info[mprage_T1w].append(s.series_id)
                continue
            elif ('MP2RAGE' in description):
                info[mp2rage_T1w].append(s.series_id)
                continue
            elif ('SPC' in description):
                if ('T2' in description): 
                    info[spc_T2w].append(s.series_id)
                    continue
                elif ('T1' in description):
                    info[spc_T1w].append(s.series_id)
                    continue
                
        #WIP
        if ('WIPfl3d' in s.sequence_name):
            if ('MAG' in description):
                info[t2starw].append({'item': s.series_id, 'part': '_part-mag'})
                continue
            if ('PHA' in description):
                info[t2starw].append({'item': s.series_id, 'part': '_part-phase'})
                continue
        
        # Field Maps needs verification
        # fm_r + 2d + 2
        if ('fm2d2r' in s.sequence_name):
            if('P' in (s.image_type[2].strip()) ):
                info[fmap_diff].append(s.series_id)
                continue
            if('M' in (s.image_type[2].strip()) ):
                info[fmap_magnitude].append(s.series_id)
                continue

        # MEGRE
        # fl + 2d + 2
        # qfl + 3d + 4
        if ('fl2d2' in s.sequence_name or \
            'qfl3d4' in s.sequence_name):
            if ('FIELD' in description \
                and 'MAP' in description):
                if('P' in (s.image_type[2].strip())):
                    info[fmap_megre_phase].append(s.series_id)
                    continue
                elif ('M' in (s.image_type[2].strip())):
                    info[fmap_megre_magnitude].append(s.series_id)
                    continue
            if (not ('FIELD' in description) and not ('MAP' in description)):
                info[megre].append(s.series_id)
                continue
        
        # MPRAGE (1 image) + MP2RAGE (3 images)
        # FGATIR, 3d-EDGE, WAIR, STIR
        # tfl + 3d + 1
        if ('tfl3d1' in s.sequence_name):
            # print("\n #################### \n series_files is {} \n #################### \n".format(s.series_files))
            if ('FGATIR' in description):
                info[fgatir_T1w].append(s.series_id)
                continue
            elif ('3D-EDGE' in description):
                info[edge3d_T1w].append(s.series_id)
                continue
            elif (s.series_files == 1 or s.series_files == 192):
                info[mprage_T1w].append(s.series_id)
                continue
            elif (s.series_files == 3):
                info[mp2rage_T1w].append(s.series_id)
                continue
            
        
        # tir + 2d + 1
        if ('tir2d1' in s.sequence_name):
            info[wair_T2w].append(s.series_id)
            continue
        
        # tir_rr + 2d + 1
        if ('tir2d1rr' in s.sequence_name):
            info[stir_T2w].append(s.series_id)
            continue
        
        # hippocampus
        # tse + 2d + 1
        if ('tse2d1' in s.sequence_name):
            info[t2w].append(s.series_id)
            continue
        
        # SPACE needs verification
        if ('spc' in s.sequence_name):
            # spc + ir
            if ('spcir' in s.sequence_name):
                info[spc_FLAIR].append(s.series_id)
                continue
            # spc + R?
            elif ('spc' in s.sequence_name):
                if ('T2' in description): 
                    info[spc_T2w].append(s.series_id)
                    continue
                elif ('T1' in description):
                    info[spc_T1w].append(s.series_id)
                    continue  
        
        # BOLD
        # epfid + 2d
        # epse + 2d
        if (('epfid2d' in s.sequence_name or 
            'epse2d' in s.sequence_name) and 'FMRI' in s.image_type[2].strip()):
            myItem = {'item': s.series_id}
            if ('SBREF' in description):
                myItem['suffix'] = 'sbref'
            else:
                myItem['suffix'] = 'bold'
            if ('PA' in description):
                myItem['dir'] = '_dir-PA'
            #    info[epi].append(myItem)
            elif ('AP' in description): 
                myItem['dir'] = '_dir-AP'
            #    info[epi].append(myItem)
            else:
                myItem['dir'] = ''
            info[bold].append(myItem)
            continue
                      
                        
        # Perfusion
        # tgse + 3d + 1
        if ('ASL' in s.image_type[2].strip() or \
            'tgse3d1' in s.sequence_name):
            myItem = {'item': s.series_id}
            if ('PA' in description and not 'PASL' in description):
                myItem['dir'] = '_dir-PA'
            elif ('AP' in description):
                myItem['dir'] = '_dir-AP'
            else:
                myItem['dir'] = ''    
            if ('ORIGINAL' in s.image_type[0].strip()):
                if ('MZERO' in description or 'M0' in description):
                    info[m0scan].append(myItem)
                    continue
                else:
                    info[asl].append(myItem)
                    continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('SUBTRACTION' in s.image_type[3].strip())):
                info[perfusion].append(s.series_id)
                continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('RCBF' in s.image_type[3].strip())):
                info[rcbf].append(s.series_id)
                continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('BAT' in s.image_type[3].strip())):
                info[bat].append(s.series_id)
                continue
            
            
        # Diffusion
        # epse + 2d
        if ('DIFFUSION' in s.image_type[2].strip() or \
            ('epse2d' in s.sequence_name and 'DWI' in description)):
            if ('ORIGINAL' in s.image_type[0].strip()):
                info[dwi].append(s.series_id)
                continue
            elif ('DERIVED' in s.image_type[0].strip()):
                if ('FA' in s.image_type[3].strip()):
                    info[dwi_FA].append(s.series_id)
                    continue
                elif ('TENSOR_B0' in s.image_type[3].strip()):
                    info[dwi_TENSORB0].append(s.series_id)
                    continue  
                elif ('TENSOR' in s.image_type[3].strip()):
                    info[dwi_TENSOR].append(s.series_id)
                    continue
                elif ('TRACE' in s.image_type[3].strip()):
                    info[dwi_TRACE].append(s.series_id)
                    continue
                elif ('ADC' in s.image_type[3].strip()):
                    info[dwi_ADC].append(s.series_id)
                    continue  
        
        # Angiography
        # fl_r + 3d + 1: SWI?
        if ('fl3d1r' in s.sequence_name):
            if ('ORIGINAL' in s.image_type[0].strip()):
                info[angio].append(s.series_id)
                continue
            elif ('DERIVED' in s.image_type[0].strip()):
                if ('MIP' in description):
                    if ('COR' in description):
                        info[angio_MIP].append({'item': s.series_id, 'acq': 'coronal'})
                        continue
                    if ('SAG' in description):
                        info[angio_MIP].append({'item': s.series_id, 'acq': 'sagittal'})
                        continue
        
        # print("\n #################### \n series_files is {} \n #################### \n".format(s.series_files))            
        info[extra].append({'item': s.series_id, 'acq': s.sequence_name, 'des': s.series_description})
                  
        
        """
            
        # FLAIR
        if ('FLAIR' in description or ('DA' in description and 'FL' in description)):
            info[flair].append(s.series_id)
            continue   
                
        info[extra].append({'item': s.series_id, 'acq': s.series_description})
    """
    
        
        

    return info
